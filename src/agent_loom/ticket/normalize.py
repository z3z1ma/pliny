from __future__ import annotations

from pathlib import Path
from typing import Any, Optional


def normalize_priority(value: Any) -> int:
    """Normalize priority inputs to an int 0..4 (0 is highest).

    Accepted inputs:
    - ints / numeric strings: 0..4
    - P-prefixed: P0..P4 (case-insensitive)
    - words: critical/blocker/urgent, high, medium/med/normal, low, lowest/trivial
    """

    if value is None:
        raise ValueError("priority is required")

    if isinstance(value, int):
        p = value
    else:
        s = str(value).strip().lower()
        if not s:
            raise ValueError("priority is required")

        if s.startswith("p") and len(s) >= 2 and s[1:].strip().isdigit():
            s = s[1:].strip()

        aliases = {
            "critical": 0,
            "blocker": 0,
            "urgent": 0,
            "highest": 0,
            "high": 1,
            "medium": 2,
            "med": 2,
            "normal": 2,
            "low": 3,
            "lowest": 4,
            "trivial": 4,
        }
        if s in aliases:
            p = aliases[s]
        else:
            try:
                p = int(s)
            except Exception as e:
                raise ValueError(
                    "Invalid priority. Use 0..4, P0..P4, or one of: "
                    "critical|high|medium|low|trivial"
                ) from e

    if p < 0 or p > 4:
        raise ValueError("Invalid priority. Must be in range 0..4 (0 is highest)")
    return int(p)


def normalize_status(value: Any) -> str:
    """Normalize status inputs to open|in_progress|closed."""

    s = str(value or "").strip().lower()
    if not s:
        return "open"

    s = s.replace("-", "_")
    s = s.replace(" ", "_")

    aliases = {
        "inprogress": "in_progress",
        "in_progress": "in_progress",
        "wip": "in_progress",
        "doing": "in_progress",
        "started": "in_progress",
        "open": "open",
        "todo": "open",
        "new": "open",
        "closed": "closed",
        "done": "closed",
        "complete": "closed",
        "completed": "closed",
    }
    if s in aliases:
        return aliases[s]

    return s


def normalize_type(value: Any) -> str:
    s = str(value or "").strip().lower()
    if not s:
        return ""

    aliases = {
        "feat": "feature",
        "feature": "feature",
        "bugfix": "bug",
        "bug": "bug",
        "chore": "chore",
        "task": "task",
        "epic": "epic",
    }
    return aliases.get(s, s)


def normalize_ticket_ref(value: str, *, tickets_dir: Optional[Path] = None) -> str:
    """Normalize common ticket reference forms to a bare id/pattern.

    Accepts:
    - #al-b110
    - al-b110.md
    - .tickets/al-b110.md
    - /abs/path/to/.tickets/al-b110.md
    """

    raw = str(value or "").strip()
    if raw.startswith("#"):
        raw = raw[1:].strip()

    if not raw:
        return ""

    # If the user passed a path-like reference, try to resolve it to a stem.
    if "/" in raw or "\\" in raw or raw.endswith(".md"):
        try:
            p = Path(raw).expanduser()
            if not p.is_absolute() and tickets_dir is not None:
                # Prefer resolving relative paths against tickets_dir's parent (repo root).
                # This covers `.tickets/<id>.md` and `<id>.md` from repo root-ish contexts.
                root = tickets_dir.parent
                cand = (root / p).resolve()
                if cand.exists() and cand.suffix == ".md":
                    return cand.stem
            if p.exists() and p.suffix == ".md":
                return p.stem
        except Exception:
            pass

    if raw.endswith(".md"):
        return raw[:-3]

    return raw
