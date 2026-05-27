from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ShapingEvent:
    session_id: str
    event: str
    data: dict
