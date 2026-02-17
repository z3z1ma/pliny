from __future__ import annotations

import datetime as dt
import time
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

from agent_loom.team.io import _atomic_write_json, _read_json
from agent_loom.team.run_state import RunPaths
from agent_loom.team.strings import sanitize
from agent_loom.team.team_config import liveness_from_run
from agent_loom.team.time import _iso_z


def recipient_key(recipient: str) -> str:
    return (
        sanitize(str(recipient or "").strip().lower(), allow=r"a-z0-9._-", max_len=48)
        or "unknown"
    )


def health_file(paths: RunPaths, recipient: str) -> Path:
    return paths.health_dir / f"{recipient_key(recipient)}.json"


def write_heartbeat(
    *,
    paths: RunPaths,
    recipient: str,
    role: str,
    pane_id: str,
    pid: int,
    current_command: str,
) -> Dict[str, Any]:
    payload = {
        "recipient": recipient_key(recipient),
        "role": str(role or "").strip().lower(),
        "pane_id": str(pane_id or "").strip(),
        "pid": int(pid),
        "last_seen_at": _iso_z(),
        "current_command": str(current_command or "").strip(),
    }
    paths.health_dir.mkdir(parents=True, exist_ok=True)
    _atomic_write_json(health_file(paths, recipient), payload)
    return payload


def clear_heartbeat(*, paths: RunPaths, recipient: str) -> None:
    try:
        health_file(paths, recipient).unlink()
    except FileNotFoundError:
        return
    except Exception:
        return


def read_heartbeat(paths: RunPaths, recipient: str) -> Dict[str, Any]:
    p = health_file(paths, recipient)
    if not p.exists():
        return {}
    try:
        payload = _read_json(p)
    except Exception:
        return {}
    return dict(payload) if isinstance(payload, dict) else {}


def _parse_iso_z(value: str) -> float:
    text = str(value or "").strip()
    if not text:
        return 0.0
    try:
        if text.endswith("Z"):
            return dt.datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp()
        return dt.datetime.fromisoformat(text).timestamp()
    except Exception:
        return 0.0


def health_state(
    *,
    paths: RunPaths,
    run: Mapping[str, Any],
    recipient: str,
    now_ts: float | None = None,
) -> Tuple[str, Dict[str, Any]]:
    payload = read_heartbeat(paths, recipient)
    if not payload:
        return "missing", {}

    liveness = liveness_from_run(run)
    now = float(now_ts) if now_ts is not None else time.time()
    ts = _parse_iso_z(str(payload.get("last_seen_at") or ""))
    if ts <= 0:
        return "missing", payload

    age_s = max(0.0, now - ts)
    enriched = dict(payload)
    enriched["age_s"] = age_s
    if age_s <= float(liveness["stale_after_s"]):
        return "alive", enriched
    if age_s <= float(liveness["dead_after_s"]):
        return "stale", enriched
    return "dead", enriched


__all__ = [
    "clear_heartbeat",
    "health_file",
    "health_state",
    "read_heartbeat",
    "recipient_key",
    "write_heartbeat",
]
