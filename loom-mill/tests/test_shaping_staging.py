from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from loom_mill.api import shaping
from loom_mill.app import create_app
from loom_mill.shaping import BlockType, SessionPhase, ShapingSession
from loom_mill.shaping.commit import CommitFlow, atomic_write_all, generate_real_id
from loom_mill.shaping.engine import ShapingEngine
from loom_mill.shaping.models import StagedRecord
from loom_mill.shaping.orchestrator import ShapingOrchestrator
from loom_mill.state import MillStateStore
from loom_mill.workstation.config import HarnessConfig


class Request:
    def __init__(self, workspace_root: Path, store: MillStateStore, body: dict | None = None, path_params: dict | None = None):
        self.app = SimpleNamespace(state=SimpleNamespace(workspace_root=str(workspace_root), store=store))
        self._body = body or {}
        self.path_params = path_params or {}

    async def json(self):
        return self._body


def _body(response) -> dict:
    return json.loads(response.body)


def _init_git(path: Path) -> None:
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "loom@example.com"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Loom Test"], cwd=path, check=True, capture_output=True)


def test_staging_crud_persists_across_reload(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape work")

    record = session.staging.propose("tickets", "Auth Fix", "# Auth Fix")
    assert record.temp_id == "temp:tickets:auth-fix"

    updated = session.staging.update(record.temp_id, title="Auth Fix Updated", content="# Updated")
    assert updated.status == "modified"
    assert updated.title == "Auth Fix Updated"

    accepted = session.staging.accept(record.temp_id)
    assert accepted.status == "accepted"

    loaded = ShapingSession.load(session.session_id, tmp_path)
    assert loaded.state.staged_records[0].content == "# Updated"
    assert loaded.state.staged_records[0].status == "accepted"

    loaded.staging.reject(record.temp_id)
    assert ShapingSession.load(session.session_id, tmp_path).state.staged_records == []


def test_staging_branch_create_switch_and_merge(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape work")
    base = session.staging.propose("tickets", "Base Ticket", "# Base")

    session.staging.create_branch("alt", "Alternative")
    session.staging.switch_branch("alt")
    session.staging.propose("specs", "Alt Spec", f"References {base.temp_id}", branch="alt")
    alt_records = session.staging.list_branch("alt")

    assert session.state.active_branch == "alt"
    assert len(alt_records) == 2
    assert any(record.temp_id.endswith(":alt") for record in alt_records)

    session.staging.merge_branch("alt")

    assert session.state.active_branch == "main"
    assert session.state.branches == ["main"]
    assert session.staging.list_branch("alt") == []
    assert len(session.staging.list_branch("main")) == 2


@pytest.mark.asyncio
async def test_commit_writes_records_resolves_temp_ids_creates_knowledge_and_git_commit(tmp_path: Path) -> None:
    _init_git(tmp_path)
    session = ShapingSession.create(tmp_path, "shape auth work")
    ticket = session.staging.propose("tickets", "Auth Fix", "# Auth Fix\n\nID: temp:tickets:auth-fix\nDepends On: temp:specs:auth-spec\n")
    spec = session.staging.propose("specs", "Auth Spec", f"# Auth Spec\n\nRelated: {ticket.temp_id}\n")
    plan = session.staging.propose("plans", "Auth Plan", f"# Auth Plan\n\nIncludes {ticket.temp_id} and {spec.temp_id}\n")
    store = MillStateStore()
    subscription = store.subscribe()
    try:
        result = await CommitFlow(session, tmp_path, store).commit()
        event = await subscription.__anext__()
    finally:
        await subscription.aclose()

    ticket_id = generate_real_id("tickets", "Auth Fix")
    spec_id = generate_real_id("specs", "Auth Spec")
    ticket_path = tmp_path / ".loom" / "tickets" / f"{ticket_id.split(':')[1]}.md"
    spec_path = tmp_path / ".loom" / "specs" / f"{spec_id.split(':')[1]}.md"

    assert result.records_created == 3
    assert ticket_path.exists()
    assert spec_path.exists()
    assert "temp:" not in ticket_path.read_text(encoding="utf-8")
    assert f"ID: {ticket_id}" in ticket_path.read_text(encoding="utf-8")
    assert spec_id in ticket_path.read_text(encoding="utf-8")
    assert ticket_id in spec_path.read_text(encoding="utf-8")
    assert (tmp_path / result.session_record_path).exists()
    assert session.state.ended_at is not None
    assert event.event == "session_ended"
    assert event.data == {"reason": "committed", "records_created": 3}

    log = subprocess.run(["git", "log", "--format=%B", "-1"], cwd=tmp_path, check=True, capture_output=True, text=True).stdout
    assert "shape: 1 tickets, 1 specs, 1 plans" in log
    assert "Auth Fix" in log


@pytest.mark.asyncio
async def test_atomic_write_rolls_back_partial_files_on_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    first = StagedRecord("temp:tickets:first", "tickets", "First", "one", "main", "proposed", "now")
    second = StagedRecord("temp:specs:second", "specs", "Second", "two", "main", "proposed", "now")
    path_map = {first.temp_id: tmp_path / ".loom" / "tickets" / "first.md", second.temp_id: tmp_path / ".loom" / "specs" / "second.md"}
    original_write_text = Path.write_text

    def fail_second(path: Path, content: str, *args, **kwargs):
        if path.name == "second.md.tmp":
            raise OSError("simulated write failure")
        return original_write_text(path, content, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", fail_second)

    with pytest.raises(OSError):
        await atomic_write_all([first, second], path_map, tmp_path)

    assert not path_map[first.temp_id].exists()
    assert not path_map[second.temp_id].exists()


@pytest.mark.asyncio
async def test_staging_api_endpoints_and_routes(tmp_path: Path) -> None:
    store = MillStateStore()
    session_id = _body(await shaping.create_shaping_session(Request(tmp_path, store, {"input": "initial"})))["session_id"]

    create = await shaping.create_staged_record(Request(tmp_path, store, {"surface": "tickets", "title": "Auth Fix", "content": "# Auth Fix"}, {"session_id": session_id}))
    temp_id = _body(create)["record"]["temp_id"]
    update = await shaping.update_staged_record(Request(tmp_path, store, {"content": "# Updated", "title": "Auth Fix 2"}, {"session_id": session_id, "temp_id": temp_id}))
    accept = await shaping.accept_staged_record(Request(tmp_path, store, path_params={"session_id": session_id, "temp_id": temp_id}))
    delete = await shaping.delete_staged_record(Request(tmp_path, store, path_params={"session_id": session_id, "temp_id": temp_id}))

    assert create.status_code == 200
    assert _body(update)["record"]["status"] == "modified"
    assert _body(accept)["record"]["status"] == "accepted"
    assert _body(delete)["rejected"] == temp_id

    routes = [(route.path, route.methods or set()) for route in create_app().routes if hasattr(route, "methods")]
    assert ("/shaping/sessions/{session_id}/commit", {"POST"}) in [(path, methods) for path, methods in routes]
    assert any(path == "/shaping/sessions/{session_id}/staged/{temp_id}/accept" and "POST" in methods for path, methods in routes)


@pytest.mark.asyncio
async def test_engine_proposal_creates_staged_record(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape notification bug")
    session.update_phase(SessionPhase.NARROWING)
    store = MillStateStore()
    output = "```action\ntype: propose\nsurface: tickets\ntitle: Fix Notification Label\ncontent: # Fix Notification Label\n```"
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, HarnessConfig(command="printf", args=[output])), store)

    blocks = await engine.advance()

    assert blocks[0].type == BlockType.AGENT_PROPOSAL
    assert blocks[0].content["temp_id"] == "temp:tickets:fix-notification-label"
    assert session.state.staged_records[0].temp_id == blocks[0].content["temp_id"]
