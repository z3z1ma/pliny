import asyncio
import os
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route, WebSocketRoute

from loom_mill.api.workstation import get_harness_config, pause_workstation, put_harness_config, start_workstation, stop_workstation
from loom_mill.api.ws import MillWebSocket
from loom_mill.state import MillStateStore
from loom_mill.watcher import LoomWatcher


async def health(request):
    return JSONResponse({"status": "ok"})


@asynccontextmanager
async def lifespan(app: Starlette):
    store = MillStateStore()
    app.state.store = store
    app.state.workstations = {}
    app.state.workstation_tasks = {}

    workspace_root = os.environ.get("LOOM_WORKSPACE_ROOT", ".")
    app.state.workspace_root = os.path.abspath(workspace_root)
    watcher = LoomWatcher(workspace_root, store=store)
    await watcher.start()
    
    yield
    
    for engine in app.state.workstations.values():
        if engine.state.status == "running":
            await engine.stop()
    for task in app.state.workstation_tasks.values():
        task.cancel()
    await asyncio.gather(*app.state.workstation_tasks.values(), return_exceptions=True)
    await watcher.stop()


def create_app() -> Starlette:
    return Starlette(
        debug=True,
        routes=[
            Route("/health", health),
            Route("/api/config/harness", get_harness_config, methods=["GET"]),
            Route("/api/config/harness", put_harness_config, methods=["PUT"]),
            Route("/api/workstation/start", start_workstation, methods=["POST"]),
            Route("/api/workstation/{ticket_id}/pause", pause_workstation, methods=["POST"]),
            Route("/api/workstation/{ticket_id}/stop", stop_workstation, methods=["POST"]),
            WebSocketRoute("/ws", MillWebSocket),
        ],
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                allow_methods=["GET", "PUT", "POST"],
                allow_headers=["Content-Type"],
            )
        ],
        lifespan=lifespan,
    )


app = create_app()
