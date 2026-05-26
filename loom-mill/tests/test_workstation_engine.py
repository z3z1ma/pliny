from __future__ import annotations

import asyncio
import os
from pathlib import Path

import pytest
import pytest_asyncio

from loom_mill.workstation import HarnessConfig, WorkstationEngine, WorkstationStatus


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
async def test_workstation_starts_harness_and_captures_output(git_workspace: Path) -> None:
    ticket_path = git_workspace / ".loom" / "tickets" / "example-ticket.md"
    engine = WorkstationEngine(
        git_workspace,
        ticket_path,
        HarnessConfig(
            command="python",
            args=["-c", "import os,sys; print(sys.argv[1]); print(os.environ['MILL_TEST_ENV'])", "{ticket_path}"],
            env={"MILL_TEST_ENV": "configured"},
        ),
    )

    await engine.start()
    worktree_path = engine.state.worktree_path
    assert worktree_path is not None
    assert worktree_path.exists()

    await engine.wait()

    assert engine.state.status == WorkstationStatus.COMPLETED
    assert engine.state.exit_code == 0
    stdout = engine.log_path("stdout").read_text(encoding="utf-8")
    assert str(ticket_path) in stdout
    assert "configured" in stdout


@pytest.mark.asyncio
async def test_workstation_records_failed_exit(git_workspace: Path) -> None:
    ticket_path = git_workspace / ".loom" / "tickets" / "example-ticket.md"
    engine = WorkstationEngine(
        git_workspace,
        ticket_path,
        HarnessConfig(command="python", args=["-c", "import sys; print('bad', file=sys.stderr); raise SystemExit(7)"]),
    )

    await engine.start()
    await engine.wait()

    assert engine.state.status == WorkstationStatus.COMPLETED
    assert engine.state.exit_code == 7
    stderr = engine.log_path("stderr").read_text(encoding="utf-8")
    assert "bad" in stderr


@pytest.mark.asyncio
async def test_workstation_stop_terminates_process(git_workspace: Path) -> None:
    ticket_path = git_workspace / ".loom" / "tickets" / "example-ticket.md"
    engine = WorkstationEngine(
        git_workspace,
        ticket_path,
        HarnessConfig(command="python", args=["-c", "import time; time.sleep(60)"]),
        stop_timeout=1,
    )

    await engine.start()
    await engine.stop()

    assert engine.state.status == WorkstationStatus.STOPPED
    assert engine.state.exit_code is not None


@pytest.mark.asyncio
async def test_workstation_teardown_removes_worktree(git_workspace: Path) -> None:
    ticket_path = git_workspace / ".loom" / "tickets" / "example-ticket.md"
    engine = WorkstationEngine(
        git_workspace,
        ticket_path,
        HarnessConfig(command="python", args=["-c", "print('done')"]),
    )

    await engine.start()
    worktree_path = engine.state.worktree_path
    assert worktree_path is not None
    await engine.wait()
    await engine.teardown()

    assert not worktree_path.exists()
    worktrees = await _run(["git", "worktree", "list", "--porcelain"], git_workspace)
    assert str(worktree_path) not in worktrees


@pytest.mark.asyncio
async def test_workstation_pause_records_paused_state(git_workspace: Path) -> None:
    ticket_path = git_workspace / ".loom" / "tickets" / "example-ticket.md"
    engine = WorkstationEngine(
        git_workspace,
        ticket_path,
        HarnessConfig(command="python", args=["-c", "import time; time.sleep(60)"]),
        stop_timeout=1,
    )

    await engine.start()
    await engine.pause()

    assert engine.state.status == WorkstationStatus.PAUSED
    assert engine.state.exit_code is not None


@pytest.mark.asyncio
async def test_workstation_resume_starts_fresh_process_with_updated_ticket(git_workspace: Path) -> None:
    ticket_path = git_workspace / ".loom" / "tickets" / "example-ticket.md"
    engine = WorkstationEngine(
        git_workspace,
        ticket_path,
        HarnessConfig(command="python", args=["-c", "import pathlib,sys; print(pathlib.Path(sys.argv[1]).read_text())", "{ticket_path}"]),
        stop_timeout=1,
    )

    await engine.start()
    first_pid = engine.state.process_id
    await engine.pause()
    ticket_path.write_text("# Example Ticket\n\nConstraint: updated during pause\n", encoding="utf-8")

    await engine.resume()
    second_pid = engine.state.process_id
    await engine.wait()

    assert engine.state.status == WorkstationStatus.COMPLETED
    assert second_pid is not None
    assert second_pid != first_pid
    stdout = engine.log_path("stdout").read_text(encoding="utf-8")
    assert "Constraint: updated during pause" in stdout


@pytest.mark.asyncio
async def test_workstation_uses_relative_cwd_override(git_workspace: Path) -> None:
    ticket_path = git_workspace / ".loom" / "tickets" / "example-ticket.md"
    (git_workspace / "nested").mkdir()
    (git_workspace / "nested" / ".gitkeep").write_text("", encoding="utf-8")
    await _run(["git", "add", "."], git_workspace)
    await _run(["git", "commit", "-m", "add nested"], git_workspace)
    engine = WorkstationEngine(
        git_workspace,
        ticket_path,
        HarnessConfig(command="python", args=["-c", "import os; print(os.getcwd())"], cwd="nested"),
    )

    await engine.start()
    await engine.wait()

    stdout = engine.log_path("stdout").read_text(encoding="utf-8")
    assert os.fspath(engine.state.worktree_path / "nested") in stdout
