import asyncio
import json
from dataclasses import asdict, is_dataclass
from datetime import date
from pathlib import Path

from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket

from loom_mill.state import MillStateStore, ShippingEvent, WorkstationIterationCompleted, WorkstationOutput, WorkstationStateChanged, WorkstationTakt


def _json_default(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, Path):
        return str(obj)
    if is_dataclass(obj):
        return asdict(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


class MillWebSocket(WebSocketEndpoint):
    encoding = "text"

    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        store: MillStateStore = websocket.app.state.store
        
        # Send initial snapshot
        snapshot = await store.snapshot()
        await websocket.send_text(json.dumps({"type": "snapshot", "data": asdict(snapshot)}, default=_json_default))
        
        # Subscribe to events
        subscription = store.subscribe()
        websocket.scope["subscription"] = subscription
        websocket.scope["subscription_task"] = asyncio.create_task(self._pump_events(websocket, subscription))

    async def _pump_events(self, websocket: WebSocket, subscription) -> None:
        try:
            async for event in subscription:
                await websocket.send_text(json.dumps(_event_payload(event), default=_json_default))
        except asyncio.CancelledError:
            pass

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        subscription = websocket.scope.get("subscription")
        if subscription:
            await subscription.aclose()
        task = websocket.scope.get("subscription_task")
        if task:
            task.cancel()


def _event_payload(event) -> dict:
    if isinstance(event, WorkstationStateChanged):
        return {
            "workstation_id": event.workstation_id,
            "event": "state_change",
            "payload": asdict(event.workstation),
        }
    if isinstance(event, WorkstationOutput):
        return {
            "workstation_id": event.workstation_id,
            "event": "log",
            "payload": asdict(event.output),
        }
    if isinstance(event, WorkstationIterationCompleted):
        return {
            "workstation_id": event.workstation_id,
            "event": "iteration",
            "payload": asdict(event.iteration),
        }
    if isinstance(event, WorkstationTakt):
        return {
            "workstation_id": event.workstation_id,
            "event": "takt",
            "payload": {"iteration": event.iteration, "duration_seconds": event.duration_seconds},
        }
    if isinstance(event, ShippingEvent):
        payload = asdict(event)
        payload.pop("workstation_id")
        return {
            "workstation_id": event.workstation_id,
            "event": "shipping",
            "payload": payload,
        }
    return {"type": type(event).__name__, "data": asdict(event)}
