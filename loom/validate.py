"""Shared record validation for Loom.

Both the ``create`` and ``diagnose`` commands import from here so that
kind-specific validation logic exists in exactly one place.
"""

from __future__ import annotations

from pathlib import Path

from .core import (
    extract_headings,
    flatten_link_values,
    issue,
    normalize_repository_scope,
    parse_timestamp,
    read_record,
    scan_records,
)
from .schema import SCHEMAS

COMMON_FIELDS = [
    "id",
    "kind",
    "schema_version",
    "status",
    "repository_scope",
    "links",
    "created_at",
    "updated_at",
]


def validate_kind(workspace: Path, kind: str | None = None) -> list[dict]:
    """Validate records against their kind schema.

    If *kind* is given, validate only that kind.  Otherwise validate all
    known kinds.
    """
    problems: list[dict] = []
    kinds = [kind] if kind else sorted(SCHEMAS)
    for path in scan_records(workspace):
        try:
            frontmatter, body = read_record(path)
        except Exception as exc:
            problems.append(issue(path, workspace, str(exc)))
            continue
        record_kind = frontmatter.get("kind")
        if record_kind not in kinds:
            continue
        schema = SCHEMAS.get(record_kind)
        if schema is None:
            continue
        record_status = frontmatter.get("status")
        if record_status not in schema["statuses"]:
            problems.append(
                issue(
                    path,
                    workspace,
                    f"invalid status for {record_kind}: {record_status}",
                )
            )
        headings = extract_headings(body)
        for section in schema["sections"]:
            if section not in headings:
                problems.append(issue(path, workspace, f"missing section: {section}"))
    return problems


def validate_structure(path: Path, workspace: Path) -> list[dict]:
    """Validate structural concerns common to all record kinds.

    Checks common fields, timestamps, scope, constitution link rules,
    and kind-specific statuses and sections.
    """
    problems: list[dict] = []
    try:
        frontmatter, body = read_record(path)
    except Exception as exc:
        return [issue(path, workspace, str(exc))]

    if frontmatter.get("kind") == "packet":
        return problems  # packets have their own structural shape

    for field in COMMON_FIELDS:
        if field not in frontmatter:
            problems.append(issue(path, workspace, f"missing field: {field}"))

    for key in ("created_at", "updated_at"):
        if key in frontmatter:
            try:
                parse_timestamp(frontmatter[key])
            except Exception:
                problems.append(issue(path, workspace, f"invalid timestamp: {key}"))

    try:
        normalize_repository_scope(workspace, frontmatter.get("repository_scope"))
    except SystemExit as exc:
        problems.append(issue(path, workspace, f"invalid repository_scope: {exc}"))

    if frontmatter.get("id") == "constitution:main" and flatten_link_values(
        frontmatter.get("links", {})
    ):
        problems.append(
            issue(
                path, workspace, "constitution:main must not declare frontmatter links"
            )
        )

    # Kind-specific validation: statuses and sections
    record_kind = frontmatter.get("kind")
    schema = SCHEMAS.get(record_kind) if isinstance(record_kind, str) else None
    if schema is not None:
        record_status = frontmatter.get("status")
        if record_status not in schema["statuses"]:
            problems.append(
                issue(
                    path,
                    workspace,
                    f"invalid status for {record_kind}: {record_status}",
                )
            )
        headings = extract_headings(body)
        for section in schema["sections"]:
            if section not in headings:
                problems.append(issue(path, workspace, f"missing section: {section}"))

    return problems
