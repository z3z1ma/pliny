from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from loom_mill.api import design
from loom_mill.app import create_app
from loom_mill.parser import parse_record
from loom_mill.state import ChatEvent, MillStateStore


class Request:
    def __init__(self, workspace_root: Path, store: MillStateStore, body: dict | None = None, path_params: dict | None = None):
        self.app = SimpleNamespace(state=SimpleNamespace(workspace_root=str(workspace_root), store=store))
        self._body = body or {}
        self.path_params = path_params or {}

    async def json(self):
        return self._body


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _body(response) -> dict:
    return json.loads(response.body)


def test_design_routes_are_registered():
    routes = [(route.path, route.methods or set()) for route in create_app().routes if hasattr(route, "methods")]

    def has_route(path: str, method: str) -> bool:
        return any(route_path == path and method in methods for route_path, methods in routes)

    assert has_route("/records", "POST")
    assert has_route("/records/{record_id}/transition", "POST")
    assert has_route("/records/{record_id:path}", "PUT")
    assert has_route("/chat/sessions", "POST")
    assert has_route("/chat/sessions/{session_id}", "GET")
    assert has_route("/chat/sessions/{session_id}/messages", "POST")
    assert has_route("/chat/sessions/{session_id}", "DELETE")


@pytest.mark.asyncio
async def test_update_record_writes_file_atomically(tmp_path: Path):
    original = """# Example Ticket

ID: ticket:20260526-example
Type: Ticket
Status: open
Created: 2026-05-26
Updated: 2026-05-26
"""
    updated = original.replace("Status: open", "Status: active")
    path = tmp_path / ".loom" / "tickets" / "20260526-example.md"
    _write(path, original)
    store = MillStateStore()
    await store.replace_all_records((parse_record(path, root=tmp_path / ".loom"),))

    response = await design.update_record(
        Request(tmp_path, store, {"content": updated}, {"record_id": "ticket:20260526-example"})
    )

    assert response.status_code == 200
    assert _body(response) == {"id": "ticket:20260526-example", "path": "tickets/20260526-example.md", "updated": True}
    assert path.read_text(encoding="utf-8") == updated


@pytest.mark.asyncio
async def test_update_record_returns_404_for_unknown_record(tmp_path: Path):
    store = MillStateStore()

    response = await design.update_record(Request(tmp_path, store, {"content": "x"}, {"record_id": "ticket:missing"}))

    assert response.status_code == 404
    assert _body(response) == {"detail": "Record not found"}


@pytest.mark.asyncio
async def test_transition_record_accepts_review_ticket_and_appends_journal(tmp_path: Path):
    content = """# Example Ticket

ID: ticket:20260526-example
Type: Ticket
Status: review
Created: 2026-05-26
Updated: 2026-05-26
Risk: low - example

## Journal

- 2026-05-26: Moved to review.
"""
    path = tmp_path / ".loom" / "tickets" / "20260526-example.md"
    _write(path, content)
    store = MillStateStore()
    await store.replace_all_records((parse_record(path, root=tmp_path / ".loom"),))

    response = await design.transition_record(
        Request(
            tmp_path,
            store,
            {"action": "accept", "notes": "Looks good."},
            {"record_id": "ticket:20260526-example"},
        )
    )

    today = design.date.today().isoformat()
    updated = path.read_text(encoding="utf-8")
    assert response.status_code == 200
    assert _body(response) == {"ok": True, "action": "accept"}
    assert "Status: closed" in updated
    assert f"Updated: {today}" in updated
    assert f"- {today}: Accepted from review. Notes: Looks good." in updated


@pytest.mark.asyncio
async def test_transition_record_request_change_returns_ticket_to_active(tmp_path: Path):
    content = """# Example Ticket

ID: ticket:20260526-example
Type: Ticket
Status: review
Created: 2026-05-26
Updated: 2026-05-26
Risk: low - example

## Journal

- 2026-05-26: Moved to review.
"""
    path = tmp_path / ".loom" / "tickets" / "20260526-example.md"
    _write(path, content)
    store = MillStateStore()
    await store.replace_all_records((parse_record(path, root=tmp_path / ".loom"),))

    response = await design.transition_record(
        Request(
            tmp_path,
            store,
            {"action": "request_change", "notes": "Needs tests."},
            {"record_id": "ticket:20260526-example"},
        )
    )

    today = design.date.today().isoformat()
    updated = path.read_text(encoding="utf-8")
    assert response.status_code == 200
    assert _body(response) == {"ok": True, "action": "request_change"}
    assert "Status: active" in updated
    assert f"Updated: {today}" in updated
    assert f"- {today}: Change requested, returned to active. Notes: Needs tests." in updated


@pytest.mark.asyncio
async def test_create_record_writes_template_and_handles_collision(tmp_path: Path):
    today = design.date.today().strftime("%Y%m%d")
    existing = tmp_path / ".loom" / "tickets" / f"{today}-untitled.md"
    _write(existing, "existing")
    store = MillStateStore()

    response = await design.create_record(Request(tmp_path, store, {"surface": "tickets"}))

    payload = _body(response)
    assert response.status_code == 200
    assert payload["id"] == f"ticket:{today}-untitled-2"
    assert payload["path"] == f"tickets/{today}-untitled-2.md"
    created = tmp_path / ".loom" / payload["path"]
    assert created.exists()
    assert "Type: Ticket" in payload["content"]
    assert "- ACC-001: " in created.read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_create_chat_session_persists_file(tmp_path: Path):
    store = MillStateStore()

    response = await design.create_chat_session(
        Request(tmp_path, store, {"harness_command": "python -m example", "document_path": "tickets/example.md"})
    )

    payload = _body(response)
    assert response.status_code == 200
    assert payload["session_id"]
    assert (tmp_path / ".mill" / "chat-sessions" / f"{payload['session_id']}.json").exists()


@pytest.mark.asyncio
async def test_get_chat_session_returns_session_state(tmp_path: Path):
    store = MillStateStore()
    create_response = await design.create_chat_session(Request(tmp_path, store, {"harness_command": "echo hi"}))
    session_id = _body(create_response)["session_id"]

    response = await design.get_chat_session(Request(tmp_path, store, path_params={"session_id": session_id}))

    assert response.status_code == 200
    assert _body(response)["id"] == session_id


@pytest.mark.asyncio
async def test_end_chat_session_marks_session_ended(tmp_path: Path):
    store = MillStateStore()
    create_response = await design.create_chat_session(Request(tmp_path, store, {"harness_command": "echo hi"}))
    session_id = _body(create_response)["session_id"]

    response = await design.end_chat_session(Request(tmp_path, store, path_params={"session_id": session_id}))

    assert response.status_code == 200
    assert _body(response)["ended_at"] is not None
    get_response = await design.get_chat_session(Request(tmp_path, store, path_params={"session_id": session_id}))
    assert _body(get_response)["ended_at"] is not None


@pytest.mark.asyncio
async def test_send_chat_message_builds_prompt_persists_messages_and_broadcasts(monkeypatch, tmp_path: Path):
    store = MillStateStore()
    document = tmp_path / ".loom" / "tickets" / "example.md"
    _write(document, "# Example\n\nID: ticket:example\n")
    create_response = await design.create_chat_session(
        Request(tmp_path, store, {"harness_command": "fake harness", "document_path": "tickets/example.md"})
    )
    session_id = _body(create_response)["session_id"]
    prompts: list[str] = []
    user_messages: list[str | None] = []

    async def fake_run_harness(command, prompt, session_id_arg, broadcast, *, user_message=None):
        prompts.append(prompt)
        user_messages.append(user_message)
        await broadcast({"event": "chat_stream", "data": {"session_id": session_id_arg, "delta": "hello", "done": False}})
        await broadcast(
            {
                "event": "chat_complete",
                "data": {"session_id": session_id_arg, "message": {"role": "assistant", "content": "hello"}},
            }
        )
        return "hello"

    monkeypatch.setattr(design, "run_harness", fake_run_harness)
    stream = store.subscribe()
    try:
        response = await design.send_chat_message(
            Request(
                tmp_path,
                store,
                {
                    "content": "shape this",
                    "context": {"path": "tickets/example.md", "selected_text": "ID: ticket:example", "line_range": [3, 3]},
                },
                {"session_id": session_id},
            )
        )
        first_event = await anext(stream)
        second_event = await anext(stream)
    finally:
        await stream.aclose()

    assert response.status_code == 200
    assert isinstance(first_event, ChatEvent)
    assert first_event.event == "chat_stream"
    assert isinstance(second_event, ChatEvent)
    assert second_event.event == "chat_complete"
    assert "Current document (tickets/example.md)" in prompts[0]
    assert "ID: ticket:example" in prompts[0]
    assert "Operator: shape this" in prompts[0]
    assert user_messages == ["shape this"]

    session_response = await design.get_chat_session(Request(tmp_path, store, path_params={"session_id": session_id}))
    messages = _body(session_response)["messages"]
    assert [message["role"] for message in messages] == ["user", "assistant"]
