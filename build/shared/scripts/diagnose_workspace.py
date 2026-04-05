#!/usr/bin/env python3
"""Check Loom workspace health and optionally fix missing structure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR.parent))

from _loom_lib.core import doctor_report, find_workspace_root  # noqa: E402


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
