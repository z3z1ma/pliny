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
from loom_mill.shaping import BlockType, InteractionBlock, SessionPhase, ShapingSession
from loom_mill.shaping.events import ShapingEvent
from loom_mill.state import MillStateStore


class Request:
    def __init__(self, workspace_root: Path, store: MillStateStore, body: dict | None = None, path_params: dict | None = None):
        self.app = SimpleNamespace(state=SimpleNamespace(workspace_root=str(workspace_root), store=store))
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
    assert state["blocks"][0]["type"] == "operator_input"
    _assert_utc_timestamp(state["created_at"])
    _assert_utc_timestamp(state["updated_at"])

    session_dir = tmp_path / ".mill" / "shaping-sessions" / session_id
    assert (session_dir / "state.json").exists()
    assert (session_dir / "context.md").exists()
    assert "shape graph mode" in (session_dir / "context.md").read_text(encoding="utf-8")
    assert json.loads((session_dir / "state.json").read_text(encoding="utf-8"))["id"] == session_id


@pytest.mark.asyncio
async def test_add_input_appends_context_adds_block_and_publishes_event(tmp_path: Path) -> None:
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
    assert payload["block"]["type"] == "operator_input"
    assert payload["block"]["content"] == {"text": "follow up"}
    assert isinstance(event, ShapingEvent)
    assert event.event == "block_added"
    assert event.data["block"]["id"] == payload["block"]["id"]

    session = ShapingSession.load(session_id, tmp_path)
    assert [block.content["text"] for block in session.state.blocks] == ["initial", "follow up"]
    context = session.read_context()
    assert context.index("initial") < context.index("follow up")


@pytest.mark.asyncio
async def test_context_append_returns_byte_length_and_persists(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "initial")

    byte_length = await session.append_context("Observation", "learned something")

    context = session.read_context()
    assert byte_length == len(context.encode("utf-8"))
    assert "## Observation" in context
    assert "learned something" in context


def test_block_add_phase_update_and_persistence_round_trip(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "initial")
    block = InteractionBlock(id="block-2", type=BlockType.AGENT_OBSERVATION, timestamp=session.state.created_at, content={"observation": "x"})

    session.add_block(block)
    session.update_phase(SessionPhase.NARROWING)
    loaded = ShapingSession.load(session.session_id, tmp_path)

    assert loaded.state.phase == SessionPhase.NARROWING
    assert [item.type for item in loaded.state.blocks] == [BlockType.OPERATOR_INPUT, BlockType.AGENT_OBSERVATION]
    assert loaded.state.blocks[1].content == {"observation": "x"}
    assert loaded.state.active_branch == "main"
    assert loaded.state.branches == ["main"]


@pytest.mark.asyncio
async def test_list_and_delete_active_sessions(tmp_path: Path) -> None:
    store = MillStateStore()
    first = _body(await shaping.create_shaping_session(Request(tmp_path, store, {"input": "first"})))["session_id"]
    second = _body(await shaping.create_shaping_session(Request(tmp_path, store, {"input": "second"})))["session_id"]

    listed = _body(await shaping.list_shaping_sessions(Request(tmp_path, store)))
    assert {item["id"] for item in listed} == {first, second}

    response = await shaping.delete_shaping_session(Request(tmp_path, store, path_params={"session_id": first}))
    assert response.status_code == 200
    assert _body(response)["ended_at"] is not None

    listed_after_delete = _body(await shaping.list_shaping_sessions(Request(tmp_path, store)))
    assert [item["id"] for item in listed_after_delete] == [second]


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
    block_payload = _event_payload(ShapingEvent(session_id="session-1", event="block_added", data={"block": {"id": "b1"}}))
    phase_payload = _event_payload(ShapingEvent(session_id="session-1", event="phase_changed", data={"phase": "narrowing"}))

    assert block_payload == {"type": "shaping:block_added", "data": {"session_id": "session-1", "block": {"id": "b1"}}}
    assert phase_payload == {"type": "shaping:phase_changed", "data": {"session_id": "session-1", "phase": "narrowing"}}
