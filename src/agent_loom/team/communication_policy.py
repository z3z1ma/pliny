from __future__ import annotations

import os
from typing import Any, Dict, List, Mapping, Tuple

from agent_loom.team.constants import (
    ENV_TEAM_ROLE,
    ENV_TEAM_WORKER_ID,
    ROLE_ARCHITECT,
    ROLE_INTEGRATOR,
    ROLE_MANAGER,
    ROLE_WORKER,
)
from agent_loom.team.errors import TeamError
from agent_loom.team.run_state import RunPaths
from agent_loom.team.strings import sanitize


def communication_policy_from_run(_run: Mapping[str, Any]) -> Dict[str, Any]:
    routes: Dict[str, Tuple[str, ...]] = {
        ROLE_MANAGER: ("all",),
        ROLE_WORKER: ("manager", "architect", "escalate"),
        ROLE_ARCHITECT: ("manager", "workers", "escalate"),
        ROLE_INTEGRATOR: ("manager", "architect"),
    }
    return {"routes": routes}


def sender_for_send() -> Tuple[str, str]:
    role = str(os.getenv(ENV_TEAM_ROLE) or "").strip().lower()
    worker_id = sanitize(
        str(os.getenv(ENV_TEAM_WORKER_ID) or "").strip().lower(), max_len=48
    )
    if not role:
        return ROLE_MANAGER, "manager"
    if role == ROLE_MANAGER:
        return ROLE_MANAGER, "manager"
    if not worker_id:
        raise TeamError(
            "TEAM_WORKER_ID missing for non-manager sender",
            code="BAD_STATE",
            exit_code=2,
        )
    return role, worker_id


def active_targets_for_role(run: Mapping[str, Any], role: str) -> List[str]:
    role_norm = str(role or "").strip().lower()
    if not role_norm:
        return []
    targets: List[str] = []
    if role_norm == ROLE_MANAGER:
        targets.append("manager")
    workers = dict(run.get("workers") or {})
    for wid, worker in workers.items():
        if bool((worker or {}).get("retired")):
            continue
        worker_role = str((worker or {}).get("role") or "").strip().lower()
        if worker_role == role_norm:
            targets.append(str(wid).strip().lower())
    return sorted(set(targets))


def resolve_send_target(
    *,
    run: Mapping[str, Any],
    target: str,
    sender_role: str,
) -> Tuple[str, bool]:
    normalized = str(target or "").strip().lower()
    if normalized not in {"escalate", "escalation"}:
        return str(target or "").strip(), False

    if sender_role == ROLE_MANAGER:
        raise TeamError(
            "Escalation target is only allowed for non-manager senders",
            code="PERMISSION",
            exit_code=2,
        )

    candidates = active_targets_for_role(run, ROLE_MANAGER)
    if not candidates:
        raise TeamError(
            "Escalation target has no active manager recipient",
            code="BAD_STATE",
            exit_code=2,
            suggestions=[f"loom team start {str(run.get('team') or '')}"],
        )
    return candidates[0], True


def route_allows_target(
    *,
    allowed_tokens: Tuple[str, ...],
    requested_target: str,
    recipient: Mapping[str, Any],
) -> bool:
    requested = str(requested_target or "").strip().lower()
    role = str(recipient.get("role") or "").strip().lower()
    worker_id = str(recipient.get("worker_id") or "").strip().lower()
    ticket_id = str(recipient.get("ticket_id") or "").strip().lower()

    for token in allowed_tokens:
        value = str(token or "").strip().lower()
        if not value:
            continue
        if value == "all":
            return True
        if value == requested:
            return True
        if value == "escalate" and requested in {"escalate", "escalation"}:
            return True
        if value == "manager" and role == ROLE_MANAGER:
            return True
        if value == "architect" and role == ROLE_ARCHITECT:
            return True
        if value == "integrator" and role == ROLE_INTEGRATOR:
            return True
        if value == "workers" and role == ROLE_WORKER:
            return True
        if value.startswith("worker:"):
            wid = value.split(":", 1)[1].strip()
            if wid and wid == worker_id:
                return True
            continue
        if value.startswith("ticket:"):
            tid = value.split(":", 1)[1].strip()
            if tid and tid == ticket_id:
                return True
            continue
    return False


def delivery_suggestions(
    *,
    paths: RunPaths,
    target: str,
    delivery_reason: str,
    meta: Mapping[str, Any],
) -> List[str]:
    suggestions: List[str] = [
        f"loom team doctor {paths.team}",
        f"loom team status {paths.team} --show-dead",
    ]

    role = str((meta or {}).get("role") or "").strip().lower()
    wid = str((meta or {}).get("worker_id") or "").strip().lower()
    tnorm = str(target or "").strip().lower()

    if delivery_reason in {"session_missing", "tmux_missing"}:
        suggestions.append(f"loom team start {paths.team} --repo {paths.repo_root}")
    elif delivery_reason in {"pane_missing", "unknown_target"}:
        if role == ROLE_INTEGRATOR or tnorm == "integrator":
            suggestions.append(f"loom team spawn-integrator {paths.team}")
            suggestions.append(f"loom team spawn-integrator {paths.team} --force")
        elif wid:
            suggestions.append(
                f"loom team bounce {paths.team} {wid} --reason delivery_failure"
            )
            suggestions.append(f"loom team resume-worker {paths.team} {wid}")
    elif delivery_reason == "unsafe_pane":
        suggestions.append(
            f'loom team send {paths.team} {tnorm} --force --message "..."'
        )
    elif delivery_reason == "unconfirmed_delivery":
        suggestions.append(
            f"loom team send {paths.team} {tnorm} --message \"...\""
        )
        if wid:
            suggestions.append(
                f"loom team bounce {paths.team} {wid} --reason unconfirmed_delivery"
            )

    return suggestions


__all__ = [
    "active_targets_for_role",
    "communication_policy_from_run",
    "delivery_suggestions",
    "resolve_send_target",
    "route_allows_target",
    "sender_for_send",
]
