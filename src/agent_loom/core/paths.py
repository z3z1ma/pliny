from __future__ import annotations

from pathlib import Path
from typing import Optional


def realpath_from(base: Path, p: str) -> Optional[Path]:
    s = (p or "").strip()
    if not s:
        return None
    pp = Path(s)
    if not pp.is_absolute():
        pp = base / pp
    try:
        return pp.expanduser().resolve()
    except Exception:
        return pp.expanduser().absolute()


def safe_relpath(p: Path, base: Path) -> str:
    try:
        return str(p.relative_to(base))
    except Exception:
        return str(p)
