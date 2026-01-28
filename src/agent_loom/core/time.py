from __future__ import annotations

import datetime as dt
import re
from typing import Optional

_DURATION_RE = re.compile(r"^\s*(\d+)\s*([smhd])\s*$", re.IGNORECASE)


def utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def isoformat_z(ts: dt.datetime) -> str:
    ts = ts.astimezone(dt.timezone.utc)
    s = ts.replace(microsecond=0).isoformat()
    return s.replace("+00:00", "Z")


def parse_iso(ts: str) -> Optional[dt.datetime]:
    if not ts:
        return None
    try:
        return dt.datetime.fromisoformat(ts)
    except Exception:
        return None


def now_iso() -> str:
    return isoformat_z(utcnow())


def parse_duration(spec: str) -> dt.timedelta:
    m = _DURATION_RE.match(spec or "")
    if not m:
        raise ValueError(f"Invalid duration: {spec!r} (expected like 30m, 2h, 1d)")
    n = int(m.group(1))
    unit = m.group(2).lower()
    if unit == "s":
        return dt.timedelta(seconds=n)
    if unit == "m":
        return dt.timedelta(minutes=n)
    if unit == "h":
        return dt.timedelta(hours=n)
    if unit == "d":
        return dt.timedelta(days=n)
    raise ValueError(f"Invalid duration unit: {unit}")


def parse_duration_seconds(s: str) -> int:
    raw = str(s or "").strip().lower()
    if not raw:
        raise ValueError("missing duration")

    if re.fullmatch(r"\d{1,2}:\d{2}(:\d{2})?", raw):
        parts = [int(p) for p in raw.split(":")]
        if len(parts) == 2:
            mm, ss = parts
            return mm * 60 + ss
        hh, mm, ss = parts
        return hh * 3600 + mm * 60 + ss

    if raw.isdigit():
        return int(raw)

    if not re.fullmatch(r"(?:\d+[smhd])+", raw):
        raise ValueError(f"invalid duration: {s}")

    total = 0
    for m in re.finditer(r"(\d+)([smhd])", raw):
        n = int(m.group(1))
        unit = m.group(2)
        if unit == "s":
            total += n
        elif unit == "m":
            total += n * 60
        elif unit == "h":
            total += n * 3600
        elif unit == "d":
            total += n * 86400
    if total <= 0:
        raise ValueError(f"invalid duration: {s}")
    return total
