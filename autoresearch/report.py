from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]


class ReportError(ValueError):
    pass


def build_report(
    artifacts_path: str | Path,
    *,
    campaign_path: str | Path | None = None,
    repo_root: Path = REPO_ROOT,
) -> str:
    del repo_root
    source = Path(artifacts_path)
    artifacts = load_trial_artifacts(source)
    summary = load_summary(source)
    plan = load_plan(source)
    campaign = load_campaign_metadata(campaign_path) if campaign_path else None

    lines = [
        "# 10x Autoresearch Trial Report",
        "",
        f"Source: `{_display_path(source)}`",
        "",
    ]
    lines.extend(_summary_section(source, summary, plan, artifacts))
    lines.extend(_scientific_contract_section(summary, plan, artifacts))
    if campaign:
        lines.extend(_campaign_section(campaign))
    if artifacts:
        lines.extend(_artifact_inspection_checklist_section(source, artifacts))
        lines.extend(_trial_artifacts_section(artifacts))
        lines.extend(_workspace_changes_section(artifacts))
    else:
        lines.extend(["No raw trial artifacts were found.", ""])
    lines.extend(_inspection_section())
    lines.extend(_limits_section())
    return "\n".join(lines)


def load_trial_artifacts(artifacts_path: str | Path) -> list[dict[str, Any]]:
    source = Path(artifacts_path)
    if not source.exists():
        raise ReportError(f"trial artifact path does not exist: {source}")

    if source.is_file():
        paths = [source]
        root = source.parent
    else:
        raw_dir = source / "raw"
        if raw_dir.is_dir():
            root = raw_dir
            paths = sorted(root.glob("*.json"))
        else:
            root = source
            paths = sorted(
                path
                for path in root.glob("*.json")
                if path.name not in {"summary.json", "plan.json", "canonical_guard.json"}
            )

    artifacts: list[dict[str, Any]] = []
    for path in paths:
        data = _load_json_file(path, "raw trial artifact")
        artifacts.append({"path": path, "relative_path": _relative_path(path, root), "data": data})
    return artifacts


def load_summary(artifacts_path: str | Path) -> dict[str, Any] | None:
    summary_path = _metadata_path(Path(artifacts_path), "summary.json")
    if not summary_path.exists():
        return None
    return _load_json_file(summary_path, "summary")


def load_plan(artifacts_path: str | Path) -> dict[str, Any] | None:
    plan_path = _metadata_path(Path(artifacts_path), "plan.json")
    if not plan_path.exists():
        return None
    return _load_json_file(plan_path, "plan")


def load_campaign_metadata(path: str | Path) -> dict[str, Any]:
    return _load_json_file(Path(path), "campaign metadata")


def write_report(
    artifacts_path: str | Path,
    out_path: str | Path,
    *,
    campaign_path: str | Path | None = None,
) -> Path:
    output_path = Path(out_path)
    report = build_report(artifacts_path, campaign_path=campaign_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown report from saved 10x autoresearch trial artifacts."
    )
    parser.add_argument(
        "--artifacts",
        type=Path,
        required=True,
        help="Experiment output directory, raw artifact directory, or one raw trial JSON file.",
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
        output_path = write_report(args.artifacts, args.out, campaign_path=args.campaign)
    except (OSError, json.JSONDecodeError, ReportError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"wrote {output_path}")
    return 0


def _summary_section(
    source: Path,
    summary: dict[str, Any] | None,
    plan: dict[str, Any] | None,
    artifacts: list[dict[str, Any]],
) -> list[str]:
    experiment_id = _first_present(
        _dict(summary).get("experiment_id"),
        _dict(plan).get("experiment_id"),
        *[artifact["data"].get("experiment_id") for artifact in artifacts],
    )
    mode = _first_present(_dict(summary).get("mode"), _dict(plan).get("mode"))
    live_calls = _first_present(
        _dict(summary).get("live_codex_calls"),
        _dict(plan).get("live_codex_calls"),
        sum(_int(artifact["data"].get("live_codex_calls")) for artifact in artifacts),
    )
    rows = [
        ("experiment_id", experiment_id),
        ("mode", mode),
        ("raw_artifacts", len(artifacts)),
        ("live_codex_calls", live_calls),
        ("summary", _present(_metadata_path(source, "summary.json"))),
        ("plan", _present(_metadata_path(source, "plan.json"))),
    ]
    if summary:
        for field in ("raw_output_dir", "workspace_dir", "codex_artifact_dir", "prompt_dir"):
            if field in summary:
                rows.append((field, summary[field]))
    return [
        "## Summary",
        "",
        "| Field | Value |",
        "| --- | --- |",
        *[f"| {_cell(name)} | {_cell(value)} |" for name, value in rows],
        "",
    ]


def _campaign_section(campaign: dict[str, Any]) -> list[str]:
    fields = (
        "campaign_id",
        "experiment_id",
        "verdict",
        "result_status",
        "promotion_decision",
        "candidate_id",
        "baseline_id",
        "statuses",
        "evidence_refs",
        "limits",
    )
    lines = [
        "## Campaign Verdict",
        "",
        "| Field | Value |",
        "| --- | --- |",
    ]
    for field in fields:
        if field in campaign:
            lines.append(f"| {_cell(field)} | {_cell(campaign[field])} |")

    manual = _dict(campaign.get("manual_inspection"))
    if manual:
        for key, value in manual.items():
            lines.append(f"| {_cell('manual_inspection.' + str(key))} | {_cell(value)} |")
    lines.extend(
        [
            "",
            "Campaign verdict metadata is manual/contextual. It does not modify raw trial artifacts.",
            "",
        ]
    )
    return lines


def _scientific_contract_section(
    summary: dict[str, Any] | None,
    plan: dict[str, Any] | None,
    artifacts: list[dict[str, Any]],
) -> list[str]:
    contract = _dict(
        _first_present(
            _dict(plan).get("scientific_contract"),
            _dict(summary).get("scientific_contract"),
            *[artifact["data"].get("scientific_contract") for artifact in artifacts],
        )
    )
    if not contract:
        return []

    rows = [
        ("question", contract.get("question")),
        ("hypothesis", contract.get("hypothesis")),
        ("expected_behavior", contract.get("expected_behavior")),
        ("inspection_criteria", contract.get("inspection_criteria")),
        ("quality_floor", contract.get("quality_floor")),
        ("verdict_record_path", contract.get("verdict_record_path")),
    ]
    return [
        "## Scientific Contract",
        "",
        "| Field | Value |",
        "| --- | --- |",
        *[f"| {_cell(name)} | {_cell(value)} |" for name, value in rows],
        "",
    ]


def _trial_artifacts_section(artifacts: list[dict[str, Any]]) -> list[str]:
    lines = [
        "## Trial Artifacts",
        "",
        "| Artifact | Scenario | Arm | Rep | Command exits | Timed out | Turns | Wall seconds | Tokens | Archived workspace | Workspace manifest |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for artifact in artifacts:
        data = artifact["data"]
        metadata = _dict(data.get("harness_metadata"))
        lines.append(
            "| {path} | {scenario} | {arm} | {rep} | {exits} | {timed_out} | {turns} | {wall} | {tokens} | {workspace} | {manifest} |".format(
                path=_cell(artifact["relative_path"]),
                scenario=_cell(data.get("scenario_id")),
                arm=_cell(data.get("variant_id")),
                rep=_cell(data.get("rep")),
                exits=_cell(_command_exits(data)),
                timed_out=_cell(data.get("timed_out")),
                turns=_cell(data.get("live_codex_calls")),
                wall=_cell(_number(data.get("wall_seconds"))),
                tokens=_cell(_tokens(data)),
                workspace=_cell(metadata.get("archived_workspace_dir")),
                manifest=_cell(metadata.get("workspace_manifest_path")),
            )
        )
    lines.append("")
    return lines


def _artifact_inspection_checklist_section(
    source: Path,
    artifacts: list[dict[str, Any]],
) -> list[str]:
    root = _artifact_root(source)
    rows = [
        ("summary.json", _present(root / "summary.json")),
        ("plan.json", _present(root / "plan.json")),
        ("canonical_guard.json", _present(root / "canonical_guard.json")),
        ("raw trial artifacts", f"{len(artifacts)} found"),
        ("codex command metadata", _count_files(root / "codex", "*.command.json")),
        ("codex stdout JSONL", _count_files(root / "codex", "*.stdout.jsonl")),
        ("codex stderr", _count_files(root / "codex", "*.stderr")),
        ("last assistant messages", _count_files(root / "codex", "*.last-message.txt")),
        ("prompts", _count_files(root / "prompts", "*.prompt.txt")),
        ("workspace manifests", _count_files(root / "workspaces", "*/workspace-manifest.json")),
        ("archived workspaces", _count_dirs(root / "workspaces")),
    ]
    return [
        "## Artifact Inspection Checklist",
        "",
        "Presence only; the scientist still judges whether each artifact supports the claim.",
        "",
        "| Artifact class | Status |",
        "| --- | --- |",
        *[f"| {_cell(name)} | {_cell(status)} |" for name, status in rows],
        "",
    ]


def _workspace_changes_section(artifacts: list[dict[str, Any]]) -> list[str]:
    lines = [
        "## Workspace And Tool Trace",
        "",
        "| Artifact | Changed files | Tool events | Raw references | Last assistant message |",
        "| --- | --- | --- | --- | --- |",
    ]
    for artifact in artifacts:
        data = artifact["data"]
        changed_files = [item.get("path") for item in _list(data.get("file_outputs")) if isinstance(item, dict)]
        lines.append(
            "| {path} | {files} | {tools} | {refs} | {message} |".format(
                path=_cell(artifact["relative_path"]),
                files=_cell(changed_files or "none"),
                tools=_cell(len(_list(data.get("tool_invocations")))),
                refs=_cell(len(_list(data.get("raw_artifact_refs")))),
                message=_cell(_last_assistant_message(data)),
            )
        )
    lines.append("")
    return lines


def _inspection_section() -> list[str]:
    return [
        "## Scientist Inspection",
        "",
        "This report does not grade, aggregate, or promote a candidate.",
        "",
        "Inspect the raw transcript, command artifacts, workspace manifest, changed files, and expected behavior for each scenario. Record rubric judgments, verdicts, limits, and any promotion or rejection rationale in durable `.10x/research/`, `.10x/evidence/`, or `.10x/reviews/` records.",
        "",
    ]


def _limits_section() -> list[str]:
    return [
        "## Report Limits",
        "",
        "- This report is a secondary view over saved trial artifacts.",
        "- Unknown means the field was absent, null, or not numeric in the loaded artifact.",
        "- The runner does not replace the LLM researcher's rubric inspection.",
        "",
    ]


def _load_json_file(path: Path, label: str) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ReportError(f"{path}: {label} must be a JSON object")
    return data


def _relative_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return path.as_posix()


def _metadata_path(source: Path, name: str) -> Path:
    if source.is_file():
        return source.parent / name
    direct = source / name
    if direct.exists() or source.name != "raw":
        return direct
    return source.parent / name


def _artifact_root(source: Path) -> Path:
    if source.is_file():
        return source.parent.parent if source.parent.name == "raw" else source.parent
    return source.parent if source.name == "raw" else source


def _count_files(root: Path, pattern: str) -> str:
    if not root.exists():
        return "not found"
    count = sum(1 for path in root.glob(pattern) if path.is_file())
    return f"{count} found"


def _count_dirs(root: Path) -> str:
    if not root.exists():
        return "not found"
    count = sum(1 for path in root.iterdir() if path.is_dir())
    return f"{count} found"


def _cell(value: Any) -> str:
    if value is None or value == "":
        text = "unknown"
    elif isinstance(value, (list, tuple)):
        text = ", ".join(_stringify(item) for item in value) if value else "none"
    elif isinstance(value, dict):
        text = json.dumps(value, sort_keys=True)
    else:
        text = _stringify(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def _stringify(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _int(value: Any) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def _number(value: Any) -> float | int | None:
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _first_present(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def _present(path: Path) -> str:
    return path.as_posix() if path.exists() else "not found"


def _command_exits(data: dict[str, Any]) -> list[Any] | str:
    exits = [
        item.get("exit_code")
        for item in _list(data.get("command_outputs"))
        if isinstance(item, dict) and "exit_code" in item
    ]
    return exits or "unknown"


def _tokens(data: dict[str, Any]) -> str:
    input_tokens = data.get("input_tokens")
    output_tokens = data.get("output_tokens")
    if input_tokens is None and output_tokens is None:
        return "unknown"
    return f"in={input_tokens or 0}; out={output_tokens or 0}"


def _last_assistant_message(data: dict[str, Any]) -> str:
    transcript = _list(data.get("transcript"))
    for item in reversed(transcript):
        if isinstance(item, dict) and item.get("role") == "assistant":
            content = str(item.get("content", "")).strip()
            return content[:157] + "..." if len(content) > 160 else content
    return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
