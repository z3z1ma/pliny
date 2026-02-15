"""Role-based permission guards for team operations."""

from __future__ import annotations

import os

from agent_loom.team.constants import (
    ENV_TEAM_ROLE,
    ENV_TEAM_WORKER_ID,
    ROLE_MANAGER,
)
from agent_loom.team.errors import TeamError
from agent_loom.team.strings import sanitize


def _team_role_from_env() -> str:
    return str(os.getenv(ENV_TEAM_ROLE) or "").strip().lower()


def _team_worker_id_from_env() -> str:
    return sanitize(str(os.getenv(ENV_TEAM_WORKER_ID) or ""), max_len=48)


def _deny_if_role_set(*, action: str) -> None:
    role = _team_role_from_env()
    if role:
        raise TeamError(
            f"Refusing to run '{action}' from inside a team pane (role={role})",
            code="PERMISSION",
            exit_code=2,
            hint=(
                "Run this command from outside tmux (human shell), or ask the manager to do it."
            ),
        )


def _require_role(*, action: str, allowed_roles: set[str]) -> None:
    role = _team_role_from_env()
    if not role:
        return
    if role not in allowed_roles:
        allowed = ", ".join(sorted(allowed_roles))
        raise TeamError(
            f"Permission denied for '{action}' (role={role}; allowed={allowed})",
            code="PERMISSION",
            exit_code=2,
            hint="Ask the manager to run it, or run from outside tmux if you are a human operator.",
        )


def _require_self_worker_id(*, action: str, requested_worker_id: str) -> None:
    role = _team_role_from_env()
    if not role or role == ROLE_MANAGER:
        return
    mine = _team_worker_id_from_env()
    req = sanitize(str(requested_worker_id or ""), max_len=48)
    if mine and req and mine != req:
        raise TeamError(
            f"Permission denied for '{action}': can only target your own worker_id (you={mine} requested={req})",
            code="PERMISSION",
            exit_code=2,
            hint="Ask the manager if another worker needs to be retired.",
        )
