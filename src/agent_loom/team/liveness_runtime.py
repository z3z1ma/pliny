from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Mapping

from agent_loom.team.health import health_state as _health_state
from agent_loom.team.io import _read_json
from agent_loom.team.run_state import RunPaths
from agent_loom.team.strings import sanitize
from agent_loom.team.tmux import (
    _pane_can_receive_chat,
    tmux_has_session,
    tmux_list_panes,
)


def _sidecar_pid_file(paths: RunPaths, recipient: str) -> Path:
    safe = (
        sanitize(str(recipient or ""), allow=r"a-zA-Z0-9._-", max_len=48) or "unknown"
    )
    return paths.sidecars_dir / f"{safe}.pid.json"


def _pid_exists(pid: int) -> bool:
    if int(pid or 0) <= 0:
        return False
    try:
        os.kill(int(pid), 0)
    except Exception:
        return False
    return True


def _sidecar_pid_alive(
    *,
    paths: RunPaths,
    run: Mapping[str, Any],
    recipient: str,
    pane_id: str,
) -> tuple[bool, Dict[str, Any], str]:
    pid_file = _sidecar_pid_file(paths, recipient)
    if not pid_file.exists():
        return False, {}, "pidfile_missing"
    try:
        payload = _read_json(pid_file)
    except Exception:
        return False, {}, "pidfile_unreadable"
    if not isinstance(payload, dict):
        return False, {}, "pidfile_invalid"

    run_id = str(run.get("run_id") or "").strip()
    pid_run_id = str(payload.get("run_id") or "").strip()
    if run_id and pid_run_id and pid_run_id != run_id:
        return False, dict(payload), "run_mismatch"

    expected_pane = str(payload.get("pane_id") or "").strip()
    target_pane = str(pane_id or "").strip()
    if target_pane and expected_pane and expected_pane != target_pane:
        return False, dict(payload), "pane_mismatch"

    raw_pid = str(payload.get("pid") or "").strip()
    try:
        pid = int(raw_pid)
    except Exception:
        return False, dict(payload), "pid_invalid"
    if pid <= 0:
        return False, dict(payload), "pid_invalid"
    if not _pid_exists(pid):
        return False, dict(payload), "pid_missing"

    return True, dict(payload), ""


def _effective_recipient_health(
    *,
    paths: RunPaths,
    run: Mapping[str, Any],
    recipient: str,
    pane_id: str,
    pane: Mapping[str, str] | None,
) -> tuple[bool, str, Dict[str, Any]]:
    heartbeat_state, heartbeat = _health_state(
        paths=paths,
        run=run,
        recipient=recipient,
    )
    pane_info = dict(pane or {})
    pane_ok = bool(pane_info and _pane_can_receive_chat(pane_info))
    state = heartbeat_state
    source = "heartbeat"
    sidecar_probe = ""
    sidecar_payload: Dict[str, Any] = {}

    if pane_ok and heartbeat_state != "alive":
        sidecar_alive, sidecar_payload, sidecar_probe = _sidecar_pid_alive(
            paths=paths,
            run=run,
            recipient=recipient,
            pane_id=str(pane_id or ""),
        )
        if sidecar_alive:
            state = "alive"
            source = "sidecar_pid"

    if not pane_ok and state == "alive":
        state = "stale"
        source = "pane_unsafe"

    enriched = dict(heartbeat or {})
    enriched["state"] = state
    enriched["heartbeat_state"] = heartbeat_state
    enriched["state_source"] = source
    if source == "sidecar_pid":
        enriched["sidecar"] = {
            "pid": int(sidecar_payload.get("pid") or 0),
            "pane_id": str(sidecar_payload.get("pane_id") or ""),
            "started_at": str(sidecar_payload.get("started_at") or ""),
            "agent_bin": str(sidecar_payload.get("agent_bin") or ""),
        }
    elif pane_ok and heartbeat_state != "alive" and sidecar_probe:
        enriched["sidecar_probe"] = sidecar_probe

    return bool(state == "alive" and pane_ok), state, enriched


def _recipient_health(
    *,
    paths: RunPaths,
    run: Mapping[str, Any],
    session: str,
    recipient: str,
    pane_id: str,
) -> tuple[str, Dict[str, Any], Dict[str, str]]:
    panes = tmux_list_panes(session) if session and tmux_has_session(session) else {}
    pane = panes.get(str(pane_id or "").strip(), {})
    _alive, state, health = _effective_recipient_health(
        paths=paths,
        run=run,
        recipient=recipient,
        pane_id=pane_id,
        pane=pane,
    )
    return state, dict(health or {}), dict(pane or {})


__all__ = [
    "_effective_recipient_health",
    "_recipient_health",
    "_sidecar_pid_file",
]
