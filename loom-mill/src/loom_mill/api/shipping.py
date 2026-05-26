from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from starlette.requests import Request
from starlette.responses import JSONResponse

from loom_mill.shipping import ShippingDock, ShippingResult


def _dock(request: Request) -> ShippingDock:
    return ShippingDock(Path(request.app.state.workspace_root), request.app.state.workstation_manager)


def _result_payload(result: ShippingResult) -> dict:
    return asdict(result)


async def ship_workstation(request: Request) -> JSONResponse:
    return await _control_shipping(request, "ship")


async def skip_workstation(request: Request) -> JSONResponse:
    return await _control_shipping(request, "skip")


async def abort_workstation(request: Request) -> JSONResponse:
    return await _control_shipping(request, "abort")


async def resolve_workstation(request: Request) -> JSONResponse:
    return await _control_shipping(request, "resolve_conflict")


async def shipping_queue(request: Request) -> JSONResponse:
    return JSONResponse([asdict(entry) for entry in _dock(request).get_queue()])


async def _control_shipping(request: Request, method: str) -> JSONResponse:
    workstation_id = request.path_params["workstation_id"]
    try:
        result = await getattr(_dock(request), method)(workstation_id)
    except KeyError:
        return JSONResponse({"error": "workstation not found"}, status_code=404)
    except RuntimeError as error:
        return JSONResponse({"error": str(error)}, status_code=409)
    return JSONResponse(_result_payload(result))
