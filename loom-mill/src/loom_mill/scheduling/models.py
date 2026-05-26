from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class TicketSummary:
    ticket_id: str
    title: str
    status: str
    path: Path
    created: date | None = None
    priority: str | None = None
    type_keywords: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SchedulingDecision:
    selected_ticket: str | None
    candidates_considered: list[str]
    filtered_out: dict[str, str]
    advisory_recommendation: list[str]
    reasoning: str


@dataclass(frozen=True)
class ScheduleOverrides:
    pinned: list[str] = field(default_factory=list)
    excluded: list[str] = field(default_factory=list)
