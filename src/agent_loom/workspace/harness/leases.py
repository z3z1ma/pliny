from __future__ import annotations

import getpass
import os
import platform
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent_loom.core.fs import fs_escape
from agent_loom.core.io import atomic_write_json, read_json
from agent_loom.core.time import now_iso, parse_duration_seconds, parse_iso_z
from agent_loom.workspace.constants import HARNESS_DIR, INTERNAL_DIR
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.guards import harness_root
from agent_loom.workspace.models import (
    LeaseAcquireResult,
    LeaseListResult,
    LeaseReleaseResult,
    LeaseRenewResult,
    LeaseShowResult,
)


DEFAULT_LEASE_TTL = "8h"


def _ttl_seconds(ttl: str) -> Optional[int]:
    s = str(ttl or "").strip()
    if not s:
        s = DEFAULT_LEASE_TTL
    if s.lower() in {"0", "none", "off", "disable", "disabled", "no"}:
        return None
    try:
        n = int(parse_duration_seconds(s))
    except Exception as e:
        raise WorkspaceError(f"Invalid --ttl: {ttl} ({e})") from e
    if n <= 0:
        return None
    return n


def _epoch(ts: str) -> Optional[float]:
    dt = parse_iso_z(str(ts or ""))
    if dt is None:
        return None
    return float(dt.timestamp())


def lease_is_expired(data: Dict[str, Any], *, now: Optional[float] = None) -> bool:
    ttl = data.get("ttl_seconds")
    if ttl is None:
        return False
    try:
        ttl_s = int(ttl)
    except Exception:
        return False
    if ttl_s <= 0:
        return False

    updated = _epoch(str(data.get("updated_at") or ""))
    if updated is None:
        return False

    n = float(time.time() if now is None else now)
    return (updated + ttl_s) <= n


def _read_active_lease(*, p: Path) -> tuple[bool, Dict[str, Any]]:
    if not p.exists():
        return False, {}
    try:
        data = read_json(p)
    except Exception:
        # If unreadable, treat as active and let callers decide.
        return True, {"error": "unreadable"}
    if not isinstance(data, dict):
        return True, {"error": "invalid"}

    if lease_is_expired(data):
        try:
            p.unlink(missing_ok=True)
        except Exception:
            pass
        return False, {}
    return True, data


def leases_dir(*, root: Path) -> Path:
    return (root / INTERNAL_DIR / HARNESS_DIR / "leases").resolve()


def lease_path(*, root: Path, key: str) -> Path:
    k = str(key or "").strip()
    if not k:
        raise WorkspaceError("Missing lease key")
    return leases_dir(root=root) / f"{fs_escape(k)}.json"


def lease_acquire(
    *,
    key: str,
    ttl: str = "",
    force: bool = False,
    root: Optional[Path] = None,
) -> LeaseAcquireResult:
    ws_root = root.resolve() if root is not None else harness_root()
    p = lease_path(root=ws_root, key=key)
    p.parent.mkdir(parents=True, exist_ok=True)

    active, existing = _read_active_lease(p=p)
    if active and not force:
        raise WorkspaceError(f"Lease already exists: {p} (use --force to steal)")

    ttl_s = _ttl_seconds(ttl)
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
    if ttl_s is not None:
        data["ttl_seconds"] = int(ttl_s)
    elif "ttl_seconds" in existing:
        data["ttl_seconds"] = existing.get("ttl_seconds")

    # Preserve acquired_at if we're force-updating an existing lease file.
    if isinstance(existing, dict) and existing.get("acquired_at"):
        data["acquired_at"] = str(existing.get("acquired_at"))

    atomic_write_json(p, data)
    return LeaseAcquireResult(
        key=key,
        lease_path=str(p.resolve()),
        existed=bool(active),
        forced=bool(force),
        data=data,
    )


def lease_release(*, key: str, root: Optional[Path] = None) -> LeaseReleaseResult:
    ws_root = root.resolve() if root is not None else harness_root()
    p = lease_path(root=ws_root, key=key)
    if not p.exists():
        return LeaseReleaseResult(key=key, lease_path=str(p.resolve()), released=False)
    p.unlink()
    return LeaseReleaseResult(key=key, lease_path=str(p.resolve()), released=True)


def lease_show(*, key: str, root: Optional[Path] = None) -> LeaseShowResult:
    ws_root = root.resolve() if root is not None else harness_root()
    p = lease_path(root=ws_root, key=key)
    active, data = _read_active_lease(p=p)
    exists = p.exists()
    return LeaseShowResult(
        key=key,
        lease_path=str(p.resolve()),
        exists=bool(exists),
        active=bool(active),
        data=data if isinstance(data, dict) else {},
    )


def lease_renew(
    *,
    key: str,
    ttl: str = "",
    root: Optional[Path] = None,
) -> LeaseRenewResult:
    ws_root = root.resolve() if root is not None else harness_root()
    p = lease_path(root=ws_root, key=key)
    active, data = _read_active_lease(p=p)
    if not active:
        raise WorkspaceError(f"Lease not found (or expired): {p}")
    if not isinstance(data, dict):
        raise WorkspaceError(f"Invalid lease data: {p}")

    ttl_s = _ttl_seconds(ttl)
    data["updated_at"] = now_iso()
    if ttl_s is not None:
        data["ttl_seconds"] = int(ttl_s)
    atomic_write_json(p, data)
    return LeaseRenewResult(
        key=key,
        lease_path=str(p.resolve()),
        renewed=True,
        data=data,
    )


def lease_is_active(*, key: str, root: Optional[Path] = None) -> bool:
    ws_root = root.resolve() if root is not None else harness_root()
    p = lease_path(root=ws_root, key=key)
    active, _ = _read_active_lease(p=p)
    return bool(active)


def lease_require_active(*, key: str, root: Optional[Path] = None) -> None:
    if not lease_is_active(key=key, root=root):
        raise WorkspaceError(
            "Missing required lease (or it expired). Acquire it first:\n\n"
            f"  loom workspace harness lease acquire {key}\n"
        )


def lease_list(*, root: Optional[Path] = None) -> LeaseListResult:
    ws_root = root.resolve() if root is not None else harness_root()
    d = leases_dir(root=ws_root)
    if not d.exists():
        return LeaseListResult(leases_dir=str(d.resolve()), leases=[], pruned_expired=0)

    leases: List[Dict[str, Any]] = []
    pruned = 0
    for p in sorted(d.glob("*.json")):
        active, data = _read_active_lease(p=p)
        if not active:
            pruned += 1
            continue
        leases.append({"path": str(p.resolve()), "data": data})

    return LeaseListResult(
        leases_dir=str(d.resolve()), leases=leases, pruned_expired=int(pruned)
    )
