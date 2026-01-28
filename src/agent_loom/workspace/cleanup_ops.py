from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.git_ops import (
    git_worktree_list_porcelain,
    git_worktree_remove_from,
)
from agent_loom.workspace.repo_ops import repo_root
from agent_loom.workspace.time_utils import parse_iso_z
from agent_loom.workspace.utils import read_json
from agent_loom.workspace.worktree_meta import repo_worktree_meta_dir


def _expired(meta: dict, now: float) -> bool:
    ttl = meta.get("ttl_seconds")
    if ttl is None:
        return False
    try:
        ttl_s = int(ttl)
    except Exception:
        return False
    if ttl_s <= 0:
        return False

    ts = meta.get("last_used_at") or meta.get("updated_at") or meta.get("created_at")
    dt = parse_iso_z(str(ts or ""))
    if dt is None:
        return False
    return (dt.timestamp() + ttl_s) <= now


def repo_worktree_cleanup_suggest(*, root: Optional[Path] = None) -> dict:
    repo = root.resolve() if root is not None else repo_root()
    meta_dir = repo_worktree_meta_dir(repo)
    if not meta_dir.exists():
        return {"repo_root": str(repo.resolve()), "candidates": []}

    now = time.time()
    candidates: List[Dict[str, Any]] = []

    # Resolve branch -> path map
    branch_to_path: Dict[str, str] = {}
    for wt in git_worktree_list_porcelain(repo):
        br = str(wt.get("branch") or "").strip()
        if br:
            branch_to_path[br] = str(Path(str(wt.get("path") or "")).resolve())

    for p in sorted(meta_dir.glob("*.json")):
        try:
            meta = read_json(p)
        except Exception:
            continue
        if not isinstance(meta, dict):
            continue
        branch = str(meta.get("branch") or "").strip()
        if not branch:
            continue
        if not _expired(meta, now):
            continue

        candidates.append(
            {
                "id": branch,
                "branch": branch,
                "path": branch_to_path.get(branch, ""),
                "reason": "ttl_expired",
                "meta_path": str(p.resolve()),
            }
        )

    return {"repo_root": str(repo.resolve()), "candidates": candidates}


def repo_worktree_cleanup_apply(
    *,
    ids: List[str],
    confirm: bool,
    force: bool = False,
    root: Optional[Path] = None,
) -> dict:
    if not confirm:
        raise WorkspaceError("Refusing to apply cleanup without --yes")

    repo = root.resolve() if root is not None else repo_root()
    branch_set = {str(x).strip() for x in (ids or []) if str(x).strip()}
    if not branch_set:
        raise WorkspaceError("Missing cleanup ids")

    removed: List[Dict[str, Any]] = []
    skipped: List[Dict[str, Any]] = []

    # Resolve branch -> path
    branch_to_path: Dict[str, Path] = {}
    for wt in git_worktree_list_porcelain(repo):
        br = str(wt.get("branch") or "").strip()
        if br:
            branch_to_path[br] = Path(str(wt.get("path") or "")).resolve()

    for br in sorted(branch_set):
        wt_path = branch_to_path.get(br)
        if wt_path is None or not wt_path.exists():
            skipped.append({"id": br, "status": "skip", "reason": "not_found"})
            continue

        try:
            git_worktree_remove_from(repo, wt_path, force=bool(force))
            removed.append({"id": br, "removed": str(wt_path.resolve())})
        except WorkspaceError as e:
            skipped.append({"id": br, "status": "skip", "reason": str(e)})

    return {"repo_root": str(repo.resolve()), "removed": removed, "skipped": skipped}
