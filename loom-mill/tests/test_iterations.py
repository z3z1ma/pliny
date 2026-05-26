from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import pytest_asyncio

from loom_mill.api.workstation import get_aggregate_diff, get_iteration, get_iteration_diff, list_iterations
from loom_mill.api.ws import _event_payload
from loom_mill.iterations import IterationStore
from loom_mill.state import MillStateStore, WorkstationTakt
from loom_mill.workstation import FactoryConfig, HarnessConfig, WorkstationEngine
from loom_mill.workstation.manager import WorkstationManager


class FakeRequest:
    def __init__(self, app, path_params: dict | None = None) -> None:
        self.app = app
        self.path_params = path_params or {}


async def _run(command: list[str], cwd: Path) -> str:
    process = await asyncio.create_subprocess_exec(
        *command,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    assert process.returncode == 0, stderr.decode(errors="replace")
    return stdout.decode(errors="replace")


@pytest_asyncio.fixture
async def git_workspace(tmp_path: Path) -> Path:
    await _run(["git", "init"], tmp_path)
    await _run(["git", "config", "user.email", "mill@example.invalid"], tmp_path)
    await _run(["git", "config", "user.name", "Mill Test"], tmp_path)
    ticket_path = tmp_path / ".loom" / "tickets" / "example-ticket.md"
    ticket_path.parent.mkdir(parents=True)
    ticket_path.write_text("# Example Ticket\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("test repo\n", encoding="utf-8")
    await _run(["git", "add", "."], tmp_path)
    await _run(["git", "commit", "-m", "initial"], tmp_path)
    return tmp_path


@pytest.mark.asyncio
async def test_commit_boundary_persists_iteration_metadata_and_diff(git_workspace: Path) -> None:
    ticket_path = git_workspace / ".loom" / "tickets" / "example-ticket.md"
    engine = WorkstationEngine(
        git_workspace,
        ticket_path,
        HarnessConfig(
            command=sys.executable,
            args=[
                "-c",
                "from pathlib import Path; import subprocess, time; "
                "Path('README.md').write_text('test repo\\nchanged\\n'); "
                "subprocess.run(['git', 'add', 'README.md'], check=True); "
                "subprocess.run(['git', 'commit', '-m', 'iteration'], check=True); "
                "time.sleep(0.2)",
            ],
        ),
        commit_poll_interval=0.05,
    )

    await engine.start()
    await engine.wait()

    records = IterationStore(git_workspace, engine.workstation_id).list()
    assert records[0].iteration == 1
    assert records[0].started_at.endswith("Z")
    assert records[0].ended_at.endswith("Z")
    assert records[0].duration_seconds > 0
    assert records[0].exit_code is None
    assert records[0].commit_sha
    assert records[0].files_changed == ["README.md"]
    assert records[0].lines_added == 1
    assert records[0].lines_removed == 0
    assert records[0].diff_stat == "+1 -0 across 1 file"
    assert "changed" in (git_workspace / ".mill" / "workstations" / engine.workstation_id / "iterations" / "1.diff").read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_exit_boundary_records_exit_code_and_survives_reload(git_workspace: Path) -> None:
    ticket_path = git_workspace / ".loom" / "tickets" / "example-ticket.md"
    engine = WorkstationEngine(
        git_workspace,
        ticket_path,
        HarnessConfig(command=sys.executable, args=["-c", "raise SystemExit(7)"]),
        commit_poll_interval=0.05,
    )

    await engine.start()
    await engine.wait()

    store = IterationStore(git_workspace, engine.workstation_id)
    reloaded = IterationStore(git_workspace, engine.workstation_id).get(1)
    assert store.root.joinpath("1.json").exists()
    assert reloaded.exit_code == 7
    assert reloaded.files_changed == []


@pytest.mark.asyncio
async def test_iteration_rest_endpoints_return_metadata_and_diffs(git_workspace: Path) -> None:
    ticket_path = git_workspace / ".loom" / "tickets" / "example-ticket.md"
    engine = WorkstationEngine(
        git_workspace,
        ticket_path,
        HarnessConfig(
            command=sys.executable,
            args=[
                "-c",
                "from pathlib import Path; import subprocess; "
                "Path('README.md').write_text('api diff\\n'); "
                "subprocess.run(['git', 'add', 'README.md'], check=True); "
                "subprocess.run(['git', 'commit', '-m', 'api'], check=True)",
            ],
        ),
    )
    await engine.start()
    await engine.wait()
    app = SimpleNamespace(state=SimpleNamespace(workspace_root=str(git_workspace)))
    params = {"workstation_id": engine.workstation_id, "iteration": "1"}

    listed = await list_iterations(FakeRequest(app, {"workstation_id": engine.workstation_id}))
    fetched = await get_iteration(FakeRequest(app, params))
    diff = await get_iteration_diff(FakeRequest(app, params))
    aggregate = await get_aggregate_diff(FakeRequest(app, {"workstation_id": engine.workstation_id}))

    assert json.loads(listed.body)[0]["iteration"] == 1
    assert json.loads(fetched.body)["files_changed"] == ["README.md"]
    assert "api diff" in diff.body.decode()
    assert "api diff" in aggregate.body.decode()


def test_takt_websocket_event_payload() -> None:
    payload = _event_payload(WorkstationTakt(workstation_id="ws-abc", iteration=3, duration_seconds=502))

    assert payload == {
        "workstation_id": "ws-abc",
        "event": "takt",
        "payload": {"iteration": 3, "duration_seconds": 502},
    }


@pytest.mark.asyncio
async def test_manager_emits_takt_event_after_iteration(git_workspace: Path) -> None:
    store = MillStateStore()
    manager = WorkstationManager(
        git_workspace,
        store,
        FactoryConfig(harness=HarnessConfig(command=sys.executable, args=["-c", "print('done')"])),
    )
    subscription = store.subscribe()
    try:
        engine = await manager.start(git_workspace / ".loom" / "tickets" / "example-ticket.md", "example-ticket")
        while True:
            event = await asyncio.wait_for(subscription.__anext__(), timeout=2)
            if isinstance(event, WorkstationTakt):
                payload = _event_payload(event)
                assert payload["workstation_id"] == engine.workstation_id
                assert payload["event"] == "takt"
                assert payload["payload"]["iteration"] == 1
                assert payload["payload"]["duration_seconds"] > 0
                break
    finally:
        await subscription.aclose()
        await manager.shutdown()
