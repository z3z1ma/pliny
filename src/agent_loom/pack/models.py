from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Literal, Optional


@dataclass(frozen=True)
class PackManifest:
    id: str
    version: str
    description: str
    install_roots: List[str]
    managed_globs: List[str]
    protected_globs: List[str]
    upstream: Optional[Dict[str, str]] = None


@dataclass(frozen=True)
class LockFileEntry:
    path: str
    sha256: str


@dataclass(frozen=True)
class InstalledPack:
    id: str
    version: str
    installed_at: str
    files: List[LockFileEntry]


@dataclass(frozen=True)
class LockFile:
    version: int
    packs: List[InstalledPack]


Action = Literal[
    "install",
    "update",
    "uninstall",
    "status",
    "doctor",
]


@dataclass(frozen=True)
class PackApplyResult:
    ok: bool
    action: Action
    pack_id: str
    pack_version: str
    dest: str
    dry_run: bool
    wrote: List[str]
    removed: List[str]
    skipped: List[str]
    drifted: List[str]
    missing: List[str]
    warnings: List[str]
