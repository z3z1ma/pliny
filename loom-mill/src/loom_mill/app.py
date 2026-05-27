import os
from contextlib import asynccontextmanager
from pathlib import Path

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route, WebSocketRoute

from loom_mill.api.design import create_chat_session, create_record, end_chat_session, get_chat_session, send_chat_message, transition_record, update_record
from loom_mill.api.records import get_record_content
from loom_mill.api.shaping import accept_staged_record, add_shaping_input, advance_shaping_session, cancel_shaping_exploration, commit_shaping_session, create_shaping_branch, create_shaping_session, create_staged_record, delete_shaping_session, delete_staged_record, edit_node, explore_shaping_session, get_shaping_context, get_shaping_session, list_shaping_explorations, list_shaping_sessions, merge_shaping_branch, reselect_option_node, select_option_node, switch_shaping_branch, update_staged_record
from loom_mill.api.shipping import abort_workstation, resolve_workstation, ship_workstation, shipping_queue, skip_workstation
from loom_mill.api.scheduling import scheduling_log, scheduling_queue, put_scheduling_enabled, put_scheduling_overrides
from loom_mill.api.workstation import (
    acknowledge_andon,
    delete_workstation,
    edit_workstation_ticket,
    get_aggregate_diff,
    get_config,
    get_harness_config,
    get_iteration,
    get_iteration_diff,
    get_workstation,
    get_workstation_logs,
    list_iterations,
    list_workstations,
    pause_workstation,
    put_config,
    put_harness_config,
    resume_workstation,
    start_workstation,
    stop_workstation,
    test_harness,
)
from loom_mill.api.ws import MillWebSocket
from loom_mill.state import MillStateStore
from loom_mill.watcher import LoomWatcher
from loom_mill.workstation.manager import WorkstationManager
from loom_mill.api.workstation import load_factory_config


async def health(request):
    return JSONResponse({"status": "ok"})


@asynccontextmanager
async def lifespan(app: Starlette):
    store = MillStateStore()
    app.state.store = store

    workspace_root = os.environ.get("LOOM_WORKSPACE_ROOT", ".")
    app.state.workspace_root = os.path.abspath(workspace_root)
    app.state.workstation_manager = WorkstationManager(
        Path(app.state.workspace_root),
        store,
        load_factory_config(Path(app.state.workspace_root) / ".mill" / "config.json"),
    )
    watcher = LoomWatcher(workspace_root, store=store)
    await watcher.start()
    
    yield
    
    await app.state.workstation_manager.shutdown()
    await watcher.stop()


def create_app() -> Starlette:
    return Starlette(
        debug=True,
        routes=[
            Route("/health", health),
            Route("/api/config/harness", get_harness_config, methods=["GET"]),
            Route("/api/config/harness", put_harness_config, methods=["PUT"]),
            Route("/harness/test", test_harness, methods=["POST"]),
            Route("/config", get_config, methods=["GET"]),
            Route("/config", put_config, methods=["PUT"]),
            Route("/records", create_record, methods=["POST"]),
            Route("/records/{record_id}/transition", transition_record, methods=["POST"]),
            Route("/records/{record_id:path}", update_record, methods=["PUT"]),
            Route("/records/{record_id:path}/content", get_record_content, methods=["GET"]),
            Route("/chat/sessions", create_chat_session, methods=["POST"]),
            Route("/chat/sessions/{session_id}", get_chat_session, methods=["GET"]),
            Route("/chat/sessions/{session_id}/messages", send_chat_message, methods=["POST"]),
            Route("/chat/sessions/{session_id}", end_chat_session, methods=["DELETE"]),
            Route("/shaping/sessions", create_shaping_session, methods=["POST"]),
            Route("/shaping/sessions", list_shaping_sessions, methods=["GET"]),
            Route("/shaping/sessions/{session_id}", get_shaping_session, methods=["GET"]),
            Route("/shaping/sessions/{session_id}/context", get_shaping_context, methods=["GET"]),
            Route("/shaping/sessions/{session_id}/input", add_shaping_input, methods=["POST"]),
            Route("/shaping/sessions/{session_id}/nodes/{node_id}/select", select_option_node, methods=["POST"]),
            Route("/shaping/sessions/{session_id}/nodes/{node_id}/edit", edit_node, methods=["POST"]),
            Route("/shaping/sessions/{session_id}/nodes/{node_id}/reselect", reselect_option_node, methods=["POST"]),
            Route("/shaping/sessions/{session_id}/advance", advance_shaping_session, methods=["POST"]),
            Route("/shaping/sessions/{session_id}/staged", create_staged_record, methods=["POST"]),
            Route("/shaping/sessions/{session_id}/staged/{temp_id}", update_staged_record, methods=["PUT"]),
            Route("/shaping/sessions/{session_id}/staged/{temp_id}", delete_staged_record, methods=["DELETE"]),
            Route("/shaping/sessions/{session_id}/staged/{temp_id}/accept", accept_staged_record, methods=["POST"]),
            Route("/shaping/sessions/{session_id}/branch", create_shaping_branch, methods=["POST"]),
            Route("/shaping/sessions/{session_id}/branch/{branch_id}/switch", switch_shaping_branch, methods=["POST"]),
            Route("/shaping/sessions/{session_id}/branch/{source}/merge", merge_shaping_branch, methods=["POST"]),
            Route("/shaping/sessions/{session_id}/commit", commit_shaping_session, methods=["POST"]),
            Route("/shaping/sessions/{session_id}/explore", explore_shaping_session, methods=["POST"]),
            Route("/shaping/sessions/{session_id}/explore/{invocation_id}/cancel", cancel_shaping_exploration, methods=["POST"]),
            Route("/shaping/sessions/{session_id}/explorations", list_shaping_explorations, methods=["GET"]),
            Route("/shaping/sessions/{session_id}", delete_shaping_session, methods=["DELETE"]),
            Route("/workstations", list_workstations, methods=["GET"]),
            Route("/workstations", start_workstation, methods=["POST"]),
            Route("/workstations/{workstation_id}", get_workstation, methods=["GET"]),
            Route("/workstations/{workstation_id}/iterations", list_iterations, methods=["GET"]),
            Route("/workstations/{workstation_id}/iterations/{iteration:int}", get_iteration, methods=["GET"]),
            Route("/workstations/{workstation_id}/iterations/{iteration:int}/diff", get_iteration_diff, methods=["GET"]),
            Route("/workstations/{workstation_id}/diff", get_aggregate_diff, methods=["GET"]),
            Route("/workstations/{workstation_id}/logs", get_workstation_logs, methods=["GET"]),
            Route("/workstations/{workstation_id}", delete_workstation, methods=["DELETE"]),
            Route("/workstations/{workstation_id}/pause", pause_workstation, methods=["POST"]),
            Route("/workstations/{workstation_id}/resume", resume_workstation, methods=["POST"]),
            Route("/shipping/queue", shipping_queue, methods=["GET"]),
            Route("/shipping/{workstation_id}/ship", ship_workstation, methods=["POST"]),
            Route("/shipping/{workstation_id}/skip", skip_workstation, methods=["POST"]),
            Route("/shipping/{workstation_id}/abort", abort_workstation, methods=["POST"]),
            Route("/shipping/{workstation_id}/resolve", resolve_workstation, methods=["POST"]),
            Route("/scheduling/queue", scheduling_queue, methods=["GET"]),
            Route("/scheduling/overrides", put_scheduling_overrides, methods=["PUT"]),
            Route("/scheduling/enabled", put_scheduling_enabled, methods=["PUT"]),
            Route("/scheduling/log", scheduling_log, methods=["GET"]),
            Route("/api/workstation/start", start_workstation, methods=["POST"]),
            Route("/api/workstation/{ticket_id}/edit", edit_workstation_ticket, methods=["POST"]),
            Route("/api/workstation/{ticket_id}/acknowledge-andon", acknowledge_andon, methods=["POST"]),
            Route("/api/workstation/{ticket_id}/pause", pause_workstation, methods=["POST"]),
            Route("/api/workstation/{ticket_id}/resume", resume_workstation, methods=["POST"]),
            Route("/api/workstation/{ticket_id}/stop", stop_workstation, methods=["POST"]),
            WebSocketRoute("/ws", MillWebSocket),
        ],
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176", "*"],
                allow_methods=["GET", "PUT", "POST", "DELETE"],
                allow_headers=["Content-Type"],
            )
        ],
        lifespan=lifespan,
    )


app = create_app()
