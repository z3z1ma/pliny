from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.guards import workspace_root
from agent_loom.workspace.poly_ops import worktree_rm, worktree_add
from agent_loom.workspace.time_utils import parse_iso_z
from agent_loom.workspace.utils import atomic_write_json, read_json
from agent_loom.workspace.worktree_meta import (
    poly_group_annotate,
    poly_group_meta_dir,
    poly_group_meta_path,
)


def poly_sandbox_create(
    *,
    group: str,
    base_ref: str,
    ttl: str = "2h",
    purpose: str = "sandbox",
    claim: bool = False,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
    clone: bool = False,
    root: Optional[Path] = None,
) -> dict:
    ws_root = root.resolve() if root is not None else workspace_root()
    wt = worktree_add(
        group=group,
        base_ref=base_ref,
        claim=bool(claim),
        clone=bool(clone),
        allow_dirty=False,
        repos=repos,
        sets=sets,
        tags=tags,
        allow_all=bool(allow_all),
        root=ws_root,
    )
    meta = poly_group_annotate(
        ws_root=ws_root,
        group=group,
        purpose=purpose,
        ttl=ttl,
        kind="sandbox",
    )
    return {"group": group, "created": wt.worktrees, **meta}


def poly_sandbox_promote(*, group: str, root: Optional[Path] = None) -> dict:
    ws_root = root.resolve() if root is not None else workspace_root()
    p = poly_group_meta_path(ws_root, group)
    if not p.exists():
        raise WorkspaceError(f"Missing group metadata: {p}")
    data = read_json(p)
    if not isinstance(data, dict):
        raise WorkspaceError(f"Invalid group metadata: {p}")
    data["kind"] = "normal"
    data.pop("ttl_seconds", None)
    atomic_write_json(p, data)
    return {"group": group, "promoted": True, "meta_path": str(p.resolve())}


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


def poly_sandbox_gc(
    *,
    confirm: bool,
    force: bool = False,
    root: Optional[Path] = None,
) -> dict:
    if not confirm:
        raise WorkspaceError("Refusing to gc sandboxes without --yes")

    ws_root = root.resolve() if root is not None else workspace_root()
    d = poly_group_meta_dir(ws_root)
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
        if _expired(meta, now):
            expired_groups.append(g)

    removed: List[str] = []
    skipped: List[Dict[str, Any]] = []
    for g in sorted(set(expired_groups)):
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
