#!/usr/bin/env python3
"""Check Loom workspace health and optionally fix missing structure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent))

from _loom.core import (  # noqa: E402
    CANONICAL_SUBTREES,
    COMMON_FIELDS,
    SECTIONS_BY_KIND,
    STATUS_BY_KIND,
    SUPPORTING_SUBTREES,
    build_record_index,
    discover_repositories,
    extract_headings,
    find_workspace_root,
    flatten_link_values,
    issue,
    normalize_repository_scope,
    parse_timestamp,
    read_record,
    relative_to_workspace,
    scan_records,
)


def rules_root_for_workspace(workspace: Path) -> Path | None:
    packaged = workspace / ".opencode/rules"
    if packaged.exists():
        return packaged
    source = workspace / "src/rules"
    if source.exists():
        return source
    return None


def skills_root_for_workspace(workspace: Path) -> Path | None:
    packaged = workspace / ".opencode/skills"
    if packaged.exists():
        return packaged
    source = workspace / "src/skills"
    if source.exists():
        return source
    return None


def workspace_layout_kind(workspace: Path) -> str:
    packaged_rules = (workspace / ".opencode/rules").exists()
    packaged_skills = (workspace / ".opencode/skills").exists()
    source_rules = (workspace / "src/rules").exists()
    source_skills = (workspace / "src/skills").exists()
    if packaged_rules and packaged_skills:
        return "packaged"
    if source_rules and source_skills:
        return "source"
    return "unknown"


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


def check_links(workspace: Path) -> list[dict]:
    problems: list[dict] = []
    index, duplicate_issues = build_record_index(workspace)
    problems.extend(duplicate_issues)
    for path in scan_records(workspace):
        try:
            frontmatter, _ = read_record(path)
        except Exception as exc:
            problems.append(issue(path, workspace, f"parse error: {exc}"))
            continue
        for ref in flatten_link_values(frontmatter.get("links", {})):
            if ref not in index:
                problems.append(issue(path, workspace, f"missing linked ref: {ref}"))
    return problems


def doctor_report(workspace: Path) -> dict:
    rules_root = rules_root_for_workspace(workspace)
    skills_root = skills_root_for_workspace(workspace)
    required_dirs = {
        "rules bundle": rules_root,
        "skills bundle": skills_root,
        ".loom": workspace / ".loom",
    }
    missing = [
        label
        for label, path in required_dirs.items()
        if path is None or not path.exists()
    ]
    missing_subtrees: list[str] = []
    loom_root = workspace / ".loom"
    if loom_root.exists():
        for subtree in CANONICAL_SUBTREES + SUPPORTING_SUBTREES:
            if not (workspace / subtree).exists():
                missing_subtrees.append(subtree)
    skill_dirs = (
        sorted(path for path in skills_root.glob("loom-*") if path.is_dir())
        if skills_root is not None and skills_root.exists()
        else []
    )
    skill_issues = []
    if skills_root is not None and skills_root.exists() and not skill_dirs:
        skill_issues.append("no Loom skills found in skills bundle")
    for skill in skill_dirs:
        if not (skill / "SKILL.md").exists():
            skill_issues.append(f"{skill.name} missing SKILL.md")
        if not (skill / "references").exists():
            skill_issues.append(f"{skill.name} missing references/")
    record_issues = validate_records(
        scan_records(workspace, include_runs=True), workspace
    )
    link_issues = check_links(workspace)
    repos = discover_repositories(workspace)
    return {
        "workspace": str(workspace),
        "bundle_layout": workspace_layout_kind(workspace),
        "rules_root": None
        if rules_root is None
        else relative_to_workspace(rules_root, workspace),
        "skills_root": None
        if skills_root is None
        else relative_to_workspace(skills_root, workspace),
        "missing_directories": missing,
        "missing_subtrees": missing_subtrees,
        "skill_count": len(skill_dirs),
        "skill_issues": skill_issues,
        "record_issue_count": len(record_issues),
        "link_issue_count": len(link_issues),
        "repositories": repos,
        "healthy": not (
            missing or missing_subtrees or skill_issues or record_issues or link_issues
        ),
    }


def fix_missing_structure(workspace: Path, report: dict) -> list[str]:
    """Create missing .loom/ root and subtree directories. Returns created paths."""
    created: list[str] = []
    loom_root = workspace / ".loom"
    if ".loom" in report["missing_directories"]:
        loom_root.mkdir(parents=True, exist_ok=True)
        created.append(".loom/")
    for subtree in report["missing_subtrees"]:
        d = workspace / subtree
        d.mkdir(parents=True, exist_ok=True)
        created.append(f"{subtree}/")
    return created


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Loom workspace health and optionally fix missing structure"
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Create missing .loom/ directories before reporting",
    )
    args = parser.parse_args()

    workspace = find_workspace_root()
    created: list[str] = []

    if args.fix:
        # Run a preliminary report to find what needs fixing
        preliminary = doctor_report(workspace)
        created = fix_missing_structure(workspace, preliminary)
        # Re-run after fixes to get the accurate final state
        report = doctor_report(workspace)
        report["fixed"] = created
    else:
        report = doctor_report(workspace)

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"workspace: {report['workspace']}")
        print(f"bundle_layout: {report['bundle_layout']}")
        print(f"rules_root: {report['rules_root']}")
        print(f"skills_root: {report['skills_root']}")
        print(f"healthy: {report['healthy']}")
        print(f"skill_count: {report['skill_count']}")
        print(f"record_issue_count: {report['record_issue_count']}")
        print(f"link_issue_count: {report['link_issue_count']}")
        if created:
            print("fixed:")
            for item in created:
                print(f"  + {item}")
        if report["missing_directories"]:
            print("missing_directories:")
            for item in report["missing_directories"]:
                print(f"  - {item}")
        if report["missing_subtrees"]:
            print("missing_subtrees:")
            for item in report["missing_subtrees"]:
                print(f"  - {item}")
        if report["skill_issues"]:
            print("skill_issues:")
            for item in report["skill_issues"]:
                print(f"  - {item}")
    return 1 if not report["healthy"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
