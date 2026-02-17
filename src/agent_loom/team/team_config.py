from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Mapping

import yaml

from agent_loom.team.constants import (
    DEFAULT_DEAD_AFTER_S,
    DEFAULT_HEARTBEAT_INTERVAL_S,
    DEFAULT_RECOVERY_COOLDOWN_S,
    DEFAULT_STALE_AFTER_S,
    DEFAULT_MAX_RECOVERIES_PER_HOUR,
    ROLE_ARCHITECT,
    ROLE_INTEGRATOR,
    ROLE_MANAGER,
    ROLE_WORKER,
)
from agent_loom.team.errors import TeamError
from agent_loom.team.time import _iso_z

_HARNESS_VALUES = {"opencode", "claude", "omp", "codex"}
_ROLES = (ROLE_MANAGER, ROLE_ARCHITECT, ROLE_WORKER, ROLE_INTEGRATOR)


class TeamConfigError(TeamError):
    def __init__(self, message: str, *, hint: str = "") -> None:
        super().__init__(message, code="ARG", exit_code=2, hint=hint)


def default_liveness_spec() -> Dict[str, int]:
    return {
        "heartbeat_interval_s": int(DEFAULT_HEARTBEAT_INTERVAL_S),
        "stale_after_s": int(DEFAULT_STALE_AFTER_S),
        "dead_after_s": int(DEFAULT_DEAD_AFTER_S),
        "recovery_cooldown_s": int(DEFAULT_RECOVERY_COOLDOWN_S),
        "max_recoveries_per_hour": int(DEFAULT_MAX_RECOVERIES_PER_HOUR),
    }


def default_team_config_spec() -> Dict[str, Any]:
    return {
        "harness": "",
        "model": "",
        "role_prompts": {"append": {role: "" for role in _ROLES}},
        "worker": {"subagents": "encouraged"},
        "liveness": default_liveness_spec(),
    }


def _expect_mapping(path: str, raw: Any) -> Mapping[str, Any]:
    if not isinstance(raw, dict):
        raise TeamConfigError(f"{path}: expected mapping/object")
    return raw


def _expect_nonempty_str(path: str, raw: Any) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise TeamConfigError(f"{path}: expected non-empty string")
    return raw.strip()


def _expect_optional_str(path: str, raw: Any) -> str:
    if raw is None:
        return ""
    if not isinstance(raw, str):
        raise TeamConfigError(f"{path}: expected string")
    return raw.strip()


def _expect_positive_int(path: str, raw: Any, *, minimum: int = 1) -> int:
    if isinstance(raw, bool):
        raise TeamConfigError(f"{path}: expected integer >= {minimum}")
    try:
        value = int(raw)
    except Exception as exc:
        raise TeamConfigError(f"{path}: expected integer >= {minimum}") from exc
    if value < minimum:
        raise TeamConfigError(f"{path}: expected integer >= {minimum}")
    return value


def _reject_unknown_keys(path: str, obj: Mapping[str, Any], allowed: set[str]) -> None:
    unknown = sorted(str(k) for k in obj.keys() if str(k) not in allowed)
    if unknown:
        raise TeamConfigError(
            f"{path}: unknown key(s): {', '.join(unknown)}",
            hint=f"Allowed keys: {', '.join(sorted(allowed))}",
        )


def normalize_team_config_spec(raw: Mapping[str, Any] | None) -> Dict[str, Any]:
    spec = default_team_config_spec()
    if raw is None:
        return spec

    root = _expect_mapping("team_config", raw)
    _reject_unknown_keys(
        "team_config",
        root,
        {"harness", "model", "role_prompts", "worker", "liveness"},
    )

    harness = _expect_optional_str("team_config.harness", root.get("harness"))
    if harness:
        normalized_harness = harness.lower()
        if normalized_harness not in _HARNESS_VALUES:
            raise TeamConfigError(
                f"team_config.harness: invalid value {harness!r}",
                hint=f"Use one of: {', '.join(sorted(_HARNESS_VALUES))}",
            )
        spec["harness"] = normalized_harness

    model = _expect_optional_str("team_config.model", root.get("model"))
    if model:
        spec["model"] = model

    role_prompts_raw = root.get("role_prompts")
    if role_prompts_raw is not None:
        role_prompts = _expect_mapping("team_config.role_prompts", role_prompts_raw)
        _reject_unknown_keys("team_config.role_prompts", role_prompts, {"append"})
        append_raw = role_prompts.get("append")
        if append_raw is not None:
            append_obj = _expect_mapping("team_config.role_prompts.append", append_raw)
            _reject_unknown_keys("team_config.role_prompts.append", append_obj, set(_ROLES))
            append = dict(spec["role_prompts"]["append"] or {})
            for role in _ROLES:
                value = append_obj.get(role)
                if value is None:
                    continue
                append[role] = _expect_optional_str(
                    f"team_config.role_prompts.append.{role}", value
                )
            spec["role_prompts"] = {"append": append}

    worker_raw = root.get("worker")
    if worker_raw is not None:
        worker_obj = _expect_mapping("team_config.worker", worker_raw)
        _reject_unknown_keys("team_config.worker", worker_obj, {"subagents"})
        subagents = _expect_optional_str(
            "team_config.worker.subagents",
            worker_obj.get("subagents"),
        )
        if subagents and subagents != "encouraged":
            raise TeamConfigError(
                "team_config.worker.subagents: unsupported value",
                hint='Use: "encouraged"',
            )
        spec["worker"] = {"subagents": subagents or "encouraged"}

    liveness_raw = root.get("liveness")
    if liveness_raw is not None:
        liveness_obj = _expect_mapping("team_config.liveness", liveness_raw)
        _reject_unknown_keys(
            "team_config.liveness",
            liveness_obj,
            {
                "heartbeat_interval_s",
                "stale_after_s",
                "dead_after_s",
                "recovery_cooldown_s",
                "max_recoveries_per_hour",
            },
        )
        liveness = dict(spec["liveness"] or {})
        for key in (
            "heartbeat_interval_s",
            "stale_after_s",
            "dead_after_s",
            "recovery_cooldown_s",
            "max_recoveries_per_hour",
        ):
            if key not in liveness_obj:
                continue
            liveness[key] = _expect_positive_int(
                f"team_config.liveness.{key}", liveness_obj.get(key), minimum=1
            )
        if int(liveness["stale_after_s"]) >= int(liveness["dead_after_s"]):
            raise TeamConfigError(
                "team_config.liveness: stale_after_s must be < dead_after_s"
            )
        spec["liveness"] = liveness

    return spec


def load_team_config_yaml(path: Path | str) -> Dict[str, Any]:
    p = Path(path).expanduser()
    try:
        text = p.read_text(encoding="utf-8")
    except OSError as exc:
        raise TeamConfigError(f"Unable to read team config file {p}: {exc}") from exc

    try:
        raw_doc = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise TeamConfigError(f"{p}: invalid YAML: {exc}") from exc

    if raw_doc is None:
        raise TeamConfigError(f"{p}: expected YAML mapping/object at top level")
    if not isinstance(raw_doc, dict):
        raise TeamConfigError(f"{p}: expected YAML mapping/object at top level")

    spec = normalize_team_config_spec(raw_doc)
    return {
        "source": str(p.resolve()),
        "loaded_at": _iso_z(),
        "spec": spec,
    }


def team_config_from_run(run: Mapping[str, Any]) -> Dict[str, Any]:
    raw = run.get("team_config")
    base = {
        "source": "",
        "loaded_at": "",
        "spec": default_team_config_spec(),
    }
    if not isinstance(raw, dict):
        return base
    source = str(raw.get("source") or "").strip()
    loaded_at = str(raw.get("loaded_at") or "").strip()
    raw_spec = raw.get("spec")
    spec = normalize_team_config_spec(raw_spec if isinstance(raw_spec, dict) else None)
    return {"source": source, "loaded_at": loaded_at, "spec": spec}


def team_config_spec_from_run(run: Mapping[str, Any]) -> Dict[str, Any]:
    return dict(team_config_from_run(run).get("spec") or default_team_config_spec())


def team_config_summary_from_run(run: Mapping[str, Any]) -> Dict[str, Any]:
    config = team_config_from_run(run)
    spec = team_config_spec_from_run(run)
    return {
        "source": str(config.get("source") or "").strip(),
        "loaded_at": str(config.get("loaded_at") or "").strip(),
        "harness": str(spec.get("harness") or "").strip(),
        "model": str(spec.get("model") or "").strip(),
        "worker_subagents": worker_subagents_from_run(run),
        "liveness": liveness_from_run(run),
    }


def liveness_from_run(run: Mapping[str, Any]) -> Dict[str, int]:
    spec = team_config_spec_from_run(run)
    raw = spec.get("liveness")
    if not isinstance(raw, dict):
        return default_liveness_spec()
    defaults = default_liveness_spec()
    out = dict(defaults)
    for key in defaults:
        try:
            out[key] = int(raw.get(key) or defaults[key])
        except Exception:
            out[key] = defaults[key]
    if out["stale_after_s"] >= out["dead_after_s"]:
        out["stale_after_s"] = defaults["stale_after_s"]
        out["dead_after_s"] = defaults["dead_after_s"]
    return out


def role_prompt_append_from_run(run: Mapping[str, Any], role: str) -> str:
    spec = team_config_spec_from_run(run)
    role_prompts = spec.get("role_prompts")
    if not isinstance(role_prompts, dict):
        return ""
    append = role_prompts.get("append")
    if not isinstance(append, dict):
        return ""
    return str(append.get(str(role or "").strip().lower()) or "").strip()


def worker_subagents_from_run(run: Mapping[str, Any]) -> str:
    spec = team_config_spec_from_run(run)
    worker = spec.get("worker")
    if not isinstance(worker, dict):
        return "encouraged"
    subagents = str(worker.get("subagents") or "").strip()
    return subagents or "encouraged"


__all__ = [
    "TeamConfigError",
    "default_liveness_spec",
    "default_team_config_spec",
    "liveness_from_run",
    "load_team_config_yaml",
    "normalize_team_config_spec",
    "role_prompt_append_from_run",
    "team_config_from_run",
    "team_config_spec_from_run",
    "team_config_summary_from_run",
    "worker_subagents_from_run",
]
