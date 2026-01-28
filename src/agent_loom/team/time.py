from __future__ import annotations

import datetime as dt
from typing import Optional


def _iso_z(ts: Optional[dt.datetime] = None) -> str:
    d = ts or dt.datetime.now(dt.timezone.utc)
    return d.isoformat().replace("+00:00", "Z")


__all__ = ["_iso_z"]
