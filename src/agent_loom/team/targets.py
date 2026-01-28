from __future__ import annotations

from typing import Any, Dict, List, Mapping, Tuple

from agent_loom.team.constants import ROLE_MANAGER, ROLE_WORKER
from agent_loom.team.errors import TeamError
from agent_loom.team.tmux import (
    _pane_can_receive_chat,
    tmux_available,
    tmux_format,
    tmux_has_session,
    tmux_list_panes,
    tmux_send_text,
    tmux_window_exists,
)


def _resolve_target(run: Mapping[str, Any], target: str) -> Tuple[str, Dict[str, str]]:
    """Resolve a Team target to a tmux pane id."""

    t = str(target or "").strip()
    if not t:
        raise TeamError("Empty target", code="ARG", exit_code=2)

    if t in ("manager", "mgr"):
        mgr = run.get("manager") or {}
        pane_id = str(mgr.get("pane_id") or "")
        if not pane_id:
            raise TeamError("manager pane_id missing", code="BAD_STATE", exit_code=2)
        return pane_id, {"role": ROLE_MANAGER, "pane_id": pane_id}

    workers = dict(run.get("workers") or {})
    if t in workers:
        w = workers[t] or {}
        pane_id = str(w.get("pane_id") or "")
        if not pane_id:
            raise TeamError(
                f"worker pane_id missing: {t}", code="BAD_STATE", exit_code=2
            )
        return pane_id, {
            "role": str(w.get("role") or ROLE_WORKER),
            "worker_id": t,
            "ticket_id": str(w.get("ticket_id") or ""),
            "pane_id": pane_id,
        }

    # Worktree key match (e.g. merge-queue).
    wk_matches: List[Tuple[str, Dict[str, Any]]] = []
    for wid, w in workers.items():
        if bool((w or {}).get("retired")):
            continue
        wk = str((w or {}).get("worktree_key") or "").strip()
        if wk and wk == t:
            wk_matches.append((wid, w or {}))
    if len(wk_matches) == 1:
        wid, w = wk_matches[0]
        pane_id = str(w.get("pane_id") or "")
        if not pane_id:
            raise TeamError(
                f"worker pane_id missing: {wid}", code="BAD_STATE", exit_code=2
            )
        return pane_id, {
            "role": str(w.get("role") or ROLE_WORKER),
            "worker_id": wid,
            "ticket_id": str(w.get("ticket_id") or ""),
            "pane_id": pane_id,
        }
    if len(wk_matches) > 1:
        raise TeamError(
            f"Multiple workers match worktree_key: {t} -> {[m[0] for m in wk_matches]}",
            code="AMBIGUOUS",
            exit_code=2,
        )

    # Window name match.
    win_matches: List[Tuple[str, Dict[str, Any]]] = []
    for wid, w in workers.items():
        if bool((w or {}).get("retired")):
            continue
        win = str((w or {}).get("window") or "").strip()
        if win and win == t:
            win_matches.append((wid, w or {}))
    if len(win_matches) == 1:
        wid, w = win_matches[0]
        pane_id = str(w.get("pane_id") or "")
        if not pane_id:
            raise TeamError(
                f"worker pane_id missing: {wid}", code="BAD_STATE", exit_code=2
            )
        return pane_id, {
            "role": str(w.get("role") or ROLE_WORKER),
            "worker_id": wid,
            "ticket_id": str(w.get("ticket_id") or ""),
            "pane_id": pane_id,
        }
    if len(win_matches) > 1:
        raise TeamError(
            f"Multiple workers match window: {t} -> {[m[0] for m in win_matches]}",
            code="AMBIGUOUS",
            exit_code=2,
        )

    matches: List[Tuple[str, Dict[str, Any]]] = []
    for wid, w in workers.items():
        if str((w or {}).get("ticket_id") or "").strip() == t and not bool(
            (w or {}).get("retired")
        ):
            matches.append((wid, w or {}))
    if len(matches) == 1:
        wid, w = matches[0]
        pane_id = str(w.get("pane_id") or "")
        if not pane_id:
            raise TeamError(
                f"worker pane_id missing for ticket: {t}", code="BAD_STATE", exit_code=2
            )
        return pane_id, {
            "role": str(w.get("role") or ROLE_WORKER),
            "worker_id": wid,
            "ticket_id": str(w.get("ticket_id") or t),
            "pane_id": pane_id,
        }
    if len(matches) > 1:
        raise TeamError(
            f"Multiple workers match ticket id: {t} -> {[m[0] for m in matches]}",
            code="AMBIGUOUS",
            exit_code=2,
        )

    raise TeamError(f"Unknown target: {target}", code="ARG", exit_code=2)


def _best_effort_tmux_nudge(
    *,
    run: Mapping[str, Any],
    session: str,
    target: str,
    line: str,
    force: bool = False,
) -> Tuple[bool, str, Dict[str, Any]]:
    meta: Dict[str, Any] = {"target": target}

    if not tmux_available():
        return False, "tmux_missing", meta
    if not session:
        return False, "session_missing", meta
    try:
        if not tmux_has_session(session):
            return False, "session_missing", meta
    except Exception as e:
        return False, "tmux_error", {**meta, "error": str(e)}

    try:
        pane_id, meta0 = _resolve_target(run, target)
        meta = dict(meta0 or meta)
    except TeamError as e:
        return (
            False,
            "unknown_target",
            {
                "target": target,
                "error": str(e),
                "code": str(getattr(e, "code", "")),
            },
        )
    except Exception as e:
        return False, "unknown_target", {"target": target, "error": str(e)}

    try:
        panes = tmux_list_panes(session)
        pane = panes.get(pane_id)
        if not pane:
            # Best-effort: refresh pane id from window name if available.
            wid = str(meta.get("worker_id") or "").strip()
            win = (
                str(
                    ((run.get("workers") or {}).get(wid) or {}).get("window") or ""
                ).strip()
                if wid
                else ""
            )
            if win and tmux_window_exists(session, win):
                try:
                    refreshed = tmux_format(f"{session}:{win}", "#{pane_id}")
                except Exception:
                    refreshed = ""
                if refreshed:
                    pane_id = refreshed
                    meta["pane_id"] = refreshed
                    panes = tmux_list_panes(session)
                    pane = panes.get(pane_id)
            if not pane:
                return False, "pane_missing", meta
        if not _pane_can_receive_chat(pane) and not force:
            return False, "unsafe_pane", meta
        tmux_send_text(pane_id, line, enter=True)
        return True, "", meta
    except TeamError as e:
        if e.code == "MISSING_BIN":
            return False, "tmux_missing", meta
        return False, "tmux_error", {**meta, "error": str(e)}
    except Exception as e:
        return False, "tmux_error", {**meta, "error": str(e)}


__all__ = ["_best_effort_tmux_nudge", "_resolve_target"]
