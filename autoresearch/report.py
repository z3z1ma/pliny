from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
STATUS_FIELDS = (
    "status",
    "verdict",
    "result",
    "outcome",
    "result_status",
    "research_status",
    "comparison_status",
)
BOOLEAN_STATUS_FIELDS = (
    "negative_result",
    "null_result",
    "backfire",
    "backfired",
    "confounded",
)


class ReportError(ValueError):
    pass


def build_report(
    scores_path: str | Path,
    *,
    campaign_path: str | Path | None = None,
    repo_root: Path = REPO_ROOT,
) -> str:
    source = Path(scores_path)
    artifacts = load_artifacts(source)
    campaign = load_campaign_metadata(campaign_path) if campaign_path else None
    score_catalog = _load_catalog(
        repo_root / "autoresearch" / "catalogs" / "scores.json",
        "scores",
    )
    scenario_catalog = _load_catalog(
        repo_root / "autoresearch" / "catalogs" / "scenarios.json",
        "scenarios",
    )

    lines = [
        "# 10x Autoresearch Score Report",
        "",
        f"Source: `{_display_path(source)}`",
        "",
    ]
    if not artifacts:
        if campaign:
            lines.extend(_campaign_section(campaign))
        lines.extend(
            [
                "No score artifacts were found.",
                "",
                "Reports are secondary views; `.10x/` records and score artifacts remain canonical.",
                "",
            ]
        )
        return "\n".join(lines)

    lines.extend(_summary_section(artifacts))
    if campaign:
        lines.extend(_campaign_section(campaign))
    lines.extend(_score_vectors_section(artifacts, score_catalog, scenario_catalog))
    lines.extend(_arm_comparison_section(artifacts, score_catalog))
    lines.extend(_scenario_breakdown_section(artifacts, score_catalog))
    lines.extend(_quality_floor_section(artifacts, score_catalog))
    lines.extend(_status_section(artifacts))
    lines.extend(_inspection_section(artifacts))
    lines.extend(_cost_section(artifacts))
    lines.extend(
        [
            "## Report Limits",
            "",
            "- This report is a secondary view over saved score artifacts.",
            "- It does not make promotion decisions or hide component failures behind a top-line aggregate.",
            "- Unknown means the field was absent, null, or not numeric in the loaded artifact.",
            "",
        ]
    )
    return "\n".join(lines)


def load_artifacts(scores_path: str | Path) -> list[dict[str, Any]]:
    source = Path(scores_path)
    if not source.exists():
        raise ReportError(f"score artifact path does not exist: {source}")

    if source.is_file():
        paths = [source]
        root = source.parent
    else:
        paths = sorted(source.rglob("*.score.json"))
        root = source

    artifacts: list[dict[str, Any]] = []
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, dict):
            raise ReportError(f"{path}: score artifact must be a JSON object")
        artifacts.append({"path": path, "relative_path": _relative_path(path, root), "data": data})
    return artifacts


def load_campaign_metadata(path: str | Path) -> dict[str, Any]:
    metadata_path = Path(path)
    data = json.loads(metadata_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ReportError(f"{metadata_path}: campaign metadata must be a JSON object")
    return data


def write_report(
    scores_path: str | Path,
    out_path: str | Path,
    *,
    campaign_path: str | Path | None = None,
) -> Path:
    output_path = Path(out_path)
    report = build_report(scores_path, campaign_path=campaign_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown report from saved 10x autoresearch score artifacts."
    )
    parser.add_argument(
        "--scores",
        type=Path,
        required=True,
        help="Directory containing *.score.json artifacts, or one score artifact file.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Markdown report path to write.",
    )
    parser.add_argument(
        "--campaign",
        type=Path,
        help="Optional campaign metadata JSON with manual verdict/status context.",
    )
    args = parser.parse_args(argv)

    try:
        output_path = write_report(args.scores, args.out, campaign_path=args.campaign)
    except (OSError, json.JSONDecodeError, ReportError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"wrote {output_path}")
    return 0


def _summary_section(artifacts: list[dict[str, Any]]) -> list[str]:
    experiments = _unique(artifact["data"].get("experiment_id") for artifact in artifacts)
    scenarios = _unique(artifact["data"].get("scenario_id") for artifact in artifacts)
    arms = _unique(artifact["data"].get("variant_id") for artifact in artifacts)
    score_ids = _unique(
        score_id
        for artifact in artifacts
        for score_id in _scores(artifact["data"])
    )
    return [
        "## Summary",
        "",
        "| Artifact count | Experiments | Scenarios | Arms | Score IDs |",
        "| --- | --- | --- | --- | --- |",
        (
            f"| {len(artifacts)} | {_join_or_unknown(experiments)} | "
            f"{_join_or_unknown(scenarios)} | {_join_or_unknown(arms)} | "
            f"{_join_or_unknown(score_ids)} |"
        ),
        "",
    ]


def _campaign_section(campaign: dict[str, Any]) -> list[str]:
    lines = [
        "## Campaign Verdict",
        "",
        "| Field | Value |",
        "| --- | --- |",
    ]
    fields = (
        "campaign_id",
        "experiment_id",
        "verdict",
        "result_status",
        "promotion_decision",
        "candidate_id",
        "baseline_id",
    )
    for field in fields:
        if field in campaign:
            lines.append(f"| {_cell(field)} | {_cell(campaign.get(field))} |")

    statuses = campaign.get("statuses")
    if statuses is not None:
        lines.append(f"| statuses | {_cell(statuses)} |")

    manual = _dict(campaign.get("manual_inspection"))
    if manual:
        lines.append(f"| manual_inspection.status | {_cell(manual.get('status'))} |")
        lines.append(f"| manual_inspection.by | {_cell(manual.get('by'))} |")

    evidence_refs = _strings(campaign.get("evidence_refs"))
    if evidence_refs:
        lines.append(f"| evidence_refs | {_cell(evidence_refs)} |")

    limits = _strings(campaign.get("limits"))
    if limits:
        lines.append(f"| limits | {_cell(limits)} |")

    lines.extend(
        [
            "",
            "Campaign verdict metadata is manual/contextual. It does not modify score artifacts or upgrade scorer trust.",
            "",
        ]
    )
    return lines


def _score_vectors_section(
    artifacts: list[dict[str, Any]],
    score_catalog: dict[str, dict[str, Any]],
    scenario_catalog: dict[str, dict[str, Any]],
) -> list[str]:
    lines = [
        "## Score Vectors",
        "",
        "| Artifact | Experiment | Scenario | Arm | Rep | Score vector |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for artifact in artifacts:
        data = artifact["data"]
        scenario = _scenario_label(data.get("scenario_id"), scenario_catalog)
        lines.append(
            "| {path} | {experiment} | {scenario} | {arm} | {rep} | {vector} |".format(
                path=_cell(artifact["relative_path"]),
                experiment=_cell(data.get("experiment_id")),
                scenario=_cell(scenario),
                arm=_cell(data.get("variant_id")),
                rep=_cell(data.get("rep")),
                vector=_cell(_score_vector(data, score_catalog)),
            )
        )
    lines.append("")
    return lines


def _arm_comparison_section(
    artifacts: list[dict[str, Any]],
    score_catalog: dict[str, dict[str, Any]],
) -> list[str]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for artifact in artifacts:
        data = artifact["data"]
        arm = str(data.get("variant_id") or "unknown")
        for score_id, score in _scores(data).items():
            grouped.setdefault((score_id, arm), []).append(score)

    lines = [
        "## Arm Score Comparison",
        "",
        "| Score | Active floor | Arm | Samples | Average | Minimum | Maximum | Floor failures |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for score_id, arm in sorted(grouped):
        scores = grouped[(score_id, arm)]
        values = [_number(score.get("value")) for score in scores]
        values = [value for value in values if value is not None]
        lines.append(
            "| {score} | {floor} | {arm} | {samples} | {avg} | {minimum} | {maximum} | {failures} |".format(
                score=_cell(_score_label(score_id, score_catalog)),
                floor=_cell(_active_floor(score_id, score_catalog)),
                arm=_cell(arm),
                samples=len(scores),
                avg=_cell(_average(values)),
                minimum=_cell(min(values) if values else None),
                maximum=_cell(max(values) if values else None),
                failures=sum(1 for score in scores if bool(score.get("floor_triggered"))),
            )
        )
    lines.append("")
    return lines


def _scenario_breakdown_section(
    artifacts: list[dict[str, Any]],
    score_catalog: dict[str, dict[str, Any]],
) -> list[str]:
    arms = _unique(artifact["data"].get("variant_id") for artifact in artifacts)
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for artifact in artifacts:
        data = artifact["data"]
        scenario_id = str(data.get("scenario_id") or "unknown")
        arm = str(data.get("variant_id") or "unknown")
        for score_id, score in _scores(data).items():
            grouped.setdefault((scenario_id, score_id, arm), []).append(score)

    lines = [
        "## Scenario Breakdown",
        "",
        "| Scenario | Score | " + " | ".join(_cell(arm) for arm in arms) + " |",
        "| --- | --- | " + " | ".join("---" for _ in arms) + " |",
    ]
    scenario_score_pairs = sorted({(scenario_id, score_id) for scenario_id, score_id, _ in grouped})
    for scenario_id, score_id in scenario_score_pairs:
        cells = []
        for arm in arms:
            scores = grouped.get((scenario_id, score_id, arm), [])
            values = [_number(score.get("value")) for score in scores]
            values = [value for value in values if value is not None]
            failures = sum(1 for score in scores if bool(score.get("floor_triggered")))
            if not scores:
                cells.append("unknown")
            else:
                suffix = f", failures={failures}" if failures else ""
                cells.append(f"{_format_value(_average(values))} (n={len(scores)}{suffix})")
        lines.append(
            "| {scenario} | {score} | {cells} |".format(
                scenario=_cell(scenario_id),
                score=_cell(_score_label(score_id, score_catalog)),
                cells=" | ".join(_cell(cell) for cell in cells),
            )
        )
    lines.append("")
    return lines


def _quality_floor_section(
    artifacts: list[dict[str, Any]],
    score_catalog: dict[str, dict[str, Any]],
) -> list[str]:
    used_score_ids = _unique(
        _base_score_id(score_id)
        for artifact in artifacts
        for score_id in _scores(artifact["data"])
    )
    lines = [
        "## Quality Floors And Failures",
        "",
        "| Score | Active floor | Quality gated |",
        "| --- | ---: | --- |",
    ]
    for score_id in used_score_ids:
        catalog_entry = score_catalog.get(score_id, {})
        lines.append(
            "| {score} | {floor} | {gated} |".format(
                score=_cell(_score_label(score_id, score_catalog)),
                floor=_cell(catalog_entry.get("active_floor")),
                gated=_cell(catalog_entry.get("quality_gated")),
            )
        )

    failures = _floor_failures(artifacts, score_catalog)
    lines.extend(["", "### Floor Failures", ""])
    if not failures:
        lines.extend(["No floor failures present in the loaded artifacts.", ""])
        return lines

    lines.extend(
        [
            "| Artifact | Scenario | Arm | Score | Value | Condition | Effect | Evidence refs |",
            "| --- | --- | --- | --- | ---: | --- | --- | --- |",
        ]
    )
    for row in failures:
        lines.append(
            "| {artifact} | {scenario} | {arm} | {score} | {value} | {condition} | {effect} | {refs} |".format(
                artifact=_cell(row["artifact"]),
                scenario=_cell(row["scenario"]),
                arm=_cell(row["arm"]),
                score=_cell(row["score"]),
                value=_cell(row["value"]),
                condition=_cell(row["condition"]),
                effect=_cell(row["effect"]),
                refs=_cell(row["evidence_refs"]),
            )
        )
    lines.append("")
    return lines


def _status_section(artifacts: list[dict[str, Any]]) -> list[str]:
    rows = []
    for artifact in artifacts:
        data = artifact["data"]
        for field, value in _status_items(data):
            rows.append(
                {
                    "artifact": artifact["relative_path"],
                    "scenario": data.get("scenario_id"),
                    "arm": data.get("variant_id"),
                    "field": field,
                    "value": value,
                }
            )

    lines = ["## Result Statuses", ""]
    if not rows:
        lines.extend(
            [
                "No negative, null, backfire, confounded, or other result statuses were present.",
                "",
            ]
        )
        return lines

    lines.extend(
        [
            "| Artifact | Scenario | Arm | Field | Value |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| {artifact} | {scenario} | {arm} | {field} | {value} |".format(
                artifact=_cell(row["artifact"]),
                scenario=_cell(row["scenario"]),
                arm=_cell(row["arm"]),
                field=_cell(row["field"]),
                value=_cell(row["value"]),
            )
        )
    lines.append("")
    return lines


def _inspection_section(artifacts: list[dict[str, Any]]) -> list[str]:
    lines = [
        "## Manual Inspection, Trust, And Limits",
        "",
        "| Artifact | Scorer | Trust | Confidence | Manual status | Manual required | Limits |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for artifact in artifacts:
        data = artifact["data"]
        scorer = _dict(data.get("scorer"))
        manual = _dict(data.get("manual_inspection"))
        limits = _dedupe(
            _strings(data.get("limits"))
            + _strings(scorer.get("limits"))
            + _strings(manual.get("limits"))
        )
        lines.append(
            "| {artifact} | {scorer} | {trust} | {confidence} | {manual_status} | {manual_required} | {limits} |".format(
                artifact=_cell(artifact["relative_path"]),
                scorer=_cell(scorer.get("id")),
                trust=_cell(_trust_level(scorer.get("trust_level"))),
                confidence=_cell(scorer.get("confidence")),
                manual_status=_cell(manual.get("status")),
                manual_required=_cell(scorer.get("manual_inspection_required")),
                limits=_cell(limits),
            )
        )
    lines.append("")
    return lines


def _cost_section(artifacts: list[dict[str, Any]]) -> list[str]:
    lines = [
        "## Costs",
        "",
        "| Artifact | Arm | Wall seconds | Input tokens | Output tokens | Tool calls | Estimated USD | Human inspection seconds |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    costs_by_arm: dict[str, list[dict[str, Any]]] = {}
    for artifact in artifacts:
        data = artifact["data"]
        arm = str(data.get("variant_id") or "unknown")
        cost = _dict(data.get("cost"))
        costs_by_arm.setdefault(arm, []).append(cost)
        lines.append(
            "| {artifact} | {arm} | {wall} | {input_tokens} | {output_tokens} | {tool_calls} | {usd} | {human} |".format(
                artifact=_cell(artifact["relative_path"]),
                arm=_cell(arm),
                wall=_cell(cost.get("wall_seconds")),
                input_tokens=_cell(cost.get("input_tokens")),
                output_tokens=_cell(cost.get("output_tokens")),
                tool_calls=_cell(cost.get("tool_calls")),
                usd=_cell(cost.get("estimated_usd")),
                human=_cell(cost.get("human_inspection_seconds")),
            )
        )

    lines.extend(["", "### Cost By Arm", ""])
    lines.extend(
        [
            "| Arm | Samples | Average wall seconds | Total tool calls | Total estimated USD |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for arm in sorted(costs_by_arm):
        costs = costs_by_arm[arm]
        wall_values = [_number(cost.get("wall_seconds")) for cost in costs]
        tool_values = [_number(cost.get("tool_calls")) for cost in costs]
        usd_values = [_number(cost.get("estimated_usd")) for cost in costs]
        lines.append(
            "| {arm} | {samples} | {wall} | {tools} | {usd} |".format(
                arm=_cell(arm),
                samples=len(costs),
                wall=_cell(_average([value for value in wall_values if value is not None])),
                tools=_cell(_sum([value for value in tool_values if value is not None])),
                usd=_cell(_sum([value for value in usd_values if value is not None])),
            )
        )
    lines.append("")
    return lines


def _load_catalog(path: Path, key: str) -> dict[str, dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    values = data.get(key)
    if not isinstance(values, list):
        return {}
    return {
        item["id"]: item
        for item in values
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def _scores(artifact: dict[str, Any]) -> dict[str, dict[str, Any]]:
    scores = artifact.get("scores")
    if not isinstance(scores, dict):
        return {}
    return {
        str(score_id): score
        for score_id, score in scores.items()
        if isinstance(score, dict)
    }


def _score_vector(
    artifact: dict[str, Any],
    score_catalog: dict[str, dict[str, Any]],
) -> str:
    scores = _scores(artifact)
    if not scores:
        return "unknown"
    parts = []
    for score_id in sorted(scores):
        score = scores[score_id]
        floor = "floor triggered" if score.get("floor_triggered") else "floor ok"
        parts.append(
            "{score}={value} ({confidence}, {floor})".format(
                score=_score_label(score_id, score_catalog),
                value=_format_value(score.get("value")),
                confidence=score.get("confidence") or "unknown confidence",
                floor=floor,
            )
        )
    return "; ".join(parts)


def _floor_failures(
    artifacts: list[dict[str, Any]],
    score_catalog: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = []
    for artifact in artifacts:
        data = artifact["data"]
        handled_score_ids: set[str] = set()
        for score_id, score in _scores(data).items():
            triggers = _dicts(score.get("floor_triggers"))
            if not triggers and score.get("floor_triggered"):
                triggers = [{"condition": "floor triggered", "effect": None, "evidence_refs": []}]
            if not triggers:
                continue
            handled_score_ids.add(_base_score_id(score_id))
            for trigger in triggers:
                rows.append(
                    _floor_failure_row(artifact, data, score_id, score, trigger, score_catalog)
                )

        for trigger in _dicts(data.get("floor_triggers")):
            trigger_score_id = str(trigger.get("score_id") or "unknown")
            if trigger_score_id in handled_score_ids:
                continue
            score = _scores(data).get(trigger_score_id, {})
            rows.append(
                _floor_failure_row(
                    artifact,
                    data,
                    trigger_score_id,
                    score,
                    trigger,
                    score_catalog,
                )
            )
    return rows


def _floor_failure_row(
    artifact: dict[str, Any],
    data: dict[str, Any],
    score_id: str,
    score: dict[str, Any],
    trigger: dict[str, Any],
    score_catalog: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    return {
        "artifact": artifact["relative_path"],
        "scenario": data.get("scenario_id"),
        "arm": data.get("variant_id"),
        "score": _score_label(score_id, score_catalog),
        "value": score.get("value"),
        "condition": trigger.get("condition"),
        "effect": trigger.get("effect"),
        "evidence_refs": _strings(trigger.get("evidence_refs")),
    }


def _status_items(data: dict[str, Any]) -> list[tuple[str, Any]]:
    rows: list[tuple[str, Any]] = []
    for field in STATUS_FIELDS:
        if field in data:
            rows.append((field, data.get(field)))
    for field in BOOLEAN_STATUS_FIELDS:
        if data.get(field) is True:
            rows.append((field, True))

    statuses = data.get("statuses")
    if isinstance(statuses, dict):
        for field, value in sorted(statuses.items()):
            rows.append((f"statuses.{field}", value))
    elif isinstance(statuses, list):
        for index, value in enumerate(statuses, 1):
            rows.append((f"statuses[{index}]", value))

    for score_id, score in _scores(data).items():
        for field in STATUS_FIELDS:
            if field in score:
                rows.append((f"scores.{score_id}.{field}", score.get(field)))
        for field in BOOLEAN_STATUS_FIELDS:
            if score.get(field) is True:
                rows.append((f"scores.{score_id}.{field}", True))
    return rows


def _score_label(score_id: str, catalog: dict[str, dict[str, Any]]) -> str:
    base_score_id = _base_score_id(score_id)
    entry = catalog.get(base_score_id, {})
    name = entry.get("name")
    if isinstance(name, str) and name:
        return f"{base_score_id} {name}"
    return score_id


def _scenario_label(
    scenario_id: Any,
    scenario_catalog: dict[str, dict[str, Any]],
) -> str:
    if not isinstance(scenario_id, str):
        return "unknown"
    entry = scenario_catalog.get(scenario_id, {})
    slug = entry.get("slug")
    if isinstance(slug, str) and slug:
        return f"{scenario_id} {slug}"
    return scenario_id


def _active_floor(score_id: str, catalog: dict[str, dict[str, Any]]) -> Any:
    return catalog.get(_base_score_id(score_id), {}).get("active_floor")


def _base_score_id(score_id: str) -> str:
    match = re.match(r"^(S00[1-9])", score_id)
    return match.group(1) if match else score_id


def _trust_level(value: Any) -> str:
    if isinstance(value, int) and not isinstance(value, bool):
        return f"Trust Level {value}"
    return "unknown"


def _unique(values: Any) -> list[str]:
    cleaned = []
    seen = set()
    for value in values:
        if value is None or value == "":
            continue
        text = str(value)
        if text not in seen:
            seen.add(text)
            cleaned.append(text)
    return sorted(cleaned)


def _join_or_unknown(values: list[str]) -> str:
    return ", ".join(values) if values else "unknown"


def _relative_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _display_path(path: Path) -> str:
    return str(path)


def _cell(value: Any) -> str:
    text = _format_value(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def _format_value(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f"{value:.2f}".rstrip("0").rstrip(".")
    if isinstance(value, list):
        return "; ".join(_format_value(item) for item in value) if value else "unknown"
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True)
    text = str(value).strip()
    return text if text else "unknown"


def _average(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def _sum(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values)


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _dicts(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str) and item.strip()]


def _dedupe(values: list[str]) -> list[str]:
    result = []
    seen = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


if __name__ == "__main__":
    raise SystemExit(main())
