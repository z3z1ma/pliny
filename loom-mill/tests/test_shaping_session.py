from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID

import pytest

from loom_mill.api import shaping
from loom_mill.api.ws import _event_payload
from loom_mill.app import create_app
from loom_mill.shaping import CanvasEdge, CanvasNode, CanvasNodeType, NodeStatus, SessionPhase, ShapingSession
from loom_mill.shaping.events import ShapingEvent
from loom_mill.shaping.session import mark_dead_recursive, mark_stale_recursive
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
                harness_config=harness_config or HarnessConfig(command="printf", args=['<node type="observation">default</node>']),
            )
        )
        self._body = body or {}
        self.path_params = path_params or {}

    async def json(self):
        return self._body


def _body(response) -> dict:
    return json.loads(response.body)


def _assert_utc_timestamp(value: str) -> None:
    parsed = datetime.fromisoformat(value)
    assert parsed.tzinfo is not None


def test_shaping_routes_are_registered() -> None:
    routes = [(route.path, route.methods or set()) for route in create_app().routes if hasattr(route, "methods")]

    def has_route(path: str, method: str) -> bool:
        return any(route_path == path and method in methods for route_path, methods in routes)

    assert has_route("/shaping/sessions", "POST")
    assert has_route("/shaping/sessions", "GET")
    assert has_route("/shaping/sessions/{session_id}", "GET")
    assert has_route("/shaping/sessions/{session_id}/context", "GET")
    assert has_route("/shaping/sessions/{session_id}/input", "POST")
    assert has_route("/shaping/sessions/{session_id}/nodes/{node_id}/select", "POST")
    assert has_route("/shaping/sessions/{session_id}/nodes/{node_id}/edit", "POST")
    assert has_route("/shaping/sessions/{session_id}/nodes/{node_id}/reselect", "POST")
    assert has_route("/shaping/sessions/{session_id}", "DELETE")


@pytest.mark.asyncio
async def test_create_session_persists_state_and_context(tmp_path: Path) -> None:
    response = await shaping.create_shaping_session(Request(tmp_path, MillStateStore(), {"input": "shape graph mode"}))

    payload = _body(response)
    session_id = payload["session_id"]
    UUID(session_id)
    state = payload["state"]
    assert response.status_code == 200
    assert state["id"] == session_id
    assert state["phase"] == "exploring"
    root = next(iter(state["nodes"].values()))
    assert root["type"] == "input"
    assert root["parent_id"] is None
    _assert_utc_timestamp(state["created_at"])
    _assert_utc_timestamp(state["updated_at"])

    session_dir = tmp_path / ".mill" / "shaping-sessions" / session_id
    assert (session_dir / "state.json").exists()
    assert (session_dir / "context.md").exists()
    assert "shape graph mode" in (session_dir / "context.md").read_text(encoding="utf-8")
    assert json.loads((session_dir / "state.json").read_text(encoding="utf-8"))["id"] == session_id


@pytest.mark.asyncio
async def test_create_session_publishes_root_node_event(tmp_path: Path) -> None:
    store = MillStateStore()
    subscription = store.subscribe()
    try:
        response = await shaping.create_shaping_session(Request(tmp_path, store, {"input": "shape graph mode"}))
        event = await subscription.__anext__()
    finally:
        await subscription.aclose()

    payload = _body(response)
    root = next(iter(payload["state"]["nodes"].values()))
    assert event.event == "node_added"
    assert event.data["node"] == root


@pytest.mark.asyncio
async def test_add_input_appends_context_adds_node_and_publishes_event(tmp_path: Path) -> None:
    store = MillStateStore()
    create_response = await shaping.create_shaping_session(Request(tmp_path, store, {"input": "initial"}))
    session_id = _body(create_response)["session_id"]
    subscription = store.subscribe()
    try:
        response = await shaping.add_shaping_input(
            Request(tmp_path, store, {"text": "follow up"}, {"session_id": session_id})
        )
        event = await subscription.__anext__()
    finally:
        await subscription.aclose()

    payload = _body(response)
    assert response.status_code == 200
    assert payload["node"]["type"] == "input"
    assert payload["node"]["content"] == {"text": "follow up"}
    assert isinstance(event, ShapingEvent)
    assert event.event == "node_added"
    assert event.data["node"]["id"] == payload["node"]["id"]

    session = ShapingSession.load(session_id, tmp_path)
    assert [node.content["text"] for node in session.state.nodes.values() if node.type == CanvasNodeType.INPUT] == ["initial", "follow up"]
    context = session.read_context()
    assert context.index("initial") < context.index("follow up")


@pytest.mark.asyncio
async def test_add_input_accepts_parent_node_id_and_adds_edge(tmp_path: Path) -> None:
    store = MillStateStore()
    session_id = _body(await shaping.create_shaping_session(Request(tmp_path, store, {"input": "initial"})))["session_id"]
    session = ShapingSession.load(session_id, tmp_path)
    parent_id = next(iter(session.state.nodes))

    response = await shaping.add_shaping_input(
        Request(tmp_path, store, {"text": "answer", "parent_node_id": parent_id}, {"session_id": session_id})
    )

    payload = _body(response)
    assert response.status_code == 200
    assert payload["node"]["parent_id"] == parent_id
    assert payload["edge"]["source_id"] == parent_id
    assert payload["edge"]["target_id"] == payload["node"]["id"]


def _add_node(session: ShapingSession, node_id: str, node_type: CanvasNodeType, parent_id: str | None, *, option_group_id: str | None = None) -> None:
    session.add_node_with_edge(
        CanvasNode(
            id=node_id,
            type=node_type,
            parent_id=parent_id,
            status=NodeStatus.ACTIVE,
            content={"label": node_id},
            position=None,
            timestamp=session.state.created_at,
            option_group_id=option_group_id,
        )
    )


@pytest.mark.asyncio
async def test_select_option_marks_siblings_dead(tmp_path: Path) -> None:
    store = MillStateStore()
    session = ShapingSession.create(tmp_path, "initial")
    session_id = session.session_id
    root_id = next(iter(session.state.nodes))
    _add_node(session, "option-a", CanvasNodeType.OPTION, root_id, option_group_id="group-1")
    _add_node(session, "option-b", CanvasNodeType.OPTION, root_id, option_group_id="group-1")
    _add_node(session, "option-c", CanvasNodeType.OPTION, root_id, option_group_id="group-1")

    response = await shaping.select_option_node(Request(tmp_path, store, path_params={"session_id": session_id, "node_id": "option-b"}))

    assert response.status_code == 200
    session = ShapingSession.load(session_id, tmp_path)
    assert session.state.nodes["option-b"].status == NodeStatus.ACTIVE
    assert session.state.nodes["option-b"].selected is True
    assert session.state.nodes["option-a"].status == NodeStatus.DEAD
    assert session.state.nodes["option-c"].status == NodeStatus.DEAD


def test_mark_dead_recursive_propagates_to_three_plus_levels(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "initial")
    root_id = next(iter(session.state.nodes))
    _add_node(session, "option-a", CanvasNodeType.OPTION, root_id, option_group_id="group-1")
    _add_node(session, "child-1", CanvasNodeType.OBSERVATION, "option-a")
    _add_node(session, "child-2", CanvasNodeType.QUESTION, "child-1")
    _add_node(session, "child-3", CanvasNodeType.RECORD, "child-2")

    affected = mark_dead_recursive(session.state, "option-a")

    assert affected == ["option-a", "child-1", "child-2", "child-3"]
    assert all(session.state.nodes[node_id].status == NodeStatus.DEAD for node_id in affected)


def test_mark_stale_recursive_marks_descendants_not_parent_or_dead_nodes(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "initial")
    root_id = next(iter(session.state.nodes))
    _add_node(session, "child-1", CanvasNodeType.OBSERVATION, root_id)
    _add_node(session, "child-2", CanvasNodeType.QUESTION, "child-1")
    _add_node(session, "dead-child", CanvasNodeType.RECORD, "child-1")
    session.state.nodes["dead-child"].status = NodeStatus.DEAD

    affected = mark_stale_recursive(session.state, root_id)

    assert affected == ["child-1", "child-2"]
    assert session.state.nodes[root_id].status == NodeStatus.ACTIVE
    assert session.state.nodes["child-1"].status == NodeStatus.STALE
    assert session.state.nodes["child-2"].status == NodeStatus.STALE
    assert session.state.nodes["dead-child"].status == NodeStatus.DEAD


@pytest.mark.asyncio
async def test_edit_input_publishes_update_invalidates_and_regenerates(tmp_path: Path) -> None:
    store = MillStateStore()
    harness = HarnessConfig(command="printf", args=['<node type="observation">replacement</node>'])
    session = ShapingSession.create(tmp_path, "initial")
    root_id = next(iter(session.state.nodes))
    _add_node(session, "old-child", CanvasNodeType.OBSERVATION, root_id)
    _add_node(session, "old-grandchild", CanvasNodeType.QUESTION, "old-child")
    subscription = store.subscribe()
    try:
        response = await shaping.edit_node(
            Request(
                tmp_path,
                store,
                {"content": "edited"},
                {"session_id": session.session_id, "node_id": root_id},
                harness_config=harness,
            )
        )
        events = [await subscription.__anext__(), await subscription.__anext__(), await subscription.__anext__(), await subscription.__anext__(), await subscription.__anext__()]
    finally:
        await subscription.aclose()

    payload = _body(response)
    loaded = ShapingSession.load(session.session_id, tmp_path)
    new_children = [node for node in loaded.state.nodes.values() if node.parent_id == root_id]
    assert response.status_code == 200
    assert payload["edited"] == root_id
    assert payload["stale_ids"] == ["old-child", "old-grandchild"]
    assert loaded.state.nodes[root_id].content["text"] == "edited"
    assert "old-child" not in loaded.state.nodes
    assert "old-grandchild" not in loaded.state.nodes
    assert len(new_children) == 1
    assert new_children[0].content["observation"] == "replacement"
    assert [_event_payload(event)["type"] for event in events] == [
        "shaping:node_updated",
        "shaping:node_invalidated",
        "shaping:nodes_removed",
        "shaping:node_added",
        "shaping:edge_added",
    ]


@pytest.mark.asyncio
async def test_cannot_edit_non_input_node(tmp_path: Path) -> None:
    store = MillStateStore()
    session = ShapingSession.create(tmp_path, "initial")
    root_id = next(iter(session.state.nodes))
    _add_node(session, "question-1", CanvasNodeType.QUESTION, root_id)

    response = await shaping.edit_node(
        Request(tmp_path, store, {"content": "edited"}, {"session_id": session.session_id, "node_id": "question-1"})
    )

    assert response.status_code == 400
    assert _body(response)["error"] == "Only input nodes are editable"


@pytest.mark.asyncio
async def test_reselect_dead_option_deactivates_old_branch_and_advances_new_branch(tmp_path: Path) -> None:
    store = MillStateStore()
    harness = HarnessConfig(command="printf", args=['<node type="observation">new branch</node>'])
    session = ShapingSession.create(tmp_path, "initial")
    root_id = next(iter(session.state.nodes))
    _add_node(session, "option-a", CanvasNodeType.OPTION, root_id, option_group_id="group-1")
    _add_node(session, "option-b", CanvasNodeType.OPTION, root_id, option_group_id="group-1")
    _add_node(session, "a-child", CanvasNodeType.OBSERVATION, "option-a")
    session.state.nodes["option-a"].selected = True
    session.state.nodes["option-b"].status = NodeStatus.DEAD
    session._persist_state()

    response = await shaping.reselect_option_node(
        Request(tmp_path, store, path_params={"session_id": session.session_id, "node_id": "option-b"}, harness_config=harness)
    )

    loaded = ShapingSession.load(session.session_id, tmp_path)
    b_children = [node for node in loaded.state.nodes.values() if node.parent_id == "option-b"]
    assert response.status_code == 200
    assert loaded.state.nodes["option-a"].status == NodeStatus.DEAD
    assert loaded.state.nodes["a-child"].status == NodeStatus.DEAD
    assert loaded.state.nodes["option-a"].selected is False
    assert loaded.state.nodes["option-b"].status == NodeStatus.ACTIVE
    assert loaded.state.nodes["option-b"].selected is True
    assert len(b_children) == 1
    assert b_children[0].content["observation"] == "new branch"


@pytest.mark.asyncio
async def test_selecting_already_selected_option_is_noop(tmp_path: Path) -> None:
    store = MillStateStore()
    session = ShapingSession.create(tmp_path, "initial")
    session_id = session.session_id
    root_id = next(iter(session.state.nodes))
    _add_node(session, "option-a", CanvasNodeType.OPTION, root_id, option_group_id="group-1")
    session.state.nodes["option-a"].selected = True
    session._persist_state()

    response = await shaping.select_option_node(Request(tmp_path, store, path_params={"session_id": session_id, "node_id": "option-a"}))

    assert response.status_code == 200
    assert _body(response)["changed_node_ids"] == []
    session = ShapingSession.load(session_id, tmp_path)
    assert session.state.nodes["option-a"].status == NodeStatus.ACTIVE
    assert session.state.nodes["option-a"].selected is True


@pytest.mark.asyncio
async def test_cannot_select_dead_option(tmp_path: Path) -> None:
    store = MillStateStore()
    session = ShapingSession.create(tmp_path, "initial")
    session_id = session.session_id
    root_id = next(iter(session.state.nodes))
    _add_node(session, "option-a", CanvasNodeType.OPTION, root_id, option_group_id="group-1")
    session.state.nodes["option-a"].status = NodeStatus.DEAD
    session._persist_state()

    response = await shaping.select_option_node(Request(tmp_path, store, path_params={"session_id": session_id, "node_id": "option-a"}))

    assert response.status_code == 409
    assert _body(response)["error"] == "Cannot select a dead option"


@pytest.mark.asyncio
async def test_context_append_returns_byte_length_and_persists(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "initial")

    byte_length = await session.append_context("Observation", "learned something")

    context = session.read_context()
    assert byte_length == len(context.encode("utf-8"))
    assert "## Observation" in context
    assert "learned something" in context


def test_node_edge_phase_update_and_persistence_round_trip(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "initial")
    root_id = next(iter(session.state.nodes))
    node = CanvasNode(
        id="node-2",
        type=CanvasNodeType.OBSERVATION,
        parent_id=root_id,
        status=NodeStatus.ACTIVE,
        content={"observation": "x"},
        position={"x": 1.0, "y": 2.0},
        timestamp=session.state.created_at,
    )

    session.add_node_with_edge(node)
    session.update_phase(SessionPhase.NARROWING)
    loaded = ShapingSession.load(session.session_id, tmp_path)

    assert loaded.state.phase == SessionPhase.NARROWING
    assert loaded.state.nodes["node-2"].type == CanvasNodeType.OBSERVATION
    assert loaded.state.nodes["node-2"].content == {"observation": "x"}
    assert loaded.state.edges[0].source_id == root_id
    assert loaded.state.edges[0].target_id == "node-2"
    assert loaded.state.active_branch == "main"
    assert loaded.state.branches == ["main"]


@pytest.mark.asyncio
async def test_list_and_delete_active_sessions(tmp_path: Path) -> None:
    store = MillStateStore()
    first = _body(await shaping.create_shaping_session(Request(tmp_path, store, {"input": "first"})))["session_id"]
    second = _body(await shaping.create_shaping_session(Request(tmp_path, store, {"input": "second"})))["session_id"]

    listed = _body(await shaping.list_shaping_sessions(Request(tmp_path, store)))
    assert {item["id"] for item in listed} == {first, second}
    assert all("node_count" in item for item in listed)
    assert {item["seed_text"] for item in listed} == {"first", "second"}
    assert all(item["status"] == "active" for item in listed)

    response = await shaping.delete_shaping_session(Request(tmp_path, store, path_params={"session_id": first}))
    assert response.status_code == 200
    assert _body(response)["ended_at"] is not None

    listed_after_delete = _body(await shaping.list_shaping_sessions(Request(tmp_path, store)))
    assert {item["id"] for item in listed_after_delete} == {first, second}
    assert next(item for item in listed_after_delete if item["id"] == first)["status"] == "committed"


@pytest.mark.asyncio
async def test_get_session_and_context_endpoints(tmp_path: Path) -> None:
    store = MillStateStore()
    session_id = _body(await shaping.create_shaping_session(Request(tmp_path, store, {"input": "initial"})))["session_id"]

    state_response = await shaping.get_shaping_session(Request(tmp_path, store, path_params={"session_id": session_id}))
    context_response = await shaping.get_shaping_context(Request(tmp_path, store, path_params={"session_id": session_id}))

    assert _body(state_response)["id"] == session_id
    context_payload = _body(context_response)
    assert "initial" in context_payload["content"]
    assert context_payload["byte_length"] == len(context_payload["content"].encode("utf-8"))


def test_shaping_websocket_event_payloads() -> None:
    node_payload = _event_payload(ShapingEvent(session_id="session-1", event="node_added", data={"node": {"id": "n1"}}))
    edge_payload = _event_payload(ShapingEvent(session_id="session-1", event="edge_added", data={"edge": {"id": "e1"}}))
    update_payload = _event_payload(ShapingEvent(session_id="session-1", event="node_updated", data={"node_id": "n1", "changes": {"status": "stale"}}))
    invalidated_payload = _event_payload(ShapingEvent(session_id="session-1", event="node_invalidated", data={"node_ids": ["n1"]}))
    removed_payload = _event_payload(ShapingEvent(session_id="session-1", event="nodes_removed", data={"node_ids": ["n1"]}))
    phase_payload = _event_payload(ShapingEvent(session_id="session-1", event="phase_changed", data={"phase": "narrowing"}))

    assert node_payload == {"type": "shaping:node_added", "data": {"session_id": "session-1", "node": {"id": "n1"}}}
    assert edge_payload == {"type": "shaping:edge_added", "data": {"session_id": "session-1", "edge": {"id": "e1"}}}
    assert update_payload == {"type": "shaping:node_updated", "data": {"session_id": "session-1", "node_id": "n1", "changes": {"status": "stale"}}}
    assert invalidated_payload == {"type": "shaping:node_invalidated", "data": {"session_id": "session-1", "node_ids": ["n1"]}}
    assert removed_payload == {"type": "shaping:nodes_removed", "data": {"session_id": "session-1", "node_ids": ["n1"]}}
    assert phase_payload == {"type": "shaping:phase_changed", "data": {"session_id": "session-1", "phase": "narrowing"}}


def test_canvas_model_construction_and_from_dict_round_trip() -> None:
    node = CanvasNode.from_dict(
        {
            "id": "n1",
            "type": "option",
            "parent_id": "g1",
            "status": "dead",
            "content": {"label": "A"},
            "position": {"x": 10, "y": 20},
            "timestamp": "2026-05-26T00:00:00+00:00",
            "option_group_id": "g1",
        }
    )
    edge = CanvasEdge.from_dict({"id": "e1", "source_id": "g1", "target_id": "n1", "type": "option_group"})

    assert node.type == CanvasNodeType.OPTION
    assert node.status == NodeStatus.DEAD
    assert node.position == {"x": 10.0, "y": 20.0}
    assert edge.type == "option_group"


def test_old_block_session_loads_empty_graph(tmp_path: Path) -> None:
    session_dir = tmp_path / ".mill" / "shaping-sessions" / "old"
    session_dir.mkdir(parents=True)
    (session_dir / "state.json").write_text(
        json.dumps({"id": "old", "phase": "exploring", "created_at": "now", "updated_at": "now", "blocks": [{"id": "b1"}]}),
        encoding="utf-8",
    )

    loaded = ShapingSession.load("old", tmp_path)

    assert loaded.state.nodes == {}
    assert loaded.state.edges == []


def test_node_status_update_and_invalidation_persist(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "initial")
    root_id = next(iter(session.state.nodes))

    session.update_node(root_id, {"status": "dead"})
    assert ShapingSession.load(session.session_id, tmp_path).state.nodes[root_id].status == NodeStatus.DEAD

    assert session.invalidate_nodes([root_id, "missing"]) == [root_id]
    assert ShapingSession.load(session.session_id, tmp_path).state.nodes[root_id].status == NodeStatus.STALE
