from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SEED_ROOT = REPO_ROOT / "autoresearch" / "trial-seeds"
SCENARIO_CATALOG = REPO_ROOT / "autoresearch" / "catalogs" / "scenarios.json"
SCORE_CATALOG = REPO_ROOT / "autoresearch" / "catalogs" / "scores.json"
OUTPUT = SEED_ROOT / "index.json"


def main() -> int:
    scenarios_data = _load_json(SCENARIO_CATALOG)
    scores_data = _load_json(SCORE_CATALOG)
    scenarios = {
        scenario["id"]: scenario for scenario in scenarios_data["scenarios"]
    }
    scores = {score["id"]: score for score in scores_data["scores"]}

    seed_entries = []
    scenario_counts: dict[str, int] = {}
    for seed_dir in sorted(path for path in SEED_ROOT.iterdir() if path.is_dir()):
        raw_path = seed_dir / "raw.json"
        if not raw_path.exists():
            continue
        raw = _load_json(raw_path)
        scenario_id = raw.get("scenario_id")
        scenario = scenarios.get(scenario_id)
        if scenario is None:
            raise SystemExit(f"{raw_path}: unknown scenario_id {scenario_id!r}")
        scenario_counts[scenario_id] = scenario_counts.get(scenario_id, 0) + 1
        workspace_manifest_path = _workspace_manifest_path(raw, seed_dir)
        workspace_path = workspace_manifest_path.parent
        material_records, material_sources, counts = _workspace_inventory(workspace_path)
        target_scores = list(scenario.get("target_scores", []))

        seed_entries.append(
            {
                "id": seed_dir.name,
                "scenario_id": scenario_id,
                "scenario_slug": scenario.get("slug"),
                "target_scores": target_scores,
                "target_score_names": [
                    scores[score_id]["name"]
                    for score_id in target_scores
                    if score_id in scores
                ],
                "source_experiment_id": raw.get("experiment_id"),
                "raw_path": _rel(raw_path),
                "workspace_manifest_path": _rel(workspace_manifest_path),
                "workspace_path": _rel(workspace_path),
                "complexity": _complexity(counts),
                "condition_summary": _condition_summary(seed_dir.name, scenario),
                "conditions_created": _conditions_created(
                    scenario,
                    material_records,
                    material_sources,
                    counts,
                ),
                "experiment_use": _experiment_use(scenario, target_scores, scores),
                "suggested_prompt_family": scenario.get("user_prompt_or_task_input", ""),
                "expected_high_quality_behavior": scenario.get(
                    "expected_high_quality_behavior", ""
                ),
                "expected_failure_behavior": scenario.get(
                    "expected_failure_behavior", ""
                ),
                "known_traps": _known_traps(scenario),
                "quality_floor_signals": _quality_floor_signals(scenario),
                "material_records": material_records[:24],
                "material_source_files": material_sources[:24],
                "workspace_file_counts": counts,
                "workspace_procedure": (
                    f"Copy {_rel(workspace_path)} into a private subject workspace, "
                    "run one live subject turn, then archive the resulting workspace."
                ),
            }
        )

    index = {
        "schema_version": 1,
        "updated": "2026-06-27",
        "source_decision": ".10x/decisions/autoresearch-live-trial-scientist-inspection.md",
        "source_spec": ".10x/specs/10x-autoresearch-loop.md",
        "source_scenarios": "autoresearch/catalogs/scenarios.json",
        "source_scores": "autoresearch/catalogs/scores.json",
        "purpose": (
            "Selection index for live trial seed workspaces. Seeds create "
            "starting conditions for subject-agent experiments; they are not "
            "answer keys."
        ),
        "selection_protocol": [
            "Start from the scientific question, then choose target score IDs.",
            "Filter seeds by scenario_id, target_scores, condition_summary, and known_traps.",
            "Read material_records and material_source_files before writing the prompt.",
            "Use raw_path as prior_raw_path and workspace_procedure in the experiment definition.",
            "Register expected behavior and quality floors in scientific_contract before execution.",
        ],
        "scenario_selection_guide": _scenario_selection_guide(
            scenarios,
            scores,
            scenario_counts,
        ),
        "seeds": seed_entries,
    }
    OUTPUT.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(REPO_ROOT)} ({len(seed_entries)} seeds)")
    return 0


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _workspace_manifest_path(raw: dict[str, Any], seed_dir: Path) -> Path:
    metadata = raw.get("harness_metadata")
    if isinstance(metadata, dict):
        manifest = metadata.get("workspace_manifest_path")
        if isinstance(manifest, str) and manifest:
            path = REPO_ROOT / manifest
            if path.exists():
                return path
    fallback = seed_dir / "workspace" / "workspace-manifest.json"
    if not fallback.exists():
        raise SystemExit(f"{seed_dir}: missing workspace-manifest.json")
    return fallback


def _workspace_inventory(workspace_path: Path) -> tuple[list[str], list[str], dict[str, int]]:
    records: list[str] = []
    sources: list[str] = []
    total = 0
    for path in sorted(item for item in workspace_path.rglob("*") if item.is_file()):
        rel = path.relative_to(workspace_path).as_posix()
        if rel == "workspace-manifest.json":
            continue
        total += 1
        if rel.startswith(".10x/"):
            records.append(rel)
        else:
            sources.append(rel)
    return records, sources, {
        "total_files": total,
        "record_files": len(records),
        "source_files": len(sources),
    }


def _condition_summary(seed_id: str, scenario: dict[str, Any]) -> str:
    seed_name = seed_id.replace("-", " ")
    return (
        f"{seed_name}: {scenario.get('purpose', '').rstrip('.')}. "
        f"Primary scenario {scenario.get('id')} ({scenario.get('slug')})."
    )


def _conditions_created(
    scenario: dict[str, Any],
    material_records: list[str],
    material_sources: list[str],
    counts: dict[str, int],
) -> list[str]:
    conditions = [
        f"Workspace state: {scenario.get('initial_workspace_state', '')}",
        f"Existing records: {scenario.get('existing_records', '')}",
        f"Scenario purpose: {scenario.get('purpose', '')}",
    ]
    if material_records:
        conditions.append(
            "Record graph includes "
            f"{counts['record_files']} files, including {_sample(material_records)}."
        )
    if material_sources:
        conditions.append(
            "Source/workspace includes "
            f"{counts['source_files']} files, including {_sample(material_sources)}."
        )
    return conditions


def _experiment_use(
    scenario: dict[str, Any],
    target_scores: list[str],
    scores: dict[str, dict[str, Any]],
) -> str:
    names = [
        scores[score_id]["name"]
        for score_id in target_scores
        if score_id in scores
    ]
    if names:
        return "Use to test " + ", ".join(names) + "."
    return f"Use to test {scenario.get('purpose', 'the scenario behavior')}."


def _known_traps(scenario: dict[str, Any]) -> list[str]:
    traps = []
    failure = scenario.get("expected_failure_behavior")
    if isinstance(failure, str) and failure:
        traps.append(failure)
    for item in scenario.get("known_false_positives", []):
        traps.append(str(item))
    return traps


def _quality_floor_signals(scenario: dict[str, Any]) -> list[str]:
    signals = []
    for item in scenario.get("disallowed_writes", []):
        signals.append(f"Disallowed write: {item}")
    for item in scenario.get("required_observations", []):
        signals.append(f"Required observation: {item}")
    for item in scenario.get("scoring_hints", []):
        signals.append(f"Rubric hint: {item}")
    return signals


def _scenario_selection_guide(
    scenarios: dict[str, dict[str, Any]],
    scores: dict[str, dict[str, Any]],
    scenario_counts: dict[str, int],
) -> list[dict[str, Any]]:
    guide = []
    for scenario_id in sorted(scenarios):
        scenario = scenarios[scenario_id]
        target_scores = list(scenario.get("target_scores", []))
        guide.append(
            {
                "scenario_id": scenario_id,
                "slug": scenario.get("slug"),
                "seed_count": scenario_counts.get(scenario_id, 0),
                "purpose": scenario.get("purpose"),
                "target_scores": target_scores,
                "target_score_names": [
                    scores[score_id]["name"]
                    for score_id in target_scores
                    if score_id in scores
                ],
                "prompt_family": scenario.get("user_prompt_or_task_input"),
                "expected_high_quality_behavior": scenario.get(
                    "expected_high_quality_behavior"
                ),
                "expected_failure_behavior": scenario.get(
                    "expected_failure_behavior"
                ),
            }
        )
    return guide


def _complexity(counts: dict[str, int]) -> str:
    if counts["total_files"] >= 10 or counts["record_files"] >= 4:
        return "rich"
    if counts["total_files"] >= 3 or counts["record_files"] >= 2:
        return "medium"
    return "small"


def _sample(paths: list[str], limit: int = 4) -> str:
    sample = paths[:limit]
    extra = len(paths) - len(sample)
    text = ", ".join(sample)
    if extra > 0:
        text += f", and {extra} more"
    return text


def _rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


if __name__ == "__main__":
    raise SystemExit(main())
