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
    "fixture_reset",
)
SCENARIO_REQUIRED_LISTS = (
    "target_scores",
    "allowed_writes",
    "disallowed_writes",
    "fixture_paths",
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
    "Variants",
    "Control",
    "Scenario Set",
    "Subject Agent And Model",
    "Harness Target",
    "Scenario And Workspace Procedure",
    "Repetition Count",
    "Prediction",
    "Metrics To Score",
    "Quality Floors",
    "Budget And Stop Conditions",
    "Write Boundary",
    "Raw Output Destination",
    "Scorer Configuration",
    "Manual Inspection Requirement",
    "Promotion Criteria",
    "Known Risks And Confounders",
    "Execution Log",
    "Score Artifacts",
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
    "scorer matched subject behavior",
    "scenario included the inputs",
    "control actually elicited",
    "candidate did not improve by silently narrowing scope",
    "score rationale points to real output",
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
    schema_path = (
        repo_root / "autoresearch" / "schemas" / "score-artifact.schema.json"
    )
    experiment_path = repo_root / "autoresearch" / "templates" / "experiment.md"
    manual_path = (
        repo_root / "autoresearch" / "templates" / "manual-inspection.md"
    )
    split_path = repo_root / "autoresearch" / "splits" / "skill-improvement-v1.json"

    scores_data = _load_json(scores_path, "scores.json", errors)
    scenarios_data = _load_json(scenarios_path, "scenarios.json", errors)
    schema_data = _load_json(schema_path, "score-artifact.schema.json", errors)

    score_ids: set[str] = set()
    if isinstance(scores_data, dict):
        _validate_contract_sources("scores.json", scores_data, errors)
        score_ids = _validate_scores(scores_data, requirement_ids, errors)

    scenario_ids: set[str] = set()
    if isinstance(scenarios_data, dict):
        _validate_contract_sources("scenarios.json", scenarios_data, errors)
        scenario_ids = _validate_scenarios(scenarios_data, score_ids, errors)

    if isinstance(schema_data, dict):
        _validate_score_artifact_schema(schema_data, errors)

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
    seed_root = repo_root / "autoresearch" / "fixtures" / "live-seeds"
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
        != ".10x/decisions/autoresearch-initial-implementation-defaults.md"
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


def _validate_score_artifact_schema(
    data: dict[str, Any], errors: list[str]
) -> None:
    label = "score-artifact.schema.json"
    if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append(f"{label}: $schema must be draft 2020-12")
    if data.get("type") != "object":
        errors.append(f"{label}: root type must be object")
    if data.get("additionalProperties") is not False:
        errors.append(f"{label}: root additionalProperties must be false")

    required = data.get("required")
    properties = data.get("properties")
    if not isinstance(required, list):
        errors.append(f"{label}: required must be a list")
        required = []
    if not isinstance(properties, dict):
        errors.append(f"{label}: properties must be an object")
        properties = {}

    for field in (
        "experiment_id",
        "scenario_id",
        "variant_id",
        "rep",
        "model",
        "harness",
        "instruction_digest",
        "fixture_digest",
        "scores",
        "cost",
        "limits",
        "scorer",
    ):
        if field not in required:
            errors.append(f"{label}: required must include {field}")
        if field not in properties:
            errors.append(f"{label}: properties must define {field}")

    _validate_schema_pattern(
        label,
        "properties.scores.propertyNames.pattern",
        _nested_get(properties, ("scores", "propertyNames", "pattern")),
        EXPECTED_SCORE_IDS,
        "S010",
        errors,
    )
    _validate_schema_pattern(
        label,
        "properties.scenario_id.pattern",
        _nested_get(properties, ("scenario_id", "pattern")),
        EXPECTED_SCENARIO_IDS,
        None,
        errors,
    )

    defs = data.get("$defs")
    if not isinstance(defs, dict):
        errors.append(f"{label}: $defs must be an object")
        defs = {}
    for name in ("confidence", "evidence_ref", "floor_trigger", "score"):
        if name not in defs:
            errors.append(f"{label}: $defs must include {name}")

    for ref in _collect_refs(data):
        if not ref.startswith("#/$defs/"):
            errors.append(f"{label}: unsupported $ref {ref}")
            continue
        ref_name = ref.removeprefix("#/$defs/")
        if ref_name not in defs:
            errors.append(f"{label}: unresolved $ref {ref}")

    score_def = defs.get("score", {})
    if isinstance(score_def, dict):
        score_required = score_def.get("required", [])
        for field in (
            "value",
            "confidence",
            "floor_triggered",
            "rationale",
            "evidence_refs",
            "limits",
        ):
            if field not in score_required:
                errors.append(f"{label}: $defs.score.required must include {field}")

    scorer = properties.get("scorer", {})
    if isinstance(scorer, dict):
        scorer_required = scorer.get("required", [])
        for field in (
            "id",
            "trust_level",
            "inputs",
            "outputs",
            "known_false_positives",
            "known_false_negatives",
            "confidence",
            "manual_inspection_required",
            "manual_inspection_requirement",
            "limits",
        ):
            if field not in scorer_required:
                errors.append(f"{label}: scorer.required must include {field}")


def _validate_schema_pattern(
    label: str,
    field: str,
    pattern: Any,
    accepted: tuple[str, ...],
    rejected: str | None,
    errors: list[str],
) -> None:
    if not isinstance(pattern, str):
        errors.append(f"{label}: {field} must be a string")
        return
    compiled = re.compile(pattern)
    for value in accepted:
        if not compiled.fullmatch(value):
            errors.append(f"{label}: {field} does not accept {value}")
    if rejected is not None and compiled.fullmatch(rejected):
        errors.append(f"{label}: {field} unexpectedly accepts {rejected}")


def _nested_get(value: Any, keys: tuple[str, ...]) -> Any:
    current = value
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _collect_refs(value: Any) -> list[str]:
    refs: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref" and isinstance(child, str):
                refs.append(child)
            else:
                refs.extend(_collect_refs(child))
    elif isinstance(value, list):
        for child in value:
            refs.extend(_collect_refs(child))
    return refs


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
            errors.append(f"{label}: missing default arm {field}")


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
