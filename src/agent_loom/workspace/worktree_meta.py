from __future__ import annotations

import getpass
import os
import platform
from pathlib import Path
from typing import Any

from agent_loom.core.io import atomic_write_json, read_json
from agent_loom.core.fs import fs_escape
from agent_loom.core.time import now_iso, parse_duration_seconds
from agent_loom.workspace.constants import INTERNAL_DIR, REPO_INTERNAL_DIR
from agent_loom.workspace.errors import WorkspaceError


def _parse_ttl_seconds(ttl_s: str) -> int:
    try:
        return parse_duration_seconds(ttl_s)
    except ValueError as e:
        raise WorkspaceError(
            "Invalid duration. Use <N>[s|m|h|d|w], for example: 30m, 2h, 7d."
        ) from e


def _owner_default() -> dict[str, Any]:
    return {
        "user": getpass.getuser(),
        "pid": os.getpid(),
        "host": platform.node(),
    }


def _migrate_meta_files(*, old_dir: Path, new_dir: Path) -> None:
    if not old_dir.exists() or not old_dir.is_dir():
        return
    new_dir.mkdir(parents=True, exist_ok=True)
    for p in sorted(old_dir.glob("*.json")):
        try:
            dst = new_dir / p.name
            if dst.exists():
                continue
            p.replace(dst)
        except Exception:
            continue


def repo_worktree_meta_dir(repo_root: Path) -> Path:
    # v2: keep metadata separate from worktree directories.
    new = (repo_root / REPO_INTERNAL_DIR / "meta" / "worktrees").resolve()
    old = (repo_root / REPO_INTERNAL_DIR / "worktrees").resolve()
    _migrate_meta_files(old_dir=old, new_dir=new)
    return new


def repo_worktree_meta_path(repo_root: Path, branch: str) -> Path:
    b = str(branch or "").strip()
    if not b:
        raise WorkspaceError("Missing branch")
    new = repo_worktree_meta_dir(repo_root) / f"{fs_escape(b)}.json"
    old = (
        repo_root / REPO_INTERNAL_DIR / "worktrees" / f"{fs_escape(b)}.json"
    ).resolve()
    if (not new.exists()) and old.exists():
        try:
            new.parent.mkdir(parents=True, exist_ok=True)
            old.replace(new)
        except Exception:
            pass
    return new


def poly_group_meta_dir(ws_root: Path) -> Path:
    # v2: keep metadata under .loom/meta.
    new = (ws_root / INTERNAL_DIR / "meta" / "groups").resolve()
    old = (ws_root / INTERNAL_DIR / "worktrees").resolve()
    _migrate_meta_files(old_dir=old, new_dir=new)
    return new


def poly_group_meta_path(ws_root: Path, group: str) -> Path:
    g = str(group or "").strip()
    if not g:
        raise WorkspaceError("Missing group")
    new = poly_group_meta_dir(ws_root) / f"{fs_escape(g)}.json"
    old = (ws_root / INTERNAL_DIR / "worktrees" / f"{fs_escape(g)}.json").resolve()
    if (not new.exists()) and old.exists():
        try:
            new.parent.mkdir(parents=True, exist_ok=True)
            old.replace(new)
        except Exception:
            pass
    return new


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
        data["ttl_seconds"] = _parse_ttl_seconds(ttl_s)
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
        data["ttl_seconds"] = _parse_ttl_seconds(ttl_s)
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


def poly_group_set_worktrees_base(*, ws_root: Path, group: str, base_path: str) -> dict:
    g = str(group or "").strip()
    if not g:
        raise WorkspaceError("Missing group")

    raw = str(base_path or "").strip()
    if not raw:
        raise WorkspaceError("Missing base_path")

    p = Path(raw).expanduser()
    if not p.is_absolute():
        p = (ws_root / p).resolve()
    else:
        p = p.resolve()

    meta_path = poly_group_meta_path(ws_root, g)
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    data = _touch_meta(meta_path)
    data["group"] = g
    data["worktrees_base_path"] = str(p)
    atomic_write_json(meta_path, data)
    return {"meta_path": str(meta_path.resolve()), "meta": data}
