from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class WorktreeDiffResult:
    worktree: str
    diff_mode: str
    base: str
    merge_base: str
    files: List[Dict[str, Any]]
    untracked: List[str]
    truncated: bool

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class WorktreeGroupDiffResult:
    group: str
    base: str
    results: List[Dict[str, Any]]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class WorktreeEnsureResult:
    branch: str
    path: str
    existed: bool
    reused: bool
    base_ref: str
    base_branch: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class WorktreeRemoveResult:
    removed: str
    branch: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class MergeAttemptResult:
    merged: bool
    worktree: str
    base: str
    base_commit: str
    topic: str
    merge_commit: str = ""
    stdout: str = ""
    stderr: str = ""
    error: str = ""
    hint: str = ""

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v != ""}


@dataclass(frozen=True)
class PrimeResult:
    payload: Dict[str, Any]


@dataclass(frozen=True)
class RepoStatusResult:
    repo_root: str
    branch: str
    commit: str
    dirty: bool
    default_branch: str


@dataclass(frozen=True)
class RepoWorktreeAddResult:
    branch: str
    path: str
    existed: bool


@dataclass(frozen=True)
class RepoWorktreePruneResult:
    pruned: bool


@dataclass(frozen=True)
class RepoWorktreeEnsureDetachedResult:
    path: str
    ref: str
    commit: str
    existed: bool


@dataclass(frozen=True)
class RepoWorktreeListResult:
    worktrees: List[Dict[str, Any]]


@dataclass(frozen=True)
class RepoWorktreeRemoveResult:
    removed: str
    branch: Optional[str] = None


@dataclass(frozen=True)
class PolyInitResult:
    workspace_file: str
    repos_dir: str
    worktrees_dir: str
    states_dir: str
    services_dir: str
    gitignore_path: str
    created: List[str]
    updated_gitignore: bool


@dataclass(frozen=True)
class RepoInitResult:
    repo_root: str
    internal_dir: str
    worktrees_dir: str
    git_exclude_path: str
    created: List[str]


@dataclass(frozen=True)
class SnapshotDiffResult:
    snapshot_path: str
    name: str
    target: Dict[str, Any]
    diffs: List[Dict[str, Any]]
    summary: Dict[str, Any]


@dataclass(frozen=True)
class SnapshotRestoreResult:
    snapshot_path: str
    name: str
    target: Dict[str, Any]
    results: List[Dict[str, Any]]
    summary: Dict[str, Any]


@dataclass(frozen=True)
class PolyExecResult:
    cmd: List[str]
    target: Dict[str, Any]
    results: List[Dict[str, Any]]
    summary: Dict[str, Any]


@dataclass(frozen=True)
class LeaseAcquireResult:
    key: str
    lease_path: str
    existed: bool
    forced: bool
    data: Dict[str, Any]


@dataclass(frozen=True)
class LeaseReleaseResult:
    key: str
    lease_path: str
    released: bool


@dataclass(frozen=True)
class LeaseListResult:
    leases_dir: str
    leases: List[Dict[str, Any]]


@dataclass(frozen=True)
class WorktreeGcResult:
    removed: List[str]
    skipped: List[Dict[str, Any]]


@dataclass(frozen=True)
class AddRepoResult:
    repo: str
    entry: Dict[str, Any]
    cloned: bool


@dataclass(frozen=True)
class RemoveRepoResult:
    repo: str
    deleted_clone: bool
    deleted_service_md: bool


@dataclass(frozen=True)
class ListReposResult:
    repos: List[Dict[str, Any]]
    repo_sets: Dict[str, Any]


@dataclass(frozen=True)
class ContextResult:
    workspace: Dict[str, Any]
    repos: List[Dict[str, Any]]
    worktrees: List[Dict[str, Any]]
    services_index: Optional[Dict[str, Any]]


@dataclass(frozen=True)
class SyncResult:
    results: List[Dict[str, Any]]
    services_index: Optional[Dict[str, Any]]


@dataclass(frozen=True)
class StatusResult:
    repos: List[Dict[str, Any]]


@dataclass(frozen=True)
class BranchResult:
    branch: str
    repos: List[Dict[str, Any]]
    services_index: Optional[Dict[str, Any]]


@dataclass(frozen=True)
class WorktreeAddResult:
    group: str
    worktrees: List[Dict[str, Any]]


@dataclass(frozen=True)
class WorktreeGroupRemoveResult:
    group: str
    removed: List[str]


@dataclass(frozen=True)
class WorktreeListResult:
    worktrees: List[Dict[str, Any]]


@dataclass(frozen=True)
class WorktreeRebaseResult:
    group: str
    results: List[Dict[str, Any]]


@dataclass(frozen=True)
class WorktreePushResult:
    group: str
    results: List[Dict[str, Any]]


@dataclass(frozen=True)
class SnapshotResult:
    snapshot_path: str
    snapshot: Dict[str, Any]


@dataclass(frozen=True)
class ServicesRefreshIndexResult:
    services_index_path: str
    index: Dict[str, Any]


@dataclass(frozen=True)
class DepsShowResult:
    service: str
    data: Dict[str, Any]


@dataclass(frozen=True)
class DepsWhoUsesResult:
    service: str
    used_by: List[str]


@dataclass(frozen=True)
class ImpactResult:
    source: Dict[str, Any]
    changed: List[str]
    unknown: List[str]
    impacted: List[str]
    all: List[str]


@dataclass(frozen=True)
class DeepenResult:
    repo: str
    depth: int = 0
    skipped: bool = False
    reason: str = ""


__all__ = [
    "AddRepoResult",
    "BranchResult",
    "ContextResult",
    "DeepenResult",
    "DepsShowResult",
    "DepsWhoUsesResult",
    "ImpactResult",
    "ListReposResult",
    "LeaseAcquireResult",
    "LeaseListResult",
    "LeaseReleaseResult",
    "MergeAttemptResult",
    "PolyInitResult",
    "PolyExecResult",
    "RepoStatusResult",
    "RepoInitResult",
    "RepoWorktreeAddResult",
    "RepoWorktreeEnsureDetachedResult",
    "RepoWorktreeListResult",
    "RepoWorktreePruneResult",
    "RepoWorktreeRemoveResult",
    "RemoveRepoResult",
    "ServicesRefreshIndexResult",
    "SnapshotResult",
    "SnapshotDiffResult",
    "SnapshotRestoreResult",
    "StatusResult",
    "SyncResult",
    "WorktreeGcResult",
    "WorktreeAddResult",
    "WorktreeEnsureResult",
    "WorktreeListResult",
    "WorktreePushResult",
    "WorktreeRebaseResult",
    "WorktreeGroupRemoveResult",
]
