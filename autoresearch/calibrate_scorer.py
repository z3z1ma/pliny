from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from autoresearch import offline_score
except ImportError:  # pragma: no cover - supports direct script execution.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from autoresearch import offline_score


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LABELS = REPO_ROOT / "autoresearch" / "calibration" / "offline-trust-labels.json"


class CalibrationError(ValueError):
    pass


def calibrate(labels_path: str | Path, *, repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    labels = _load_labels(labels_path)
    thresholds = labels["thresholds"]
    rows = []
    metrics: dict[str, dict[str, Any]] = {}

    for label in labels["labels"]:
        fixture_path = _resolve_path(repo_root, label["fixture"])
        artifact = offline_score.score_fixture(fixture_path)
        score_id = label["score_id"]
        score = artifact["scores"].get(score_id)
        if score is None:
            raise CalibrationError(f"{label['fixture']}: missing score {score_id}")
        threshold = _threshold(thresholds, score_id)
        value = score["value"]
        predicted_pass = value >= threshold
        expected_pass = bool(label["expected_pass"])
        outcome = _outcome(predicted_pass, expected_pass)
        row = {
            "fixture": label["fixture"],
            "scenario_id": artifact["scenario_id"],
            "variant_id": artifact["variant_id"],
            "score_id": score_id,
            "value": value,
            "threshold": threshold,
            "expected_pass": expected_pass,
            "predicted_pass": predicted_pass,
            "outcome": outcome,
            "human_rationale": label.get("rationale", ""),
            "scorer_rationale": score.get("rationale", ""),
        }
        rows.append(row)
        bucket = metrics.setdefault(
            score_id,
            {"tp": 0, "fp": 0, "tn": 0, "fn": 0, "samples": 0, "mismatches": []},
        )
        bucket["samples"] += 1
        if outcome == "true-positive":
            bucket["tp"] += 1
        elif outcome == "false-positive":
            bucket["fp"] += 1
            bucket["mismatches"].append(row)
        elif outcome == "true-negative":
            bucket["tn"] += 1
        elif outcome == "false-negative":
            bucket["fn"] += 1
            bucket["mismatches"].append(row)

    for score_id, bucket in metrics.items():
        bucket["precision"] = _ratio(bucket["tp"], bucket["tp"] + bucket["fp"])
        bucket["recall"] = _ratio(bucket["tp"], bucket["tp"] + bucket["fn"])
        bucket["specificity"] = _ratio(bucket["tn"], bucket["tn"] + bucket["fp"])
        bucket["accuracy"] = _ratio(
            bucket["tp"] + bucket["tn"],
            bucket["tp"] + bucket["tn"] + bucket["fp"] + bucket["fn"],
        )

    return {
        "schema_version": 1,
        "label_set_id": labels["label_set_id"],
        "scorer_id": "offline-coverage-v1",
        "current_trust_level": offline_score.TRUST_LEVEL,
        "recommended_trust_level": 1,
        "recommendation": (
            "Keep offline-coverage-v1 at Trust Level 1. This labeled set is useful "
            "for mismatch diagnostics but is too small and fixture-bound for Trust Level 2."
        ),
        "thresholds": thresholds,
        "metrics": metrics,
        "rows": rows,
        "limits": [
            "Labels cover only selected saved fixtures for S001, S004, and S007.",
            "Fixture labels are human-authored but not independently reviewed.",
            "Passing calibration rows do not establish promotion readiness.",
        ],
    }


def write_outputs(result: dict[str, Any], out_dir: str | Path) -> dict[str, str]:
    output_root = Path(out_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    json_path = output_root / "scorer-calibration.json"
    markdown_path = output_root / "scorer-calibration.md"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(_markdown(result), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(markdown_path)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compare offline scorer output against human-labeled fixtures."
    )
    parser.add_argument("--labels", type=Path, default=DEFAULT_LABELS)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = calibrate(args.labels)
        paths = write_outputs(result, args.out)
    except (OSError, json.JSONDecodeError, CalibrationError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(paths, indent=2))
    return 0


def _load_labels(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise CalibrationError("labels file must be a JSON object")
    if data.get("schema_version") != 1:
        raise CalibrationError("labels schema_version must be 1")
    if not isinstance(data.get("label_set_id"), str) or not data["label_set_id"]:
        raise CalibrationError("labels file missing label_set_id")
    if not isinstance(data.get("thresholds"), dict):
        raise CalibrationError("labels file missing thresholds")
    if not isinstance(data.get("labels"), list) or not data["labels"]:
        raise CalibrationError("labels file missing labels")
    for index, label in enumerate(data["labels"], 1):
        if not isinstance(label, dict):
            raise CalibrationError(f"label {index}: must be an object")
        for field in ("fixture", "score_id", "expected_pass"):
            if field not in label:
                raise CalibrationError(f"label {index}: missing {field}")
    return data


def _threshold(thresholds: dict[str, Any], score_id: str) -> float:
    value = thresholds.get(score_id)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CalibrationError(f"missing numeric threshold for {score_id}")
    return float(value)


def _outcome(predicted_pass: bool, expected_pass: bool) -> str:
    if predicted_pass and expected_pass:
        return "true-positive"
    if predicted_pass and not expected_pass:
        return "false-positive"
    if not predicted_pass and expected_pass:
        return "false-negative"
    return "true-negative"


def _ratio(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def _resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def _markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Offline Scorer Calibration",
        "",
        f"Label set: `{result['label_set_id']}`",
        f"Scorer: `{result['scorer_id']}`",
        f"Current trust level: {result['current_trust_level']}",
        f"Recommended trust level: {result['recommended_trust_level']}",
        "",
        result["recommendation"],
        "",
        "## Metrics",
        "",
        "| Score | Samples | TP | FP | TN | FN | Precision | Recall | Specificity | Accuracy |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for score_id in sorted(result["metrics"]):
        metric = result["metrics"][score_id]
        lines.append(
            "| {score} | {samples} | {tp} | {fp} | {tn} | {fn} | {precision} | {recall} | {specificity} | {accuracy} |".format(
                score=score_id,
                samples=metric["samples"],
                tp=metric["tp"],
                fp=metric["fp"],
                tn=metric["tn"],
                fn=metric["fn"],
                precision=_format_metric(metric["precision"]),
                recall=_format_metric(metric["recall"]),
                specificity=_format_metric(metric["specificity"]),
                accuracy=_format_metric(metric["accuracy"]),
            )
        )
    lines.extend(["", "## Rows", ""])
    lines.extend(
        [
            "| Fixture | Score | Value | Threshold | Expected | Predicted | Outcome |",
            "| --- | --- | ---: | ---: | --- | --- | --- |",
        ]
    )
    for row in result["rows"]:
        lines.append(
            "| {fixture} | {score} | {value} | {threshold} | {expected} | {predicted} | {outcome} |".format(
                fixture=row["fixture"],
                score=row["score_id"],
                value=_format_metric(row["value"]),
                threshold=_format_metric(row["threshold"]),
                expected=str(row["expected_pass"]).lower(),
                predicted=str(row["predicted_pass"]).lower(),
                outcome=row["outcome"],
            )
        )
    lines.extend(["", "## Limits", ""])
    for limit in result["limits"]:
        lines.append(f"- {limit}")
    lines.append("")
    return "\n".join(lines)


def _format_metric(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.3f}".rstrip("0").rstrip(".")
    return str(value)


if __name__ == "__main__":
    raise SystemExit(main())
