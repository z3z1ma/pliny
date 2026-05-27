from __future__ import annotations

import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from loom_mill.api import shaping
from loom_mill.api.ws import _event_payload
from loom_mill.app import create_app
from loom_mill.shaping import CanvasNode, CanvasNodeType, NodeStatus, SessionPhase, ShapingSession
from loom_mill.shaping.engine import ShapingEngine
from loom_mill.shaping.orchestrator import ShapingOrchestrator
from loom_mill.shaping.parser import parse_canvas_response
from loom_mill.shaping.prompts import build_canvas_prompt
from loom_mill.shaping.session import utc_now
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
    ):
        self.app = SimpleNamespace(
            state=SimpleNamespace(
                workspace_root=str(workspace_root),
                store=store,
                harness_config=harness_config or _printf_harness('<node type="observation">default</node>'),
            )
        )
        self._body = body or {}
        self.path_params = path_params or {}

    async def json(self):
        return self._body


def _body(response) -> dict:
    return json.loads(response.body)


def _printf_harness(output: str) -> HarnessConfig:
    return HarnessConfig(command="printf", args=[output])


def test_parse_canvas_response_question_record_option_group_and_fallback() -> None:
    question = parse_canvas_response('<node type="question" options="tickets,specs">Which surface?</node>')
    record = parse_canvas_response('<node type="record" surface="tickets" title="T"># T</node>')
    option_group = parse_canvas_response(
        '<node type="option-group" reasoning="tradeoff"><option label="A">Alpha</option><option label="B">Beta</option></node>'
        '<explore goal="inspect records"/>'
    )
    fallback = parse_canvas_response("plain observation")

    assert question.nodes[0].options == ["tickets", "specs"]
    assert record.nodes[0].surface == "tickets"
    assert record.nodes[0].title == "T"
    assert option_group.nodes[0].type == "option_group"
    assert option_group.nodes[0].option_labels == ["A", "B"]
    assert option_group.explore_goal == "inspect records"
    assert fallback.nodes[0].type == "observation"


def test_canvas_prompt_includes_context_history_and_phase() -> None:
    node = CanvasNode(
        id="n1",
        type=CanvasNodeType.INPUT,
        parent_id=None,
        status=NodeStatus.ACTIVE,
        timestamp=utc_now(),
        content={"text": "shape graph mode"},
        position=None,
    )

    prompt = build_canvas_prompt("context facts", [node], SessionPhase.EXPLORING)

    assert "## Current Phase: exploring" in prompt
    assert "context facts" in prompt
    assert "input: shape graph mode" in prompt
    assert "Respond with XML-like nodes" in prompt


@pytest.mark.asyncio
async def test_engine_advance_with_question_publishes_node_and_moves_to_narrowing(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a graph view")
    store = MillStateStore()
    output = '<node type="question" options="navigation, analysis">Is this for navigation or analysis?</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    subscription = store.subscribe()
    try:
        nodes = await engine.advance()
        events = [await subscription.__anext__(), await subscription.__anext__()]
    finally:
        await subscription.aclose()

    assert len(nodes) == 1
    assert nodes[0].type == CanvasNodeType.QUESTION
    assert nodes[0].content["question"] == "Is this for navigation or analysis?"
    assert session.state.phase == SessionPhase.NARROWING
    assert [_event_payload(event)["type"] for event in events] == ["shaping:node_added", "shaping:edge_added"]


@pytest.mark.asyncio
async def test_engine_advance_with_option_group_creates_option_nodes_and_edges(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a graph view")
    root_id = next(iter(session.state.nodes))
    store = MillStateStore()
    output = '<node type="option-group" reasoning="tradeoff"><option label="A">Alpha</option><option label="B">Beta</option></node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)

    nodes = await engine.advance()

    assert [node.type for node in nodes] == [CanvasNodeType.OPTION_GROUP, CanvasNodeType.OPTION, CanvasNodeType.OPTION]
    assert nodes[0].parent_id == root_id
    assert nodes[1].option_group_id == nodes[0].id
    assert nodes[1].parent_id == nodes[0].id
    assert nodes[2].parent_id == nodes[0].id
    assert [edge.type for edge in session.state.edges] == ["causal", "option_group", "option_group"]


@pytest.mark.asyncio
async def test_engine_advance_with_multiple_nodes_creates_siblings(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a graph view")
    root_id = next(iter(session.state.nodes))
    store = MillStateStore()
    output = (
        '<node type="observation">Existing context is enough.</node>'
        '<node type="question" options="Yes,No">Proceed?</node>'
    )
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)

    nodes = await engine.advance()

    assert [node.type for node in nodes] == [CanvasNodeType.OBSERVATION, CanvasNodeType.QUESTION]
    assert [node.parent_id for node in nodes] == [root_id, root_id]


@pytest.mark.asyncio
async def test_engine_advance_with_proposal_publishes_node_and_moves_to_proposing(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape notification bug")
    session.update_phase(SessionPhase.NARROWING)
    store = MillStateStore()
    output = (
        '<node type="record" surface="tickets" title="Fix notification label">'
        "# Fix notification label\n\nID: ticket:20260526-fix-notification-label\nType: Ticket\nStatus: open\n"
        "</node>"
    )
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)

    nodes = await engine.advance()

    assert nodes[0].type == CanvasNodeType.RECORD
    assert nodes[0].content["surface"] == "tickets"
    assert nodes[0].content["title"] == "Fix notification label"
    assert "Type: Ticket" in nodes[0].content["content"]
    assert nodes[0].content["temp_id"] == "temp:tickets:fix-notification-label"
    assert session.state.staged_records[0].temp_id == nodes[0].content["temp_id"]
    assert session.state.phase == SessionPhase.PROPOSING


@pytest.mark.asyncio
async def test_engine_transitions_to_refining_after_operator_feedback_on_proposal(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape notification bug")
    session.update_phase(SessionPhase.PROPOSING)
    session.add_node(
        CanvasNode(
            id="proposal-1",
            type=CanvasNodeType.RECORD,
            parent_id=None,
            status=NodeStatus.ACTIVE,
            timestamp=utc_now(),
            content={"surface": "tickets", "title": "Fix notification label", "content": "# Fix"},
            position=None,
        )
    )
    session.add_node(
        CanvasNode(
            id="input-2",
            type=CanvasNodeType.INPUT,
            parent_id=None,
            status=NodeStatus.ACTIVE,
            timestamp=utc_now(),
            content={"text": "split this"},
            position=None,
        )
    )
    store = MillStateStore()
    output = '<node type="observation">I will refine the proposal around the split.</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)

    nodes = await engine.advance()

    assert session.state.phase == SessionPhase.REFINING
    assert nodes[0].type == CanvasNodeType.OBSERVATION


@pytest.mark.asyncio
async def test_advance_endpoint_returns_nodes(tmp_path: Path) -> None:
    store = MillStateStore()
    harness = _printf_harness('<node type="observation">Existing context is enough to proceed.</node>')
    create_response = await shaping.create_shaping_session(Request(tmp_path, store, {"input": "initial"}, harness_config=harness))
    session_id = _body(create_response)["session_id"]

    response = await shaping.advance_shaping_session(Request(tmp_path, store, path_params={"session_id": session_id}, harness_config=harness))

    payload = _body(response)
    assert response.status_code == 200
    assert payload["session_id"] == session_id
    assert payload["nodes"][0]["type"] == "observation"
    assert payload["nodes"][0]["content"]["observation"] == "Existing context is enough to proceed."


@pytest.mark.asyncio
async def test_advance_endpoint_returns_system_node_for_missing_harness(tmp_path: Path) -> None:
    store = MillStateStore()
    harness = HarnessConfig(command="definitely-not-a-loom-mill-harness")
    create_response = await shaping.create_shaping_session(Request(tmp_path, store, {"input": "initial"}, harness_config=harness))
    session_id = _body(create_response)["session_id"]

    response = await shaping.advance_shaping_session(Request(tmp_path, store, path_params={"session_id": session_id}, harness_config=harness))

    payload = _body(response)
    assert response.status_code == 200
    assert payload["nodes"][0]["type"] == "observation"
    assert "Set up a harness in Settings" in payload["nodes"][0]["content"]["message"]


@pytest.mark.asyncio
async def test_advance_endpoint_returns_exploration_start_node(tmp_path: Path) -> None:
    store = MillStateStore()
    harness = _printf_harness('<explore goal="inspect scope"/>')
    create_response = await shaping.create_shaping_session(Request(tmp_path, store, {"input": "initial"}, harness_config=harness))
    session_id = _body(create_response)["session_id"]

    request = Request(tmp_path, store, path_params={"session_id": session_id}, harness_config=harness)
    response = await shaping.advance_shaping_session(request)
    orchestrator = request.app.state.shaping_orchestrators[session_id]
    for _ in range(100):
        if orchestrator.active_count == 0:
            break
        await asyncio.sleep(0.01)

    payload = _body(response)
    assert response.status_code == 200
    assert payload["nodes"][0]["type"] == "processing"
    assert payload["nodes"][0]["content"]["goal"] == "inspect scope"


def test_advance_route_is_registered() -> None:
    routes = [(route.path, route.methods or set()) for route in create_app().routes if hasattr(route, "methods")]

    assert any(route_path == "/shaping/sessions/{session_id}/advance" and "POST" in methods for route_path, methods in routes)
