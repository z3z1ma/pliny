from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ShapingEventName = Literal[
    "node_added",
    "edge_added",
    "node_updated",
    "node_invalidated",
    "phase_changed",
    "exploration_start",
    "exploration_stream",
    "exploration_complete",
    "exploration_cancelled",
    "session_ended",
]


@dataclass(frozen=True)
class ShapingEvent:
    session_id: str
    event: ShapingEventName
    data: dict
