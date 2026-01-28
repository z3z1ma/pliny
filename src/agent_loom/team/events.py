from __future__ import annotations

import datetime as dt
import os
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, Mapping, Optional

from agent_loom.team.constants import (
    ENV_TEAM_ROLE,
    ENV_TEAM_TICKET_ID,
    ENV_TEAM_WORKER_ID,
)
from agent_loom.team.io import _atomic_write_json
from agent_loom.team.run_state import RunPaths
from agent_loom.team.strings import sanitize
from agent_loom.team.time import _iso_z


def best_effort(fn: Callable[[], Any], *, label: str = "") -> Any:
    del label
    try:
        return fn()
    except Exception:
        return None


def _json_safe(x: Any) -> Any:
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    if isinstance(x, dt.datetime):
        return x.isoformat()
    if isinstance(x, Mapping):
        return {str(k): _json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple, set)):
        return [_json_safe(v) for v in x]
    return str(x)


def _event_stamp(ts: str) -> str:
    return str(ts or "").replace(":", "").replace("-", "").replace(".", "")


def event_actor_context() -> Dict[str, Any]:
    role = str(os.getenv(ENV_TEAM_ROLE) or "").strip() or "cli"
    worker_id = sanitize(str(os.getenv(ENV_TEAM_WORKER_ID) or ""), max_len=48)
    ticket_id = str(os.getenv(ENV_TEAM_TICKET_ID) or "").strip()
    pane_id = str(os.environ.get("TMUX_PANE") or "").strip()
    try:
        host = str(getattr(os.uname(), "nodename", "") or "")
    except Exception:
        host = ""
    return {
        "role": role,
        "worker_id": worker_id,
        "ticket_id": ticket_id,
        "pane_id": pane_id,
        "pid": os.getpid(),
        "host": host,
        "cwd": str(Path.cwd().resolve()),
    }


def write_event(
    paths: RunPaths,
    *,
    event_type: str,
    run: Optional[Mapping[str, Any]] = None,
    ok: bool = True,
    summary: str = "",
    refs: Optional[Mapping[str, Any]] = None,
    data: Optional[Mapping[str, Any]] = None,
    error: Optional[Mapping[str, str]] = None,
    op_id: str = "",
    parent_op_id: str = "",
) -> Dict[str, Any]:
    ts = _iso_z()
    eid = uuid.uuid4().hex[:12]
    et = sanitize(str(event_type or ""), allow=r"a-zA-Z0-9._-", max_len=80) or "event"

    actor = event_actor_context()
    payload: Dict[str, Any] = {
        "v": 1,
        "id": eid,
        "ts": ts,
        "type": et,
        "run": {
            "team": str((run or {}).get("team") or paths.team),
            "run_id": str((run or {}).get("run_id") or ""),
            "session": str((run or {}).get("session") or ""),
        },
        "actor": actor,
        "refs": dict(refs or {}),
        "op": {"op_id": str(op_id or ""), "parent_op_id": str(parent_op_id or "")},
        "ok": bool(ok),
        "error": dict(error or {}),
        "summary": str(summary or ""),
        "data": dict(data or {}),
    }

    payload = _json_safe(payload)

    paths.events_dir.mkdir(parents=True, exist_ok=True)
    fname = f"{_event_stamp(ts)}_{eid}_{et}.json"
    _atomic_write_json(paths.events_dir / fname, payload)
    return payload


def safe_write_event(paths: RunPaths, **kwargs: Any) -> None:
    et = str(kwargs.get("event_type") or "")
    best_effort(lambda: write_event(paths, **kwargs), label=f"write_event:{et}")


__all__ = [
    "_event_stamp",
    "_json_safe",
    "best_effort",
    "event_actor_context",
    "safe_write_event",
    "write_event",
]
