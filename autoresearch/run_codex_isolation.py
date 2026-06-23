from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SUPPRESSED_INSTRUCTION_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".cursor/rules",
    ".agents/skills",
]
DEFAULT_PROMPTS = [
    "This is Codex isolation smoke 1. Do not use tools. Do not write files. Reply exactly: CODEX_ISOLATION_SMOKE_1_OK",
    "This is Codex isolation smoke 2. Do not use tools. Do not write files. Reply exactly: CODEX_ISOLATION_SMOKE_2_OK",
]


class IsolationError(ValueError):
    pass


def build_plan(max_runs: int) -> dict[str, Any]:
    if max_runs <= 0:
        raise IsolationError("max_runs must be positive")
    prompts = DEFAULT_PROMPTS[:max_runs]
    return {
        "harness": "codex-cli",
        "max_runs": max_runs,
        "planned_runs": [
            {"run": index, "prompt": prompt, "expected_fragment": f"CODEX_ISOLATION_SMOKE_{index}_OK"}
            for index, prompt in enumerate(prompts, 1)
        ],
        "argv_policy": ["codex", "--ask-for-approval", "never", "--disable", "plugins", "exec"],
        "exec_args": ["--ephemeral", "--json", "--ignore-user-config", "--sandbox", "read-only"],
        "env_policy": {
            "CODEX_HOME": "inherit authenticated operator home; do not record secret values",
            "OPENAI_API_KEY": "inherit only if configured; do not record value",
        },
        "limits": _limits(),
    }


def run_battery(out_dir: str | Path, max_runs: int) -> dict[str, Any]:
    plan = build_plan(max_runs)
    output_root = Path(out_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    runs = []
    for item in plan["planned_runs"]:
        runs.append(_run_one(output_root, item["run"], item["prompt"], item["expected_fragment"]))
    summary = {
        "schema_version": 1,
        "harness": "codex-cli",
        "runs": runs,
        "run_count": len(runs),
        "all_exit_zero": all(run["exit_code"] == 0 for run in runs),
        "all_expected_fragments_present": all(run["expected_fragment_present"] for run in runs),
        "any_plugin_or_skill_warnings": any(run["plugin_or_skill_warnings_present"] for run in runs),
        "any_workspace_contamination": any(run["workspace_contamination_present"] for run in runs),
        "limits": _limits(),
    }
    (output_root / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run a small live Codex isolation battery with no-tool prompts."
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-runs", type=int, default=2)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args(argv)
    if args.dry_run and args.run:
        print("choose only one of --dry-run or --run", file=sys.stderr)
        return 2
    try:
        result = run_battery(args.out, args.max_runs) if args.run else build_plan(args.max_runs)
    except (OSError, IsolationError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


def _run_one(output_root: Path, run_number: int, prompt: str, expected_fragment: str) -> dict[str, Any]:
    run_dir = output_root / f"run-{run_number:04d}"
    workspace = run_dir / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    command_path = run_dir / "command.json"
    manifest_path = run_dir / "workspace-manifest.json"
    stdout_path = run_dir / "codex.stdout.jsonl"
    stderr_path = run_dir / "codex.stderr"
    last_message_path = run_dir / "last-message.txt"
    pre_present = _present_suppressed(workspace)
    argv = [
        "codex",
        "--ask-for-approval",
        "never",
        "--disable",
        "plugins",
        "exec",
        "--cd",
        str(workspace),
        "--skip-git-repo-check",
        "--ephemeral",
        "--json",
        "--output-last-message",
        str(last_message_path),
        "--ignore-user-config",
        "--sandbox",
        "read-only",
        prompt,
    ]
    started = _now()
    completed = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    ended = _now()
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    last_message = last_message_path.read_text(encoding="utf-8") if last_message_path.exists() else ""
    events = _jsonl_events(completed.stdout)
    usage = _usage(events)
    post_present = _present_suppressed(workspace)
    non_git_files = _non_git_files(workspace)
    stderr_has_loader_warnings = _has_loader_warnings(completed.stderr)

    command = {
        "schema_version": 1,
        "run": run_number,
        "start_timestamp_utc": started,
        "end_timestamp_utc": ended,
        "argv": argv,
        "exit_code": completed.returncode,
        "stdout_jsonl_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "last_message_path": str(last_message_path),
        "expected_fragment": expected_fragment,
        "expected_fragment_present": expected_fragment in last_message,
        "usage": usage,
        "plugin_or_skill_warnings_present": stderr_has_loader_warnings,
    }
    command_path.write_text(json.dumps(command, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "schema_version": 1,
        "run": run_number,
        "workspace": str(workspace),
        "suppressed_instruction_files": SUPPRESSED_INSTRUCTION_FILES,
        "pre_run_present_suppressed_instruction_files": pre_present,
        "post_run_present_suppressed_instruction_files": post_present,
        "post_run_non_git_workspace_files": non_git_files,
        "workspace_contamination_present": bool(post_present or non_git_files),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    return {
        "run": run_number,
        "exit_code": completed.returncode,
        "expected_fragment": expected_fragment,
        "expected_fragment_present": expected_fragment in last_message,
        "jsonl_event_count": len(events),
        "usage": usage,
        "plugin_or_skill_warnings_present": stderr_has_loader_warnings,
        "workspace_contamination_present": manifest["workspace_contamination_present"],
        "command_path": str(command_path),
        "workspace_manifest_path": str(manifest_path),
        "stdout_jsonl_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "last_message_path": str(last_message_path),
    }


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


def _has_loader_warnings(stderr: str) -> bool:
    markers = (
        "codex_core_plugins",
        "codex_core_skills",
        "plugin manifest",
        "skill loader",
    )
    return any(marker in stderr for marker in markers)


def _present_suppressed(workspace: Path) -> list[str]:
    return [path for path in SUPPRESSED_INSTRUCTION_FILES if (workspace / path).exists()]


def _non_git_files(workspace: Path) -> list[str]:
    result = []
    for path in workspace.rglob("*"):
        if not path.is_file():
            continue
        try:
            relative = path.relative_to(workspace)
        except ValueError:
            continue
        if relative.parts and relative.parts[0] == ".git":
            continue
        result.append(str(relative))
    return sorted(result)


def _limits() -> list[str]:
    return [
        "Smoke prompts request no tools and no file writes.",
        "This battery does not prove hidden system context absence.",
        "Authenticated operator CODEX_HOME is inherited; secret values are not recorded.",
        "Results are isolation evidence, not candidate quality evidence.",
    ]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
