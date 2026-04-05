#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent))

from _loom.core import (
    discover_repositories,
    find_workspace_root,
    resolve_repository_for_path,
)  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Discover Loom repositories in the workspace"
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--path")
    args = parser.parse_args()

    workspace = find_workspace_root()
    repos = discover_repositories(workspace)
    if args.path:
        owner = resolve_repository_for_path(workspace, Path(args.path))
        payload = {"repositories": repos, "owner": owner}
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print(
                f"owner\t{owner['repository_id']}\t{owner['path']}\t{owner['worktree_id']}"
            )
        return 0
    if args.json:
        print(json.dumps({"repositories": repos}, indent=2))
    else:
        for repo in repos:
            print(f"{repo['repository_id']}\t{repo['path']}\t{repo['worktree_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
