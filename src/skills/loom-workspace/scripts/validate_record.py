#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent))

from _loom.core import COMMON_FIELDS, SECTIONS_BY_KIND, STATUS_BY_KIND, extract_headings, find_workspace_root, flatten_link_values, issue, normalize_repository_scope, parse_timestamp, read_record, scan_records  # noqa: E402


def validate_record_path(path: Path, workspace: Path) -> list[dict]:
    problems: list[dict] = []
    try:
        frontmatter, body = read_record(path)
    except Exception as exc:
        return [issue(path, workspace, str(exc))]

    for field in COMMON_FIELDS:
        if field not in frontmatter and frontmatter.get("kind") != "packet":
            problems.append(issue(path, workspace, f"missing field: {field}"))

    kind = frontmatter.get("kind")
    if kind not in STATUS_BY_KIND:
        problems.append(issue(path, workspace, f"unknown kind: {kind}"))
        return problems

    status = frontmatter.get("status")
    if status not in STATUS_BY_KIND[kind]:
        problems.append(issue(path, workspace, f"invalid status for {kind}: {status}"))

    try:
        normalize_repository_scope(workspace, frontmatter.get("repository_scope"))
    except SystemExit as exc:
        problems.append(issue(path, workspace, f"invalid repository_scope: {exc}"))

    for key in ("created_at", "updated_at"):
        if key in frontmatter:
            try:
                parse_timestamp(frontmatter[key])
            except Exception:
                problems.append(issue(path, workspace, f"invalid timestamp: {key}"))

    if frontmatter.get("id") == "constitution:main" and flatten_link_values(
        frontmatter.get("links", {})
    ):
        problems.append(
            issue(
                path,
                workspace,
                "constitution:main must not declare frontmatter links",
            )
        )

    required_sections = SECTIONS_BY_KIND.get(kind, [])
    headings = extract_headings(body)
    missing_sections = [
        section for section in required_sections if section not in headings
    ]
    for section in missing_sections:
        problems.append(issue(path, workspace, f"missing section: {section}"))

    if kind == "packet":
        for field in [
            "mode",
            "target",
            "scope",
            "allowed_repositories",
            "allowed_worktrees",
            "cross_repository_reads",
            "writes_restricted_to_scope",
            "generated_at",
            "generated_by",
            "compiler_version",
            "source_refs",
            "trust_boundary",
            "output_contract",
        ]:
            if field not in frontmatter:
                problems.append(
                    issue(path, workspace, f"missing packet field: {field}")
                )
        mode = frontmatter.get("mode", {})
        if (
            isinstance(mode, dict)
            and mode.get("execution")
            and "allowed_write_refs" not in frontmatter
        ):
            problems.append(
                issue(path, workspace, "execution packet missing allowed_write_refs")
            )

    return problems


def validate_records(paths: list[Path], workspace: Path) -> list[dict]:
    problems: list[dict] = []
    for path in paths:
        problems.extend(validate_record_path(path, workspace))
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Loom records")
    parser.add_argument("path", nargs="?")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    workspace = find_workspace_root()
    if args.path:
        target = (
            (workspace / args.path).resolve()
            if not Path(args.path).is_absolute()
            else Path(args.path)
        )
        problems = (
            validate_record_path(target, workspace)
            if target.exists()
            else [issue(None, workspace, f"missing path: {args.path}")]
        )
    else:
        problems = validate_records(
            scan_records(workspace, include_runs=True), workspace
        )

    if args.json:
        print(json.dumps({"issues": problems}, indent=2))
    elif problems:
        for problem in problems:
            print(f"ERROR {problem['path']}: {problem['message']}")
    else:
        print("All checked records are structurally valid")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
