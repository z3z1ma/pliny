from __future__ import annotations

import asyncio
import json
from dataclasses import asdict
from pathlib import Path

from starlette.requests import Request
from starlette.responses import JSONResponse

from loom_mill.state import MillStateStore, WorkstationStateChanged
from loom_mill.workstation import HarnessConfig, WorkstationEngine, WorkstationState, WorkstationStatus


DEFAULT_HARNESS = HarnessConfig(command="opencode", args=["run", "--model", "gpt-5.5", "{ticket_path}"])


def _workspace_root(request: Request) -> Path:
    return Path(request.app.state.workspace_root)


def _config_path(request: Request) -> Path:
    return _workspace_root(request) / ".mill" / "config.json"


def _ticket_path(request: Request, ticket_id: str) -> Path:
    slug = ticket_id.removeprefix("ticket:")
    return _workspace_root(request) / ".loom" / "tickets" / f"{slug}.md"


def _state_payload(state: WorkstationState) -> dict:
    payload = asdict(state)
    if state.worktree_path is not None:
        payload["worktree_path"] = str(state.worktree_path)
    return payload


def _config_payload(config: HarnessConfig) -> dict:
    return {
        "command": config.command,
        "args": config.args,
        "env": config.env or {},
        "cwd": config.cwd,
    }


def _parse_config(data: dict) -> HarnessConfig:
    command = str(data.get("command") or "").strip()
    if not command:
        raise ValueError("command is required")

    args_value = data.get("args", [])
    if not isinstance(args_value, list):
        raise ValueError("args must be a list")
    args = [str(arg) for arg in args_value]

    env_value = data.get("env") or {}
    if not isinstance(env_value, dict):
        raise ValueError("env must be an object")
    env = {str(key): str(value) for key, value in env_value.items() if str(key).strip()}

    cwd_value = data.get("cwd")
    cwd = str(cwd_value).strip() if cwd_value else None
    return HarnessConfig(command=command, args=args, env=env, cwd=cwd)


def load_harness_config(config_path: Path) -> HarnessConfig:
    if not config_path.exists():
        return DEFAULT_HARNESS
    data = json.loads(config_path.read_text(encoding="utf-8"))
    return _parse_config(data.get("harness", data))


def save_harness_config(config_path: Path, config: HarnessConfig) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps({"harness": _config_payload(config)}, indent=2) + "\n", encoding="utf-8")


async def get_harness_config(request: Request) -> JSONResponse:
    return JSONResponse(_config_payload(load_harness_config(_config_path(request))))


async def put_harness_config(request: Request) -> JSONResponse:
    try:
        config = _parse_config(await request.json())
    except (json.JSONDecodeError, ValueError) as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    save_harness_config(_config_path(request), config)
    return JSONResponse(_config_payload(config))


async def start_workstation(request: Request) -> JSONResponse:
    data = await request.json()
    ticket_id = str(data.get("ticket_id") or "").removeprefix("ticket:")
    if not ticket_id:
        return JSONResponse({"error": "ticket_id is required"}, status_code=400)

    engines: dict[str, WorkstationEngine] = request.app.state.workstations
    for engine_ticket_id, engine in engines.items():
        if engine.state.status == WorkstationStatus.RUNNING:
            return JSONResponse({"error": f"workstation already running for {engine_ticket_id}"}, status_code=409)

    ticket_path = _ticket_path(request, ticket_id)
    if not ticket_path.exists():
        return JSONResponse({"error": "ticket not found"}, status_code=404)

    previous = engines.get(ticket_id)
    if previous is not None and previous.state.status != WorkstationStatus.RUNNING:
        await previous.teardown()

    engine = WorkstationEngine(_workspace_root(request), ticket_path, load_harness_config(_config_path(request)))
    engines[ticket_id] = engine
    state = await engine.start()
    await _publish_workstation(request, ticket_id, state)
    task = asyncio.create_task(_monitor_workstation(request.app.state.store, ticket_id, engine))
    request.app.state.workstation_tasks[ticket_id] = task
    return JSONResponse(_state_payload(state))


async def pause_workstation(request: Request) -> JSONResponse:
    return await _control_workstation(request, request.path_params["ticket_id"], WorkstationStatus.PAUSED)


async def stop_workstation(request: Request) -> JSONResponse:
    return await _control_workstation(request, request.path_params["ticket_id"], WorkstationStatus.STOPPED)


async def _control_workstation(request: Request, ticket_id: str, target_status: WorkstationStatus) -> JSONResponse:
    ticket_id = ticket_id.removeprefix("ticket:")
    engine = request.app.state.workstations.get(ticket_id)
    if engine is None:
        return JSONResponse({"error": "workstation not found"}, status_code=404)

    state = await (engine.pause() if target_status == WorkstationStatus.PAUSED else engine.stop())
    await _publish_workstation(request, ticket_id, state)
    if target_status == WorkstationStatus.STOPPED:
        await engine.teardown()
    return JSONResponse(_state_payload(state))


async def _publish_workstation(request: Request, ticket_id: str, state: WorkstationState) -> None:
    store: MillStateStore = request.app.state.store
    await store.replace_workstation_state(ticket_id, state)
    await store.publish(WorkstationStateChanged(ticket_id=ticket_id, workstation=state))


async def _monitor_workstation(store: MillStateStore, ticket_id: str, engine: WorkstationEngine) -> None:
    await engine.wait()
    await store.replace_workstation_state(ticket_id, engine.state)
    await store.publish(WorkstationStateChanged(ticket_id=ticket_id, workstation=engine.state))
