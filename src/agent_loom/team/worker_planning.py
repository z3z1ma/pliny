from __future__ import annotations

import uuid
from typing import Any, Dict, Mapping

from agent_loom.team.composition_runtime import (
    ResolvedMemberProfile,
    list_always_on_member_profiles,
)
from agent_loom.team.constants import (
    DEFAULT_ARCHITECT_AGENT,
    DEFAULT_HARNESS,
    DEFAULT_INTEGRATOR_AGENT,
    DEFAULT_MANAGER_AGENT,
    DEFAULT_WORKER_AGENT,
    ROLE_ARCHITECT,
    ROLE_INTEGRATOR,
    ROLE_MANAGER,
    ROLE_WORKER,
)
from agent_loom.team.strings import sanitize


def normalize_harness(value: str) -> str:
    harness = str(value or "").strip().lower()
    if harness in {"opencode", "claude", "omp", "codex"}:
        return harness
    return DEFAULT_HARNESS


def agent_for_role(run: Mapping[str, Any], role: str, *, harness: str) -> str:
    selected_harness = normalize_harness(harness)
    cfg = (
        (run.get(selected_harness) or {})
        if isinstance(run.get(selected_harness), dict)
        else (
            (run.get("opencode") or {}) if isinstance(run.get("opencode"), dict) else {}
        )
    )
    if role == ROLE_WORKER:
        return str(cfg.get("worker_agent") or DEFAULT_WORKER_AGENT)
    if role == ROLE_ARCHITECT:
        return str(cfg.get("architect_agent") or DEFAULT_ARCHITECT_AGENT)
    if role == ROLE_INTEGRATOR:
        return str(cfg.get("integrator_agent") or DEFAULT_INTEGRATOR_AGENT)
    if role == ROLE_MANAGER:
        return str(cfg.get("manager_agent") or DEFAULT_MANAGER_AGENT)
    return str(cfg.get("worker_agent") or DEFAULT_WORKER_AGENT)


def model_for_role(run: Mapping[str, Any], role: str, *, harness: str) -> str:
    selected_harness = normalize_harness(harness)
    cfg = (
        (run.get(selected_harness) or {})
        if isinstance(run.get(selected_harness), dict)
        else (
            (run.get("opencode") or {}) if isinstance(run.get("opencode"), dict) else {}
        )
    )
    models = cfg.get("models") if isinstance(cfg.get("models"), dict) else {}
    model = str((models or {}).get(str(role or "").strip()) or "").strip()
    if model:
        return model
    return str(cfg.get("model") or "").strip()


def _default_architect_profile(
    *, run: Mapping[str, Any], harness: str
) -> ResolvedMemberProfile:
    return ResolvedMemberProfile(
        member_id="architect",
        role=ROLE_ARCHITECT,
        lifecycle="always_on",
        source="loom",
        agent=agent_for_role(run, ROLE_ARCHITECT, harness=harness),
        harness=harness,
        model="",
        workspace="repo_root",
        worktree_key="",
        description="",
        triggers=(),
        primary_workflows=(),
    )


def always_on_profiles_for_run(run: Mapping[str, Any]) -> list[ResolvedMemberProfile]:
    profiles = list(list_always_on_member_profiles(run))
    if not any(
        str(profile.role or "").strip().lower() == ROLE_ARCHITECT
        for profile in profiles
    ):
        harness = normalize_harness(str(run.get("harness") or ""))
        profiles.append(_default_architect_profile(run=run, harness=harness))

    deduped: dict[str, ResolvedMemberProfile] = {}
    for profile in profiles:
        member_id = str(profile.member_id or "").strip()
        if not member_id:
            continue
        deduped[member_id] = profile

    return sorted(
        deduped.values(),
        key=lambda profile: (
            0 if str(profile.role or "").strip().lower() == ROLE_ARCHITECT else 1,
            str(profile.member_id or "").strip(),
        ),
    )


def workspace_for_always_on_profile(profile: ResolvedMemberProfile) -> tuple[str, str]:
    role = str(profile.role or "").strip().lower()
    if role in {ROLE_MANAGER, ROLE_ARCHITECT}:
        return "repo_root", ""
    if role == ROLE_INTEGRATOR:
        return "worktree", "merge-queue"

    workspace = str(profile.workspace or "").strip().lower()
    if workspace not in {"repo_root", "worktree"}:
        workspace = "repo_root"

    worktree_key = sanitize(str(profile.worktree_key or ""), max_len=80) or sanitize(
        str(profile.member_id or ""),
        max_len=80,
    )
    if not worktree_key:
        worktree_key = f"persona-{uuid.uuid4().hex[:8]}"

    return workspace, worktree_key


def persona_worktree_branch(*, run_id: str, member_id: str) -> str:
    run_key = sanitize(str(run_id or ""), allow=r"a-zA-Z0-9._-", max_len=16) or "run"
    member_key = (
        sanitize(str(member_id or ""), allow=r"a-zA-Z0-9._-", max_len=40) or "persona"
    )
    return f"team/{run_key}-{member_key}"


def max_headcount(run: Mapping[str, Any]) -> int:
    raw_limits = run.get("limits")
    limits: Dict[str, Any] = dict(raw_limits) if isinstance(raw_limits, dict) else {}
    raw = limits.get("max_headcount", 0)
    try:
        headcount = int(raw)
    except Exception:
        return 0
    return headcount if headcount > 0 else 0


def active_spawn_headcount(
    run: Mapping[str, Any],
) -> tuple[int, list[str], dict[str, str]]:
    raw_workers = run.get("workers")
    workers: Dict[str, Any] = dict(raw_workers) if isinstance(raw_workers, dict) else {}
    active_ids: list[str] = []
    active_roles: dict[str, str] = {}
    for worker_id in sorted(workers):
        worker = workers.get(worker_id)
        if not isinstance(worker, dict):
            continue
        if bool(worker.get("retired")):
            continue
        role = str(worker.get("role") or "").strip().lower()
        if role != ROLE_WORKER:
            continue
        active_ids.append(str(worker_id))
        active_roles[str(worker_id)] = role
    return len(active_ids), active_ids, active_roles
