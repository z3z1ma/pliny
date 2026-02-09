from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent_loom.core.fs import fs_unescape
from agent_loom.core.git import is_git_repo
from agent_loom.core.io import read_json
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.git.core import (
    git_is_dirty,
    git_worktree_remove,
    git_worktree_remove_from,
)
from agent_loom.workspace.guards import harness_root
from agent_loom.workspace.models import WorktreeGcResult
from agent_loom.workspace.harness.leases import lease_is_active, lease_path
from agent_loom.workspace.constants import HARNESS_DIR, INTERNAL_DIR
from agent_loom.workspace.state import (
    load_workspace,
    worktrees_base,
    ws_repos_dir,
    ws_worktrees_dir,
)


def _cleanup_group_artifacts(*, ws_root: Path, group: str) -> None:
    try:
        from agent_loom.workspace.worktree_meta import harness_group_meta_path

        harness_group_meta_path(ws_root, group).unlink(missing_ok=True)
    except Exception:
        pass
    try:
        lease_path(root=ws_root, key=f"group:{group}").unlink(missing_ok=True)
    except Exception:
        pass


def worktree_gc(
    *,
    older_than_days: int = 0,
    skip_leased: bool = False,
    force: bool = False,
    confirm: bool,
    root: Optional[Path] = None,
) -> WorktreeGcResult:
    if not confirm:
        raise WorkspaceError("Refusing to gc worktrees without --yes")

    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)

    groups: dict[str, Path] = {}
    wt_root = (ws_root / ws_worktrees_dir(ws)).resolve()
    if wt_root.exists():
        for group_dir in sorted(p for p in wt_root.iterdir() if p.is_dir()):
            groups[fs_unescape(group_dir.name)] = group_dir.resolve()

    meta_dir = (ws_root / INTERNAL_DIR / HARNESS_DIR / "meta" / "groups").resolve()
    if meta_dir.exists():
        for p in sorted(meta_dir.glob("*.json")):
            try:
                meta = read_json(p)
            except Exception:
                continue
            if not isinstance(meta, dict):
                continue
            group = str(meta.get("group") or "").strip() or fs_unescape(p.stem)
            if not group:
                continue
            groups[group] = worktrees_base(ws_root, ws, group).resolve()

    if not groups:
        return WorktreeGcResult(removed=[], skipped=[])

    now = time.time()
    cutoff = now - (max(0, int(older_than_days)) * 86400)

    removed: List[str] = []
    skipped: List[Dict[str, Any]] = []

    for group, group_dir in sorted(groups.items(), key=lambda x: x[0]):
        if not group_dir.exists() or not group_dir.is_dir():
            _cleanup_group_artifacts(ws_root=ws_root, group=group)
            continue

        if older_than_days > 0:
            if group_dir.stat().st_mtime >= cutoff:
                skipped.append({"group": group, "status": "skip", "reason": "too_new"})
                continue

        if skip_leased:
            key = f"group:{group}"
            if lease_is_active(key=key, root=ws_root):
                lease = lease_path(root=ws_root, key=key)
                skipped.append(
                    {
                        "group": group,
                        "status": "skip",
                        "reason": "leased",
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

        # If the group is now empty, remove group dir + artifacts.
        try:
            if group_dir.exists() and not any(p.is_dir() for p in group_dir.iterdir()):
                group_dir.rmdir()
        except Exception:
            pass
        if not group_dir.exists():
            _cleanup_group_artifacts(ws_root=ws_root, group=group)

    return WorktreeGcResult(removed=removed, skipped=skipped)
