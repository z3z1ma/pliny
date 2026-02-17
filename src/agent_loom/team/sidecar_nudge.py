from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, Mapping, Optional

from agent_loom.team.run_state import RunPaths
from agent_loom.team.tmux import (
    _pane_can_receive_chat,
    _pane_is_busy,
    _pane_last_activity_ts,
    tmux_format,
    tmux_list_panes,
    tmux_send_text,
)


class SidecarNudger:
    def __init__(
        self,
        *,
        pane_id: str,
        harness: str,
        cooldown_s: float,
        child_alive_fn: Callable[[], bool],
        record_warning_fn: Callable[..., None],
    ) -> None:
        self._pane_id = str(pane_id or "").strip()
        self._harness = str(harness or "").strip().lower()
        self._cooldown_s = float(cooldown_s or 0.0)
        self._child_alive_fn = child_alive_fn
        self._record_warning_fn = record_warning_fn
        self._last_nudge_at_by_key: Dict[str, float] = {}
        self._inbox_retry_state: Dict[str, Dict[str, Any]] = {}

    def safe_nudge(
        self,
        text: str,
        *,
        key: str = "general",
        cooldown_override_s: Optional[float] = None,
        confirm_activity: bool = False,
    ) -> tuple[bool, str]:
        nudge_key = str(key or "general").strip().lower() or "general"
        now = time.time()
        effective_cooldown = (
            float(cooldown_override_s)
            if cooldown_override_s is not None
            else float(self._cooldown_s)
        )
        last_nudge_at = float(self._last_nudge_at_by_key.get(nudge_key) or 0.0)
        if (now - last_nudge_at) < max(0.0, float(effective_cooldown)):
            return False, "cooldown"
        if not self._child_alive_fn():
            return False, "child_not_running"
        try:
            session = tmux_format(self._pane_id, "#{session_name}")
            if not session:
                return False, "session_missing"
            pane = dict(tmux_list_panes(session).get(self._pane_id) or {})
            if not pane or not _pane_can_receive_chat(pane):
                return False, "unsafe_pane"
            before = _pane_last_activity_ts(pane) if confirm_activity else 0.0
            busy_before = _pane_is_busy(pane, busy_window_s=8.0)
            tmux_send_text(
                self._pane_id,
                text,
                enter=True,
                ctrl_enter=(self._harness == "omp"),
            )
            self._last_nudge_at_by_key[nudge_key] = now
            if not confirm_activity:
                return True, "sent"
            if before <= 0:
                return True, "confirm_skipped"
            deadline = time.time() + 1.2
            while time.time() < deadline:
                time.sleep(0.2)
                latest = dict(tmux_list_panes(session).get(self._pane_id) or {})
                if not latest:
                    break
                if _pane_last_activity_ts(latest) > before:
                    return True, "activity_confirmed"
            if busy_before:
                return True, "busy_pre_send"
            return False, "activity_unconfirmed"
        except Exception as exc:
            self._record_warning_fn("nudge.send_text", error=exc, once=True)
            return False, "tmux_error"

    def inbox_nudge(
        self,
        *,
        paths: RunPaths,
        recipient: str,
        inbox_list_messages_fn: Callable[..., List[Dict[str, Any]]],
        handle_control_message_fn: Callable[[Mapping[str, Any]], bool],
    ) -> None:
        inbox_busy_defer_s = 90.0
        inbox_success_recheck_s = max(300.0, float(self._cooldown_s))
        inbox_retry_base_s = 20.0
        inbox_retry_max_s = max(120.0, min(600.0, float(self._cooldown_s)))

        def _retry_backoff_s(attempts: int) -> float:
            att = max(1, int(attempts))
            return min(inbox_retry_max_s, inbox_retry_base_s * (2.0 ** float(att - 1)))

        try:
            msgs = inbox_list_messages_fn(paths, to=recipient, unacked_only=True, limit=25)
        except Exception as exc:
            self._record_warning_fn("inbox.list", error=exc, once=True)
            return
        if not msgs:
            return

        user_msgs: List[Dict[str, Any]] = []
        for m in msgs:
            if handle_control_message_fn(m):
                continue
            user_msgs.append(dict(m))
        if not user_msgs:
            return

        now = time.time()
        active_ids: set[str] = set()
        for msg in user_msgs:
            mid = str(msg.get("id") or "").strip()
            if not mid:
                continue
            active_ids.add(mid)
            if mid not in self._inbox_retry_state:
                self._inbox_retry_state[mid] = {
                    "attempts": 0,
                    "next_due_at": 0.0,
                    "last_reason": "",
                }
        for stale_mid in list(self._inbox_retry_state.keys()):
            if stale_mid not in active_ids:
                self._inbox_retry_state.pop(stale_mid, None)

        ordered_msgs = sorted(
            user_msgs,
            key=lambda m: (
                str(m.get("created_at") or ""),
                str(m.get("id") or ""),
            ),
        )
        candidate: Optional[Dict[str, Any]] = None
        for msg in ordered_msgs:
            mid = str(msg.get("id") or "").strip()
            if not mid:
                continue
            state = dict(self._inbox_retry_state.get(mid) or {})
            next_due_at = float(state.get("next_due_at") or 0.0)
            if now >= next_due_at:
                candidate = msg
                break
        if candidate is None:
            return

        session = ""
        pane: Dict[str, str] = {}
        try:
            session = tmux_format(self._pane_id, "#{session_name}")
            if session:
                pane = dict(tmux_list_panes(session).get(self._pane_id) or {})
        except Exception:
            session = ""
            pane = {}

        mid = str(candidate.get("id") or "").strip()
        state = dict(self._inbox_retry_state.get(mid) or {})
        attempts = int(state.get("attempts") or 0)
        if pane and _pane_is_busy(pane, busy_window_s=30.0):
            state["last_reason"] = "busy"
            state["next_due_at"] = now + inbox_busy_defer_s
            self._inbox_retry_state[mid] = state
            return

        first = (
            str(candidate.get("message") or "").splitlines()[0]
            if candidate.get("message")
            else ""
        )
        if len(first) > 100:
            first = first[:97] + "..."
        ok, reason = self.safe_nudge(
            f"TEAM: inbox has {len(user_msgs)} unacked. Run: loom team inbox {paths.team} list --to {recipient} --unacked (newest id={mid}: {first})",
            key=f"inbox:{mid}",
            cooldown_override_s=0.0,
            confirm_activity=True,
        )
        if ok:
            state["attempts"] = 0
            state["last_reason"] = reason
            state["next_due_at"] = now + inbox_success_recheck_s
        else:
            attempts += 1
            state["attempts"] = attempts
            state["last_reason"] = reason
            state["next_due_at"] = now + _retry_backoff_s(attempts)
            self._record_warning_fn(
                "inbox.nudge_retry",
                detail=f"id={mid} reason={reason} attempts={attempts}",
                once=False,
            )
        self._inbox_retry_state[mid] = state


__all__ = ["SidecarNudger"]
