from __future__ import annotations

import datetime as dt


def parse_iso_z(ts: str) -> dt.datetime | None:
    raw = str(ts or "").strip()
    if not raw:
        return None
    try:
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        return dt.datetime.fromisoformat(raw)
    except Exception:
        return None
