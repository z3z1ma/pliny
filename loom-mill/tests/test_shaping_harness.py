from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from loom_mill.api import shaping
from loom_mill.api.ws import _event_payload
from loom_mill.shaping import BlockType, ShapingSession
from loom_mill.shaping.harness import InvocationConfig, run_bounded_invocation
from loom_mill.shaping.orchestrator import ShapingOrchestrator
from loom_mill.state import MillStateStore
from loom_mill.workstation.config import HarnessConfig


class Request:
    def __init__(
        self,
        workspace_root: Path,
        store: MillStateStore,
        body: dict | None = None,
        path_params: dict | None = None,
        harness_config: HarnessConfig | None = None,
        timeout_seconds: float = 120.0,
    ):
        self.app = SimpleNamespace(
            state=SimpleNamespace(
                workspace_root=str(workspace_root),
                store=store,
                harness_config=harness_config or _python_harness("print('## Summary')\nprint('default')"),
                shaping_timeout_seconds=timeout_seconds,
            )
        )
        self._body = body or {}
        self.path_params = path_params or {}

    async def json(self):
        return self._body


def _body(response) -> dict:
    return json.loads(response.body)


def _python_harness(code: str) -> HarnessConfig:
    return HarnessConfig(command=sys.executable, args=["-c", code])


async def _wait_for(predicate, timeout: float = 2.0) -> None:
    deadline = asyncio.get_running_loop().time() + timeout
    while not predicate():
        if asyncio.get_running_loop().time() > deadline:
            raise AssertionError("condition was not met before timeout")
        await asyncio.sleep(0.01)


@pytest.mark.asyncio
async def test_run_bounded_invocation_streams_output_and_extracts_summary(tmp_path: Path) -> None:
    script = """
import sys
prompt = sys.stdin.read()
print('saw goal' if 'inspect auth' in prompt else 'missing goal')
print('## Summary')
print('auth patterns found')
"""
    streamed: list[str] = []

    result = await run_bounded_invocation(
        InvocationConfig(
            goal="inspect auth",
            context_excerpt="existing context",
            command=sys.executable,
            args=["-c", script],
            cwd=str(tmp_path),
        ),
        "inv-1",
        on_stream=streamed.append,
    )

    assert result.exit_code == 0
    assert "saw goal" in result.output
    assert streamed == ["saw goal\n", "## Summary\n", "auth patterns found\n"]
    assert result.context_summary == "auth patterns found"


@pytest.mark.asyncio
async def test_parallel_explorations_complete_and_append_context(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "initial shaping goal")
    store = MillStateStore()
    script = """
import sys, time
prompt = sys.stdin.read()
goal = prompt.split('# Exploration Goal', 1)[1].split('# Session Context', 1)[0].strip()
time.sleep(0.05)
print('output for ' + goal)
print('## Summary')
print('summary for ' + goal)
"""
    orchestrator = ShapingOrchestrator(session, store, _python_harness(script))

    ids = await asyncio.gather(*(orchestrator.launch(f"goal {index}") for index in range(3)))
    await _wait_for(lambda: orchestrator.active_count == 0)

    context = session.read_context()
    assert len(set(ids)) == 3
    assert context.count("## Exploration: goal") == 3
    for index in range(3):
        assert f"summary for goal {index}" in context

    explorations = orchestrator.list_explorations()
    assert {item["status"] for item in explorations} == {"complete"}


@pytest.mark.asyncio
async def test_cancel_in_flight_exploration_records_system_block(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "initial")
    orchestrator = ShapingOrchestrator(
        session,
        MillStateStore(),
        _python_harness("import time\ntime.sleep(10)"),
    )

    invocation_id = await orchestrator.launch("slow exploration")
    assert await orchestrator.cancel(invocation_id) is True
    await _wait_for(lambda: orchestrator.active_count == 0)

    assert invocation_id not in session.state.active_explorations
    assert any(
        block.type == BlockType.SYSTEM and block.content.get("invocation_id") == invocation_id
        for block in session.state.blocks
    )
    assert orchestrator.list_explorations()[0]["status"] == "cancelled"


@pytest.mark.asyncio
async def test_timeout_kills_subprocess(tmp_path: Path) -> None:
    result = await run_bounded_invocation(
        InvocationConfig(
            goal="timeout",
            context_excerpt="",
            command=sys.executable,
            args=["-c", "import time\ntime.sleep(10)"],
            cwd=str(tmp_path),
            timeout_seconds=0.05,
        ),
        "inv-timeout",
    )

    assert result.exit_code != 0
    assert "Timed out after 0.05 seconds" in result.stderr
    assert result.duration_seconds < 2


@pytest.mark.asyncio
async def test_exploration_api_publishes_websocket_events(tmp_path: Path) -> None:
    store = MillStateStore()
    script = """
print('line one')
print('## Summary')
print('event summary')
"""
    harness = _python_harness(script)
    create_response = await shaping.create_shaping_session(Request(tmp_path, store, {"input": "initial"}, harness_config=harness))
    session_id = _body(create_response)["session_id"]
    request = Request(tmp_path, store, {"goal": "event exploration"}, {"session_id": session_id}, harness)
    subscription = store.subscribe()
    try:
        response = await shaping.explore_shaping_session(request)
        invocation_id = _body(response)["invocation_id"]
        events = []
        while not events or _event_payload(events[-1])["type"] != "shaping:exploration_complete":
            events.append(await asyncio.wait_for(subscription.__anext__(), timeout=1))
    finally:
        await subscription.aclose()

    payloads = [_event_payload(event) for event in events]
    assert payloads[0] == {
        "type": "shaping:exploration_start",
        "data": {"session_id": session_id, "invocation_id": invocation_id, "goal": "event exploration"},
    }
    assert any(payload["type"] == "shaping:exploration_stream" and payload["data"]["delta"] == "line one\n" for payload in payloads)
    assert payloads[-1]["type"] == "shaping:exploration_complete"


def test_exploration_routes_are_registered() -> None:
    from loom_mill.app import create_app

    routes = [(route.path, route.methods or set()) for route in create_app().routes if hasattr(route, "methods")]

    def has_route(path: str, method: str) -> bool:
        return any(route_path == path and method in methods for route_path, methods in routes)

    assert has_route("/shaping/sessions/{session_id}/explore", "POST")
    assert has_route("/shaping/sessions/{session_id}/explore/{invocation_id}/cancel", "POST")
    assert has_route("/shaping/sessions/{session_id}/explorations", "GET")
