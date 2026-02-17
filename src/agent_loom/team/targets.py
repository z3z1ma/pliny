from __future__ import annotations

from typing import Any, Dict, List, Mapping, Tuple

from agent_loom.team.constants import (
    ROLE_ARCHITECT,
    ROLE_INTEGRATOR,
    ROLE_MANAGER,
    ROLE_WORKER,
)
from agent_loom.team.errors import TeamError
from agent_loom.team.strings import sanitize
from agent_loom.team.tmux import (
    _pane_can_receive_chat,
    tmux_available,
    tmux_format,
    tmux_has_session,
    tmux_list_panes,
    tmux_send_text,
    tmux_window_exists,
)


def _canonical_worker_id(value: str) -> str:
    return (
        sanitize(str(value or "").strip().lower(), allow=r"a-z0-9._-", max_len=48) or ""
    )


def _canonical_ticket_id(value: str) -> str:
    return str(value or "").strip().lower()


def _active_workers(run: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
    workers: Dict[str, Dict[str, Any]] = {}
    raw_workers = run.get("workers")
    if not isinstance(raw_workers, dict):
        return workers
    for raw_id, raw_worker in raw_workers.items():
        if not isinstance(raw_worker, dict):
            continue
        if bool(raw_worker.get("retired")):
            continue
        worker_id = _canonical_worker_id(str(raw_worker.get("worker_id") or raw_id))
        if not worker_id:
            continue
        worker = dict(raw_worker)
        worker["worker_id"] = worker_id
        worker["ticket_id"] = _canonical_ticket_id(str(worker.get("ticket_id") or ""))
        workers[worker_id] = worker
    return workers


def _resolve_worker_by_role(
    run: Mapping[str, Any], role: str, *, label: str
) -> Tuple[str, Dict[str, str]]:
    matches: List[Tuple[str, Dict[str, Any]]] = []
    for wid, worker in _active_workers(run).items():
        if str(worker.get("role") or "").strip().lower() == role:
            matches.append((wid, worker))
    if not matches:
        raise TeamError(f"No active {label} target", code="ARG", exit_code=2)
    if len(matches) > 1:
        raise TeamError(
            f"Multiple active {label} targets: {[wid for wid, _w in matches]}",
            code="AMBIGUOUS",
            exit_code=2,
        )
    wid, worker = matches[0]
    pane_id = str(worker.get("pane_id") or "").strip()
    if not pane_id:
        raise TeamError(f"{label} pane_id missing", code="BAD_STATE", exit_code=2)
    return pane_id, {
        "role": role,
        "worker_id": wid,
        "ticket_id": str(worker.get("ticket_id") or ""),
        "pane_id": pane_id,
    }


def _resolve_target(run: Mapping[str, Any], target: str) -> Tuple[str, Dict[str, str]]:
    """Resolve a Team target to a tmux pane id."""

    raw = str(target or "").strip()
    if not raw:
        raise TeamError("Empty target", code="ARG", exit_code=2)

    token = raw.lower()
    if token in {"manager", "mgr"}:
        mgr = run.get("manager") or {}
        pane_id = str(mgr.get("pane_id") or "")
        if not pane_id:
            raise TeamError("manager pane_id missing", code="BAD_STATE", exit_code=2)
        return pane_id, {"role": ROLE_MANAGER, "pane_id": pane_id}

    if token == "architect":
        return _resolve_worker_by_role(run, ROLE_ARCHITECT, label="architect")
    if token == "integrator":
        return _resolve_worker_by_role(run, ROLE_INTEGRATOR, label="integrator")

    workers = _active_workers(run)

    if token.startswith("worker:"):
        worker_id = _canonical_worker_id(token.split(":", 1)[1])
        if not worker_id:
            raise TeamError("Empty worker target", code="ARG", exit_code=2)
        worker = workers.get(worker_id)
        if not worker:
            raise TeamError(f"Unknown worker target: {raw}", code="ARG", exit_code=2)
        pane_id = str(worker.get("pane_id") or "").strip()
        if not pane_id:
            raise TeamError(
                f"worker pane_id missing: {worker_id}", code="BAD_STATE", exit_code=2
            )
        return pane_id, {
            "role": str(worker.get("role") or ROLE_WORKER),
            "worker_id": worker_id,
            "ticket_id": str(worker.get("ticket_id") or ""),
            "pane_id": pane_id,
        }

    if token.startswith("ticket:"):
        ticket_id = _canonical_ticket_id(token.split(":", 1)[1])
        if not ticket_id:
            raise TeamError("Empty ticket target", code="ARG", exit_code=2)
        matches = [
            (wid, worker)
            for wid, worker in workers.items()
            if str(worker.get("ticket_id") or "") == ticket_id
        ]
        if not matches:
            raise TeamError(f"Unknown ticket target: {raw}", code="ARG", exit_code=2)
        if len(matches) > 1:
            raise TeamError(
                f"Multiple workers match ticket id: {ticket_id} -> {[wid for wid, _w in matches]}",
                code="AMBIGUOUS",
                exit_code=2,
            )
        wid, worker = matches[0]
        pane_id = str(worker.get("pane_id") or "").strip()
        if not pane_id:
            raise TeamError(
                f"worker pane_id missing for ticket: {ticket_id}",
                code="BAD_STATE",
                exit_code=2,
            )
        return pane_id, {
            "role": str(worker.get("role") or ROLE_WORKER),
            "worker_id": wid,
            "ticket_id": ticket_id,
            "pane_id": pane_id,
        }

    raise TeamError(f"Unknown target: {target}", code="ARG", exit_code=2)


def _resolve_targets(run: Mapping[str, Any], target: str) -> List[Dict[str, str]]:
    """Resolve single or grouped Team target(s) to concrete pane metadata."""

    raw = str(target or "").strip()
    if not raw:
        raise TeamError("Empty target", code="ARG", exit_code=2)

    token = raw.lower()
    if token == "workers":
        resolved: List[Dict[str, str]] = []
        for wid, worker in sorted(_active_workers(run).items()):
            role = str(worker.get("role") or "").strip().lower()
            if role != ROLE_WORKER:
                continue
            pane_id = str(worker.get("pane_id") or "").strip()
            if not pane_id:
                continue
            resolved.append(
                {
                    "target": f"worker:{wid}",
                    "pane_id": pane_id,
                    "role": role,
                    "worker_id": wid,
                    "ticket_id": str(worker.get("ticket_id") or ""),
                }
            )
        if not resolved:
            raise TeamError(
                "Target resolved to zero recipients: workers",
                code="ARG",
                exit_code=2,
            )
        return resolved

    pane_id, meta = _resolve_target(run, raw)
    return [
        {
            "target": raw,
            "pane_id": pane_id,
            "role": str(meta.get("role") or ""),
            "worker_id": str(meta.get("worker_id") or ""),
            "ticket_id": str(meta.get("ticket_id") or ""),
        }
    ]


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
        tmux_send_text(
            pane_id,
            line,
            enter=True,
            ctrl_enter=(str(run.get("harness") or "").strip().lower() == "omp"),
        )
        return True, "", meta
    except TeamError as e:
        if e.code == "MISSING_BIN":
            return False, "tmux_missing", meta
        return False, "tmux_error", {**meta, "error": str(e)}
    except Exception as e:
        return False, "tmux_error", {**meta, "error": str(e)}


__all__ = ["_best_effort_tmux_nudge", "_resolve_target", "_resolve_targets"]
