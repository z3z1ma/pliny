from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from loom_mill.api import shaping
from loom_mill.app import create_app
from loom_mill.shaping import CanvasNodeType, SessionPhase, ShapingSession
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

    with pytest.raises(ValueError, match="accepted"):
        loaded.staging.reject(record.temp_id)
    assert ShapingSession.load(session.session_id, tmp_path).state.staged_records[0].status == "accepted"


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
    session.staging.accept(ticket.temp_id)
    session.staging.accept(spec.temp_id)
    session.staging.accept(plan.temp_id)
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
async def test_commit_only_writes_accepted_records(tmp_path: Path) -> None:
    _init_git(tmp_path)
    session = ShapingSession.create(tmp_path, "shape accepted only")
    accepted = session.staging.propose("tickets", "Accepted Ticket", "# Accepted Ticket\n")
    pending = session.staging.propose("specs", "Pending Spec", "# Pending Spec\n")
    session.staging.accept(accepted.temp_id)
    store = MillStateStore()

    result = await CommitFlow(session, tmp_path, store).commit()

    accepted_id = generate_real_id("tickets", "Accepted Ticket")
    pending_id = generate_real_id("specs", "Pending Spec")
    accepted_path = tmp_path / ".loom" / "tickets" / f"{accepted_id.split(':')[1]}.md"
    pending_path = tmp_path / ".loom" / "specs" / f"{pending_id.split(':')[1]}.md"

    assert result.records_created == 1
    assert accepted_path.exists()
    assert not pending_path.exists()
    assert all("pending-spec" not in path for path in result.paths)


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
async def test_commit_failure_resets_index_and_deletes_written_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _init_git(tmp_path)
    session = ShapingSession.create(tmp_path, "shape rollback")
    record = session.staging.propose("tickets", "Rollback Ticket", "# Rollback Ticket\n")
    session.staging.accept(record.temp_id)
    store = MillStateStore()
    flow = CommitFlow(session, tmp_path, store)
    original_run_git = flow._run_git

    def fail_commit(args: list[str]) -> None:
        if args and args[0] == "commit":
            raise RuntimeError("simulated commit failure")
        original_run_git(args)

    monkeypatch.setattr(flow, "_run_git", fail_commit)

    with pytest.raises(RuntimeError, match="rolled back written files"):
        await flow.commit()

    status = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=tmp_path, check=True, capture_output=True, text=True)
    assert status.stdout.strip() == ""
    assert not (tmp_path / ".loom" / "tickets" / f"{generate_real_id('tickets', 'Rollback Ticket').split(':')[1]}.md").exists()


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
    assert delete.status_code == 400
    assert "accepted" in _body(delete)["error"]

    routes = [(route.path, route.methods or set()) for route in create_app().routes if hasattr(route, "methods")]
    assert ("/shaping/sessions/{session_id}/commit", {"POST"}) in [(path, methods) for path, methods in routes]
    assert any(path == "/shaping/sessions/{session_id}/staged/{temp_id}/accept" and "POST" in methods for path, methods in routes)


@pytest.mark.asyncio
async def test_engine_proposal_creates_staged_record(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape notification bug")
    session.update_phase(SessionPhase.NARROWING)
    store = MillStateStore()
    output = '<node type="record" surface="tickets" title="Fix Notification Label"># Fix Notification Label</node>'
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, HarnessConfig(command="printf", args=[output])), store)

    nodes = await engine.advance()

    assert nodes[0].type == CanvasNodeType.RECORD
    assert nodes[0].content["temp_id"] == "temp:tickets:fix-notification-label"
    assert session.state.staged_records[0].temp_id == nodes[0].content["temp_id"]


def _session_with_two_specs(tmp_path) -> ShapingSession:
    session = ShapingSession.create(tmp_path, "shape a feature")
    session.staging.propose("specs", "Spec A", "# Spec A\nbody a", "main")
    session.staging.propose("specs", "Spec B", "# Spec B\nbody b", "main")
    return session


def test_consolidate_stages_merged_and_discards_targets(tmp_path) -> None:
    session = _session_with_two_specs(tmp_path)
    merged = session.staging.consolidate(
        ["temp:specs:spec-a", "temp:specs:spec-b"],
        surface="specs",
        title="Spec Combined",
        content="# Spec Combined\nmerged body",
    )
    temp_ids = {r.temp_id for r in session.state.staged_records}
    assert merged.temp_id in temp_ids
    assert "temp:specs:spec-a" not in temp_ids
    assert "temp:specs:spec-b" not in temp_ids


def test_consolidate_refuses_accepted_target(tmp_path) -> None:
    session = _session_with_two_specs(tmp_path)
    session.staging.accept("temp:specs:spec-a")
    with pytest.raises(ValueError, match="accepted"):
        session.staging.consolidate(
            ["temp:specs:spec-a", "temp:specs:spec-b"],
            surface="specs",
            title="Spec Combined",
            content="# merged",
        )


def test_accepted_record_is_immutable_except_idempotent_accept(tmp_path) -> None:
    session = ShapingSession.create(tmp_path, "shape a feature")
    record = session.staging.propose("specs", "Accepted", "# Accepted", "main")
    accepted = session.staging.accept(record.temp_id)
    modified_at = accepted.modified_at

    assert session.staging.accept(record.temp_id).modified_at == modified_at
    with pytest.raises(ValueError, match="accepted"):
        session.staging.update(record.temp_id, content="# Mutated")
    with pytest.raises(ValueError, match="accepted"):
        session.staging.reject(record.temp_id)
    assert session.staging._find(record.temp_id).content == "# Accepted"


@pytest.mark.asyncio
async def test_staging_api_refuses_to_update_accepted_record(tmp_path: Path) -> None:
    store = MillStateStore()
    session_id = _body(await shaping.create_shaping_session(Request(tmp_path, store, {"input": "initial"})))["session_id"]
    create = await shaping.create_staged_record(
        Request(tmp_path, store, {"surface": "specs", "title": "Accepted", "content": "# Accepted"}, {"session_id": session_id})
    )
    temp_id = _body(create)["record"]["temp_id"]
    await shaping.accept_staged_record(Request(tmp_path, store, path_params={"session_id": session_id, "temp_id": temp_id}))

    update = await shaping.update_staged_record(
        Request(tmp_path, store, {"content": "# Mutated"}, {"session_id": session_id, "temp_id": temp_id})
    )

    assert update.status_code == 400
    assert "accepted" in _body(update)["error"]


def test_consolidate_allows_merged_id_matching_removed_target_without_duplicates(tmp_path) -> None:
    session = _session_with_two_specs(tmp_path)

    merged = session.staging.consolidate(
        ["temp:specs:spec-a", "temp:specs:spec-b"],
        surface="specs",
        title="Spec A",
        content="# Spec A\nmerged",
    )

    temp_ids = [record.temp_id for record in session.state.staged_records]
    assert merged.temp_id == "temp:specs:spec-a"
    assert temp_ids.count("temp:specs:spec-a") == 1
    assert "temp:specs:spec-b" not in temp_ids


def test_consolidate_rejects_duplicate_targets_before_mutating(tmp_path) -> None:
    session = _session_with_two_specs(tmp_path)

    with pytest.raises(ValueError, match="unique"):
        session.staging.consolidate(
            ["temp:specs:spec-a", "temp:specs:spec-a"],
            surface="specs",
            title="Spec Combined",
            content="# merged",
        )

    assert {record.temp_id for record in session.state.staged_records} == {"temp:specs:spec-a", "temp:specs:spec-b"}
