from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CompoundInstallResult:
    dest: str
    dry_run: bool
    wrote: list[str]
    skipped: list[str]
    warnings: list[str]


@dataclass(frozen=True)
class CompoundSyncResult:
    committed: bool
    count: int
    files: list[str]
    sha: str
    message: str


__all__ = [
    "CompoundInstallResult",
    "CompoundSyncResult",
]
