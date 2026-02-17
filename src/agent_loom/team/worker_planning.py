from __future__ import annotations

from typing import Any, Dict, Mapping

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

