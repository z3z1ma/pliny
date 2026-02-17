from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class StartResult:
    team: str
    session: str
    run_id: str
    run_dir: str
    repo_root: str
    tickets_dir: str
    manager: Dict[str, Any]
    charter: str
    created: bool


@dataclass(frozen=True)
class PrimeResult:
    markdown: str


@dataclass(frozen=True)
class InitAgentsResult:
    repo_root: str
    wrote: List[str]
    updated: List[str]
    skipped: List[str]
    missing: List[str]
    warnings: List[str]


@dataclass(frozen=True)
class AttachResult:
    team: str
    session: str
    manager_window: str


@dataclass(frozen=True)
class ObjectiveShowResult:
    team: str
    objective: str
    objective_rev: int
    objective_updated_at: str
    charter: str


@dataclass(frozen=True)
class ObjectiveUpdateResult:
    team: str
    mode: str
    objective_rev: int
    objective_updated_at: str
    charter: str
    inbox_id: str
    nudged: bool


@dataclass(frozen=True)
class DoneResult:
    team: str
    done: bool
    detail: Dict[str, Any]
    sent: bool = False
    inbox_id: str = ""
    existing_inbox_id: str = ""
    cooldown: bool = False
    nudged: bool = False


@dataclass(frozen=True)
class JanitorResult:
    team: str
    older_than_s: int
    dry_run: bool
    removed_workers: List[str]
    removed_worktrees: List[str]
    pruned_orphans: List[str]
    skipped_active_paths: List[str]


@dataclass(frozen=True)
class DisbandResult:
    team: str
    session: str
    worktrees_removed: bool
    state_removed: bool
    process_cleanup: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PauseResult:
    team: str
    session: str
    paused_at: str
    session_killed: bool


@dataclass(frozen=True)
class ResumeTeamResult:
    team: str
    session: str
    resumed_at: str
    manager: Dict[str, Any]
    resumed_workers: List[str]
    skipped_workers: List[Dict[str, str]]
    integrator: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SpawnResult:
    team: str
    session: str
    repo_root: str
    run_dir: str
    tickets_dir: str
    worker: Dict[str, Any]
    ticket: Dict[str, Any]


@dataclass(frozen=True)
class SpawnIntegratorResult:
    team: str
    worker_id: str
    window: str
    pane_id: str
    worktree: str
    respawned: bool
    worker: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class StatusResult:
    team: str
    run_id: str
    session: str
    repo_root: str
    run_dir: str
    tickets_dir: str
    sprint: Dict[str, Any]
    team_config: Dict[str, Any]
    inbox: Dict[str, Any]
    merge_queue: Dict[str, Any]
    manager: Dict[str, Any]
    workers: Dict[str, Any]
    warnings: List[Dict[str, str]]


@dataclass(frozen=True)
class DoctorResult:
    team: str
    run_id: str
    session: str
    issues: List[Dict[str, Any]]
    suggestions: List[str]


@dataclass(frozen=True)
class CaptureResult:
    team: str
    target: Dict[str, Any]
    pane: Dict[str, Any]
    captured_at: str
    output: str
    output_file: str
    meta_file: str


@dataclass(frozen=True)
class SendResult:
    team: str
    target: Dict[str, Any]
    delivered: bool
    delivery_reason: str
    inbox: Dict[str, Any]
    deliveries: List[Dict[str, Any]] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class WaitResult:
    team: str
    recipient: str
    seconds: int
    wake_reason: str
    signaled: bool
    elapsed_s: float
    channel: str


@dataclass(frozen=True)
class MergeEnqueueResult:
    team: str
    item: Dict[str, Any]
    nudged: bool


@dataclass(frozen=True)
class MergeListResult:
    team: str
    count: int
    items: List[Dict[str, Any]]


@dataclass(frozen=True)
class MergeNextResult:
    team: str
    item: Optional[Dict[str, Any]]


@dataclass(frozen=True)
class MergeDoneResult:
    team: str
    item: Dict[str, Any]


@dataclass(frozen=True)
class ShipResult:
    team: str
    merged: bool
    target_branch: str
    merge_branch: str
    shipped_at: str
    shipped_ids: List[str]
    ws: Dict[str, Any]
    push: Dict[str, Any]


@dataclass(frozen=True)
class RetireResult:
    team: str
    worker_id: str
    retired: bool


@dataclass(frozen=True)
class MarkRetirableResult:
    team: str
    worker_id: str
    marked: bool


@dataclass(frozen=True)
class PrepSprintResult:
    team: str
    sprint: Dict[str, Any]
    ticket_id: str
    worker_id: str
    spawned: bool


@dataclass(frozen=True)
class SprintShowResult:
    team: str
    sprint: Dict[str, Any]
    rev: int


@dataclass(frozen=True)
class SprintSetResult:
    team: str
    sprint: Dict[str, Any]
    rev: int
    charter: str


@dataclass(frozen=True)
class SprintClearResult:
    team: str
    rev: int
    charter: str


@dataclass(frozen=True)
class BounceResult:
    team: str
    worker_id: str
    inbox_id: str


@dataclass(frozen=True)
class TuiResult:
    recipient: str
    run_id: str
    exit_reason: str


@dataclass(frozen=True)
class InboxListResult:
    team: str
    count: int
    messages: List[Dict[str, Any]]


@dataclass(frozen=True)
class InboxShowResult:
    team: str
    message: Dict[str, Any]


@dataclass(frozen=True)
class InboxAckResult:
    team: str
    message: Dict[str, Any]


@dataclass(frozen=True)
class InboxSendResult:
    team: str
    inbox: Dict[str, Any]
    nudged: bool


__all__ = [
    "InitAgentsResult",
    "PrimeResult",
    "AttachResult",
    "CaptureResult",
    "DisbandResult",
    "DoneResult",
    "DoctorResult",
    "InboxAckResult",
    "InboxListResult",
    "InboxSendResult",
    "InboxShowResult",
    "JanitorResult",
    "MarkRetirableResult",
    "PrepSprintResult",
    "SprintShowResult",
    "SprintSetResult",
    "SprintClearResult",
    "MergeDoneResult",
    "MergeEnqueueResult",
    "MergeListResult",
    "MergeNextResult",
    "ObjectiveShowResult",
    "ObjectiveUpdateResult",
    "PauseResult",
    "RetireResult",
    "ResumeTeamResult",
    "BounceResult",
    "SendResult",
    "ShipResult",
    "SpawnIntegratorResult",
    "SpawnResult",
    "StartResult",
    "StatusResult",
    "TuiResult",
    "WaitResult",
]
