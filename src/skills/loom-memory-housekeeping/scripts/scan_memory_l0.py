#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent))

from _loom.core import find_workspace_root  # noqa: E402

MEMORY_ROOT = Path(".loom/memories")
EXPECTED_DOMAINS = ("system", "user")
L0_PATTERN = re.compile(r"^<!-- L0: .+ -->$")


def memory_root(workspace: Path) -> Path:
    return workspace / MEMORY_ROOT


def list_memory_markdown_files(workspace: Path) -> list[Path]:
    root = memory_root(workspace)
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def read_l0_summary(path: Path) -> str | None:
    try:
        first_line = path.read_text().splitlines()[0].strip()
    except IndexError:
        return None
    if not L0_PATTERN.match(first_line):
        return None
    return first_line.removeprefix("<!-- L0: ").removesuffix(" -->")


def collect_l0_rows(workspace: Path, domain: str | None = None) -> list[dict[str, str]]:
    root = memory_root(workspace)
    rows = []
    for path in list_memory_markdown_files(workspace):
        relative_path = path.relative_to(root)
        if relative_path.parts[:1] == ("glacier",) and relative_path.name != "index.md":
            continue
        if domain and domain != "all":
            if relative_path.parts[:1] == (domain,):
                pass
            elif relative_path.as_posix() != "hot-memory.md":
                continue
        summary = read_l0_summary(path)
        if summary is None:
            continue
        rows.append({"path": str(relative_path), "summary": summary})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List L0 summaries from Loom memory files"
    )
    parser.add_argument(
        "--domain",
        choices=["all", *EXPECTED_DOMAINS],
        default="all",
        help="Restrict output to one memory domain",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    workspace = find_workspace_root()
    rows = collect_l0_rows(workspace, domain=args.domain)
    if args.json:
        print(json.dumps(rows, indent=2, sort_keys=True))
    else:
        for row in rows:
            print(f"{row['path']}: {row['summary']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
