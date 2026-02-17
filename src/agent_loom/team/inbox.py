from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

from agent_loom.team.channels import channel_for
from agent_loom.team.errors import TeamError
from agent_loom.team.events import best_effort, safe_write_event
from agent_loom.team.io import _atomic_write_json, _read_json
from agent_loom.team.run_state import RunPaths, load_run
from agent_loom.team.strings import message_preview
from agent_loom.team.targets import _best_effort_tmux_nudge, _resolve_target
from agent_loom.team.time import _iso_z
from agent_loom.team.tmux import tmux_signal


def _sprint_info(run: Mapping[str, Any]) -> Dict[str, Any]:
    s = run.get("sprint")
    if not isinstance(s, dict):
        return {}
    name = str(s.get("name") or "").strip()
    if not name:
        return {}
    out: Dict[str, Any] = {"name": name}
    slug = str(s.get("slug") or "").strip()
    tag = str(s.get("tag") or "").strip()
    rev = s.get("rev")
    started_at = str(s.get("started_at") or "").strip()
    if slug:
        out["slug"] = slug
    if tag:
        out["tag"] = tag
    if isinstance(rev, int):
        out["rev"] = rev
    if started_at:
        out["started_at"] = started_at
    return out


def _prefix_message_with_sprint(run: Mapping[str, Any], message: str) -> str:
    msg = str(message or "")
    if not msg:
        return msg
    if msg.startswith("[Sprint:"):
        return msg
    s = _sprint_info(run)
    name = str(s.get("name") or "").strip()
    if not name:
        return msg
    return f"[Sprint: {name}] {msg}"


def _inbox_msg_path(paths: RunPaths, msg_id: str) -> Optional[Path]:
    inbox = paths.inbox_dir
    read_dir = paths.inbox_read_dir
    matches: List[Path] = []
    if inbox.exists():
        matches.extend(list(inbox.glob(f"*_{msg_id}.json")))
    if read_dir.exists():
        matches.extend(list(read_dir.glob(f"*_{msg_id}.json")))
    if not matches:
        return None
    return sorted(matches, key=lambda p: p.name)[-1]


def inbox_write_message(
    paths: RunPaths,
    *,
    to: str,
    message: str,
    sender: str = "team",
    kind: str = "note",
    meta: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    paths.inbox_dir.mkdir(parents=True, exist_ok=True)
    msg_id = uuid.uuid4().hex[:12]
    created_at = _iso_z()
    stamp = created_at.replace(":", "").replace("-", "").replace(".", "")
    fname = f"{stamp}_{msg_id}.json"
    payload: Dict[str, Any] = {
        "id": msg_id,
        "created_at": created_at,
        "from": str(sender or "team"),
        "to": str(to or ""),
        "kind": str(kind or "note"),
        "message": str(message or ""),
        "meta": dict(meta or {}),
        "acked_at": "",
    }
    _atomic_write_json(paths.inbox_dir / fname, payload)

    run0 = best_effort(lambda: load_run(paths), label="inbox.wrote.load_run")
    run = run0 if isinstance(run0, dict) else None
    safe_write_event(
        paths,
        event_type="inbox.wrote",
        run=run,
        summary=f"Inbox wrote kind={payload.get('kind')} to={payload.get('to')} id={msg_id}",
        refs={
            "inbox_id": msg_id,
            "to": str(payload.get("to") or ""),
            "kind": str(payload.get("kind") or ""),
        },
        data={
            "from": str(payload.get("from") or ""),
            "bytes": len(str(payload.get("message") or "").encode("utf-8")),
            "meta": dict(payload.get("meta") or {}),
        },
    )
    return payload


def inbox_list_messages(
    paths: RunPaths,
    *,
    to: Optional[str] = None,
    unacked_only: bool = False,
    limit: int = 200,
) -> List[Dict[str, Any]]:
    inbox = paths.inbox_dir
    read_dir = paths.inbox_read_dir
    files: List[Path] = []
    if inbox.exists():
        files.extend([p for p in inbox.glob("*.json") if p.is_file()])
    if read_dir.exists():
        files.extend([p for p in read_dir.glob("*.json") if p.is_file()])
    if not files:
        return []
    files = sorted(files, key=lambda p: p.name, reverse=True)
    out: List[Dict[str, Any]] = []
    for fp in files:
        try:
            msg = _read_json(fp)
        except Exception:
            continue
        if not isinstance(msg, dict):
            continue
        if to and str(msg.get("to") or "").strip() != to:
            continue
        if unacked_only and str(msg.get("acked_at") or "").strip():
            continue
        out.append(msg)
        if len(out) >= int(limit):
            break
    return out


def inbox_ack_message(paths: RunPaths, msg_id: str) -> Dict[str, Any]:
    p = _inbox_msg_path(paths, msg_id)
    if not p or not p.exists():
        raise TeamError(f"inbox message not found: {msg_id}", code="ARG", exit_code=2)
    msg = _read_json(p)
    if not isinstance(msg, dict):
        raise TeamError(f"invalid inbox message: {p}", code="BAD_STATE", exit_code=2)
    if not str(msg.get("acked_at") or "").strip():
        msg["acked_at"] = _iso_z()
        _atomic_write_json(p, msg)

    try:
        if p.parent == paths.inbox_dir:
            paths.inbox_read_dir.mkdir(parents=True, exist_ok=True)
            os.replace(p, paths.inbox_read_dir / p.name)
    except Exception:
        pass
    return msg


def _inbox_unacked(paths: RunPaths, inbox_id: str) -> bool:
    mid = str(inbox_id or "").strip()
    if not mid:
        return False
    p = _inbox_msg_path(paths, mid)
    if not p or not p.exists():
        return False
    try:
        msg = _read_json(p)
    except Exception:
        return False
    if not isinstance(msg, dict):
        return False
    return not bool(str(msg.get("acked_at") or "").strip())


def _inbox_recipient_for_target(run: Mapping[str, Any], target: str) -> str:
    t = str(target or "").strip()
    if not t:
        return ""
    tnorm = t.lower()
    if tnorm in ("manager", "mgr"):
        return "manager"
    if tnorm in {"architect", "integrator"}:
        return tnorm
    if tnorm.startswith("worker:"):
        return str(tnorm.split(":", 1)[1] or "").strip().lower()
    try:
        _pane_id0, meta0 = _resolve_target(run, t)
        wid = str(meta0.get("worker_id") or "").strip()
        return wid or t
    except Exception:
        return tnorm


def _inbox_write_and_maybe_nudge(
    *,
    paths: RunPaths,
    run: Mapping[str, Any],
    target: str,
    message: str,
    sender: str,
    kind: str,
    meta_extra: Optional[Mapping[str, Any]] = None,
    nudge: bool = True,
    force: bool = False,
    line_info: str = "",
) -> Tuple[Dict[str, Any], str, bool, str, Dict[str, Any]]:
    run_id = str(run.get("run_id") or "")
    session = str(run.get("session") or "")

    message = _prefix_message_with_sprint(run, message)
    sprint = _sprint_info(run)

    recipient = _inbox_recipient_for_target(run, target)
    meta: Dict[str, Any] = {
        "run_id": run_id,
        "target": target,
        "recipient": recipient,
        **({"sprint": sprint} if sprint else {}),
        **dict(meta_extra or {}),
    }

    inbox_msg = inbox_write_message(
        paths,
        to=recipient,
        message=message,
        sender=sender,
        kind=kind,
        meta=meta,
    )

    tmux_signal(channel_for(run_id=run_id, to=recipient))

    delivered = False
    delivery_reason = ""
    tmux_meta: Dict[str, Any] = {"target": target}
    if nudge:
        preview = message_preview(message, max_len=100)
        info = str(line_info or "").strip()
        extra = f" {info}" if info else ""
        line = f"TEAM inbox id={inbox_msg.get('id', '')}{extra} | {preview} (run {run_id[:8]})"
        delivered, delivery_reason, tmux_meta = _best_effort_tmux_nudge(
            run=run,
            session=session,
            target=target,
            line=line,
            force=force,
        )

    return inbox_msg, recipient, delivered, delivery_reason, tmux_meta


__all__ = [
    "_inbox_msg_path",
    "_inbox_unacked",
    "_inbox_write_and_maybe_nudge",
    "inbox_ack_message",
    "inbox_list_messages",
    "inbox_write_message",
]
