from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import pytest_asyncio

from loom_mill.api.shipping import ship_workstation, shipping_queue
from loom_mill.shipping import ShippingDock
from loom_mill.state import MillStateStore, ShippingEvent
from loom_mill.workstation import FactoryConfig, HarnessConfig, WorkstationEngine, WorkstationStatus
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
    await _run(["git", "init", "-b", "main"], tmp_path)
    await _run(["git", "config", "user.email", "mill@example.invalid"], tmp_path)
    await _run(["git", "config", "user.name", "Mill Test"], tmp_path)
    (tmp_path / ".loom" / "tickets").mkdir(parents=True)
    (tmp_path / "README.md").write_text("base\n", encoding="utf-8")
    await _run(["git", "add", "."], tmp_path)
    await _run(["git", "commit", "-m", "initial"], tmp_path)
    return tmp_path


async def _add_workstation(manager: WorkstationManager, ticket_id: str, branch: str, body: str = "Status: review\n") -> WorkstationEngine:
    ticket_path = manager.workspace_root / ".loom" / "tickets" / f"{ticket_id}.md"
    ticket_path.write_text(f"# {ticket_id}\n\n{body}", encoding="utf-8")
    worktree_path = manager.workspace_root / ".mill" / "worktrees" / branch
    worktree_path.parent.mkdir(parents=True, exist_ok=True)
    await _run(["git", "worktree", "add", "-b", branch, str(worktree_path), "HEAD"], manager.workspace_root)
    engine = WorkstationEngine(
        manager.workspace_root,
        ticket_path,
        HarnessConfig(command=sys.executable, args=["-c", "print('unused')"]),
        workstation_id=f"ws-{ticket_id}",
        ticket_id=ticket_id,
    )
    engine.state.status = WorkstationStatus.COMPLETED
    engine.state.worktree_path = worktree_path
    manager.workstations[engine.workstation_id] = engine
    return engine


async def _commit_file(worktree_path: Path, name: str, content: str, message: str) -> None:
    (worktree_path / name).write_text(content, encoding="utf-8")
    await _run(["git", "add", name], worktree_path)
    await _run(["git", "commit", "-m", message], worktree_path)


@pytest.mark.asyncio
async def test_auto_merge_creates_no_ff_merge_and_cleans_worktree(git_workspace: Path) -> None:
    store = MillStateStore()
    manager = WorkstationManager(git_workspace, store, FactoryConfig(default_target_branch="main"))
    engine = await _add_workstation(manager, "ticket-a", "ws-ticket-a")
    await _commit_file(engine.state.worktree_path, "a.txt", "a\n", "ticket a")
    subscription = store.subscribe()

    result = await ShippingDock(git_workspace, manager).ship(engine.workstation_id)

    assert result.action == "merged"
    assert result.merge_sha is not None
    assert engine.state.status == WorkstationStatus.FINISHED
    assert engine.state.worktree_path is None
    assert not (git_workspace / ".mill" / "worktrees" / "ws-ticket-a").exists()
    parents = await _run(["git", "rev-list", "--parents", "-n", "1", "HEAD"], git_workspace)
    assert len(parents.split()) == 3
    branches = await _run(["git", "branch", "--list", "ws-ticket-a"], git_workspace)
    assert branches.strip() == ""
    event = await subscription.__anext__()
    while not isinstance(event, ShippingEvent):
        event = await subscription.__anext__()
    assert event.action == "merged"


@pytest.mark.asyncio
async def test_operator_approved_queues_until_explicit_ship(git_workspace: Path) -> None:
    store = MillStateStore()
    manager = WorkstationManager(
        git_workspace,
        store,
        FactoryConfig(shipping_mode="operator-approved", default_target_branch="main"),
    )
    engine = await _add_workstation(manager, "ticket-a", "ws-ticket-a")
    await _commit_file(engine.state.worktree_path, "a.txt", "a\n", "ticket a")
    app = SimpleNamespace(state=SimpleNamespace(workspace_root=str(git_workspace), workstation_manager=manager))

    queued = await shipping_queue(FakeRequest(app))
    assert json.loads(queued.body)[0]["workstation_id"] == engine.workstation_id
    assert not (git_workspace / "a.txt").exists()

    shipped = await ship_workstation(FakeRequest(app, {"workstation_id": engine.workstation_id}))
    assert shipped.status_code == 200
    assert json.loads(shipped.body)["action"] == "merged"
    assert (git_workspace / "a.txt").read_text(encoding="utf-8") == "a\n"


@pytest.mark.asyncio
async def test_target_branch_uses_ticket_override(git_workspace: Path) -> None:
    await _run(["git", "checkout", "-b", "dev"], git_workspace)
    await _run(["git", "checkout", "main"], git_workspace)
    await _run(["git", "checkout", "-b", "feature-x"], git_workspace)
    await _run(["git", "checkout", "main"], git_workspace)
    store = MillStateStore()
    manager = WorkstationManager(git_workspace, store, FactoryConfig(default_target_branch="dev"))
    engine = await _add_workstation(manager, "ticket-a", "ws-ticket-a", "Status: review\nTarget Branch: feature-x\n")
    await _commit_file(engine.state.worktree_path, "target.txt", "target\n", "target change")

    result = await ShippingDock(git_workspace, manager).ship(engine.workstation_id)

    assert result.target_branch == "feature-x"
    feature_tree = await _run(["git", "ls-tree", "--name-only", "feature-x"], git_workspace)
    dev_tree = await _run(["git", "ls-tree", "--name-only", "dev"], git_workspace)
    assert "target.txt" in feature_tree
    assert "target.txt" not in dev_tree


@pytest.mark.asyncio
async def test_merge_conflict_sets_conflict_state_and_reports_files(git_workspace: Path) -> None:
    (git_workspace / "shared.txt").write_text("base\n", encoding="utf-8")
    await _run(["git", "add", "shared.txt"], git_workspace)
    await _run(["git", "commit", "-m", "shared base"], git_workspace)
    store = MillStateStore()
    manager = WorkstationManager(git_workspace, store, FactoryConfig(default_target_branch="main"))
    engine = await _add_workstation(manager, "ticket-a", "ws-ticket-a")
    await _commit_file(engine.state.worktree_path, "shared.txt", "worktree\n", "worktree conflict")
    (git_workspace / "shared.txt").write_text("main\n", encoding="utf-8")
    await _run(["git", "add", "shared.txt"], git_workspace)
    await _run(["git", "commit", "-m", "main conflict"], git_workspace)

    result = await ShippingDock(git_workspace, manager).ship(engine.workstation_id)

    assert result.action == "conflict"
    assert result.conflict_files == ["shared.txt"]
    assert engine.state.status == WorkstationStatus.CONFLICT
    assert engine.state.andon.active is True
    unresolved = await _run(["git", "diff", "--name-only", "--diff-filter=U"], git_workspace)
    assert unresolved.strip() == ""
    assert engine.state.worktree_path.exists()


@pytest.mark.asyncio
async def test_sequential_merges_include_previous_changes(git_workspace: Path) -> None:
    store = MillStateStore()
    manager = WorkstationManager(git_workspace, store, FactoryConfig(default_target_branch="main"))
    first = await _add_workstation(manager, "ticket-a", "ws-ticket-a")
    await _commit_file(first.state.worktree_path, "a.txt", "a\n", "ticket a")
    second = await _add_workstation(manager, "ticket-b", "ws-ticket-b")
    await _commit_file(second.state.worktree_path, "b.txt", "b\n", "ticket b")

    await ShippingDock(git_workspace, manager).ship(first.workstation_id)
    await ShippingDock(git_workspace, manager).ship(second.workstation_id)

    assert (git_workspace / "a.txt").read_text(encoding="utf-8") == "a\n"
    assert (git_workspace / "b.txt").read_text(encoding="utf-8") == "b\n"


@pytest.mark.asyncio
async def test_skip_cleans_worktree_without_merge(git_workspace: Path) -> None:
    store = MillStateStore()
    manager = WorkstationManager(git_workspace, store, FactoryConfig(default_target_branch="main"))
    engine = await _add_workstation(manager, "ticket-a", "ws-ticket-a")
    await _commit_file(engine.state.worktree_path, "skip.txt", "skip\n", "skip change")

    result = await ShippingDock(git_workspace, manager).skip(engine.workstation_id)

    assert result.action == "skipped"
    assert engine.state.status == WorkstationStatus.FINISHED
    assert not (git_workspace / "skip.txt").exists()
    assert not (git_workspace / ".mill" / "worktrees" / "ws-ticket-a").exists()
