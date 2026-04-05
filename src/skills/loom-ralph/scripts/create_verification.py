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
    collect_link_assignments,
    resolve_record_scope_args,
)
from _loom.core import (  # noqa: E402
    build_record_index,
    create_record,
    find_workspace_root,
    flatten_link_values,
    merge_repository_scopes,
    read_record,
    relative_to_workspace,
    set_sections,
)


def create_verification_record(
    workspace: Path,
    slug: str,
    *,
    title: str | None = None,
    links: dict[str, list[str]] | None = None,
    sections: dict[str, str] | None = None,
    repository_scope: dict | None = None,
) -> Path:
    inferred_scope = repository_scope
    if inferred_scope is None and links:
        index, issues = build_record_index(workspace)
        if issues:
            raise SystemExit(
                "Fix record parse issues before inferring verification scope"
            )
        linked_scopes = []
        for ref in flatten_link_values(links):
            path = index.get(ref)
            if path is None:
                continue
            frontmatter, _body = read_record(path)
            linked_scopes.append(frontmatter.get("repository_scope"))
        inferred_scope = merge_repository_scopes(workspace, linked_scopes)
    path = create_record(
        "verification",
        slug,
        workspace,
        title=title,
        initial_links=links,
        repository_scope=inferred_scope,
    )
    if sections:
        set_sections(workspace, str(path), sections)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a Loom verification record",
        epilog=(
            "Examples: --link ticket:0005 --link spec:loom-repository-bootstrap "
            "or --link ticket=ticket:0005"
        ),
    )
    parser.add_argument("slug")
    parser.add_argument("--title")
    parser.add_argument("--link", action="append", default=[])
    parser.add_argument("--section", action="append", default=[])
    add_scope_arguments(parser)
    args = parser.parse_args()

    workspace = find_workspace_root()
    sections = {
        heading: "\n".join(values)
        for heading, values in collect_assignments(
            args.section, label="section assignment"
        ).items()
    }
    path = create_verification_record(
        workspace,
        args.slug,
        title=args.title,
        links=collect_link_assignments(args.link, label="link assignment"),
        sections=sections or None,
        repository_scope=resolve_record_scope_args(args, workspace),
    )
    print(relative_to_workspace(path, workspace))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
