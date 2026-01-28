from __future__ import annotations

import getpass
import os
import platform
from pathlib import Path
from typing import Any

from agent_loom.workspace.constants import INTERNAL_DIR, REPO_INTERNAL_DIR
from agent_loom.workspace.duration import parse_duration_seconds
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.state import fs_escape
from agent_loom.workspace.utils import atomic_write_json, now_iso, read_json


def _owner_default() -> dict[str, Any]:
    return {
        "user": getpass.getuser(),
        "pid": os.getpid(),
        "host": platform.node(),
    }


def repo_worktree_meta_dir(repo_root: Path) -> Path:
    return (repo_root / REPO_INTERNAL_DIR / "worktrees").resolve()


def repo_worktree_meta_path(repo_root: Path, branch: str) -> Path:
    b = str(branch or "").strip()
    if not b:
        raise WorkspaceError("Missing branch")
    return repo_worktree_meta_dir(repo_root) / f"{fs_escape(b)}.json"


def poly_group_meta_dir(ws_root: Path) -> Path:
    return (ws_root / INTERNAL_DIR / "worktrees").resolve()


def poly_group_meta_path(ws_root: Path, group: str) -> Path:
    g = str(group or "").strip()
    if not g:
        raise WorkspaceError("Missing group")
    return poly_group_meta_dir(ws_root) / f"{fs_escape(g)}.json"


def _touch_meta(path: Path) -> dict:
    data: dict
    if path.exists():
        try:
            data = read_json(path)
        except Exception:
            data = {}
    else:
        data = {}

    if not isinstance(data, dict):
        data = {}

    now = now_iso()
    data.setdefault("created_at", now)
    data["updated_at"] = now
    data["last_used_at"] = now
    return data


def repo_worktree_annotate(
    *,
    repo_root: Path,
    branch: str,
    purpose: str,
    ticket_id: str = "",
    owner: str = "",
    ttl: str = "",
    kind: str = "normal",
) -> dict:
    path = repo_worktree_meta_path(repo_root, branch)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = _touch_meta(path)

    data["branch"] = branch
    data["purpose"] = str(purpose or "").strip()
    data["ticket_id"] = str(ticket_id or "").strip()
    data["kind"] = str(kind or "normal").strip() or "normal"

    if owner.strip():
        data["owner"] = str(owner)
    else:
        data.setdefault("owner", _owner_default())

    ttl_s = str(ttl or "").strip()
    if ttl_s:
        data["ttl_seconds"] = parse_duration_seconds(ttl_s)
    else:
        data.pop("ttl_seconds", None)

    atomic_write_json(path, data)
    return {"meta_path": str(path.resolve()), "meta": data}


def poly_group_annotate(
    *,
    ws_root: Path,
    group: str,
    purpose: str,
    ticket_id: str = "",
    owner: str = "",
    ttl: str = "",
    kind: str = "normal",
) -> dict:
    path = poly_group_meta_path(ws_root, group)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = _touch_meta(path)

    data["group"] = group
    data["purpose"] = str(purpose or "").strip()
    data["ticket_id"] = str(ticket_id or "").strip()
    data["kind"] = str(kind or "normal").strip() or "normal"

    if owner.strip():
        data["owner"] = str(owner)
    else:
        data.setdefault("owner", _owner_default())

    ttl_s = str(ttl or "").strip()
    if ttl_s:
        data["ttl_seconds"] = parse_duration_seconds(ttl_s)
    else:
        data.pop("ttl_seconds", None)

    atomic_write_json(path, data)
    return {"meta_path": str(path.resolve()), "meta": data}


def repo_worktree_touch(*, repo_root: Path, branch: str) -> None:
    path = repo_worktree_meta_path(repo_root, branch)
    if not path.exists():
        return
    data = _touch_meta(path)
    atomic_write_json(path, data)


def poly_group_touch(*, ws_root: Path, group: str) -> None:
    path = poly_group_meta_path(ws_root, group)
    if not path.exists():
        return
    data = _touch_meta(path)
    atomic_write_json(path, data)
