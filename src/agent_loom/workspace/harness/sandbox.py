from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.guards import harness_root
from agent_loom.workspace.harness.core import worktree_rm, worktree_add
from agent_loom.core.io import atomic_write_json, read_json
from agent_loom.workspace.lifecycle import meta_is_expired
from agent_loom.workspace.harness.leases import lease_is_active, lease_path
from agent_loom.workspace.worktree_meta import (
    harness_group_annotate,
    harness_group_meta_dir,
    harness_group_meta_path,
)


def harness_sandbox_create(
    *,
    group: str,
    base_ref: str,
    ttl: str = "2h",
    purpose: str = "sandbox",
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
    clone: bool = False,
    root: Optional[Path] = None,
) -> dict:
    ws_root = root.resolve() if root is not None else harness_root()
    wt = worktree_add(
        group=group,
        base_ref=base_ref,
        clone=bool(clone),
        allow_dirty=False,
        repos=repos,
        sets=sets,
        tags=tags,
        allow_all=bool(allow_all),
        root=ws_root,
    )
    meta = harness_group_annotate(
        ws_root=ws_root,
        group=group,
        purpose=purpose,
        ttl=ttl,
        kind="sandbox",
    )
    return {"group": group, "created": wt.worktrees, **meta}


def harness_sandbox_promote(*, group: str, root: Optional[Path] = None) -> dict:
    ws_root = root.resolve() if root is not None else harness_root()
    p = harness_group_meta_path(ws_root, group)
    if not p.exists():
        raise WorkspaceError(f"Missing group metadata: {p}")
    data = read_json(p)
    if not isinstance(data, dict):
        raise WorkspaceError(f"Invalid group metadata: {p}")
    data["kind"] = "normal"
    data.pop("ttl_seconds", None)
    atomic_write_json(p, data)
    try:
        from agent_loom.workspace.worktree_meta import harness_group_touch

        harness_group_touch(ws_root=ws_root, group=group)
    except Exception:
        pass
    return {"group": group, "promoted": True, "meta_path": str(p.resolve())}


def harness_sandbox_gc(
    *,
    confirm: bool,
    force: bool = False,
    root: Optional[Path] = None,
) -> dict:
    if not confirm:
        raise WorkspaceError("Refusing to gc sandboxes without --yes")

    ws_root = root.resolve() if root is not None else harness_root()
    d = harness_group_meta_dir(ws_root)
    if not d.exists():
        return {"removed": [], "skipped": []}

    now = time.time()
    expired_groups: List[str] = []
    for p in sorted(d.glob("*.json")):
        try:
            meta = read_json(p)
        except Exception:
            continue
        if not isinstance(meta, dict):
            continue
        if str(meta.get("kind") or "") != "sandbox":
            continue
        g = str(meta.get("group") or "").strip()
        if not g:
            continue
        if meta_is_expired(meta, now=now):
            expired_groups.append(g)

    removed: List[str] = []
    skipped: List[Dict[str, Any]] = []
    for g in sorted(set(expired_groups)):
        key = f"group:{g}"
        lease = lease_path(root=ws_root, key=key)
        if lease_is_active(key=key, root=ws_root):
            skipped.append(
                {
                    "group": g,
                    "reason": "leased",
                    "lease_path": str(lease.resolve()),
                }
            )
            continue
        try:
            res = worktree_rm(
                group=g,
                allow_all=True,
                force=bool(force),
                confirm=True,
                root=ws_root,
            )
            removed.extend(res.removed)
        except WorkspaceError as e:
            skipped.append({"group": g, "reason": str(e)})

    return {"removed": removed, "skipped": skipped}
