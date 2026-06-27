from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXPECTED_SCORE_IDS = tuple(f"S{i:03d}" for i in range(1, 10))
EXPECTED_SCENARIO_IDS = tuple(f"SCN-{i:03d}" for i in range(1, 16))
FALLBACK_REQUIREMENT_IDS = tuple(f"REQ-{i:03d}" for i in range(1, 23))
SKILL_BODY_CHAR_BUDGET = 40_000

SCORE_REQUIRED_TEXT = (
    "id",
    "slug",
    "name",
    "summary_rubric",
)
SCORE_REQUIRED_LISTS = (
    "inputs",
    "outputs",
    "sub_scores",
    "hard_floors",
    "manual_inspection_triggers",
    "known_false_positives",
    "known_false_negatives",
    "related_requirements",
)
SCENARIO_REQUIRED_TEXT = (
    "id",
    "slug",
    "purpose",
    "user_prompt_or_task_input",
    "initial_workspace_state",
    "existing_records",
    "expected_high_quality_behavior",
    "expected_failure_behavior",
    "workspace_reset_procedure",
)
SCENARIO_REQUIRED_LISTS = (
    "target_scores",
    "allowed_writes",
    "disallowed_writes",
    "trial_seed_paths",
    "required_observations",
    "scoring_hints",
    "known_false_positives",
    "known_false_negatives",
)
EXPERIMENT_TEMPLATE_SECTIONS = (
    "Experiment ID",
    "Driver",
    "Question Or Hypothesis",
    "Motivation",
    "Method Tier",
    "Arms",
    "Control",
    "Scenario Set",
    "Scientific Contract",
    "Subject Agent And Model",
    "Harness Target",
    "Scenario And Workspace Procedure",
    "Repetition Count",
    "Prediction",
    "Rubric Criteria",
    "Quality Floors",
    "Budget And Stop Conditions",
    "Write Boundary",
    "Raw Output Destination",
    "Rubric And Inspection Configuration",
    "Manual Inspection Requirement",
    "Promotion Criteria",
    "Known Risks And Confounders",
    "Execution Log",
    "Trial Artifacts",
    "Manual Inspection Findings",
    "Final Verdict",
)
MANUAL_INSPECTION_SECTIONS = (
    "Scope",
    "Required Checks",
    "Recording Triggers",
    "Observations",
    "Findings",
    "Conclusion And Limits",
)
MANUAL_INSPECTION_CHECKS = (
    "rubric judgment matches subject behavior",
    "scenario included the inputs",
    "control actually elicited",
    "candidate did not improve by silently narrowing scope",
    "judgment rationale points to real output",
    "No high-severity failure",
)


@dataclass
class ValidationResult:
    errors: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_contracts(root: str | Path) -> ValidationResult:
    repo_root = Path(root)
    errors: list[str] = []

    spec_text = _read_text(
        repo_root / ".10x" / "specs" / "10x-autoresearch-loop.md",
        ".10x/specs/10x-autoresearch-loop.md",
        errors,
    )
    requirement_ids = _ids_from_text(spec_text, r"\bREQ-\d{3}\b")
    if not requirement_ids:
        requirement_ids = set(FALLBACK_REQUIREMENT_IDS)

    scores_path = repo_root / "autoresearch" / "catalogs" / "scores.json"
    scenarios_path = repo_root / "autoresearch" / "catalogs" / "scenarios.json"
    experiment_path = repo_root / "autoresearch" / "templates" / "experiment.md"
    manual_path = (
        repo_root / "autoresearch" / "templates" / "manual-inspection.md"
    )
    split_path = repo_root / "autoresearch" / "splits" / "skill-improvement-v1.json"
    seed_index_path = repo_root / "autoresearch" / "trial-seeds" / "index.json"

    scores_data = _load_json(scores_path, "scores.json", errors)
    scenarios_data = _load_json(scenarios_path, "scenarios.json", errors)

    score_ids: set[str] = set()
    if isinstance(scores_data, dict):
        _validate_contract_sources("scores.json", scores_data, errors)
        _validate_score_shared_rules(scores_data, errors)
        score_ids = _validate_scores(scores_data, requirement_ids, errors)

    scenario_ids: set[str] = set()
    if isinstance(scenarios_data, dict):
        _validate_contract_sources("scenarios.json", scenarios_data, errors)
        scenario_ids = _validate_scenarios(scenarios_data, score_ids, errors)

    experiment_text = _read_text(
        experiment_path, "templates/experiment.md", errors
    )
    if experiment_text is not None:
        _validate_experiment_template(experiment_text, errors)

    manual_text = _read_text(
        manual_path, "templates/manual-inspection.md", errors
    )
    if manual_text is not None:
        _validate_manual_inspection_template(manual_text, errors)

    split_data = _load_json(split_path, "splits/skill-improvement-v1.json", errors)
    if isinstance(split_data, dict):
        _validate_skill_improvement_split(split_data, scenario_ids, errors)

    _validate_live_seed_workspaces(repo_root, errors)
    seed_index_data = _load_json(
        seed_index_path, "trial-seeds/index.json", errors
    )
    if isinstance(seed_index_data, dict):
        _validate_trial_seed_index(
            repo_root,
            seed_index_data,
            scenario_ids,
            score_ids,
            errors,
        )
    _validate_skill_size_budget(repo_root, errors)

    return ValidationResult(errors)


def _load_json(path: Path, label: str, errors: list[str]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{label}: file not found")
    except json.JSONDecodeError as exc:
        errors.append(f"{label}: invalid JSON at line {exc.lineno}: {exc.msg}")
    return None


def _validate_live_seed_workspaces(repo_root: Path, errors: list[str]) -> None:
    seed_root = repo_root / "autoresearch" / "trial-seeds"
    if not seed_root.exists():
        return

    for raw_path in sorted(seed_root.glob("*/raw.json")):
        raw_label = _rel_label(repo_root, raw_path)
        raw = _load_json(raw_path, raw_label, errors)
        if not isinstance(raw, dict):
            continue

        metadata = raw.get("harness_metadata")
        if not isinstance(metadata, dict) or metadata.get("kind") != "seed-workspace":
            continue

        manifest_ref = metadata.get("workspace_manifest_path")
        if not _non_empty_string(manifest_ref):
            errors.append(f"{raw_label}: seed-workspace requires workspace_manifest_path")
            continue

        manifest_path = _resolve_repo_path(repo_root, manifest_ref)
        manifest_label = _rel_label(repo_root, manifest_path)
        manifest = _load_json(manifest_path, manifest_label, errors)
        if not isinstance(manifest, dict):
            continue

        workspace_ref = manifest.get("workspace")
        if not _non_empty_string(workspace_ref):
            errors.append(f"{manifest_label}: seed workspace manifest requires workspace")
            continue

        workspace_path = _resolve_seed_workspace_path(
            repo_root,
            manifest_path,
            workspace_ref,
        )
        if not workspace_path.is_dir():
            errors.append(
                f"{manifest_label}: workspace does not resolve to a directory: {workspace_ref}"
            )
            continue

        if (workspace_path / manifest_path.name).resolve() != manifest_path.resolve():
            errors.append(
                f"{manifest_label}: resolved workspace must contain its workspace manifest"
            )


def _validate_trial_seed_index(
    repo_root: Path,
    data: dict[str, Any],
    scenario_ids: set[str],
    score_ids: set[str],
    errors: list[str],
) -> None:
    label = "trial-seeds/index.json"
    if data.get("schema_version") != 1:
        errors.append(f"{label}: schema_version must be 1")
    if data.get("source_scenarios") != "autoresearch/catalogs/scenarios.json":
        errors.append(f"{label}: source_scenarios must point to scenarios catalog")
    if data.get("source_scores") != "autoresearch/catalogs/scores.json":
        errors.append(f"{label}: source_scores must point to scores catalog")
    if not isinstance(data.get("selection_protocol"), list) or not data["selection_protocol"]:
        errors.append(f"{label}: selection_protocol must be a non-empty list")

    seed_root = repo_root / "autoresearch" / "trial-seeds"
    actual_seed_ids = {
        path.name
        for path in seed_root.iterdir()
        if path.is_dir() and (path / "raw.json").exists()
    }
    seeds = data.get("seeds")
    if not isinstance(seeds, list) or not seeds:
        errors.append(f"{label}: seeds must be a non-empty list")
        return

    indexed_ids: set[str] = set()
    for index, seed in enumerate(seeds):
        if not isinstance(seed, dict):
            errors.append(f"{label}: seeds[{index}] must be an object")
            continue
        seed_id = seed.get("id")
        seed_label = f"{label}:{seed_id or index}"
        if not _non_empty_string(seed_id):
            errors.append(f"{seed_label}: id must be a non-empty string")
            continue
        if seed_id in indexed_ids:
            errors.append(f"{label}: duplicate seed id {seed_id}")
        indexed_ids.add(seed_id)

        scenario_id = seed.get("scenario_id")
        if scenario_id not in scenario_ids:
            errors.append(f"{seed_label}: unknown scenario_id {scenario_id}")
        for score_id in seed.get("target_scores", []):
            if score_id not in score_ids:
                errors.append(f"{seed_label}: unknown target score {score_id}")

        for field in (
            "condition_summary",
            "experiment_use",
            "suggested_prompt_family",
            "expected_high_quality_behavior",
            "expected_failure_behavior",
            "raw_path",
            "workspace_manifest_path",
            "workspace_path",
            "workspace_procedure",
        ):
            if not _non_empty_string(seed.get(field)):
                errors.append(f"{seed_label}: {field} must be a non-empty string")
        for field in (
            "target_scores",
            "conditions_created",
            "known_traps",
            "quality_floor_signals",
            "material_records",
            "material_source_files",
        ):
            if not isinstance(seed.get(field), list):
                errors.append(f"{seed_label}: {field} must be a list")

        raw_path = _resolve_repo_path(repo_root, str(seed.get("raw_path", "")))
        manifest_path = _resolve_repo_path(
            repo_root,
            str(seed.get("workspace_manifest_path", "")),
        )
        workspace_path = _resolve_repo_path(repo_root, str(seed.get("workspace_path", "")))
        if not raw_path.exists():
            errors.append(f"{seed_label}: raw_path does not exist")
        if not manifest_path.exists():
            errors.append(f"{seed_label}: workspace_manifest_path does not exist")
        if not workspace_path.is_dir():
            errors.append(f"{seed_label}: workspace_path does not exist")
        if raw_path.exists() and raw_path.parent.name != seed_id:
            errors.append(f"{seed_label}: raw_path must live under the seed directory")

    missing = sorted(actual_seed_ids - indexed_ids)
    extra = sorted(indexed_ids - actual_seed_ids)
    if missing:
        errors.append(f"{label}: missing seed index entries: {', '.join(missing)}")
    if extra:
        errors.append(f"{label}: seed index entries without raw seed: {', '.join(extra)}")


def _read_text(path: Path, label: str, errors: list[str]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"{label}: file not found")
        return None


def _validate_skill_size_budget(repo_root: Path, errors: list[str]) -> None:
    skill_text = _read_text(repo_root / "SKILL.md", "SKILL.md", errors)
    if skill_text is None:
        return
    body_chars = skill_body_char_count(skill_text)
    if body_chars > SKILL_BODY_CHAR_BUDGET:
        errors.append(
            "SKILL.md: body character count "
            f"{body_chars} exceeds budget {SKILL_BODY_CHAR_BUDGET}"
        )


def skill_body_char_count(text: str) -> int:
    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == "---":
        for index, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                return len("".join(lines[index + 1 :]))
    return len(text)


def _resolve_repo_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return repo_root / path


def _resolve_seed_workspace_path(
    repo_root: Path,
    manifest_path: Path,
    workspace_ref: str,
) -> Path:
    path = Path(workspace_ref)
    if path.is_absolute():
        return path
    manifest_relative = manifest_path.parent / path
    if manifest_relative.is_dir():
        return manifest_relative
    return repo_root / path


def _rel_label(repo_root: Path, path: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return str(path)


def _ids_from_text(text: str | None, pattern: str) -> set[str]:
    if text is None:
        return set()
    return set(re.findall(pattern, text))


def _validate_contract_sources(
    label: str, data: dict[str, Any], errors: list[str]
) -> None:
    if data.get("schema_version") != 1:
        errors.append(f"{label}: schema_version must be 1")
    if data.get("source_spec") != ".10x/specs/10x-autoresearch-loop.md":
        errors.append(f"{label}: source_spec must point to the active spec")
    if (
        data.get("source_decision")
        != ".10x/decisions/autoresearch-live-trial-scientist-inspection.md"
    ):
        errors.append(f"{label}: source_decision must point to the active decision")


def _validate_scores(
    data: dict[str, Any], requirement_ids: set[str], errors: list[str]
) -> set[str]:
    scores = data.get("scores")
    if not isinstance(scores, list):
        errors.append("scores.json: scores must be a list")
        return set()

    score_ids = _validate_id_set(
        "scores.json", "score", scores, EXPECTED_SCORE_IDS, errors
    )
    for index, score in enumerate(scores):
        if not isinstance(score, dict):
            errors.append(f"scores.json: scores[{index}] must be an object")
            continue
        label = f"scores.json:{score.get('id', index)}"

        for field in SCORE_REQUIRED_TEXT:
            if not _non_empty_string(score.get(field)):
                errors.append(f"{label}: {field} must be a non-empty string")
        for field in SCORE_REQUIRED_LISTS:
            value = score.get(field)
            if not isinstance(value, list):
                errors.append(f"{label}: {field} must be a list")

        range_value = score.get("range")
        if not isinstance(range_value, dict):
            errors.append(f"{label}: range must be an object")
        else:
            if not _number(range_value.get("minimum")):
                errors.append(f"{label}: range.minimum must be numeric")
            maximum = range_value.get("maximum")
            if maximum is not None and not _number(maximum):
                errors.append(f"{label}: range.maximum must be numeric or null")

        if not isinstance(score.get("higher_is_better"), bool):
            errors.append(f"{label}: higher_is_better must be boolean")
        if not isinstance(score.get("quality_gated"), bool):
            errors.append(f"{label}: quality_gated must be boolean")
        if score.get("quality_gated") is True and not _number(score.get("active_floor")):
            errors.append(f"{label}: quality_gated scores need numeric active_floor")

        sub_scores = score.get("sub_scores")
        if isinstance(sub_scores, list):
            _validate_sub_scores(label, sub_scores, score.get("id"), errors)

        hard_floors = score.get("hard_floors")
        if isinstance(hard_floors, list):
            for floor_index, floor in enumerate(hard_floors):
                if not isinstance(floor, dict):
                    errors.append(
                        f"{label}: hard_floors[{floor_index}] must be an object"
                    )
                elif not _non_empty_string(floor.get("condition")):
                    errors.append(
                        f"{label}: hard_floors[{floor_index}].condition is required"
                    )

        related = score.get("related_requirements")
        if isinstance(related, list):
            for requirement_id in related:
                if requirement_id not in requirement_ids:
                    errors.append(
                        f"{label}: unknown related requirement {requirement_id}"
                    )

    return score_ids


def _validate_score_shared_rules(data: dict[str, Any], errors: list[str]) -> None:
    label = "scores.json:shared_rules"
    shared = data.get("shared_rules")
    if not isinstance(shared, dict):
        errors.append(f"{label}: shared_rules must be an object")
        return
    if "top_line_rule" in shared:
        errors.append(f"{label}: top_line_rule is retired")
    for field in (
        "manual_scoring_policy",
        "confidence_policy",
        "floor_policy",
    ):
        if not _non_empty_string(shared.get(field)):
            errors.append(f"{label}: {field} must be a non-empty string")
    if not isinstance(shared.get("score_band_guide"), dict) or not shared["score_band_guide"]:
        errors.append(f"{label}: score_band_guide must be a non-empty object")
    labels = shared.get("confidence_labels")
    if not isinstance(labels, list) or not all(_non_empty_string(item) for item in labels):
        errors.append(f"{label}: confidence_labels must be a list of non-empty strings")
    required_outputs = shared.get("inspection_outputs_should_include")
    if not isinstance(required_outputs, list):
        errors.append(f"{label}: inspection_outputs_should_include must be a list")
    else:
        for required in ("evidence references", "unsupported assumptions", "floor_triggers"):
            if required not in required_outputs:
                errors.append(f"{label}: inspection outputs must include {required}")


def _validate_sub_scores(
    label: str, sub_scores: list[Any], score_id: Any, errors: list[str]
) -> None:
    if not sub_scores:
        if score_id != "S009":
            errors.append(f"{label}: sub_scores must not be empty")
        return

    total = 0
    for index, sub_score in enumerate(sub_scores):
        if not isinstance(sub_score, dict):
            errors.append(f"{label}: sub_scores[{index}] must be an object")
            continue
        if not _non_empty_string(sub_score.get("name")):
            errors.append(f"{label}: sub_scores[{index}].name is required")
        points = sub_score.get("points")
        if not _number(points):
            errors.append(f"{label}: sub_scores[{index}].points must be numeric")
        else:
            total += points
    if total != 100:
        errors.append(f"{label}: sub_scores points must total 100")


def _validate_scenarios(
    data: dict[str, Any], score_ids: set[str], errors: list[str]
) -> set[str]:
    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list):
        errors.append("scenarios.json: scenarios must be a list")
        return set()

    scenario_ids = _validate_id_set(
        "scenarios.json", "scenario", scenarios, EXPECTED_SCENARIO_IDS, errors
    )
    for index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            errors.append(f"scenarios.json: scenarios[{index}] must be an object")
            continue
        label = f"scenarios.json:{scenario.get('id', index)}"

        for field in SCENARIO_REQUIRED_TEXT:
            if not _non_empty_string(scenario.get(field)):
                errors.append(f"{label}: {field} must be a non-empty string")
        for field in SCENARIO_REQUIRED_LISTS:
            value = scenario.get(field)
            if not isinstance(value, list):
                errors.append(f"{label}: {field} must be a list")

        for target_score in scenario.get("target_scores", []):
            if target_score not in score_ids:
                errors.append(f"{label}: unknown target score {target_score}")

        for field in (
            "target_scores",
            "disallowed_writes",
            "required_observations",
            "scoring_hints",
            "known_false_positives",
            "known_false_negatives",
        ):
            value = scenario.get(field)
            if isinstance(value, list) and not value:
                errors.append(f"{label}: {field} must not be empty")

    return scenario_ids


def _validate_id_set(
    label: str,
    kind: str,
    records: list[Any],
    expected_ids: tuple[str, ...],
    errors: list[str],
) -> set[str]:
    found: list[str] = []
    seen: set[str] = set()
    id_pattern = re.compile(r"^S00[1-9]$" if kind == "score" else r"^SCN-\d{3}$")

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            continue
        record_id = record.get("id")
        if not isinstance(record_id, str):
            errors.append(f"{label}: {kind} at index {index} needs string id")
            continue
        if not id_pattern.fullmatch(record_id):
            errors.append(f"{label}: invalid {kind} id {record_id}")
        if record_id in seen:
            errors.append(f"{label}: duplicate {kind} ID {record_id}")
        seen.add(record_id)
        found.append(record_id)

    found_set = set(found)
    missing = [record_id for record_id in expected_ids if record_id not in found_set]
    extra = [record_id for record_id in found if record_id not in expected_ids]
    if missing:
        errors.append(f"{label}: missing {kind} IDs: {', '.join(missing)}")
    if extra:
        errors.append(f"{label}: unexpected {kind} IDs: {', '.join(extra)}")
    return found_set


def _validate_experiment_template(text: str, errors: list[str]) -> None:
    label = "templates/experiment.md"
    _validate_common_headers(label, text, errors)
    for section in EXPERIMENT_TEMPLATE_SECTIONS:
        if f"## {section}" not in text:
            errors.append(f"{label}: missing section {section}")
    for field in ("MINE", "MICRO", "FULL"):
        if field not in text:
            errors.append(f"{label}: missing method tier {field}")
    for field in ("no-10x-control", "current-10x", "candidate-variant"):
        if field not in text:
            errors.append(f"{label}: missing example arm {field}")
    for field in (
        "scientific_contract",
        "question",
        "hypothesis",
        "expected_behavior",
        "inspection_criteria",
        "quality_floor",
        "verdict_record_path",
        "workspace_procedure",
        "max_harness_runs",
        "estimated_wall_seconds_per_run",
        "timeout_seconds_per_run",
    ):
        if field not in text:
            errors.append(f"{label}: missing runner definition field {field}")
    if "exact ordered arms" not in text:
        errors.append(f"{label}: must state that the arms list is exact")
    if "autoresearch/trial-seeds/index.json" not in text:
        errors.append(f"{label}: must point scientists to the trial seed index")
    if "autoresearch/catalogs/scores.json" not in text:
        errors.append(f"{label}: must point scientists to the manual scoring rubric")


def _validate_manual_inspection_template(text: str, errors: list[str]) -> None:
    label = "templates/manual-inspection.md"
    _validate_common_headers(label, text, errors)
    if "Relates-To:" not in text:
        errors.append(f"{label}: missing Relates-To header")
    for section in MANUAL_INSPECTION_SECTIONS:
        if f"## {section}" not in text:
            errors.append(f"{label}: missing section {section}")
    for required_check in MANUAL_INSPECTION_CHECKS:
        if required_check not in text:
            errors.append(f"{label}: missing required check {required_check}")


def _validate_skill_improvement_split(
    data: dict[str, Any], scenario_ids: set[str], errors: list[str]
) -> None:
    label = "splits/skill-improvement-v1.json"
    if data.get("schema_version") != 1:
        errors.append(f"{label}: schema_version must be 1")
    if data.get("source_scenarios") != "autoresearch/catalogs/scenarios.json":
        errors.append(f"{label}: source_scenarios must point to scenarios catalog")

    exploration = _scenario_list(label, "exploration_scenarios", data, scenario_ids, errors)
    held_out = _scenario_list(label, "held_out_scenarios", data, scenario_ids, errors)
    review = _scenario_list(label, "review_scenarios", data, scenario_ids, errors)

    overlap = sorted(set(exploration) & set(held_out))
    if overlap:
        errors.append(f"{label}: exploration and held_out overlap: {', '.join(overlap)}")
    missing = sorted(scenario_ids - (set(exploration) | set(held_out)))
    if missing:
        errors.append(f"{label}: scenarios missing from exploration/held_out: {', '.join(missing)}")
    if not set(held_out).issubset(set(review)):
        errors.append(f"{label}: review_scenarios must include all held_out_scenarios")

    rules = data.get("rules")
    if not isinstance(rules, list) or not rules:
        errors.append(f"{label}: rules must be a non-empty list")
    elif not all(_non_empty_string(rule) for rule in rules):
        errors.append(f"{label}: rules must contain only non-empty strings")


def _scenario_list(
    label: str,
    field: str,
    data: dict[str, Any],
    scenario_ids: set[str],
    errors: list[str],
) -> list[str]:
    value = data.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{label}: {field} must be a non-empty list")
        return []
    result = []
    seen = set()
    for item in value:
        if not isinstance(item, str):
            errors.append(f"{label}: {field} entries must be strings")
            continue
        if item in seen:
            errors.append(f"{label}: {field} duplicate scenario {item}")
        seen.add(item)
        if item not in scenario_ids:
            errors.append(f"{label}: {field} unknown scenario {item}")
        result.append(item)
    return result


def _validate_common_headers(label: str, text: str, errors: list[str]) -> None:
    for header in ("Status:", "Created:", "Updated:"):
        if not re.search(rf"^{re.escape(header)}", text, flags=re.MULTILINE):
            errors.append(f"{label}: missing {header} header")


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate autoresearch static contracts."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root containing autoresearch/ and .10x/.",
    )
    args = parser.parse_args(argv)

    result = validate_contracts(args.root)
    if result.ok:
        print("autoresearch contracts valid")
        return 0

    print("autoresearch contracts invalid", file=sys.stderr)
    for error in result.errors:
        print(f"- {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
