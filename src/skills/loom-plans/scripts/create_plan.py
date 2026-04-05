#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent.parent))

from _loom.cli import (  # noqa: E402
    add_scope_arguments,
    collect_assignments,
    resolve_record_scope_args,
)
from _loom.core import (
    create_record,
    find_workspace_root,
    relative_to_workspace,
    set_sections,
)  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Loom plan record")
    parser.add_argument("slug")
    parser.add_argument("--title")
    parser.add_argument("--status")
    parser.add_argument("--link", action="append", default=[])
    parser.add_argument("--section", action="append", default=[])
    add_scope_arguments(parser)
    args = parser.parse_args()

    workspace = find_workspace_root()
    path = create_record(
        "plan",
        args.slug,
        workspace,
        title=args.title,
        status=args.status,
        initial_links=collect_assignments(args.link, label="link assignment"),
        repository_scope=resolve_record_scope_args(args, workspace),
    )
    if args.section:
        set_sections(
            workspace,
            str(path),
            {
                heading: "\n".join(values)
                for heading, values in collect_assignments(
                    args.section, label="section assignment"
                ).items()
            },
        )
    print(relative_to_workspace(path, workspace))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
