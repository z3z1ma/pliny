from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha256(text: str) -> str:
    return _sha256_bytes(text.encode("utf-8"))


def observations_prefix_sha256(file_path: Path, *, prefix_bytes: int = 4096) -> str:
    """Hash the first N bytes of the observations file.

    Stable across appends; changes when file is replaced/rotated.
    """

    if prefix_bytes <= 0:
        prefix_bytes = 1
    if not file_path.exists():
        return ""
    try:
        with file_path.open("rb") as f:
            prefix = f.read(int(prefix_bytes))
        return _sha256_bytes(prefix) if prefix else ""
    except Exception:
        return ""


@dataclass(frozen=True)
class ObservationCount:
    count: int
    tail_sha256: str


@dataclass(frozen=True)
class ObservationIngest:
    start_offset_bytes: int
    end_offset_bytes: int
    items: List[Dict[str, Any]]
    parse_errors: int
    partial_line_ignored: bool


def read_observations_tail(file_path: Path, *, max_lines: int) -> List[Dict[str, Any]]:
    if max_lines <= 0:
        return []
    if not file_path.exists():
        return []
    # Stream to avoid loading very large files.
    lines: list[str] = []
    with file_path.open("r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            if not ln.strip():
                continue
            lines.append(ln.rstrip("\n"))
            if len(lines) > int(max_lines):
                lines = lines[-int(max_lines) :]
    tail = lines
    out: List[Dict[str, Any]] = []
    for ln in tail:
        try:
            obj = json.loads(ln)
        except Exception:
            continue
        if isinstance(obj, dict):
            out.append(obj)
    return out


def count_observations(file_path: Path) -> ObservationCount:
    if not file_path.exists():
        return ObservationCount(count=0, tail_sha256="")

    count = 0
    tail_lines: list[str] = []
    try:
        with file_path.open("r", encoding="utf-8", errors="replace") as f:
            for ln in f:
                if not ln.strip():
                    continue
                count += 1
                tail_lines.append(ln.rstrip("\n"))
                if len(tail_lines) > 200:
                    tail_lines = tail_lines[-200:]
    except Exception:
        return ObservationCount(count=0, tail_sha256="")

    tail = "\n".join(tail_lines)
    return ObservationCount(count=int(count), tail_sha256=_sha256(tail) if tail else "")


def ingest_observations_since(
    file_path: Path, *, start_offset_bytes: int
) -> ObservationIngest:
    """Stream JSONL observations from a byte offset.

    Cursor semantics:
    - Offset is in bytes.
    - Only complete lines (ending with '\n') are ingested.
    - A final partial line is ignored and does not advance the cursor.
    """

    if start_offset_bytes < 0:
        start_offset_bytes = 0

    if not file_path.exists():
        return ObservationIngest(
            start_offset_bytes=int(start_offset_bytes),
            end_offset_bytes=int(start_offset_bytes),
            items=[],
            parse_errors=0,
            partial_line_ignored=False,
        )

    items: List[Dict[str, Any]] = []
    parse_errors = 0
    partial_ignored = False
    end_offset = int(start_offset_bytes)

    try:
        with file_path.open("rb") as f:
            f.seek(int(start_offset_bytes))
            while True:
                pos = f.tell()
                raw = f.readline()
                if raw == b"":
                    break
                if not raw.endswith(b"\n"):
                    partial_ignored = True
                    f.seek(pos)
                    break
                end_offset = f.tell()
                if not raw.strip():
                    continue
                try:
                    decoded = raw.decode("utf-8", errors="strict").rstrip("\n")
                    obj = json.loads(decoded)
                except Exception:
                    parse_errors += 1
                    decoded2 = raw.decode("utf-8", errors="replace").rstrip("\n")
                    snippet = decoded2[:2000]
                    items.append(
                        {
                            "_compound_parse_error": True,
                            "raw_snippet": snippet,
                            "raw_sha256": _sha256(decoded2),
                        }
                    )
                    continue
                if isinstance(obj, dict):
                    items.append(obj)
    except Exception:
        return ObservationIngest(
            start_offset_bytes=int(start_offset_bytes),
            end_offset_bytes=int(start_offset_bytes),
            items=[],
            parse_errors=0,
            partial_line_ignored=False,
        )

    return ObservationIngest(
        start_offset_bytes=int(start_offset_bytes),
        end_offset_bytes=int(end_offset),
        items=items,
        parse_errors=int(parse_errors),
        partial_line_ignored=bool(partial_ignored),
    )
