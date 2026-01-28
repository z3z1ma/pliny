from __future__ import annotations

import getpass
import os
import platform
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent_loom.workspace.constants import INTERNAL_DIR
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.guards import workspace_root
from agent_loom.workspace.models import (
    LeaseAcquireResult,
    LeaseListResult,
    LeaseReleaseResult,
)
from agent_loom.workspace.state import fs_escape
from agent_loom.workspace.utils import atomic_write_json, now_iso, read_json


def leases_dir(*, root: Path) -> Path:
    return (root / INTERNAL_DIR / "leases").resolve()


def lease_path(*, root: Path, key: str) -> Path:
    k = str(key or "").strip()
    if not k:
        raise WorkspaceError("Missing lease key")
    return leases_dir(root=root) / f"{fs_escape(k)}.json"


def lease_acquire(
    *,
    key: str,
    force: bool = False,
    root: Optional[Path] = None,
) -> LeaseAcquireResult:
    ws_root = root.resolve() if root is not None else workspace_root()
    p = lease_path(root=ws_root, key=key)
    p.parent.mkdir(parents=True, exist_ok=True)

    existed = p.exists()
    if existed and not force:
        raise WorkspaceError(f"Lease already exists: {p} (use --force to steal)")

    data: Dict[str, Any] = {
        "key": key,
        "owner": {
            "user": getpass.getuser(),
            "pid": os.getpid(),
            "host": platform.node(),
        },
        "acquired_at": now_iso(),
        "updated_at": now_iso(),
    }
    atomic_write_json(p, data)
    return LeaseAcquireResult(
        key=key,
        lease_path=str(p.resolve()),
        existed=bool(existed),
        forced=bool(force),
        data=data,
    )


def lease_release(*, key: str, root: Optional[Path] = None) -> LeaseReleaseResult:
    ws_root = root.resolve() if root is not None else workspace_root()
    p = lease_path(root=ws_root, key=key)
    if not p.exists():
        return LeaseReleaseResult(key=key, lease_path=str(p.resolve()), released=False)
    p.unlink()
    return LeaseReleaseResult(key=key, lease_path=str(p.resolve()), released=True)


def lease_list(*, root: Optional[Path] = None) -> LeaseListResult:
    ws_root = root.resolve() if root is not None else workspace_root()
    d = leases_dir(root=ws_root)
    if not d.exists():
        return LeaseListResult(leases_dir=str(d.resolve()), leases=[])

    leases: List[Dict[str, Any]] = []
    for p in sorted(d.glob("*.json")):
        try:
            data = read_json(p)
        except Exception:
            data = {"error": "unreadable"}
        leases.append({"path": str(p.resolve()), "data": data})

    return LeaseListResult(leases_dir=str(d.resolve()), leases=leases)
