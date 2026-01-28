from __future__ import annotations

import hashlib
import re


def sanitize(s: str, *, allow: str = r"a-zA-Z0-9._-", max_len: int = 64) -> str:
    s2 = (s or "").strip()
    if not s2:
        return ""
    s2 = re.sub(r"\s+", "-", s2)
    s2 = re.sub(rf"[^{allow}]+", "-", s2)
    s2 = re.sub(r"-+", "-", s2).strip("-")
    out = s2[:max_len].strip("-")
    if out in (".", ".."):
        return ""
    return out


def generate_stable_key(s: str, *, max_len: int = 80) -> str:
    """Return a filesystem-safe key that is stable and collision-resistant."""

    raw = str(s or "").strip()
    if not raw:
        return ""
    base = sanitize(raw, max_len=max_len)
    if not base:
        return ""
    if base == raw and len(base) <= max_len:
        return base
    h = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8]
    head = sanitize(base, max_len=max(1, max_len - 9))
    if not head:
        head = "x"
    return f"{head}-{h}"[:max_len].strip("-")


def message_preview(text: str, *, max_len: int = 100) -> str:
    first = str(text or "").splitlines()[0] if str(text or "") else ""
    if len(first) > max_len:
        return first[: max(0, max_len - 3)] + "..."
    return first


__all__ = ["sanitize", "generate_stable_key", "message_preview"]
