from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import asdict
from datetime import date, datetime
from pathlib import Path

from starlette.requests import Request
from starlette.responses import JSONResponse

from loom_mill.chat.harness import run_harness
from loom_mill.chat.prompt import build_prompt
from loom_mill.chat.session import ChatContext, ChatMessage, SessionStore
from loom_mill.parser import parse_record
from loom_mill.state import ChatEvent, MillStateStore, RecordAdded, RecordChanged


SURFACES = {
    "tickets": ("Ticket", "open"),
    "specs": ("Spec", "draft"),
    "plans": ("Plan", "open"),
    "research": ("Research", "open"),
    "knowledge": ("Knowledge Preference", "active"),
}


def _workspace_root(request: Request) -> Path:
    return Path(request.app.state.workspace_root)


def _session_store(request: Request) -> SessionStore:
    return SessionStore(_workspace_root(request) / ".mill" / "chat-sessions")


def _payload(session) -> dict:
    return asdict(session)


async def _json_body(request: Request) -> dict:
    try:
        body = await request.json()
    except json.JSONDecodeError as error:
        raise ValueError("invalid JSON") from error
    if not isinstance(body, dict):
        raise ValueError("JSON body must be an object")
    return body


def _slug(value: str | None) -> str:
    raw = (value or "untitled").strip().lower()
    slug = re.sub(r"[^a-z0-9_-]+", "-", raw).strip("-")
    return slug or "untitled"


def _dated_slug(slug: str, today: str) -> str:
    return slug if re.match(r"^\d{8}-", slug) else f"{today.replace('-', '')}-{slug}"


def _unique_path(directory: Path, stem: str) -> tuple[Path, str]:
    candidate = directory / f"{stem}.md"
    if not candidate.exists():
        return candidate, stem
    index = 2
    while True:
        candidate_stem = f"{stem}-{index}"
        candidate = directory / f"{candidate_stem}.md"
        if not candidate.exists():
            return candidate, candidate_stem
        index += 1


def _template(surface: str, stem: str, today: date) -> tuple[str, str]:
    iso_date = today.isoformat()
    ymd = iso_date.replace("-", "")
    plain_slug = stem.removeprefix(f"{ymd}-")
    if surface == "tickets":
        record_id = f"ticket:{stem}"
        content = f"# Untitled Ticket\n\nID: {record_id}\nType: Ticket\nStatus: open\nCreated: {iso_date}\nUpdated: {iso_date}\n\n## Summary\n\n## Scope\n\n## Acceptance\n\n- ACC-001: \n"
    elif surface == "specs":
        record_id = f"spec:{stem}"
        content = f"# Untitled Spec\n\nID: {record_id}\nType: Spec\nStatus: draft\nCreated: {iso_date}\nUpdated: {iso_date}\n\n## Summary\n\n## Requirements\n\n- REQ-001: \n"
    elif surface == "plans":
        record_id = f"plan:{stem}"
        content = f"# Untitled Plan\n\nID: {record_id}\nType: Plan\nStatus: open\nCreated: {iso_date}\nUpdated: {iso_date}\n\n## Summary\n\n## Execution Units\n"
    elif surface == "research":
        record_id = f"research:{stem}"
        content = f"# Untitled Research\n\nID: {record_id}\nType: Research\nStatus: open\nCreated: {iso_date}\nUpdated: {iso_date}\n\n## Summary\n\n## Findings\n"
    else:
        record_id = f"knowledge:{stem if stem.startswith(ymd) else plain_slug}"
        content = f"# Untitled Knowledge\n\nID: {record_id}\nType: Knowledge Preference\nStatus: active\nCreated: {iso_date}\nUpdated: {iso_date}\n\n## Summary\n"
    return record_id, content


async def update_record(request: Request) -> JSONResponse:
    record_id = request.path_params["record_id"]
    try:
        body = await _json_body(request)
        content = body["content"]
        if not isinstance(content, str):
            raise ValueError("content must be a string")
    except (KeyError, ValueError) as error:
        return JSONResponse({"error": str(error)}, status_code=400)

    store: MillStateStore = request.app.state.store
    snapshot = await store.snapshot()
    record = next((item for item in snapshot.records if item.metadata.id == record_id), None)
    if record is None:
        return JSONResponse({"detail": "Record not found"}, status_code=404)

    path = _workspace_root(request) / ".loom" / record.path
    if not path.exists():
        return JSONResponse({"detail": "Record not found"}, status_code=404)

    tmp_name = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp_file:
            tmp_name = tmp_file.name
            tmp_file.write(content)
        os.replace(tmp_name, path)
    finally:
        if tmp_name and os.path.exists(tmp_name):
            os.unlink(tmp_name)

    updated = parse_record(path, root=_workspace_root(request) / ".loom")
    if updated is not None:
        previous = await store.replace_record(updated)
        if previous is not None:
            await store.publish(RecordChanged(path=updated.path, record=updated, previous=previous))
    return JSONResponse({"id": record_id, "path": record.path, "updated": True})


async def create_record(request: Request) -> JSONResponse:
    try:
        body = await _json_body(request)
        surface = str(body.get("surface") or "")
        if surface not in SURFACES:
            raise ValueError("surface must be tickets, specs, plans, research, or knowledge")
    except ValueError as error:
        return JSONResponse({"error": str(error)}, status_code=400)

    today = date.today()
    base_slug = _slug(body.get("slug"))
    stem = base_slug if surface == "specs" else _dated_slug(base_slug, today.isoformat())
    directory = _workspace_root(request) / ".loom" / surface
    directory.mkdir(parents=True, exist_ok=True)
    path, stem = _unique_path(directory, stem)
    record_id, content = _template(surface, stem, today)
    path.write_text(content, encoding="utf-8")

    record = parse_record(path, root=_workspace_root(request) / ".loom")
    if record is not None:
        await request.app.state.store.replace_record(record)
        await request.app.state.store.publish(RecordAdded(path=record.path, record=record))

    return JSONResponse({"id": record_id, "path": str(path.relative_to(_workspace_root(request) / ".loom")), "content": content})


async def create_chat_session(request: Request) -> JSONResponse:
    try:
        body = await _json_body(request)
    except ValueError as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    harness_command = str(body.get("harness_command") or "opencode run")
    session = _session_store(request).create(harness_command, body.get("document_path"))
    return JSONResponse({"session_id": session.id, "created_at": session.created_at, "session": _payload(session)})


async def get_chat_session(request: Request) -> JSONResponse:
    session = _session_store(request).get(request.path_params["session_id"])
    if session is None:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    return JSONResponse(_payload(session))


def _document_path(root: Path, document_path: str) -> Path | None:
    candidate = Path(document_path)
    if candidate.is_absolute():
        resolved = candidate.resolve()
    else:
        direct = (root / candidate).resolve()
        loom_relative = (root / ".loom" / candidate).resolve()
        resolved = direct if direct.exists() else loom_relative
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        return None
    return resolved


def _read_document(root: Path, document_path: str | None) -> str | None:
    if not document_path:
        return None
    path = _document_path(root, document_path)
    if path is None or not path.exists():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


async def send_chat_message(request: Request) -> JSONResponse:
    session_id = request.path_params["session_id"]
    store = _session_store(request)
    session = store.get(session_id)
    if session is None:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    if session.ended_at is not None:
        return JSONResponse({"error": "Session has ended"}, status_code=409)

    try:
        body = await _json_body(request)
        content = body["content"]
        if not isinstance(content, str) or not content.strip():
            raise ValueError("content must be a non-empty string")
        context = ChatContext.from_dict(body.get("context"))
    except (KeyError, ValueError) as error:
        return JSONResponse({"error": str(error)}, status_code=400)

    document_content = _read_document(_workspace_root(request), session.document_path)
    prompt = build_prompt(session, content, document_content, context)
    user_message = ChatMessage(role="user", content=content, context=context, timestamp=datetime.now().isoformat())
    store.add_message(session_id, user_message)

    async def broadcast(message: dict) -> None:
        await request.app.state.store.publish(ChatEvent(event=message["event"], data=message["data"]))

    try:
        response_text = await run_harness(session.harness_command, prompt, session_id, broadcast)
    except Exception as error:
        await broadcast({"event": "chat_error", "data": {"session_id": session_id, "error": str(error)}})
        return JSONResponse({"error": str(error)}, status_code=500)

    assistant_message = ChatMessage(role="assistant", content=response_text, timestamp=datetime.now().isoformat())
    store.add_message(session_id, assistant_message)
    return JSONResponse({"session_id": session_id, "message": asdict(assistant_message)})


async def end_chat_session(request: Request) -> JSONResponse:
    try:
        session = _session_store(request).end(request.path_params["session_id"])
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    return JSONResponse({"session_id": session.id, "ended_at": session.ended_at})
