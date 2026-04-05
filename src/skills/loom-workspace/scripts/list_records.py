#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent))

from _loom.core import (  # noqa: E402
    find_workspace_root,
    read_record,
    relative_to_workspace,
    scan_records,
)


def list_records(
    workspace: Path,
    *,
    kind: str | None = None,
    status: str | None = None,
    include_runs: bool = False,
) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for path in scan_records(workspace, include_runs=include_runs):
        frontmatter, _body = read_record(path)
        record_kind = frontmatter.get("kind")
        record_status = frontmatter.get("status")
        if kind and record_kind != kind:
            continue
        if status and record_status != status:
            continue
        results.append(
            {
                "id": frontmatter.get("id", "unknown"),
                "kind": record_kind or "unknown",
                "status": record_status or "unknown",
                "path": relative_to_workspace(path, workspace),
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="List Loom records")
    parser.add_argument("--kind")
    parser.add_argument("--status")
    parser.add_argument("--include-runs", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    workspace = find_workspace_root()
    records = list_records(
        workspace,
        kind=args.kind,
        status=args.status,
        include_runs=args.include_runs,
    )
    if args.json:
        print(json.dumps(records, indent=2, sort_keys=True))
    else:
        for item in records:
            print(f"{item['id']}\t{item['kind']}\t{item['status']}\t{item['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
