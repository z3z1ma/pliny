from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Iterable

from .models import LoomGraph, LoomRecord, RecordMetadata

TOP_LABELS = {
    "ID",
    "Type",
    "Status",
    "Created",
    "Updated",
    "Risk",
    "Priority",
    "Depends On",
}

TOP_LABEL_RE = re.compile(r"^(ID|Type|Status|Created|Updated|Risk|Priority|Depends On):\s*(.*)$")
HEADING_RE = re.compile(r"^(#|##|###)\s+(.+?)\s*$")
REFERENCE_RE = re.compile(
    r"\b(?:"
    r"ticket:\d{8}-[A-Za-z0-9][A-Za-z0-9_-]*"
    r"|spec:[A-Za-z0-9][A-Za-z0-9_-]*"
    r"|plan:\d{8}-[A-Za-z0-9][A-Za-z0-9_-]*"
    r"|evidence:\d{8}-[A-Za-z0-9][A-Za-z0-9_-]*"
    r"|audit:\d{8}-[A-Za-z0-9][A-Za-z0-9_-]*"
    r"|research:\d{8}-[A-Za-z0-9][A-Za-z0-9_-]*"
    r"|knowledge:[A-Za-z0-9][A-Za-z0-9_-]*"
    r"|constitution:[A-Za-z0-9][A-Za-z0-9_-]*"
    r"|decision:\d{4}"
    r"|roadmap:[A-Za-z0-9][A-Za-z0-9_-]*"
    r"|principle:[A-Za-z0-9][A-Za-z0-9_-]*"
    r")\b"
)
LABELED_ID_RE = re.compile(r"\b(?:ACC|REQ|SCN|FIND|OQ|RD)-\d{3}\b")


def parse_records(directory: str | Path) -> LoomGraph:
    root = Path(directory)
    records = []
    if not root.exists() or not root.is_dir():
        return LoomGraph(root=str(root), records=())

    for path in sorted(root.rglob("*.md")):
        record = parse_record(path, root=root)
        if record is not None:
            records.append(record)
    return LoomGraph(root=str(root), records=tuple(records))


def parse_record(path: str | Path, root: str | Path | None = None) -> LoomRecord | None:
    record_path = Path(path)
    try:
        text = record_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    lines = text.splitlines()
    metadata = _parse_metadata(lines)
    output_path = _display_path(record_path, Path(root) if root is not None else None)

    return LoomRecord(
        path=output_path,
        surface=_surface_for(record_path, Path(root) if root is not None else None),
        metadata=metadata,
        headings=tuple(_parse_headings(lines)),
        references=tuple(_unique(REFERENCE_RE.findall(text))),
        labeled_ids=tuple(_unique(LABELED_ID_RE.findall(text))),
    )


def _parse_metadata(lines: Iterable[str]) -> RecordMetadata:
    values: dict[str, str] = {}
    for line in lines:
        if line.startswith("# ") or line.startswith("## "):
            continue
        match = TOP_LABEL_RE.match(line)
        if match is None:
            continue
        label, value = match.groups()
        if label in TOP_LABELS:
            values[label] = value.strip()

    depends_on = tuple(_unique(REFERENCE_RE.findall(values.get("Depends On", ""))))
    return RecordMetadata(
        id=values.get("ID") or None,
        type=values.get("Type") or None,
        status=values.get("Status") or None,
        created=_parse_date(values.get("Created")),
        updated=_parse_date(values.get("Updated")),
        risk=values.get("Risk") or None,
        priority=values.get("Priority") or None,
        depends_on=depends_on,
    )


def _parse_headings(lines: Iterable[str]) -> list[tuple[int, str]]:
    headings = []
    for line in lines:
        match = HEADING_RE.match(line)
        if match is None:
            continue
        marks, title = match.groups()
        headings.append((len(marks), title.strip()))
    return headings


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _display_path(path: Path, root: Path | None) -> str:
    if root is None:
        return str(path)
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _surface_for(path: Path, root: Path | None) -> str | None:
    if root is None:
        return None
    try:
        relative = path.relative_to(root)
    except ValueError:
        return None
    return relative.parts[0] if relative.parts else None


def _unique(values: Iterable[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
