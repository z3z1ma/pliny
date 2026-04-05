from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .core import merge_repository_scopes, resolve_repository_for_path


LINK_REF_RE = re.compile(r"^(?P<kind>[a-z][a-z0-9_-]*):(?P<name>.+)$")


def parse_assignment(value: str, *, label: str = "assignment") -> tuple[str, str]:
    if "=" not in value:
        raise SystemExit(f"Invalid {label}: {value!r}. Expected KEY=VALUE")
    key, raw_value = value.split("=", 1)
    key = key.strip()
    raw_value = raw_value.strip()
    if not key or not raw_value:
        raise SystemExit(f"Invalid {label}: {value!r}. Expected KEY=VALUE")
    return key, raw_value


def collect_assignments(
    values: list[str], *, label: str = "assignment"
) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for item in values:
        key, value = parse_assignment(item, label=label)
        grouped.setdefault(key, []).append(value)
    return grouped


def parse_link_assignment(
    value: str, *, label: str = "link assignment"
) -> tuple[str, str]:
    if "=" in value:
        return parse_assignment(value, label=label)
    match = LINK_REF_RE.match(value.strip())
    if match:
        return match.group("kind"), value.strip()
    raise SystemExit(
        f"Invalid {label}: {value!r}. Expected KEY=VALUE or a record ref like ticket:0004"
    )


def collect_link_assignments(
    values: list[str], *, label: str = "link assignment"
) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for item in values:
        key, value = parse_link_assignment(item, label=label)
        grouped.setdefault(key, []).append(value)
    return grouped


def add_scope_arguments(parser: Any) -> None:
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="Path governed by this record; repeat to infer multi-repository scope",
    )
    parser.add_argument(
        "--repository",
        action="append",
        default=[],
        help="Explicit owning repository id; repeat to declare multi-repository scope",
    )
    parser.add_argument(
        "--workspace-scope",
        action="store_true",
        help="Mark the record as workspace-scoped instead of repository-scoped",
    )


def resolve_record_scope_args(args: Any, workspace: Path) -> dict | None:
    if getattr(args, "workspace_scope", False):
        if getattr(args, "path", []) or getattr(args, "repository", []):
            raise SystemExit(
                "Use either --workspace-scope or explicit --path/--repository inputs, not both"
            )
        return {"kind": "workspace", "workspace_id": "workspace:main"}
    scopes: list[dict | None] = []
    for repository_id in getattr(args, "repository", []):
        scopes.append({"kind": "repository", "repository_id": repository_id})
    for target in getattr(args, "path", []):
        owner = resolve_repository_for_path(workspace, Path(target))
        scopes.append({"kind": "repository", "repository_id": owner["repository_id"]})
    return merge_repository_scopes(workspace, scopes)


def load_text_argument(text: str | None, file_path: str | None) -> str:
    if text is None and file_path is None:
        raise SystemExit("Provide --text or --file")
    if text is not None and file_path is not None:
        raise SystemExit("Use either --text or --file, not both")
    if text is not None:
        return text
    if file_path is None:
        raise SystemExit("Provide --text or --file")
    return Path(file_path).read_text().rstrip()
