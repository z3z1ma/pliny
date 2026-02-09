from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from agent_loom.core.io import read_json
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.guards import harness_root
from agent_loom.workspace.lifecycle import meta_is_expired
from agent_loom.workspace.harness.leases import lease_is_active, lease_path
from agent_loom.workspace.harness.core import worktree_rm
from agent_loom.workspace.state import load_workspace, worktrees_base
from agent_loom.workspace.worktree_meta import (
    harness_group_meta_dir,
    harness_group_meta_path,
)


def harness_cleanup_suggest(*, root: Optional[Path] = None) -> dict:
    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)

    meta_dir = harness_group_meta_dir(ws_root)
    if not meta_dir.exists():
        return {"workspace_root": str(ws_root), "candidates": []}

    now = time.time()
    candidates: List[Dict[str, Any]] = []
    for p in sorted(meta_dir.glob("*.json")):
        try:
            meta = read_json(p)
        except Exception:
            continue
        if not isinstance(meta, dict):
            continue

        group = str(meta.get("group") or "").strip()
        if not group:
            continue
        if not meta_is_expired(meta, now=now):
            continue

        lease = lease_path(root=ws_root, key=f"group:{group}")
        base = worktrees_base(ws_root, ws, group)
        is_leased = bool(lease_is_active(key=f"group:{group}", root=ws_root))
        candidates.append(
            {
                "id": group,
                "group": group,
                "reason": "ttl_expired",
                "leased": is_leased,
                "lease_path": str(lease.resolve()) if is_leased else "",
                "meta_path": str(p.resolve()),
                "worktrees_dir": str(base.resolve()),
            }
        )

    return {"workspace_root": str(ws_root), "candidates": candidates}


def harness_cleanup_apply(
    *,
    ids: Sequence[str],
    confirm: bool,
    force: bool = False,
    root: Optional[Path] = None,
) -> dict:
    if not confirm:
        raise WorkspaceError("Refusing to apply cleanup without --yes")

    ws_root = root.resolve() if root is not None else harness_root()
    ws = load_workspace(ws_root)

    group_set = {str(x).strip() for x in (ids or []) if str(x).strip()}
    if not group_set:
        raise WorkspaceError("Missing cleanup ids")

    removed: List[Dict[str, Any]] = []
    skipped: List[Dict[str, Any]] = []

    for group in sorted(group_set):
        lease = lease_path(root=ws_root, key=f"group:{group}")
        if lease_is_active(key=f"group:{group}", root=ws_root):
            skipped.append(
                {
                    "id": group,
                    "status": "skip",
                    "reason": "leased",
                    "lease_path": str(lease.resolve()),
                }
            )
            continue

        base = worktrees_base(ws_root, ws, group)
        if not base.exists():
            # No worktrees left; still delete metadata.
            try:
                harness_group_meta_path(ws_root, group).unlink(missing_ok=True)
            except Exception:
                pass
            removed.append({"id": group, "removed": ""})
            continue

        try:
            res = worktree_rm(
                group=group,
                allow_all=True,
                force=bool(force),
                confirm=True,
                root=ws_root,
            )

            # Best-effort: ensure group-level artifacts are removed.
            try:
                if base.exists() and not any(p.is_dir() for p in base.iterdir()):
                    base.rmdir()
            except Exception:
                pass
            try:
                harness_group_meta_path(ws_root, group).unlink(missing_ok=True)
            except Exception:
                pass

            removed.append({"id": group, "removed": res.removed})
        except WorkspaceError as e:
            skipped.append({"id": group, "status": "skip", "reason": str(e)})

    return {"workspace_root": str(ws_root), "removed": removed, "skipped": skipped}
