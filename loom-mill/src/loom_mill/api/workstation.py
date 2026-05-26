from __future__ import annotations

import asyncio
import json
import os
import shlex
import sys
from collections import deque
from dataclasses import asdict
from pathlib import Path

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from loom_mill.iterations import IterationStore
from loom_mill.state import WorkstationStateChanged
from loom_mill.workstation import FactoryConfig, HarnessConfig, WorkstationState, WorkstationStatus
from loom_mill.workstation.manager import WorkstationManager


DEFAULT_CONFIG = FactoryConfig()


def _workspace_root(request: Request) -> Path:
    return Path(request.app.state.workspace_root)


def _config_path(request: Request) -> Path:
    return _workspace_root(request) / ".mill" / "config.json"


def _ticket_path(request: Request, ticket_id: str) -> Path:
    slug = ticket_id.removeprefix("ticket:")
    return _workspace_root(request) / ".loom" / "tickets" / f"{slug}.md"


def _manager(request: Request) -> WorkstationManager:
    return request.app.state.workstation_manager


def _state_payload(state: WorkstationState) -> dict:
    payload = asdict(state)
    if state.worktree_path is not None:
        payload["worktree_path"] = str(state.worktree_path)
    return payload


def _iteration_store(request: Request, workstation_id: str) -> IterationStore:
    return IterationStore(_workspace_root(request), workstation_id)


def _harness_payload(config: HarnessConfig) -> dict:
    return {
        "command": config.command,
        "args": config.args,
        "env": config.env or {},
        "cwd": config.cwd,
    }


def _config_payload(config: FactoryConfig) -> dict:
    return {
        "max_workstations": config.max_workstations,
        "harness": _harness_payload(config.harness),
        "shipping_mode": config.shipping_mode,
        "default_target_branch": config.default_target_branch,
        "cleanup_branch_after_merge": config.cleanup_branch_after_merge,
        "ready_to_ship_statuses": config.ready_to_ship_statuses,
        "scheduling_enabled": config.scheduling_enabled,
        "ready_ticket_statuses": config.ready_ticket_statuses,
        "spc_enabled": config.spc_enabled,
        "spc_model": config.spc_model,
        "spc_thresholds": config.spc_thresholds,
        "spc_timeout_seconds": config.spc_timeout_seconds,
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


def load_factory_config(config_path: Path) -> FactoryConfig:
    if not config_path.exists():
        return DEFAULT_CONFIG
    data = json.loads(config_path.read_text(encoding="utf-8"))
    harness = _parse_config(data.get("harness", data))
    max_workstations = int(data.get("max_workstations", 1))
    if max_workstations < 1:
        raise ValueError("max_workstations must be at least 1")
    shipping_mode = str(data.get("shipping_mode", DEFAULT_CONFIG.shipping_mode))
    if shipping_mode not in {"auto-merge", "operator-approved"}:
        raise ValueError("shipping_mode must be auto-merge or operator-approved")
    statuses = data.get("ready_to_ship_statuses", DEFAULT_CONFIG.ready_to_ship_statuses)
    if not isinstance(statuses, list):
        raise ValueError("ready_to_ship_statuses must be a list")
    ready_ticket_statuses = data.get("ready_ticket_statuses", DEFAULT_CONFIG.ready_ticket_statuses)
    if not isinstance(ready_ticket_statuses, list):
        raise ValueError("ready_ticket_statuses must be a list")
    return FactoryConfig(
        max_workstations=max_workstations,
        harness=harness,
        shipping_mode=shipping_mode,
        default_target_branch=str(data.get("default_target_branch", DEFAULT_CONFIG.default_target_branch)),
        cleanup_branch_after_merge=bool(data.get("cleanup_branch_after_merge", DEFAULT_CONFIG.cleanup_branch_after_merge)),
        ready_to_ship_statuses=[str(status) for status in statuses],
        scheduling_enabled=bool(data.get("scheduling_enabled", DEFAULT_CONFIG.scheduling_enabled)),
        ready_ticket_statuses=[str(status) for status in ready_ticket_statuses],
        spc_enabled=bool(data.get("spc_enabled", DEFAULT_CONFIG.spc_enabled)),
        spc_model=str(data.get("spc_model") or ""),
        spc_thresholds=dict(data.get("spc_thresholds", DEFAULT_CONFIG.spc_thresholds)),
        spc_timeout_seconds=float(data.get("spc_timeout_seconds", DEFAULT_CONFIG.spc_timeout_seconds)),
    )


def load_harness_config(config_path: Path) -> HarnessConfig:
    return load_factory_config(config_path).harness


def save_factory_config(config_path: Path, config: FactoryConfig) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(_config_payload(config), indent=2) + "\n", encoding="utf-8")


def save_harness_config(config_path: Path, config: HarnessConfig) -> None:
    existing = load_factory_config(config_path)
    save_factory_config(
        config_path,
        FactoryConfig(
            max_workstations=existing.max_workstations,
            harness=config,
            shipping_mode=existing.shipping_mode,
            default_target_branch=existing.default_target_branch,
            cleanup_branch_after_merge=existing.cleanup_branch_after_merge,
            ready_to_ship_statuses=existing.ready_to_ship_statuses,
            scheduling_enabled=existing.scheduling_enabled,
            ready_ticket_statuses=existing.ready_ticket_statuses,
            spc_enabled=existing.spc_enabled,
            spc_model=existing.spc_model,
            spc_thresholds=existing.spc_thresholds,
            spc_timeout_seconds=existing.spc_timeout_seconds,
        ),
    )


async def get_harness_config(request: Request) -> JSONResponse:
    return JSONResponse(_harness_payload(load_harness_config(_config_path(request))))


async def put_harness_config(request: Request) -> JSONResponse:
    try:
        config = _parse_config(await request.json())
    except (json.JSONDecodeError, ValueError) as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    save_harness_config(_config_path(request), config)
    _manager(request).update_config(load_factory_config(_config_path(request)))
    return JSONResponse(_harness_payload(config))


async def test_harness(request: Request) -> JSONResponse:
    """Run configured harness command with --version to verify it works."""
    config = load_harness_config(_config_path(request))
    cmd = [config.command, "--version"]
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=5.0)
        output = stdout.decode(errors="replace").strip()[:500]
        if not output:
            output = stderr.decode(errors="replace").strip()[:500]
        return JSONResponse({"success": proc.returncode == 0, "output": output})
    except FileNotFoundError:
        return JSONResponse({"success": False, "error": f"Command not found: {cmd[0]}"})
    except asyncio.TimeoutError:
        return JSONResponse({"success": False, "error": "Command timed out (5s)"})
    except Exception as error:
        return JSONResponse({"success": False, "error": str(error)})


async def get_config(request: Request) -> JSONResponse:
    return JSONResponse(_config_payload(load_factory_config(_config_path(request))))


async def put_config(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        existing = load_factory_config(_config_path(request))
        harness = _parse_config(data["harness"]) if isinstance(data.get("harness"), dict) else existing.harness
        max_workstations = int(data.get("max_workstations", existing.max_workstations))
        if max_workstations < 1:
            raise ValueError("max_workstations must be at least 1")
        shipping_mode = str(data.get("shipping_mode", existing.shipping_mode))
        if shipping_mode not in {"auto-merge", "operator-approved"}:
            raise ValueError("shipping_mode must be auto-merge or operator-approved")
        statuses = data.get("ready_to_ship_statuses", existing.ready_to_ship_statuses)
        if not isinstance(statuses, list):
            raise ValueError("ready_to_ship_statuses must be a list")
        ready_ticket_statuses = data.get("ready_ticket_statuses", existing.ready_ticket_statuses)
        if not isinstance(ready_ticket_statuses, list):
            raise ValueError("ready_ticket_statuses must be a list")
        spc_thresholds = data.get("spc_thresholds", existing.spc_thresholds)
        if not isinstance(spc_thresholds, dict):
            raise ValueError("spc_thresholds must be an object")
    except (json.JSONDecodeError, TypeError, ValueError) as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    config = FactoryConfig(
        max_workstations=max_workstations,
        harness=harness,
        shipping_mode=shipping_mode,
        default_target_branch=str(data.get("default_target_branch", existing.default_target_branch)),
        cleanup_branch_after_merge=bool(data.get("cleanup_branch_after_merge", existing.cleanup_branch_after_merge)),
        ready_to_ship_statuses=[str(status) for status in statuses],
        scheduling_enabled=bool(data.get("scheduling_enabled", existing.scheduling_enabled)),
        ready_ticket_statuses=[str(status) for status in ready_ticket_statuses],
        spc_enabled=bool(data.get("spc_enabled", existing.spc_enabled)),
        spc_model=str(data.get("spc_model") or ""),
        spc_thresholds=spc_thresholds,
        spc_timeout_seconds=float(data.get("spc_timeout_seconds", existing.spc_timeout_seconds)),
    )
    save_factory_config(_config_path(request), config)
    _manager(request).update_config(config)
    return JSONResponse(_config_payload(config))


async def start_workstation(request: Request) -> JSONResponse:
    data = await request.json()
    ticket_id = str(data.get("ticket_id") or "").removeprefix("ticket:")
    if not ticket_id:
        return JSONResponse({"error": "ticket_id is required"}, status_code=400)

    ticket_path = _ticket_path(request, ticket_id)
    if not ticket_path.exists():
        return JSONResponse({"error": "ticket not found"}, status_code=404)

    try:
        harness = _parse_config(data["harness"]) if isinstance(data.get("harness"), dict) else None
        engine = await _manager(request).start(ticket_path, ticket_id, harness=harness)
    except (RuntimeError, ValueError) as error:
        return JSONResponse({"error": str(error)}, status_code=409)
    state = engine.state
    return JSONResponse(_state_payload(state))


async def list_workstations(request: Request) -> JSONResponse:
    return JSONResponse([_state_payload(state) for state in _manager(request).list()])


async def get_workstation(request: Request) -> JSONResponse:
    engine = _manager(request).get(request.path_params["workstation_id"])
    if engine is None:
        return JSONResponse({"error": "workstation not found"}, status_code=404)
    return JSONResponse(_state_payload(engine.state))


async def list_iterations(request: Request) -> JSONResponse:
    store = _iteration_store(request, request.path_params["workstation_id"])
    return JSONResponse([asdict(record) for record in store.list()])


async def get_iteration(request: Request) -> JSONResponse:
    store = _iteration_store(request, request.path_params["workstation_id"])
    try:
        record = store.get(int(request.path_params["iteration"]))
    except (FileNotFoundError, ValueError):
        return JSONResponse({"error": "iteration not found"}, status_code=404)
    return JSONResponse(asdict(record))


async def get_iteration_diff(request: Request) -> Response:
    store = _iteration_store(request, request.path_params["workstation_id"])
    try:
        iteration = int(request.path_params["iteration"])
    except ValueError:
        return JSONResponse({"error": "iteration not found"}, status_code=404)
    diff = store.diff(iteration)
    if diff is None:
        return JSONResponse({"error": "iteration diff not found"}, status_code=404)
    return Response(diff, media_type="text/plain")


async def get_aggregate_diff(request: Request) -> Response:
    store = _iteration_store(request, request.path_params["workstation_id"])
    return Response(store.aggregate_diff(), media_type="text/plain")


async def get_workstation_logs(request: Request) -> JSONResponse:
    engine = _manager(request).get(request.path_params["workstation_id"])
    if engine is None:
        return JSONResponse({"error": "workstation not found"}, status_code=404)

    stream = str(request.query_params.get("stream", "stdout"))
    if stream not in {"stdout", "stderr"}:
        return JSONResponse({"error": "stream must be stdout or stderr"}, status_code=400)

    try:
        tail = int(request.query_params.get("tail", "100"))
    except ValueError:
        return JSONResponse({"error": "tail must be an integer"}, status_code=400)
    if tail < 0:
        return JSONResponse({"error": "tail must be non-negative"}, status_code=400)

    log_path = engine.log_path(stream)
    lines: deque[str] = deque(maxlen=tail)
    if log_path.exists() and tail > 0:
        with log_path.open(encoding="utf-8") as log_file:
            for line in log_file:
                lines.append(line.rstrip("\r\n"))
    return JSONResponse({"workstation_id": engine.workstation_id, "stream": stream, "lines": list(lines)})


async def delete_workstation(request: Request) -> JSONResponse:
    workstation_id = request.path_params["workstation_id"]
    try:
        state = await _manager(request).stop(workstation_id, remove=True)
    except KeyError:
        return JSONResponse({"error": "workstation not found"}, status_code=404)
    return JSONResponse(_state_payload(state))


async def pause_workstation(request: Request) -> JSONResponse:
    return await _control_workstation(request, request.path_params.get("workstation_id") or request.path_params["ticket_id"], WorkstationStatus.PAUSED)


async def resume_workstation(request: Request) -> JSONResponse:
    workstation_id = request.path_params.get("workstation_id") or request.path_params["ticket_id"]
    engine = _get_engine_by_route_param(request, workstation_id)
    if engine is None:
        return JSONResponse({"error": "workstation not found"}, status_code=404)
    if engine.state.status != WorkstationStatus.PAUSED:
        return JSONResponse({"error": "workstation is not paused"}, status_code=409)

    try:
        state = await _manager(request).resume(engine.workstation_id)
    except RuntimeError as error:
        return JSONResponse({"error": str(error)}, status_code=409)
    return JSONResponse(_state_payload(state))


async def acknowledge_andon(request: Request) -> JSONResponse:
    ticket_id = request.path_params["ticket_id"].removeprefix("ticket:")
    engine = _manager(request).get_by_ticket(ticket_id)
    if engine is None:
        return JSONResponse({"error": "workstation not found"}, status_code=404)

    state = engine.acknowledge_andon()
    await request.app.state.store.replace_workstation_state(engine.workstation_id, state)
    await request.app.state.store.publish(WorkstationStateChanged(workstation_id=engine.workstation_id, workstation=state))
    return JSONResponse(_state_payload(state))


async def stop_workstation(request: Request) -> JSONResponse:
    return await _control_workstation(request, request.path_params.get("workstation_id") or request.path_params["ticket_id"], WorkstationStatus.STOPPED)


async def edit_workstation_ticket(request: Request) -> JSONResponse:
    ticket_id = request.path_params["ticket_id"].removeprefix("ticket:")
    ticket_path = _ticket_path(request, ticket_id)
    if not ticket_path.exists():
        return JSONResponse({"error": "ticket not found"}, status_code=404)

    editor = os.environ.get("EDITOR")
    if editor:
        command = [*shlex.split(editor), str(ticket_path)]
    elif sys.platform == "darwin":
        command = ["open", str(ticket_path)]
    else:
        return JSONResponse({"error": "EDITOR is not configured"}, status_code=409)

    try:
        await asyncio.create_subprocess_exec(
            *command,
            cwd=_workspace_root(request),
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
    except OSError as error:
        return JSONResponse({"error": f"failed to open editor: {error}"}, status_code=500)

    return JSONResponse({"path": str(ticket_path)})


async def _control_workstation(request: Request, ticket_id: str, target_status: WorkstationStatus) -> JSONResponse:
    engine = _get_engine_by_route_param(request, ticket_id)
    if engine is None:
        return JSONResponse({"error": "workstation not found"}, status_code=404)

    try:
        state = await (
            _manager(request).pause(engine.workstation_id)
            if target_status == WorkstationStatus.PAUSED
            else _manager(request).stop(engine.workstation_id, remove=False)
        )
    except RuntimeError as error:
        return JSONResponse({"error": str(error)}, status_code=409)
    return JSONResponse(_state_payload(state))


def _get_engine_by_route_param(request: Request, value: str):
    manager = _manager(request)
    return manager.get(value) or manager.get_by_ticket(value)
