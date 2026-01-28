from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class VaultPaths:
    root: Path
    notes_dir: Path
    personal_notes_dir: Path
    ephemeral_notes_dir: Path
    db_path: Path
    meta_path: Path


@dataclass
class Note:
    id: str
    title: str
    body: str
    created_at: str
    updated_at: str
    tags: List[str]
    aliases: List[str]
    visibility: str
    status: str
    scopes: List[Dict[str, Any]]
    links_frontmatter: List[str]
    frontmatter: Dict[str, Any]


@dataclass(frozen=True)
class PrimeResult:
    payload: Dict[str, Any]


@dataclass(frozen=True)
class InitResult:
    ok: bool
    vault: str
    meta: Dict[str, Any]
    db: Dict[str, Any]
    gitignore: List[Dict[str, Any]]


@dataclass(frozen=True)
class AddResult:
    ok: bool
    id: str
    path: str
    visibility: str
    links: Dict[str, Any]


@dataclass(frozen=True)
class EditResult:
    ok: bool
    id: str
    path: str
    moved: bool
    updated: bool
    warnings: List[str]
    links: Dict[str, Any]


@dataclass(frozen=True)
class ReindexResult:
    ok: bool
    indexed: int
    updated: int
    deleted: int
    skipped: int
    warnings: List[Dict[str, Any]]


@dataclass(frozen=True)
class JanitorNote:
    id: str
    path: str
    visibility: str
    stale_scopes: List[Dict[str, Any]]
    warnings: List[str]


@dataclass(frozen=True)
class JanitorReportResult:
    ok: bool
    count: int
    notes: List[JanitorNote]


@dataclass(frozen=True)
class JanitorFixResult:
    ok: bool
    dry_run: bool = False
    count: int = 0
    notes: List[JanitorNote] = field(default_factory=list)
    hint: str = ""
    updated_notes: int = 0
    reported: int = 0


@dataclass(frozen=True)
class LinkBacklink:
    id: str
    title: str
    path: str
    updated_at: str


@dataclass(frozen=True)
class LinkBacklinksResult:
    backlinks: List[LinkBacklink]
    warnings: List[Dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class LinkNeighborsResult:
    id: str
    k: int
    neighbors: Dict[str, List[str]] | None = None
    nodes: List[Dict[str, Any]] | None = None
    warnings: List[Dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class LinkValidateRow:
    src_id: str
    dst_raw: str
    resolution: str
    style: str
    alias_text: str
    anchor: str


@dataclass(frozen=True)
class LinkValidateResult:
    rows: List[LinkValidateRow]
    warnings: List[Dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class LinkGraphEdge:
    src_id: str
    dst_id: str | None
    dst_raw: str
    resolution: str
    style: str


@dataclass(frozen=True)
class LinkGraphResult:
    edges: List[LinkGraphEdge]
    warnings: List[Dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class RecallScore:
    final: float
    fts: float
    bm25: float | None
    scope: float
    recency: float


@dataclass(frozen=True)
class RecallWhy:
    matched_tags: List[str] | None = None
    excluded_tags: List[str] | None = None
    matched_scopes: List[Dict[str, Any]] | None = None
    excluded_scopes: List[Dict[str, Any]] | None = None
    fts_snippet: str | None = None
    recency_age_days: float | None = None
    via: List[str] | None = None
    graph_distance: int | None = None


@dataclass(frozen=True)
class RecallItem:
    id: str
    title: str
    path: str
    visibility: str
    status: str
    tags: List[str]
    aliases: List[str]
    scopes: List[Dict[str, Any]]
    created_at: str
    updated_at: str
    preview: str
    score: RecallScore | None = None
    why: RecallWhy | None = None
    role: str = "hit"
    body: str | None = None


@dataclass(frozen=True)
class RecallResult:
    items: List[RecallItem]
    context_text: str = ""
    warnings: List[Dict[str, Any]] = field(default_factory=list)


__all__ = [
    "AddResult",
    "EditResult",
    "InitResult",
    "JanitorFixResult",
    "JanitorNote",
    "JanitorReportResult",
    "LinkBacklink",
    "LinkBacklinksResult",
    "LinkGraphEdge",
    "LinkGraphResult",
    "LinkNeighborsResult",
    "LinkValidateResult",
    "LinkValidateRow",
    "Note",
    "PrimeResult",
    "RecallItem",
    "RecallResult",
    "RecallScore",
    "RecallWhy",
    "ReindexResult",
    "VaultPaths",
]
