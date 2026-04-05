#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent))

from _loom.cli import collect_link_assignments  # noqa: E402
from _loom.core import (  # noqa: E402
    find_workspace_root,
    flatten_link_values,
    normalize_links,
    read_record,
    relative_to_workspace,
    resolve_record_path,
    utc_now,
    write_record,
)


def mutate_links(
    workspace: Path,
    target: str,
    *,
    additions: dict[str, list[str]] | None = None,
    removals: dict[str, list[str]] | None = None,
) -> Path:
    path = resolve_record_path(workspace, target)
    frontmatter, body = read_record(path)
    record_id = frontmatter.get("id")
    links: dict[str, list[str]] = normalize_links(frontmatter.get("links", {}))
    if record_id == "constitution:main" and flatten_link_values(additions or {}):
        raise SystemExit(
            "constitution:main must not declare frontmatter links; "
            "remove links from other records instead"
        )
    for key, values in (additions or {}).items():
        links.setdefault(key, [])
        for value in values:
            if value not in links[key]:
                links[key].append(value)
    for key, values in (removals or {}).items():
        if key not in links:
            continue
        links[key] = [value for value in links[key] if value not in values]
        if not links[key]:
            links.pop(key)
    if record_id == "constitution:main" and flatten_link_values(links):
        raise SystemExit(
            "constitution:main must not declare frontmatter links; "
            "remove every existing link instead"
        )
    frontmatter["links"] = links
    frontmatter["updated_at"] = utc_now()
    write_record(path, frontmatter, body)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add or remove Loom record links",
        epilog=(
            "Examples: --add ticket:0004 --add plan:bootstrap-repository "
            "or --add ticket=ticket:0004. constitution:main may only have links removed."
        ),
    )
    parser.add_argument("target")
    parser.add_argument("--add", action="append", default=[])
    parser.add_argument("--remove", action="append", default=[])
    args = parser.parse_args()

    if not args.add and not args.remove:
        raise SystemExit("Provide at least one --add or --remove assignment")

    workspace = find_workspace_root()
    path = mutate_links(
        workspace,
        args.target,
        additions=collect_link_assignments(args.add, label="link assignment"),
        removals=collect_link_assignments(args.remove, label="link assignment"),
    )
    print(relative_to_workspace(path, workspace))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
