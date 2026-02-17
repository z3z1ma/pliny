from __future__ import annotations

import shutil
import subprocess
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence

from agent_loom.team.constants import (
    ROLE_MANAGER,
    TMUX_OPT_ROLE,
    TMUX_OPT_TICKET_ID,
    TMUX_OPT_WORKER_ID,
)
from agent_loom.team.errors import TeamError
from agent_loom.team.exec import _require_bin, _run
from agent_loom.team.strings import sanitize


def tmux_available() -> bool:
    return shutil.which("tmux") is not None


def tmux_cmd(
    args: Sequence[str], *, check: bool = True, timeout: Optional[float] = 10.0
) -> subprocess.CompletedProcess[str]:
    _require_bin("tmux")
    return _run(["tmux", *args], check=check, timeout=timeout)


def tmux_wait_for(channel: str, *, timeout_s: Optional[float] = None) -> bool:
    if not channel:
        return False
    try:
        p = subprocess.run(
            ["tmux", "wait-for", channel],
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_s,
        )
        return p.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def tmux_signal(channel: str) -> None:
    if not channel:
        return
    try:
        tmux_cmd(["wait-for", "-S", channel], check=False, timeout=2.0)
    except Exception:
        return


def tmux_has_session(session: str) -> bool:
    if not session:
        return False
    p = tmux_cmd(["has-session", "-t", session], check=False)
    return p.returncode == 0


def tmux_format(target: str, fmt: str) -> str:
    p = tmux_cmd(["display-message", "-p", "-t", target, fmt], check=True, timeout=5.0)
    return (p.stdout or "").strip()


def tmux_set_option(
    *, target: str, option: str, value: str, pane: bool = False
) -> None:
    args = ["set-option", "-t", target]
    if pane:
        args.append("-p")
    args += [option, value]
    tmux_cmd(args, check=False)


def tmux_get_option(*, target: str, option: str, pane: bool = False) -> str:
    args = ["show-option", "-v", "-t", target]
    if pane:
        args.append("-p")
    args.append(option)
    p = tmux_cmd(args, check=False)
    return (p.stdout or "").strip()


def tmux_list_panes(session: str) -> Dict[str, Dict[str, str]]:
    fmt = "\t".join(
        [
            "#{pane_id}",
            "#{session_name}",
            "#{window_name}",
            "#{window_id}",
            "#{pane_dead}",
            "#{pane_pid}",
            "#{pane_start_path}",
            "#{pane_current_path}",
            "#{pane_title}",
            "#{pane_active}",
            "#{pane_start_command}",
            "#{pane_current_command}",
            "#{pane_synchronized}",
            "#{pane_last_activity}",
            "#{pane_id} #{pane_title}",
            "#{pane_id} #{pane_current_command}",
        ]
    )
    p = tmux_cmd(["list-panes", "-a", "-t", session, "-F", fmt], check=False)
    if p.returncode != 0:
        return {}

    panes: Dict[str, Dict[str, str]] = {}
    for line in (p.stdout or "").splitlines():
        parts = line.split("\t")
        if len(parts) < 16:
            continue
        pane_id = parts[0]
        panes[pane_id] = {
            "pane_id": pane_id,
            "session_name": parts[1],
            "window_name": parts[2],
            "window_id": parts[3],
            "dead": parts[4],
            "pid": parts[5],
            "start_path": parts[6],
            "path": parts[7],
            "title": parts[8],
            "active": parts[9],
            "start_command": parts[10],
            "current_command": parts[11],
            "synchronized": parts[12],
            "last_activity": parts[13],
            "title_raw": parts[14],
            "cmd_raw": parts[15],
        }
    return panes


def tmux_capture(pane_id: str, *, lines: int = 200, join_wrapped: bool = True) -> str:
    args = ["capture-pane", "-p", "-t", pane_id, "-S", f"-{int(lines)}"]
    if join_wrapped:
        args.append("-J")
    p = tmux_cmd(args, check=True)
    return p.stdout or ""


def tmux_send_text(
    pane_id: str, text: str, *, enter: bool = True, ctrl_enter: bool = False
) -> None:
    lines = (text or "").splitlines() or [""]
    for line in lines:
        tmux_cmd(["send-keys", "-t", pane_id, "-l", line], check=True)
        if enter:
            tmux_cmd(
                ["send-keys", "-t", pane_id, "C-Enter" if ctrl_enter else "Enter"],
                check=True,
            )


def tmux_select_window(session: str, window: str) -> None:
    tmux_cmd(["select-window", "-t", f"{session}:{window}"], check=False)


def tmux_kill_session(session: str) -> None:
    tmux_cmd(["kill-session", "-t", session], check=False)


def tmux_kill_window(session: str, window: str) -> None:
    tmux_cmd(["kill-window", "-t", f"{session}:{window}"], check=False)


def tmux_window_exists(session: str, window: str) -> bool:
    p = tmux_cmd(["list-windows", "-t", session, "-F", "#{window_name}"], check=False)
    if p.returncode != 0:
        return False
    names = set((p.stdout or "").splitlines())
    return window in names


def tmux_unique_window_name(session: str, desired: str) -> str:
    base = sanitize(desired, allow=r"a-zA-Z0-9._-", max_len=40) or "win"
    if not tmux_window_exists(session, base):
        return base
    for i in range(2, 1000):
        cand = f"{base}-{i}"
        if not tmux_window_exists(session, cand):
            return cand
    return f"{base}-{uuid.uuid4().hex[:6]}"


def tmux_new_window(
    *,
    session: str,
    name: str,
    cwd: Path,
    command: Sequence[str],
    env: Optional[Mapping[str, str]] = None,
    set_options: Optional[Mapping[str, Any]] = None,
) -> str:
    tmux_cmd(
        [
            "new-window",
            "-d",
            "-t",
            session,
            "-n",
            name,
            "-c",
            str(cwd),
            *tmux_env_flags(env or {}),
            *list(command),
        ],
        check=True,
    )

    if set_options:
        for opt, val in set_options.items():
            o = str(opt or "").strip()
            if not o:
                continue
            tmux_set_option(target=session, option=o, value=str(val or ""))

    pane_id = tmux_format(f"{session}:{name}", "#{pane_id}")
    if not pane_id:
        raise TeamError(
            f"Unable to resolve pane id for new window: {session}:{name}",
            code="TMUX",
            exit_code=2,
        )
    return pane_id


def tmux_mark_pane(
    *,
    pane_id: str,
    role: str,
    worker_id: str = "",
    ticket_id: Optional[str] = "",
) -> None:
    ticket = str(ticket_id or "")
    title = (
        "team:manager"
        if role == ROLE_MANAGER
        else f"team:{worker_id}:{ticket}".strip(":")
    )
    tmux_cmd(["select-pane", "-t", pane_id, "-T", title], check=False)

    tmux_set_option(target=pane_id, option=TMUX_OPT_ROLE, value=role, pane=True)
    if worker_id:
        tmux_set_option(
            target=pane_id, option=TMUX_OPT_WORKER_ID, value=worker_id, pane=True
        )
    if ticket:
        tmux_set_option(
            target=pane_id, option=TMUX_OPT_TICKET_ID, value=ticket, pane=True
        )


def _pane_can_receive_chat(pane: Mapping[str, str]) -> bool:
    cmd = str(pane.get("current_command") or "")
    if str(pane.get("dead") or "") == "1":
        return False
    if cmd in ("bash", "zsh", "fish", "sh", "dash"):
        return False
    return True


def _pane_last_activity_ts(pane: Mapping[str, str]) -> float:
    raw = str(pane.get("last_activity") or "").strip()
    if not raw:
        return 0.0
    try:
        return float(raw)
    except Exception:
        return 0.0


def _pane_is_busy(pane: Mapping[str, str], *, busy_window_s: float = 45.0) -> bool:
    if not _pane_can_receive_chat(pane):
        return False
    last = _pane_last_activity_ts(pane)
    if last <= 0:
        return False
    return (time.time() - last) <= max(1.0, float(busy_window_s))


def tmux_env_flags(env: Mapping[str, str]) -> list[str]:
    out: list[str] = []
    for k, v in (env or {}).items():
        out += ["-e", f"{k}={v}"]
    return out


__all__ = [
    "_pane_is_busy",
    "_pane_last_activity_ts",
    "_pane_can_receive_chat",
    "tmux_available",
    "tmux_capture",
    "tmux_cmd",
    "tmux_env_flags",
    "tmux_format",
    "tmux_get_option",
    "tmux_has_session",
    "tmux_kill_session",
    "tmux_kill_window",
    "tmux_list_panes",
    "tmux_mark_pane",
    "tmux_new_window",
    "tmux_select_window",
    "tmux_send_text",
    "tmux_set_option",
    "tmux_signal",
    "tmux_unique_window_name",
    "tmux_wait_for",
    "tmux_window_exists",
]
