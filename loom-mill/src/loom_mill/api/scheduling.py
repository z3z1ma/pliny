from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from starlette.requests import Request
from starlette.responses import JSONResponse

from loom_mill.api.workstation import load_factory_config, save_factory_config
from loom_mill.scheduling import ScheduleOverrides, SchedulingAgent


def _workspace_root(request: Request) -> Path:
    return Path(request.app.state.workspace_root)


def _config_path(request: Request) -> Path:
    return _workspace_root(request) / ".mill" / "config.json"


def _agent(request: Request) -> SchedulingAgent:
    return SchedulingAgent(_workspace_root(request), request.app.state.workstation_manager)


async def scheduling_queue(request: Request) -> JSONResponse:
    return JSONResponse(_agent(request).queue())


async def put_scheduling_overrides(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        pinned = data.get("pinned", [])
        excluded = data.get("excluded", [])
        if not isinstance(pinned, list) or not isinstance(excluded, list):
            raise ValueError("pinned and excluded must be lists")
    except (json.JSONDecodeError, ValueError) as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    overrides = _agent(request).save_overrides(ScheduleOverrides(pinned=[str(item) for item in pinned], excluded=[str(item) for item in excluded]))
    return JSONResponse(asdict(overrides))


async def put_scheduling_enabled(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        enabled = bool(data["enabled"])
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    existing = load_factory_config(_config_path(request))
    config = existing.__class__(
        max_workstations=existing.max_workstations,
        harness=existing.harness,
        shipping_mode=existing.shipping_mode,
        default_target_branch=existing.default_target_branch,
        cleanup_branch_after_merge=existing.cleanup_branch_after_merge,
        ready_to_ship_statuses=existing.ready_to_ship_statuses,
        scheduling_enabled=enabled,
        ready_ticket_statuses=existing.ready_ticket_statuses,
        spc_model=existing.spc_model,
    )
    save_factory_config(_config_path(request), config)
    request.app.state.workstation_manager.update_config(config)
    return JSONResponse({"enabled": config.scheduling_enabled})


async def scheduling_log(request: Request) -> JSONResponse:
    try:
        limit = int(request.query_params.get("limit", "100"))
    except ValueError:
        return JSONResponse({"error": "limit must be an integer"}, status_code=400)
    return JSONResponse(_agent(request).read_log(limit=limit))
