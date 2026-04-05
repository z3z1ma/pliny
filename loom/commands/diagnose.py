"""Check Loom workspace structural health and optionally fix missing directories."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..core import (
    CANONICAL_SUBTREES,
    SUPPORTING_SUBTREES,
    discover_repositories,
    find_workspace_root,
    relative_to_workspace,
    scan_records,
)
from ..validate import validate_structure
from .check_links import check_links


# ---------------------------------------------------------------------------
# Workspace layout
# ---------------------------------------------------------------------------


def rules_root_for_workspace(workspace: Path) -> Path | None:
    for candidate in [workspace / ".opencode/rules", workspace / "rules"]:
        if candidate.exists():
            return candidate
    return None


def skills_root_for_workspace(workspace: Path) -> Path | None:
    for candidate in [workspace / ".opencode/skills", workspace / "skills"]:
        if candidate.exists():
            return candidate
    return None


def workspace_layout_kind(workspace: Path) -> str:
    if (workspace / ".opencode/rules").exists() and (
        workspace / ".opencode/skills"
    ).exists():
        return "packaged"
    if (workspace / "rules").exists() and (workspace / "skills").exists():
        return "source"
    return "unknown"


# ---------------------------------------------------------------------------
# Doctor report
# ---------------------------------------------------------------------------


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
    structural_issues: list[dict] = []
    for path in scan_records(workspace, include_runs=True):
        structural_issues.extend(validate_structure(path, workspace))
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
        "structural_issue_count": len(structural_issues),
        "link_issue_count": len(link_issues),
        "repositories": repos,
        "healthy": not (
            missing
            or missing_subtrees
            or skill_issues
            or structural_issues
            or link_issues
        ),
    }


def fix_missing_structure(workspace: Path, report: dict) -> list[str]:
    """Create missing .loom/ root and subtree directories."""
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


def register(subparsers: Any) -> None:
    parser = subparsers.add_parser(
        "diagnose",
        help="Check Loom workspace health and optionally fix missing structure",
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Create missing .loom/ directories before reporting",
    )
    parser.set_defaults(func=run)


def run(args: Any) -> int:
    workspace = find_workspace_root()
    created: list[str] = []

    if args.fix:
        preliminary = doctor_report(workspace)
        created = fix_missing_structure(workspace, preliminary)
        report = doctor_report(workspace)
        report["fixed"] = created
    else:
        report = doctor_report(workspace)

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"workspace: {report['workspace']}")
        print(f"healthy: {report['healthy']}")
        print(f"skill_count: {report['skill_count']}")
        print(f"structural_issue_count: {report['structural_issue_count']}")
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
