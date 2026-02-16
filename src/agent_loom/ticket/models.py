from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent_loom.ticket.frontmatter import extract_title


@dataclasses.dataclass(frozen=True)
class GitStatusEntry:
    xy: str
    path: str
    path2: str = ""


@dataclasses.dataclass
class Ticket:
    path: Path
    fm: Dict[str, Any]
    body: str

    @property
    def id(self) -> str:
        return str(self.fm.get("id", ""))

    @property
    def title(self) -> str:
        return extract_title(self.body)

    @property
    def status(self) -> str:
        return str(self.fm.get("status", "open"))

    @property
    def priority(self) -> int:
        try:
            return int(self.fm.get("priority", 2))
        except Exception:
            return 2


@dataclasses.dataclass
class TicketConfig:
    prefix: str = ""
    github_default_repo: str = ""  # owner/repo
    jira_base_url: str = ""  # e.g. https://example.atlassian.net
    sprint_name: str = ""
    sprint_tag: str = ""
    extra: Dict[str, Any] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass(frozen=True)
class TicketVersionResult:
    name: str
    version: str


@dataclasses.dataclass(frozen=True)
class TicketInitResult:
    initialized: str


@dataclasses.dataclass(frozen=True)
class TicketSprintContextResult:
    name: str
    tag: str

@dataclasses.dataclass(frozen=True)
class TicketCreateResult:
    id: str
    path: str


@dataclasses.dataclass(frozen=True)
class TicketStatusResult:
    id: str
    status: str


@dataclasses.dataclass(frozen=True)
class TicketUpdateResult:
    id: str


@dataclasses.dataclass(frozen=True)
class TicketAddNoteResult:
    id: str
    timestamp: str


@dataclasses.dataclass(frozen=True)
class TicketSummary:
    id: str
    title: str
    status: str
    priority: int
    assignee: str
    tags: List[str]
    claimed_by: str
    deps: List[str] = dataclasses.field(default_factory=list)
    blockers: List[str] = dataclasses.field(default_factory=list)
    mtime: str = ""


@dataclasses.dataclass(frozen=True)
class TicketListResult:
    count: int
    tickets: List[TicketSummary]


@dataclasses.dataclass(frozen=True)
class TicketRelationships:
    blockers: List[str]
    blocking: List[str]
    children: List[str]
    linked: List[str]


@dataclasses.dataclass(frozen=True)
class TicketDetails:
    id: str
    title: str
    status: str
    priority: int
    type: str
    assignee: str
    tags: List[str]
    deps: List[str]
    links: List[str]
    external_ref: str
    parent: str
    claimed_by: str


@dataclasses.dataclass(frozen=True)
class TicketShowResult:
    ticket: TicketDetails
    relationships: TicketRelationships
    body: str
    frontmatter: Dict[str, Any]
    lease: Dict[str, Any]


@dataclasses.dataclass(frozen=True)
class TicketGraphEdge:
    src: str
    dst: str
    kind: str


@dataclasses.dataclass(frozen=True)
class TicketHealth:
    counts: Dict[str, Any]
    ready: int
    blocked: int
    bottlenecks: List[Dict[str, Any]]


@dataclasses.dataclass(frozen=True)
class TicketGraph:
    nodes: List[str]
    edges: List[TicketGraphEdge]


@dataclasses.dataclass(frozen=True)
class TicketViewResult:
    ticket: TicketDetails
    graph: TicketGraph
    health: TicketHealth


@dataclasses.dataclass(frozen=True)
class TicketDepResult:
    root: str
    nodes: List[str]
    edges: List[TicketGraphEdge]
    health: TicketHealth


@dataclasses.dataclass(frozen=True)
class TicketDependencyResult:
    id: str
    dependency: str
    changed: Optional[bool] = None


@dataclasses.dataclass(frozen=True)
class TicketLinkResult:
    id: str
    target: str


@dataclasses.dataclass(frozen=True)
class TicketLinkManyResult:
    ids: List[str]
    changed: int


@dataclasses.dataclass(frozen=True)
class TicketCyclesResult:
    cycles: List[List[str]]


@dataclasses.dataclass(frozen=True)
class TicketClaimResult:
    id: str
    claimed_by: str
    claim_expires: str
    heartbeat: str


@dataclasses.dataclass(frozen=True)
class TicketHeartbeatResult:
    id: str
    heartbeat: str
    claim_expires: str


@dataclasses.dataclass(frozen=True)
class TicketReleaseResult:
    id: str


@dataclasses.dataclass(frozen=True)
class TicketSwarmAgent:
    agent: str
    active: bool
    last_heartbeat: str
    claims: List[str]


@dataclasses.dataclass(frozen=True)
class TicketSwarmResult:
    agents: List[TicketSwarmAgent]


@dataclasses.dataclass(frozen=True)
class TicketSyncResult:
    committed: bool
    count: int
    files: List[str]
    sha: str = ""
    message: str = ""


@dataclasses.dataclass(frozen=True)
class TicketSyncExternalItem:
    id: str
    external_ref: str
    ok: bool
    changed: bool
    note: str = ""
    error: str = ""


@dataclasses.dataclass(frozen=True)
class TicketSyncExternalResult:
    results: List[TicketSyncExternalItem]


@dataclasses.dataclass(frozen=True)
class TicketQueryResult:
    result: Any


@dataclasses.dataclass(frozen=True)
class TicketPrimeResult:
    payload: Dict[str, Any]


__all__ = [
    "GitStatusEntry",
    "Ticket",
    "TicketAddNoteResult",
    "TicketClaimResult",
    "TicketCreateResult",
    "TicketCyclesResult",
    "TicketDepResult",
    "TicketDependencyResult",
    "TicketDetails",
    "TicketGraph",
    "TicketGraphEdge",
    "TicketHealth",
    "TicketHeartbeatResult",
    "TicketInitResult",
    "TicketLinkResult",
    "TicketLinkManyResult",
    "TicketListResult",
    "TicketPrimeResult",
    "TicketSprintContextResult",
    "TicketQueryResult",
    "TicketReleaseResult",
    "TicketRelationships",
    "TicketShowResult",
    "TicketStatusResult",
    "TicketSummary",
    "TicketSwarmAgent",
    "TicketSwarmResult",
    "TicketSyncExternalItem",
    "TicketSyncExternalResult",
    "TicketSyncResult",
    "TicketUpdateResult",
    "TicketVersionResult",
    "TicketViewResult",
    "TicketConfig",
]
