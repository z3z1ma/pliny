from __future__ import annotations

from dataclasses import dataclass

from agent_loom.workspace.errors import WorkspaceError


@dataclass(frozen=True)
class Duration:
    seconds: int


_MULT = {
    "s": 1,
    "m": 60,
    "h": 60 * 60,
    "d": 24 * 60 * 60,
    "w": 7 * 24 * 60 * 60,
}


def parse_duration_seconds(raw: str) -> int:
    s = str(raw or "").strip()
    if not s:
        raise WorkspaceError("Missing duration")

    # Allow pure seconds.
    if s.isdigit():
        return max(0, int(s))

    unit = s[-1]
    num = s[:-1]
    if unit not in _MULT or not num.isdigit():
        raise WorkspaceError(
            "Invalid duration. Use <N>[s|m|h|d|w], for example: 30m, 2h, 7d."
        )

    return max(0, int(num) * _MULT[unit])
