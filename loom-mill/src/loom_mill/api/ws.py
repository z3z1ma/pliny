import asyncio
import json
from dataclasses import asdict, is_dataclass
from datetime import date
from pathlib import Path

from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket

from loom_mill.state import MillStateStore


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
                event_type = type(event).__name__
                await websocket.send_text(json.dumps({"type": event_type, "data": asdict(event)}, default=_json_default))
        except asyncio.CancelledError:
            pass

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        subscription = websocket.scope.get("subscription")
        if subscription:
            await subscription.aclose()
        task = websocket.scope.get("subscription_task")
        if task:
            task.cancel()
