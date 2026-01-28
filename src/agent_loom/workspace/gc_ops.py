from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent_loom.workspace.constants import INTERNAL_DIR
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.git_ops import (
    git_is_dirty,
    git_worktree_remove,
    git_worktree_remove_from,
)
from agent_loom.workspace.guards import workspace_root
from agent_loom.workspace.models import WorktreeGcResult
from agent_loom.workspace.state import (
    fs_escape,
    fs_unescape,
    load_workspace,
    ws_repos_dir,
    ws_worktrees_dir,
)
from agent_loom.workspace.utils import is_git_repo


def _lease_file_for_group(ws_root: Path, group: str) -> Path:
    key = f"group:{group}"
    return (ws_root / INTERNAL_DIR / "leases" / f"{fs_escape(key)}.json").resolve()


def worktree_gc(
    *,
    older_than_days: int = 0,
    unclaimed_only: bool = False,
    force: bool = False,
    confirm: bool,
    root: Optional[Path] = None,
) -> WorktreeGcResult:
    if not confirm:
        raise WorkspaceError("Refusing to gc worktrees without --yes")

    ws_root = root.resolve() if root is not None else workspace_root()
    ws = load_workspace(ws_root)

    wt_root = (ws_root / ws_worktrees_dir(ws)).resolve()
    if not wt_root.exists():
        return WorktreeGcResult(removed=[], skipped=[])

    now = time.time()
    cutoff = now - (max(0, int(older_than_days)) * 86400)

    removed: List[str] = []
    skipped: List[Dict[str, Any]] = []

    for group_dir in sorted(p for p in wt_root.iterdir() if p.is_dir()):
        group = fs_unescape(group_dir.name)

        if older_than_days > 0:
            if group_dir.stat().st_mtime >= cutoff:
                skipped.append({"group": group, "status": "skip", "reason": "too_new"})
                continue

        if unclaimed_only:
            lease = _lease_file_for_group(ws_root, group)
            if lease.exists():
                skipped.append(
                    {
                        "group": group,
                        "status": "skip",
                        "reason": "claimed",
                        "lease_path": str(lease),
                    }
                )
                continue

        for repo_dir in sorted(p for p in group_dir.iterdir() if p.is_dir()):
            repo_name = repo_dir.name
            if not is_git_repo(repo_dir):
                skipped.append(
                    {
                        "group": group,
                        "repo": repo_name,
                        "status": "skip",
                        "reason": "not_a_repo",
                        "path": str(repo_dir.resolve()),
                    }
                )
                continue

            if git_is_dirty(repo_dir) and not force:
                skipped.append(
                    {
                        "group": group,
                        "repo": repo_name,
                        "status": "skip",
                        "reason": "dirty",
                        "path": str(repo_dir.resolve()),
                    }
                )
                continue

            repo_path = (ws_root / ws_repos_dir(ws) / repo_name).resolve()
            try:
                if repo_path.exists() and is_git_repo(repo_path):
                    git_worktree_remove_from(repo_path, repo_dir, force=bool(force))
                else:
                    git_worktree_remove(repo_dir, force=bool(force))
                removed.append(str(repo_dir.resolve()))
            except WorkspaceError as e:
                skipped.append(
                    {
                        "group": group,
                        "repo": repo_name,
                        "status": "skip",
                        "reason": "remove_failed",
                        "error": str(e),
                        "path": str(repo_dir.resolve()),
                    }
                )

    return WorktreeGcResult(removed=removed, skipped=skipped)
