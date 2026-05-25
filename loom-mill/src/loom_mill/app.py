import asyncio
import os
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, WebSocketRoute

from loom_mill.api.ws import MillWebSocket
from loom_mill.state import MillStateStore
from loom_mill.watcher import LoomWatcher


async def health(request):
    return JSONResponse({"status": "ok"})


@asynccontextmanager
async def lifespan(app: Starlette):
    store = MillStateStore()
    app.state.store = store
    
    workspace_root = os.environ.get("LOOM_WORKSPACE_ROOT", ".")
    watcher = LoomWatcher(workspace_root, store=store)
    await watcher.start()
    
    yield
    
    await watcher.stop()


def create_app() -> Starlette:
    return Starlette(
        debug=True,
        routes=[
            Route("/health", health),
            WebSocketRoute("/ws", MillWebSocket),
        ],
        lifespan=lifespan,
    )


app = create_app()
