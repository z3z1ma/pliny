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


def test_parse_canvas_response_ignores_ops_inside_record_markdown() -> None:
    parsed = parse_canvas_response(
        '<node type="record" surface="specs" title="Spec">'
        '# Spec\n\nLiteral node example: <node type="observation">Example</node>\n'
        'Literal closing tag example: </node>\n'
        'Literal op example: <op kind="discard-staged" temp_id="temp:specs:kept"/>\n'
        '</node>'
    )

    assert parsed.ops == []
    assert len(parsed.nodes) == 1
    assert '<op kind="discard-staged"' in parsed.nodes[0].content


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

    prompt = build_canvas_prompt("context facts", "graph view text", [node], SessionPhase.EXPLORING)

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
    collected: list[dict] = []
    try:
        nodes = await engine.advance()
        # Drain multiple events including possible advance_stream events
        for _ in range(5):
            try:
                event = await asyncio.wait_for(subscription.__anext__(), timeout=1.0)
            except (StopAsyncIteration, asyncio.TimeoutError):
                break
            collected.append(_event_payload(event))
    finally:
        await subscription.aclose()

    assert len(nodes) == 1
    assert nodes[0].type == CanvasNodeType.QUESTION
    assert nodes[0].content["question"] == "Is this for navigation or analysis?"
    assert session.state.phase == SessionPhase.NARROWING
    # Filter for the node/edge events we care about
    node_edge_events = [e["type"] for e in collected if e["type"] in ("shaping:node_added", "shaping:edge_added")]
    assert node_edge_events == ["shaping:node_added", "shaping:edge_added"]


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
async def test_engine_regenerate_removes_stale_direct_subtree_and_replaces_children(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a graph view")
    root_id = next(iter(session.state.nodes))
    session.add_node_with_edge(
        CanvasNode(
            id="stale-child",
            type=CanvasNodeType.OBSERVATION,
            parent_id=root_id,
            status=NodeStatus.STALE,
            content={"observation": "old"},
            position=None,
            timestamp=utc_now(),
        )
    )
    session.add_node_with_edge(
        CanvasNode(
            id="stale-grandchild",
            type=CanvasNodeType.QUESTION,
            parent_id="stale-child",
            status=NodeStatus.STALE,
            content={"question": "old question"},
            position=None,
            timestamp=utc_now(),
        )
    )
    store = MillStateStore()
    output = '<node type="observation">replacement child</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)

    nodes = await engine.regenerate(root_id, max_depth=3)

    assert "stale-child" not in session.state.nodes
    assert "stale-grandchild" not in session.state.nodes
    assert all(edge.source_id != "stale-child" and edge.target_id != "stale-child" for edge in session.state.edges)
    assert len(nodes) == 1
    assert nodes[0].parent_id == root_id
    assert nodes[0].content["observation"] == "replacement child"


@pytest.mark.asyncio
async def test_engine_regenerate_max_depth_zero_does_not_remove_or_advance(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a graph view")
    root_id = next(iter(session.state.nodes))
    session.add_node_with_edge(
        CanvasNode(
            id="stale-child",
            type=CanvasNodeType.OBSERVATION,
            parent_id=root_id,
            status=NodeStatus.STALE,
            content={"observation": "old"},
            position=None,
            timestamp=utc_now(),
        )
    )
    store = MillStateStore()
    output = '<node type="observation">replacement child</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)

    nodes = await engine.regenerate(root_id, max_depth=0)

    assert nodes == []
    assert "stale-child" in session.state.nodes
    assert [node.parent_id for node in session.state.nodes.values()].count(root_id) == 1


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


@pytest.mark.asyncio
async def test_advance_maps_tension_node_type(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    store = MillStateStore()
    output = '<node type="tension">Cache vs freshness.</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    nodes = await engine.advance()
    assert nodes[0].type == CanvasNodeType.TENSION
    assert nodes[0].content["tension"] == "Cache vs freshness."


@pytest.mark.asyncio
async def test_advance_maps_framing_node_type(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    store = MillStateStore()
    output = '<node type="framing">We need cache invalidation.</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    nodes = await engine.advance()
    assert nodes[0].type == CanvasNodeType.FRAMING
    assert nodes[0].content["framing"] == "We need cache invalidation."


@pytest.mark.asyncio
async def test_advance_maps_decision_node_type(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    store = MillStateStore()
    output = '<node type="decision">Use LRU cache.</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    nodes = await engine.advance()
    assert nodes[0].type == CanvasNodeType.DECISION
    assert nodes[0].content["decision"] == "Use LRU cache."


@pytest.mark.asyncio
async def test_advance_applies_discard_staged_op(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    session.staging.propose("specs", "Doomed", "# doomed", "main")
    store = MillStateStore()
    output = '<op kind="discard-staged" temp_id="temp:specs:doomed"/>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    await engine.advance()
    temp_ids = {r.temp_id for r in session.state.staged_records}
    assert "temp:specs:doomed" not in temp_ids


@pytest.mark.asyncio
async def test_advance_supersede_consolidates_without_double_add(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    session.staging.propose("specs", "Spec A", "# A", "main")
    session.staging.propose("specs", "Spec B", "# B", "main")
    store = MillStateStore()
    output = (
        '<op kind="supersede" targets="temp:specs:spec-a,temp:specs:spec-b"/>'
        '<node type="record" surface="specs" title="Spec Merged"># Merged</node>'
    )
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    await engine.advance()
    temp_ids = {r.temp_id for r in session.state.staged_records}
    assert "temp:specs:spec-merged" in temp_ids
    assert "temp:specs:spec-a" not in temp_ids
    assert "temp:specs:spec-b" not in temp_ids


@pytest.mark.asyncio
async def test_advance_bad_op_fails_closed_with_observation(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    store = MillStateStore()
    output = '<op kind="discard-staged" temp_id="temp:specs:nonexistent"/>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    nodes = await engine.advance()
    assert any(n.type == CanvasNodeType.OBSERVATION and "could not be applied" in str(n.content) for n in nodes)


@pytest.mark.asyncio
async def test_advance_edit_staged_updates_record(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    session.staging.propose("specs", "Draft", "# Draft", "main")
    store = MillStateStore()
    output = (
        '<op kind="edit-staged" temp_id="temp:specs:draft"/>'
        '<node type="record" surface="specs" title="Draft"># Revised</node>'
    )
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    await engine.advance()
    record = next(r for r in session.state.staged_records if r.temp_id == "temp:specs:draft")
    assert record.content == "# Revised"
    assert record.status == "modified"


@pytest.mark.asyncio
async def test_advance_continue_op_changes_parent(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    store = MillStateStore()
    output1 = '<node type="observation">Root</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output1)), store)
    root_nodes = await engine.advance()
    root_id = root_nodes[0].id

    output2 = f'<op kind="continue" from="{root_id}"/><node type="observation">Child</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output2)), store)
    child_nodes = await engine.advance()
    # the appended child observation should attach to root_id
    assert any(n.parent_id == root_id and n.content.get("observation") == "Child" for n in child_nodes)


@pytest.mark.asyncio
async def test_advance_continue_unknown_node_fails_closed(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    store = MillStateStore()
    output = '<op kind="continue" from="does-not-exist"/><node type="observation">Child</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    nodes = await engine.advance()
    assert any(n.type == CanvasNodeType.OBSERVATION and "unknown node" in str(n.content) for n in nodes)
    assert not any(n.content.get("observation") == "Child" for n in nodes)


@pytest.mark.asyncio
async def test_advance_continue_unknown_node_skips_other_mutation_ops(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    record = session.staging.propose("specs", "Draft", "# Draft", "main")
    store = MillStateStore()
    output = f'<op kind="continue" from="does-not-exist"/><op kind="discard-staged" temp_id="{record.temp_id}"/>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)

    nodes = await engine.advance()

    assert any(n.type == CanvasNodeType.OBSERVATION and "unknown node" in str(n.content) for n in nodes)
    assert [r.temp_id for r in session.state.staged_records] == [record.temp_id]


@pytest.mark.asyncio
async def test_advance_revise_unknown_node_fails_closed_without_paired_node(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    store = MillStateStore()
    output = '<op kind="revise" node="does-not-exist"/><node type="observation">Replacement</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)

    nodes = await engine.advance()

    assert any(n.type == CanvasNodeType.OBSERVATION and "unknown node" in str(n.content) for n in nodes)
    assert not any(n.content.get("observation") == "Replacement" for n in nodes)


@pytest.mark.asyncio
async def test_advance_invalid_parent_op_does_not_stale_valid_revise_target(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    root_id = next(iter(session.state.nodes))
    child = CanvasNode(
        id="child",
        type=CanvasNodeType.OBSERVATION,
        parent_id=root_id,
        status=NodeStatus.ACTIVE,
        content={"observation": "child"},
        position=None,
        timestamp=utc_now(),
    )
    session.add_node(child)
    store = MillStateStore()
    output = f'<op kind="revise" node="{root_id}"/><op kind="continue" from="missing"/><node type="observation">Replacement</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)

    nodes = await engine.advance()

    assert any(n.type == CanvasNodeType.OBSERVATION and "unknown node" in str(n.content) for n in nodes)
    assert session.state.nodes["child"].status == NodeStatus.ACTIVE
    assert not any(n.content.get("observation") == "Replacement" for n in nodes)


@pytest.mark.asyncio
async def test_advance_revise_stales_full_descendant_subtree(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    root_id = next(iter(session.state.nodes))
    child = CanvasNode(
        id="child",
        type=CanvasNodeType.OBSERVATION,
        parent_id=root_id,
        status=NodeStatus.ACTIVE,
        content={"observation": "child"},
        position=None,
        timestamp=utc_now(),
    )
    grandchild = CanvasNode(
        id="grandchild",
        type=CanvasNodeType.OBSERVATION,
        parent_id="child",
        status=NodeStatus.ACTIVE,
        content={"observation": "grandchild"},
        position=None,
        timestamp=utc_now(),
    )
    session.add_node(child)
    session.add_node(grandchild)
    store = MillStateStore()
    output = f'<op kind="revise" node="{root_id}"/><node type="observation">Replacement</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)

    nodes = await engine.advance()

    assert session.state.nodes["child"].status == NodeStatus.STALE
    assert session.state.nodes["grandchild"].status == NodeStatus.STALE
    assert any(n.parent_id == root_id and n.content.get("observation") == "Replacement" for n in nodes)


@pytest.mark.asyncio
async def test_advance_revise_publishes_descendant_invalidations(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    root_id = next(iter(session.state.nodes))
    child = CanvasNode(
        id="child",
        type=CanvasNodeType.OBSERVATION,
        parent_id=root_id,
        status=NodeStatus.ACTIVE,
        content={"observation": "child"},
        position=None,
        timestamp=utc_now(),
    )
    grandchild = CanvasNode(
        id="grandchild",
        type=CanvasNodeType.OBSERVATION,
        parent_id="child",
        status=NodeStatus.ACTIVE,
        content={"observation": "grandchild"},
        position=None,
        timestamp=utc_now(),
    )
    session.add_node(child)
    session.add_node(grandchild)
    store = MillStateStore()
    output = f'<op kind="revise" node="{root_id}"/><node type="observation">Replacement</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    subscription = store.subscribe()
    collected: list[dict] = []
    try:
        await engine.advance()
        for _ in range(8):
            try:
                event = await asyncio.wait_for(subscription.__anext__(), timeout=1.0)
            except (StopAsyncIteration, asyncio.TimeoutError):
                break
            collected.append(_event_payload(event))
    finally:
        await subscription.aclose()

    invalidations = [event for event in collected if event["type"] == "shaping:node_invalidated"]
    assert invalidations
    assert invalidations[0]["data"]["node_ids"] == ["child", "grandchild"]


@pytest.mark.asyncio
async def test_advance_discard_accepted_staged_op_reports_error_and_keeps_record(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    record = session.staging.propose("specs", "Accepted", "# Accepted", "main")
    session.staging.accept(record.temp_id)
    store = MillStateStore()
    output = f'<op kind="discard-staged" temp_id="{record.temp_id}"/>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)

    nodes = await engine.advance()

    assert any(n.type == CanvasNodeType.OBSERVATION and "accepted" in str(n.content) for n in nodes)
    assert session.state.staged_records[0].temp_id == record.temp_id
    assert session.state.staged_records[0].status == "accepted"


@pytest.mark.asyncio
async def test_advance_edit_accepted_staged_op_reports_error_and_keeps_record(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    record = session.staging.propose("specs", "Accepted", "# Accepted", "main")
    session.staging.accept(record.temp_id)
    store = MillStateStore()
    output = f'<op kind="edit-staged" temp_id="{record.temp_id}"/><node type="record" surface="specs" title="Accepted"># Mutated</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)

    nodes = await engine.advance()

    assert any(n.type == CanvasNodeType.OBSERVATION and "accepted" in str(n.content) for n in nodes)
    assert session.state.staged_records[0].content == "# Accepted"
    assert session.state.staged_records[0].status == "accepted"


@pytest.mark.asyncio
async def test_framing_node_does_not_force_narrowing(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")  # starts in EXPLORING
    store = MillStateStore()
    output = '<node type="framing">A lens.</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    await engine.advance()
    assert session.state.phase == SessionPhase.EXPLORING


@pytest.mark.asyncio
async def test_tension_node_does_not_force_narrowing(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    store = MillStateStore()
    output = '<node type="tension">A risk.</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    await engine.advance()
    assert session.state.phase == SessionPhase.EXPLORING


@pytest.mark.asyncio
async def test_question_still_transitions_to_narrowing(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    store = MillStateStore()
    output = '<node type="question">Which path?</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    await engine.advance()
    assert session.state.phase == SessionPhase.NARROWING


@pytest.mark.asyncio
async def test_decision_step_publishes_advance_stream(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    store = MillStateStore()
    output = '<node type="observation">done</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    subscription = store.subscribe()
    collected: list[dict] = []
    try:
        await engine.advance()
        # Drain a handful of events; the decision stream should appear among them.
        for _ in range(6):
            try:
                event = await asyncio.wait_for(subscription.__anext__(), timeout=1.0)
            except (StopAsyncIteration, asyncio.TimeoutError):
                break
            collected.append(_event_payload(event))
    finally:
        await subscription.aclose()

    stream_events = [e for e in collected if e["type"] == "shaping:advance_stream"]
    assert stream_events, f"expected an advance_stream event, got {[e['type'] for e in collected]}"
    assert any("done" in str(e.get("data", {}).get("delta", "")) for e in stream_events)
