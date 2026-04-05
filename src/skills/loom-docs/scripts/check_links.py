#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent))

from _loom.core import (  # noqa: E402
    build_record_index,
    find_workspace_root,
    flatten_link_values,
    issue,
    read_record,
    scan_records,
)


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Loom record links")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    workspace = find_workspace_root()
    problems = check_links(workspace)
    if args.json:
        print(json.dumps({"issues": problems}, indent=2))
    elif problems:
        for problem in problems:
            print(f"ERROR {problem['path']}: {problem['message']}")
    else:
        print("All checked links resolve")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
