from __future__ import annotations

import random
import re
import time
import uuid
from typing import Any, Callable, Dict, Mapping, Optional

from agent_loom.team.constants import (
    DEFAULT_AUTOCAPTURE_MAX_S,
    DEFAULT_AUTOCAPTURE_MIN_S,
)
from agent_loom.team.events import (
    _event_stamp,
    best_effort,
    safe_write_event,
    write_event,
)
from agent_loom.team.inbox import _inbox_write_and_maybe_nudge
from agent_loom.team.io import _atomic_write_json, _atomic_write_text
from agent_loom.team.run_state import RunPaths, locked_run
from agent_loom.team.strings import sanitize
from agent_loom.team.time import _iso_z
from agent_loom.team.tmux import (
    tmux_available,
    tmux_capture,
    tmux_has_session,
    tmux_wait_for,
)
from agent_loom.team.worker_planning import active_spawn_headcount

_CHECKIN_STREAK_THRESHOLD = 2
_CHECKIN_PER_WORKER_COOLDOWN_S = 20.0 * 60.0
_CHECKIN_MAX_TARGETS = 2
_IDLE_NOISE_TIME_RE = re.compile(r"\b\d{1,2}:\d{2}(:\d{2})?\b")
_IDLE_NOISE_TS_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}[T ][0-9:.+-Z]+\b")
_IDLE_NOISE_PCT_RE = re.compile(r"(?<!\d)\d{1,3}%")


def wait_for_wake(
    *,
    session: str,
    channel: str,
    seconds: int,
    tmux_available_fn: Optional[Callable[[], bool]] = None,
    tmux_has_session_fn: Optional[Callable[[str], bool]] = None,
    tmux_wait_for_fn: Optional[Callable[..., bool]] = None,
    sleep_fn: Optional[Callable[[float], None]] = None,
) -> tuple[str, bool]:
    if tmux_available_fn is None:
        tmux_available_fn = tmux_available
    if tmux_has_session_fn is None:
        tmux_has_session_fn = tmux_has_session
    if tmux_wait_for_fn is None:
        tmux_wait_for_fn = tmux_wait_for
    if sleep_fn is None:
        sleep_fn = time.sleep

    use_tmux = False
    if session and tmux_available_fn():
        try:
            use_tmux = tmux_has_session_fn(session)
        except Exception:
            use_tmux = False

    if use_tmux:
        signaled = tmux_wait_for_fn(channel, timeout_s=float(seconds))
        return ("signal" if signaled else "timeout", bool(signaled))

    sleep_fn(float(seconds))
    return ("sleep", False)


def next_autocapture_delay_s(*, initial: bool) -> float:
    if initial:
        return 30.0 + (random.random() * 60.0)
    lo = float(min(DEFAULT_AUTOCAPTURE_MIN_S, DEFAULT_AUTOCAPTURE_MAX_S))
    hi = float(max(DEFAULT_AUTOCAPTURE_MIN_S, DEFAULT_AUTOCAPTURE_MAX_S))
    if hi <= 0 or hi <= lo:
        return max(60.0, lo)
    return lo + (random.random() * (hi - lo))


def normalize_capture_for_idle(text: str) -> str:
    out_lines: list[str] = []
    for raw in str(text or "").splitlines():
        line = raw.rstrip()
        line = _IDLE_NOISE_TS_RE.sub("<ts>", line)
        line = _IDLE_NOISE_TIME_RE.sub("<time>", line)
        line = _IDLE_NOISE_PCT_RE.sub("<pct>", line)
        line = re.sub(r"\s+", " ", line).strip()
        if not line:
            continue
        out_lines.append(line)
    if not out_lines:
        return ""
    # Keep a bounded tail so a scrolling transcript can still be compared cheaply.
    return "\n".join(out_lines[-120:])


def capture_pane_and_persist(
    paths: RunPaths,
    *,
    run: Mapping[str, Any],
    pane_id: str,
    target_key: str,
    target_meta: Mapping[str, Any],
    pane: Mapping[str, Any],
    lines: int,
    no_join: bool,
    summary: str,
) -> Dict[str, Any]:
    captured_at = _iso_z()
    out = tmux_capture(pane_id, lines=int(lines), join_wrapped=not bool(no_join))

    cap_id = uuid.uuid4().hex[:12]
    safe_target = (
        sanitize(str(target_key or ""), allow=r"a-zA-Z0-9._-", max_len=40) or "target"
    )
    base = f"{_event_stamp(captured_at)}_{cap_id}_{safe_target}"
    cap_txt = paths.captures_dir / f"{base}.txt"
    cap_json = paths.captures_dir / f"{base}.json"

    def _persist_capture() -> None:
        paths.captures_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write_text(cap_txt, out)
        _atomic_write_json(
            cap_json,
            {
                "id": cap_id,
                "captured_at": captured_at,
                "team": str(run.get("team") or paths.team),
                "run_id": str(run.get("run_id") or ""),
                "target": dict(target_meta or {}),
                "pane": dict(pane or {}),
                "lines": int(lines),
                "output_file": str(cap_txt),
                "bytes": len(out.encode("utf-8")),
            },
        )

    best_effort(_persist_capture, label="capture.persist")

    safe_write_event(
        paths,
        event_type="capture.saved",
        run=run,
        summary=str(summary or f"Captured {safe_target} lines={int(lines)}"),
        refs={
            **(dict(target_meta or {})),
            "capture_id": cap_id,
            "capture_file": str(cap_txt),
            "capture_meta": str(cap_json),
        },
        data={
            "lines": int(lines),
            "bytes": len(out.encode("utf-8")),
            "no_join": bool(no_join),
        },
    )

    return {
        "id": cap_id,
        "captured_at": captured_at,
        "output": out,
        "output_file": str(cap_txt),
        "meta_file": str(cap_json),
    }


def manager_checkin_after_wait(
    *,
    paths: RunPaths,
    wake_reason: str,
    now_fn: Optional[Callable[[], float]] = None,
    locked_run_fn: Optional[Callable[..., Any]] = None,
    active_spawn_headcount_fn: Optional[
        Callable[[Mapping[str, Any]], tuple[int, list[str], Mapping[str, str]]]
    ] = None,
    inbox_write_and_maybe_nudge_fn: Optional[Callable[..., Any]] = None,
    write_event_fn: Optional[Callable[..., Any]] = None,
) -> None:
    if now_fn is None:
        now_fn = time.time
    if locked_run_fn is None:
        locked_run_fn = locked_run
    if active_spawn_headcount_fn is None:
        active_spawn_headcount_fn = active_spawn_headcount
    if inbox_write_and_maybe_nudge_fn is None:
        inbox_write_and_maybe_nudge_fn = _inbox_write_and_maybe_nudge
    if write_event_fn is None:
        write_event_fn = write_event

    timeout_like = str(wake_reason or "").strip().lower() in {"timeout", "sleep"}
    now = now_fn()

    def _get_ops_dict(run: Dict[str, Any]) -> Dict[str, Any]:
        raw = run.get("ops")
        return dict(raw) if isinstance(raw, dict) else {}

    def _get_mgr_dict(ops: Dict[str, Any]) -> Dict[str, Any]:
        raw = ops.get("manager")
        return dict(raw) if isinstance(raw, dict) else {}

    def _get_checkin_dict(mgr: Dict[str, Any]) -> Dict[str, Any]:
        raw = mgr.get("checkin")
        return dict(raw) if isinstance(raw, dict) else {}

    def _coerce_float(v: Any) -> float:
        try:
            return float(v)
        except Exception:
            return 0.0

    def _coerce_int(v: Any) -> int:
        try:
            return int(v)
        except Exception:
            return 0

    with locked_run_fn(paths) as run:
        ops = _get_ops_dict(run)
        mgr = _get_mgr_dict(ops)
        checkin = _get_checkin_dict(mgr)

        streak = _coerce_int(checkin.get("timeout_streak"))
        by_worker_raw = checkin.get("by_worker")
        by_worker: Dict[str, float] = {}
        if isinstance(by_worker_raw, dict):
            for k, v in by_worker_raw.items():
                kk = str(k).strip()
                if kk:
                    by_worker[kk] = _coerce_float(v)

        if not timeout_like:
            checkin["timeout_streak"] = 0
            checkin["updated_at"] = now
            mgr["checkin"] = checkin
            ops["manager"] = mgr
            run["ops"] = ops
            return

        streak += 1
        checkin["timeout_streak"] = streak
        checkin["updated_at"] = now

        if streak < _CHECKIN_STREAK_THRESHOLD:
            mgr["checkin"] = checkin
            ops["manager"] = mgr
            run["ops"] = ops
            return

        active_count, active_ids, _active_roles = active_spawn_headcount_fn(run)
        if active_count <= 0:
            mgr["checkin"] = checkin
            ops["manager"] = mgr
            run["ops"] = ops
            return

        eligible: list[str] = []
        for wid in active_ids:
            last = float(by_worker.get(str(wid), 0.0))
            if last <= 0.0 or (now - last) >= _CHECKIN_PER_WORKER_COOLDOWN_S:
                eligible.append(str(wid))

        eligible.sort(key=lambda w: (by_worker.get(w, 0.0), w))
        targets = eligible[:_CHECKIN_MAX_TARGETS]
        if not targets:
            mgr["checkin"] = checkin
            ops["manager"] = mgr
            run["ops"] = ops
            return

        sent_to: list[str] = []
        for wid in targets:
            try:
                msg = (
                    "TEAM: manager check-in. Please post a loom ticket update (status + next step). "
                    "If blocked, summarize what you tried and give 2 options. "
                    "If you have no moves, you may self-retire (keeps worktree): "
                    f"`loom team retire {paths.team} {wid}`."
                )
                inbox_write_and_maybe_nudge_fn(
                    paths=paths,
                    run=run,
                    target=wid,
                    message=msg,
                    sender="manager",
                    kind="checkin",
                    meta_extra={
                        "op": "manager_checkin",
                        "timeout_streak": streak,
                        "worker_id": wid,
                    },
                    nudge=True,
                    force=False,
                    line_info="manager_checkin",
                )
                by_worker[str(wid)] = now
                sent_to.append(str(wid))
            except Exception:
                continue

        if sent_to:
            checkin["timeout_streak"] = 0
            checkin["last_checkin_at"] = now
            checkin["by_worker"] = dict(by_worker)

            write_event_fn(
                paths,
                event_type="manager.checkin",
                run=run,
                summary=f"Manager check-in sent_to={','.join(sent_to)}",
                refs={"recipients": ",".join(sent_to)},
                data={
                    "sent_to": list(sent_to),
                    "timeout_streak": int(streak),
                    "cooldown_s": int(_CHECKIN_PER_WORKER_COOLDOWN_S),
                    "max_targets": int(_CHECKIN_MAX_TARGETS),
                },
            )

        mgr["checkin"] = checkin
        ops["manager"] = mgr
        run["ops"] = ops
