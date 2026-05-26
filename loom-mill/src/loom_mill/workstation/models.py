from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from loom_mill.processes import IterationSummary
from loom_mill.processes.backpressure import BackpressureSignal


class WorkstationStatus(StrEnum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"
    FINISHED = "finished"
    CONFLICT = "conflict"


@dataclass(frozen=True)
class OutputEvent:
    stream: str
    line: str
    timestamp: str

    @property
    def data(self) -> str:
        return self.line + "\n"


@dataclass
class WorkstationState:
    id: str | None = None
    ticket_id: str | None = None
    status: WorkstationStatus = WorkstationStatus.IDLE
    worktree_path: Path | None = None
    started_at: str | None = None
    iteration_count: int = 0
    last_event_at: str | None = None
    process_id: int | None = None
    exit_code: int | None = None
    output: list[OutputEvent] = field(default_factory=list)
    iteration_summary: IterationSummary | None = None
    backpressure_signals: list[BackpressureSignal] = field(default_factory=list)
    andon: AndonState = field(default_factory=lambda: AndonState())


@dataclass
class AndonState:
    active: bool = False
    signals: list[BackpressureSignal] = field(default_factory=list)
