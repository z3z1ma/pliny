from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any

try:
    from autoresearch import offline_score
except ImportError:  # pragma: no cover - supports direct script execution.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from autoresearch import offline_score


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIOS_PATH = REPO_ROOT / "autoresearch" / "catalogs" / "scenarios.json"
MARKDOWN_DEFINITION_START = "<!-- codex-subject-runner-definition:start -->"
MARKDOWN_DEFINITION_END = "<!-- codex-subject-runner-definition:end -->"
DEFAULT_ARMS = ("no-10x-control", "current-10x", "candidate-variant")
SUPPRESSED_INSTRUCTION_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".cursor/rules",
    ".agents/skills",
]


class ExperimentError(ValueError):
    pass


class BudgetError(ExperimentError):
    pass


def load_definition(path: str | Path) -> dict[str, Any]:
    definition_path = Path(path)
    text = definition_path.read_text(encoding="utf-8")
    if definition_path.suffix == ".json":
        data = json.loads(text)
    else:
        data = _load_markdown_definition(text)
    if not isinstance(data, dict):
        raise ExperimentError("experiment definition must be a JSON object")
    return data


def build_plan(
    definition: dict[str, Any],
    *,
    repo_root: Path = REPO_ROOT,
    out_dir: str | Path | None = None,
) -> dict[str, Any]:
    catalog = _load_scenario_catalog(repo_root)
    _validate_definition_shape(definition)

    scenario_by_id = {scenario["id"]: scenario for scenario in catalog["scenarios"]}
    arms = _planned_arms(definition, repo_root)
    scenarios = _planned_scenarios(definition, scenario_by_id)
    repetitions = _positive_int(definition.get("repetitions"), "repetitions")
    planned_calls = len(arms) * len(scenarios) * repetitions
    budget = _budget(definition, catalog, planned_calls)
    output_root = Path(out_dir) if out_dir else _default_output_dir(definition)
    artifact_dirs = _artifact_dirs(output_root)

    samples = []
    for scenario in scenarios:
        for arm in arms:
            for rep in range(repetitions):
                user_message = _scenario_user_message(scenario, arm["id"])
                prior_raw_path = _prior_raw_path(scenario, arm["id"])
                live_run_key = run_key(
                    definition["experiment_id"],
                    scenario["id"],
                    arm["id"],
                    rep,
                    definition["model"],
                    definition["harness"],
                    arm["instruction_digest"],
                    user_message,
                    prior_raw_path,
                )
                stem = _artifact_stem(live_run_key)
                prior_context = _load_prior_context(repo_root, prior_raw_path)
                workspace_dir = prior_context.get("workspace_dir") or artifact_dirs["workspaces"] / stem
                raw_path = artifact_dirs["raw"] / f"{stem}.json"
                score_path = artifact_dirs["scores"] / f"{stem}.score.json"
                command_path = artifact_dirs["codex"] / f"{stem}.command.json"
                stdout_path = artifact_dirs["codex"] / f"{stem}.stdout.jsonl"
                stderr_path = artifact_dirs["codex"] / f"{stem}.stderr"
                last_message_path = artifact_dirs["codex"] / f"{stem}.last-message.txt"
                prompt_path = artifact_dirs["prompts"] / f"{stem}.prompt.txt"
                manifest_path = workspace_dir / "workspace-manifest.json"
                turns = _planned_turns(
                    artifact_dirs,
                    stem,
                    workspace_dir,
                    last_message_path,
                    arm,
                    user_message,
                    prior_context.get("transcript", []),
                )
                samples.append(
                    {
                        "experiment_id": definition["experiment_id"],
                        "scenario_id": scenario["id"],
                        "variant_id": arm["id"],
                        "rep": rep,
                        "model": definition["model"],
                        "harness": definition["harness"],
                        "harness_kind": "codex-live-subject",
                        "instruction_source": arm["instruction_source"],
                        "instruction_path": arm.get("instruction_path"),
                        "base_instruction_path": arm.get("base_instruction_path"),
                        "instruction_text": arm["instruction_text"],
                        "instruction_digest": arm["instruction_digest"],
                        "live_run_key": live_run_key,
                        "scenario_prompt": user_message,
                        "prior_raw_path": prior_context.get("raw_path"),
                        "prior_transcript": prior_context.get("transcript", []),
                        "prompt": turns[0]["prompt"],
                        "prompt_path": str(prompt_path),
                        "planned_workspace_dir": str(workspace_dir),
                        "planned_raw_output_path": str(raw_path),
                        "planned_score_artifact_path": str(score_path),
                        "planned_command_path": str(command_path),
                        "planned_stdout_jsonl_path": str(stdout_path),
                        "planned_stderr_path": str(stderr_path),
                        "planned_last_message_path": str(last_message_path),
                        "planned_workspace_manifest_path": str(manifest_path),
                        "planned_turns": turns,
                        "planned_codex_argv": turns[0]["planned_codex_argv"],
                        "timeout_seconds": budget["timeout_seconds_per_run"],
                        "control_isolation": _control_isolation(),
                        "live_codex_calls": 1,
                    }
                )

    return {
        "experiment_id": definition["experiment_id"],
        "method_tier": definition["method_tier"],
        "mode": "plan",
        "registered_definition": True,
        "driver": definition.get("driver"),
        "model": definition["model"],
        "harness": definition["harness"],
        "harness_kind": "codex-live-subject",
        "arms": arms,
        "scenarios": scenarios,
        "repetitions": repetitions,
        "budget": budget,
        "artifact_root": str(output_root),
        "artifact_dirs": {name: str(path) for name, path in artifact_dirs.items()},
        "samples": samples,
        "live_codex_calls": sum(sample["live_codex_calls"] for sample in samples),
        "promotion_decision": "not-performed",
        "limits": _limits(),
    }


def run_key(
    experiment_id: str,
    scenario_id: str,
    variant_id: str,
    rep: int,
    model: str,
    harness: str,
    instruction_digest: str,
    prompt: str,
    prior_raw_path: str | None,
) -> str:
    payload = {
        "experiment_id": experiment_id,
        "harness": harness,
        "instruction_digest": instruction_digest,
        "model": model,
        "prior_raw_path": prior_raw_path,
        "prompt": prompt,
        "rep": rep,
        "scenario_id": scenario_id,
        "variant_id": variant_id,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def run_live(
    definition: dict[str, Any],
    out_dir: str | Path,
    *,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    plan = build_plan(definition, repo_root=repo_root, out_dir=out_dir)
    output_root = Path(out_dir)
    artifact_dirs = {name: Path(path) for name, path in plan["artifact_dirs"].items()}
    for path in artifact_dirs.values():
        path.mkdir(parents=True, exist_ok=True)

    written_samples = []
    for sample in plan["samples"]:
        written_samples.append(_run_sample(sample, repo_root=repo_root))

    plan["mode"] = "live"
    plan["samples"] = written_samples
    plan_path = output_root / "plan.json"
    plan_path.write_text(json.dumps(_public_plan(plan), indent=2) + "\n", encoding="utf-8")

    summary = {
        "experiment_id": plan["experiment_id"],
        "mode": "live",
        "samples_written": len(written_samples),
        "raw_output_dir": plan["artifact_dirs"]["raw"],
        "score_artifact_dir": plan["artifact_dirs"]["scores"],
        "workspace_dir": plan["artifact_dirs"]["workspaces"],
        "codex_artifact_dir": plan["artifact_dirs"]["codex"],
        "plan_path": str(plan_path),
        "live_codex_calls": sum(sample["live_codex_calls"] for sample in written_samples),
        "promotion_decision": "not-performed",
        "budget": plan["budget"],
        "limits": plan["limits"],
    }
    (output_root / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run one live Codex subject-agent experiment from a registered definition."
    )
    parser.add_argument("--experiment", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args(argv)
    if args.dry_run and args.run:
        print("choose only one of --dry-run or --run", file=sys.stderr)
        return 2
    try:
        definition = load_definition(args.experiment)
        out_dir = args.out or _default_output_dir(definition)
        result = (
            run_live(definition, out_dir)
            if args.run
            else _public_plan(build_plan(definition, out_dir=out_dir))
        )
    except (OSError, ExperimentError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


def _run_sample(sample: dict[str, Any], *, repo_root: Path) -> dict[str, Any]:
    workspace = Path(sample["planned_workspace_dir"])
    raw_path = Path(sample["planned_raw_output_path"])
    score_path = Path(sample["planned_score_artifact_path"])
    command_path = Path(sample["planned_command_path"])
    stdout_path = Path(sample["planned_stdout_jsonl_path"])
    stderr_path = Path(sample["planned_stderr_path"])
    prompt_path = Path(sample["prompt_path"])
    manifest_path = Path(sample["planned_workspace_manifest_path"])

    workspace.mkdir(parents=True, exist_ok=True)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    score_path.parent.mkdir(parents=True, exist_ok=True)
    command_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.parent.mkdir(parents=True, exist_ok=True)

    pre_present = _present_suppressed(workspace)
    prior_transcript = list(sample.get("prior_transcript", []))
    transcript: list[dict[str, str]] = list(prior_transcript)
    command_outputs = []
    raw_refs = [sample["prior_raw_path"]] if sample.get("prior_raw_path") else []
    all_events: list[dict[str, Any]] = []
    usage = {"input_tokens": 0, "output_tokens": 0}
    wall_seconds = 0.0
    timed_out = False
    exit_code = 0

    for planned_turn in sample["planned_turns"]:
        prompt_path = Path(planned_turn["prompt_path"])
        command_path = Path(planned_turn["command_path"])
        stdout_path = Path(planned_turn["stdout_jsonl_path"])
        stderr_path = Path(planned_turn["stderr_path"])
        last_message_path = Path(planned_turn["last_message_path"])
        prompt = _turn_prompt(
            sample,
            planned_turn["user_message"],
            transcript,
        )
        argv = _planned_codex_argv(workspace, prompt, last_message_path)

        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        command_path.parent.mkdir(parents=True, exist_ok=True)
        prompt_path.write_text(prompt, encoding="utf-8")

        started = _now()
        start = time.monotonic()
        turn_timed_out = False
        try:
            completed = subprocess.run(
                argv,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=float(sample["timeout_seconds"]),
            )
        except subprocess.TimeoutExpired as exc:
            turn_timed_out = True
            completed = SimpleNamespace(
                returncode=124,
                stdout=_coerce_timeout_output(exc.stdout),
                stderr=(
                    _coerce_timeout_output(exc.stderr)
                    + f"\nTimed out after {sample['timeout_seconds']} seconds."
                ).strip(),
            )
        turn_wall_seconds = time.monotonic() - start
        ended = _now()

        stdout_path.write_text(completed.stdout, encoding="utf-8")
        stderr_path.write_text(completed.stderr, encoding="utf-8")
        last_message = last_message_path.read_text(encoding="utf-8") if last_message_path.exists() else ""
        events = _jsonl_events(completed.stdout)
        turn_usage = _usage(events)
        all_events.extend(events)
        usage["input_tokens"] += int(turn_usage.get("input_tokens") or 0)
        usage["output_tokens"] += int(turn_usage.get("output_tokens") or 0)
        wall_seconds += turn_wall_seconds
        timed_out = timed_out or turn_timed_out
        exit_code = completed.returncode

        command = {
            "schema_version": 1,
            "start_timestamp_utc": started,
            "end_timestamp_utc": ended,
            "turn_index": planned_turn["turn_index"],
            "argv": _public_argv(argv, prompt_path),
            "exit_code": completed.returncode,
            "stdout_jsonl_path": str(stdout_path),
            "stderr_path": str(stderr_path),
            "last_message_path": str(last_message_path),
            "prompt_path": str(prompt_path),
            "usage": turn_usage,
            "timed_out": turn_timed_out,
            "timeout_seconds": sample["timeout_seconds"],
            "control_isolation": sample["control_isolation"],
        }
        command_path.write_text(json.dumps(command, indent=2) + "\n", encoding="utf-8")

        transcript.append({"role": "user", "content": planned_turn["user_message"]})
        transcript.append({"role": "assistant", "content": last_message})
        command_outputs.append(
            {
                "command": " ".join(argv[:8]) + " ...",
                "exit_code": completed.returncode,
                "output": _command_output(completed.stderr, stdout_path),
            }
        )
        raw_refs.extend(
            [
                str(prompt_path),
                str(command_path),
                str(stdout_path),
                str(stderr_path),
                str(last_message_path),
            ]
        )
        if completed.returncode != 0:
            break

    post_present = _present_suppressed(workspace)
    file_outputs = _workspace_file_outputs(workspace, manifest_path)
    tool_invocations = _tool_invocations(all_events)

    manifest = {
        "schema_version": 1,
        "experiment_id": sample["experiment_id"],
        "scenario_id": sample["scenario_id"],
        "variant_id": sample["variant_id"],
        "workspace": str(workspace),
        "suppressed_instruction_files": SUPPRESSED_INSTRUCTION_FILES,
        "pre_run_present_suppressed_instruction_files": pre_present,
        "post_run_present_suppressed_instruction_files": post_present,
        "post_run_files": [item["path"] for item in file_outputs],
        "workspace_contamination_present": bool(pre_present or post_present),
        "timed_out": timed_out,
        "timeout_seconds": sample["timeout_seconds"],
        "completed_new_turns": (len(transcript) - len(prior_transcript)) // 2,
        "transcript_turns": len(transcript) // 2,
        "planned_new_turns": len(sample["planned_turns"]),
        "control_isolation": sample["control_isolation"],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    raw_fixture = {
        "schema_version": 1,
        "experiment_id": sample["experiment_id"],
        "scenario_id": sample["scenario_id"],
        "variant_id": sample["variant_id"],
        "rep": sample["rep"],
        "model": sample["model"],
        "harness": sample["harness"],
        "instruction_digest": sample["instruction_digest"],
        "transcript": transcript,
        "tool_invocations": tool_invocations,
        "file_outputs": file_outputs,
        "command_outputs": command_outputs,
        "raw_artifact_refs": raw_refs + [str(manifest_path), str(raw_path)],
        "wall_seconds": wall_seconds,
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "timed_out": timed_out,
        "timeout_seconds": sample["timeout_seconds"],
        "live_codex_calls": (len(transcript) - len(prior_transcript)) // 2,
        "harness_metadata": {
            "kind": "codex-live-subject",
            "instruction_source": sample["instruction_source"],
            "instruction_path": sample.get("instruction_path"),
            "base_instruction_path": sample.get("base_instruction_path"),
            "workspace_manifest_path": str(manifest_path),
            "prior_raw_path": sample.get("prior_raw_path"),
            "prior_turn_count": len(prior_transcript) // 2,
            "turns": [
                {
                    "turn_index": turn["turn_index"],
                    "prompt_path": turn["prompt_path"],
                    "command_path": turn["command_path"],
                    "stdout_jsonl_path": turn["stdout_jsonl_path"],
                    "stderr_path": turn["stderr_path"],
                    "last_message_path": turn["last_message_path"],
                }
                for turn in sample["planned_turns"]
            ],
            "control_isolation": sample["control_isolation"],
            "timed_out": timed_out,
            "timeout_seconds": sample["timeout_seconds"],
            "promotion_limit": "Live subject output is candidate-quality evidence, not promotion authority.",
        },
    }
    raw_path.write_text(json.dumps(raw_fixture, indent=2) + "\n", encoding="utf-8")

    score_artifact = offline_score.score_fixture(raw_path)
    errors = offline_score.validate_score_artifact(score_artifact)
    if errors:
        raise ExperimentError(f"{raw_path}: invalid score artifact: {'; '.join(errors)}")
    score_path.write_text(json.dumps(score_artifact, indent=2) + "\n", encoding="utf-8")

    sample = dict(sample)
    sample.update(
        {
            "exit_code": exit_code,
            "wall_seconds": wall_seconds,
            "usage": usage,
            "timed_out": timed_out,
            "timeout_seconds": sample["timeout_seconds"],
            "workspace_manifest_path": str(manifest_path),
            "turns": sample["planned_turns"],
            "raw_output_path": str(raw_path),
            "score_artifact_path": str(score_path),
            "live_codex_calls": (len(transcript) - len(prior_transcript)) // 2,
            "prior_raw_path": sample.get("prior_raw_path"),
        }
    )
    return sample


def _load_scenario_catalog(repo_root: Path) -> dict[str, Any]:
    return json.loads(
        (repo_root / "autoresearch" / "catalogs" / "scenarios.json").read_text(
            encoding="utf-8"
        )
    )


def _load_markdown_definition(text: str) -> dict[str, Any]:
    start = text.find(MARKDOWN_DEFINITION_START)
    end = text.find(MARKDOWN_DEFINITION_END)
    if start == -1 or end == -1 or end <= start:
        raise ExperimentError(
            "Markdown experiment records must include a codex-subject-runner-definition JSON block"
        )
    block = text[start + len(MARKDOWN_DEFINITION_START) : end].strip()
    if block.startswith("```json"):
        block = block.removeprefix("```json").strip()
    if block.endswith("```"):
        block = block.removesuffix("```").strip()
    return json.loads(block)


def _validate_definition_shape(definition: dict[str, Any]) -> None:
    required = ("experiment_id", "method_tier", "model", "harness", "arms", "scenarios")
    for field in required:
        if field not in definition:
            raise ExperimentError(f"experiment definition missing {field}")
    if definition["method_tier"] not in {"MICRO", "FULL"}:
        raise ExperimentError("run_codex_subject only supports method_tier MICRO or FULL")
    if "codex" not in str(definition["harness"]).lower():
        raise ExperimentError("run_codex_subject requires a Codex harness")
    if not isinstance(definition["arms"], list) or not definition["arms"]:
        raise ExperimentError("arms must be a non-empty list")
    if not isinstance(definition["scenarios"], list) or not definition["scenarios"]:
        raise ExperimentError("scenarios must be a non-empty list")


def _planned_arms(definition: dict[str, Any], repo_root: Path) -> list[dict[str, Any]]:
    by_id = {}
    for arm in definition["arms"]:
        if not isinstance(arm, dict) or not arm.get("id"):
            raise ExperimentError("each arm must be an object with id")
        by_id[arm["id"]] = arm

    missing = [arm_id for arm_id in DEFAULT_ARMS if arm_id not in by_id]
    if missing:
        raise ExperimentError("live subject definitions must include arms: " + ", ".join(missing))

    planned = []
    for arm_id in DEFAULT_ARMS:
        arm = by_id[arm_id]
        instruction_text = _instruction_text(arm, repo_root)
        planned.append(
            {
                "id": arm_id,
                "instruction_source": arm.get("instruction_source", ""),
                "instruction_path": arm.get("instruction_path"),
                "base_instruction_path": arm.get("base_instruction_path"),
                "instruction_text": instruction_text,
                "instruction_digest": _digest_bytes(instruction_text.encode("utf-8")),
            }
        )
    return planned


def _instruction_text(arm: dict[str, Any], repo_root: Path) -> str:
    parts = []
    base_path = arm.get("base_instruction_path")
    if isinstance(base_path, str) and base_path:
        parts.append(_resolve_path(repo_root, base_path).read_text(encoding="utf-8"))
    instruction_text = arm.get("instruction_text")
    if isinstance(instruction_text, str):
        parts.append(instruction_text)
    instruction_path = arm.get("instruction_path")
    if isinstance(instruction_path, str) and instruction_path:
        parts.append(_resolve_path(repo_root, instruction_path).read_text(encoding="utf-8"))
    if not parts:
        if arm.get("id") == "no-10x-control":
            return "You are a coding agent. Answer the user's task directly."
        raise ExperimentError(f"{arm.get('id', '<unknown>')}: missing instruction text or path")
    return "\n\n".join(parts)


def _planned_scenarios(
    definition: dict[str, Any],
    scenario_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    scenarios = []
    for scenario in definition["scenarios"]:
        if isinstance(scenario, str):
            scenario = {"id": scenario}
        if not isinstance(scenario, dict) or not scenario.get("id"):
            raise ExperimentError("each scenario must be an object with id")
        scenario_id = scenario["id"]
        catalog_scenario = scenario_by_id.get(scenario_id)
        if catalog_scenario is None:
            raise ExperimentError(f"unknown scenario_id {scenario_id}")
        scenarios.append(
            {
                "id": scenario_id,
                "prompt": scenario.get(
                    "prompt",
                    catalog_scenario.get("user_prompt_or_task_input", ""),
                ),
                "prompt_is_explicit": "prompt" in scenario,
                "prompts_by_arm": scenario.get("prompts_by_arm"),
                "prior_raw_path": _prior_raw_path(scenario, None),
                "prior_raw_paths": scenario.get("prior_raw_paths"),
            }
        )
    return scenarios


def _scenario_user_message(scenario: dict[str, Any], arm_id: str) -> str:
    prompts_by_arm = scenario.get("prompts_by_arm")
    if prompts_by_arm is not None:
        if not isinstance(prompts_by_arm, dict):
            raise ExperimentError("scenario prompts_by_arm must be an object")
        value = prompts_by_arm.get(arm_id)
        if value is not None:
            if not isinstance(value, str) or not value.strip():
                raise ExperimentError("scenario prompts_by_arm values must be non-empty strings")
            return value
        if not scenario.get("prompt_is_explicit"):
            raise ExperimentError(
                "scenario prompts_by_arm must include every arm or provide an explicit prompt fallback"
            )
    value = scenario.get("prompt")
    if not isinstance(value, str) or not value.strip():
        raise ExperimentError("scenario prompt must be a non-empty string")
    return value


def _prior_raw_path(scenario: dict[str, Any], arm_id: str | None) -> str | None:
    raw_paths = scenario.get("prior_raw_paths")
    if isinstance(raw_paths, dict) and arm_id:
        value = raw_paths.get(arm_id)
        if value is not None and not isinstance(value, str):
            raise ExperimentError("scenario prior_raw_paths values must be strings")
        return value
    value = scenario.get("prior_raw_path")
    if value is not None and not isinstance(value, str):
        raise ExperimentError("scenario prior_raw_path must be a string")
    return value


def _load_prior_context(repo_root: Path, prior_raw_path: str | None) -> dict[str, Any]:
    if not prior_raw_path:
        return {}
    raw_path = _resolve_path(repo_root, prior_raw_path)
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    transcript = raw.get("transcript")
    if not isinstance(transcript, list):
        raise ExperimentError(f"{prior_raw_path}: prior raw artifact missing transcript")
    cleaned_transcript = []
    for item in transcript:
        if isinstance(item, dict) and isinstance(item.get("role"), str) and isinstance(item.get("content"), str):
            cleaned_transcript.append({"role": item["role"], "content": item["content"]})
    metadata = raw.get("harness_metadata") if isinstance(raw.get("harness_metadata"), dict) else {}
    manifest_path = metadata.get("workspace_manifest_path")
    workspace_dir = None
    if isinstance(manifest_path, str):
        manifest = json.loads(_resolve_path(repo_root, manifest_path).read_text(encoding="utf-8"))
        workspace = manifest.get("workspace")
        if isinstance(workspace, str):
            workspace_dir = _resolve_path(repo_root, workspace)
    return {
        "raw_path": str(raw_path),
        "transcript": cleaned_transcript,
        "workspace_dir": workspace_dir,
    }


def _budget(
    definition: dict[str, Any],
    catalog: dict[str, Any],
    planned_runs: int,
) -> dict[str, Any]:
    tier = definition["method_tier"]
    defaults = (
        catalog["budget_defaults"]["micro_campaign"]
        if tier == "MICRO"
        else catalog["budget_defaults"]["full_campaign"]
    )
    requested = definition.get("budget", {})
    if requested and not isinstance(requested, dict):
        raise ExperimentError("budget must be an object")

    if tier == "MICRO":
        max_runs = min(
            int(requested.get("max_harness_runs", defaults["max_subject_agent_samples"])),
            int(defaults["max_subject_agent_samples"]),
        )
    else:
        max_runs = min(
            int(requested.get("max_harness_runs", defaults["max_harness_runs"])),
            int(defaults["max_harness_runs"]),
        )
    estimate_seconds = float(requested.get("estimated_wall_seconds_per_run", 0))
    timeout_seconds = float(
        requested.get("timeout_seconds_per_run", estimate_seconds if estimate_seconds > 0 else 1800)
    )
    max_hours = float(defaults["max_wall_clock_hours"])
    planned_hours = planned_runs * estimate_seconds / 3600
    if planned_runs > max_runs:
        raise BudgetError(f"planned {planned_runs} harness runs exceeds {tier} cap {max_runs}")
    if planned_hours > max_hours:
        raise BudgetError(f"planned {planned_hours:.2f} wall-clock hours exceeds {tier} cap {max_hours:g}")
    if timeout_seconds <= 0:
        raise BudgetError("timeout_seconds_per_run must be positive")
    budget = {
        "planned_harness_runs": planned_runs,
        "max_harness_runs": max_runs,
        "estimated_wall_seconds_per_run": estimate_seconds,
        "timeout_seconds_per_run": timeout_seconds,
        "planned_wall_clock_hours": planned_hours,
        "max_wall_clock_hours": max_hours,
    }
    if "suggested_per_run_cap_hours" in defaults:
        budget["suggested_per_run_cap_hours"] = defaults["suggested_per_run_cap_hours"]
    return budget


def _planned_turns(
    artifact_dirs: dict[str, Path],
    stem: str,
    workspace_dir: Path,
    first_last_message_path: Path,
    arm: dict[str, Any],
    user_message: str,
    prior_transcript: list[dict[str, str]],
) -> list[dict[str, Any]]:
    turns = []
    prompt_path = artifact_dirs["prompts"] / f"{stem}.prompt.txt"
    command_path = artifact_dirs["codex"] / f"{stem}.command.json"
    stdout_path = artifact_dirs["codex"] / f"{stem}.stdout.jsonl"
    stderr_path = artifact_dirs["codex"] / f"{stem}.stderr"
    prompt = _turn_prompt({"scenario_prompt": user_message, **arm}, user_message, prior_transcript)
    turns.append(
        {
            "turn_index": len(prior_transcript) // 2,
            "user_message": user_message,
            "prompt": prompt,
            "prompt_path": str(prompt_path),
            "command_path": str(command_path),
            "stdout_jsonl_path": str(stdout_path),
            "stderr_path": str(stderr_path),
            "last_message_path": str(first_last_message_path),
            "planned_codex_argv": _planned_codex_argv(
                workspace_dir,
                prompt,
                first_last_message_path,
            ),
        }
    )
    return turns


def _turn_prompt(sample: dict[str, Any], user_message: str, transcript: list[dict[str, str]]) -> str:
    transcript_block = ""
    if transcript:
        lines = ["Prior transcript:"]
        for item in transcript:
            lines.append(f"{item['role'].title()}: {item['content']}")
        transcript_block = "\n".join(lines) + "\n\n"
    return (
        "You are the subject agent in a 10x autoresearch evaluation.\n"
        "Use only the instructions between <instructions> and </instructions> "
        "as your project-level operating instructions for this run.\n"
        "Do not discuss scoring, the benchmark, or these wrapper tags.\n\n"
        "<instructions>\n"
        f"{sample['instruction_text']}\n"
        "</instructions>\n\n"
        f"{transcript_block}"
        "User message:\n"
        f"{user_message}\n"
    )


def _planned_codex_argv(workspace_dir: Path, prompt: str, last_message_path: Path) -> list[str]:
    return [
        "codex",
        "--ask-for-approval",
        "never",
        "--disable",
        "plugins",
        "exec",
        "--cd",
        str(workspace_dir),
        "--skip-git-repo-check",
        "--ephemeral",
        "--json",
        "--output-last-message",
        str(last_message_path),
        "--ignore-user-config",
        "--sandbox",
        "workspace-write",
        prompt,
    ]


def _control_isolation() -> dict[str, Any]:
    return {
        "suppress_instruction_files": SUPPRESSED_INSTRUCTION_FILES,
        "codex_args": ["--disable", "plugins", "--ignore-user-config"],
        "workspace_strategy": "Run from generated workspaces that omit project instruction files and skill directories.",
        "instruction_strategy": "Pass current and candidate instructions explicitly in the prompt; no-10x receives minimal instructions.",
        "limitation": "Codex system context and authenticated home remain outside this runner's control.",
    }


def _artifact_dirs(root: Path) -> dict[str, Path]:
    return {
        "raw": root / "raw",
        "scores": root / "scores",
        "workspaces": root / "workspaces",
        "codex": root / "codex",
        "prompts": root / "prompts",
    }


def _default_output_dir(definition: dict[str, Any]) -> Path:
    return REPO_ROOT / ".10x/evidence/.storage/codex-subject" / definition["experiment_id"]


def _resolve_path(repo_root: Path, path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return repo_root / candidate


def _artifact_stem(key: str) -> str:
    return key.replace("sha256:", "sha256-")


def _digest_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _positive_int(value: Any, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ExperimentError(f"{field} must be a positive integer")
    return value


def _present_suppressed(workspace: Path) -> list[str]:
    return [path for path in SUPPRESSED_INSTRUCTION_FILES if (workspace / path).exists()]


def _workspace_file_outputs(workspace: Path, manifest_path: Path) -> list[dict[str, str]]:
    outputs = []
    for path in sorted(workspace.rglob("*")):
        if not path.is_file() or path == manifest_path:
            continue
        try:
            relative = path.relative_to(workspace)
        except ValueError:
            continue
        if relative.parts and relative.parts[0] == ".git":
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = "<binary file omitted>"
        outputs.append(
            {
                "path": str(relative),
                "action": "write",
                "content": _truncate(content, 200000),
            }
        )
    return outputs


def _jsonl_events(text: str) -> list[dict[str, Any]]:
    events = []
    for line in text.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def _usage(events: list[dict[str, Any]]) -> dict[str, Any]:
    for event in reversed(events):
        usage = event.get("usage")
        if isinstance(usage, dict):
            return usage
    return {}


def _tool_invocations(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    invocations = []
    for event in events:
        event_type = str(event.get("type", ""))
        if "tool" in event_type or "function" in event_type:
            invocations.append(event)
            continue
        item = event.get("item")
        if not isinstance(item, dict):
            continue
        if event_type == "item.completed" and item.get("type") in {
            "command_execution",
            "file_change",
        }:
            invocations.append(event)
    return invocations


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n<truncated>"


def _coerce_timeout_output(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _command_output(stderr: str, stdout_path: Path) -> str:
    if stderr:
        return _truncate(stderr, 4000)
    return f"stdout JSONL stored at {stdout_path}"


def _limits() -> list[str]:
    return [
        "This runner executes candidate instructions but still uses Trust Level 1 offline scoring.",
        "Codex system context and authenticated home remain outside this runner's control.",
        "Manual inspection is required before promotion or durable verdicts.",
        "The runner executes one registered experiment and does not loop or generate candidates.",
    ]


def _public_plan(plan: dict[str, Any]) -> dict[str, Any]:
    visible = copy.deepcopy(plan)
    for arm in visible.get("arms", []):
        if isinstance(arm, dict):
            arm.pop("instruction_text", None)
    for scenario in visible.get("scenarios", []):
        if isinstance(scenario, dict):
            scenario.pop("prompt_is_explicit", None)
    for sample in visible.get("samples", []):
        if isinstance(sample, dict):
            sample.pop("instruction_text", None)
            sample.pop("prompt", None)
            argv = sample.get("planned_codex_argv")
            prompt_path = sample.get("prompt_path")
            if isinstance(argv, list) and isinstance(prompt_path, str):
                sample["planned_codex_argv"] = _public_argv(argv, Path(prompt_path))
            for turn in sample.get("planned_turns", []):
                if isinstance(turn, dict):
                    turn.pop("prompt", None)
                    turn_argv = turn.get("planned_codex_argv")
                    turn_prompt_path = turn.get("prompt_path")
                    if isinstance(turn_argv, list) and isinstance(turn_prompt_path, str):
                        turn["planned_codex_argv"] = _public_argv(
                            turn_argv,
                            Path(turn_prompt_path),
                        )
    return visible


def _public_argv(argv: list[str], prompt_path: Path) -> list[str]:
    if not argv:
        return argv
    visible = list(argv)
    visible[-1] = f"<prompt stored at {prompt_path}>"
    return visible


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
