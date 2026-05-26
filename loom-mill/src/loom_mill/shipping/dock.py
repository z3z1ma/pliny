from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from loom_mill.state import ShippingEvent, WorkstationStateChanged
from loom_mill.workstation import WorkstationStatus
from loom_mill.workstation.manager import WorkstationManager


ShippingAction = Literal["merged", "conflict", "skipped", "aborted"]


@dataclass(frozen=True)
class ShippingResult:
    workstation_id: str
    ticket_id: str
    action: ShippingAction
    target_branch: str
    merge_sha: str | None = None
    conflict_files: list[str] | None = None


@dataclass(frozen=True)
class ShippingQueueEntry:
    workstation_id: str
    ticket_id: str
    target_branch: str
    status: str


@dataclass(frozen=True)
class GitResult:
    returncode: int
    stdout: str
    stderr: str


class ShippingDock:
    def __init__(self, workspace_root: Path, manager: WorkstationManager) -> None:
        self.workspace_root = workspace_root.resolve()
        self.manager = manager
        self.store = manager.store
        self.config = manager.config

    async def ship(self, workstation_id: str) -> ShippingResult:
        engine = self._require_engine(workstation_id)
        target_branch = self._target_branch(engine.ticket_path)
        worktree_ref = await self._worktree_ref(engine.state.worktree_path)

        await self._git("checkout", target_branch, check=True)
        merge = await self._git(
            "merge",
            "--no-ff",
            worktree_ref,
            "-m",
            f"Merge {engine.ticket_id} from workstation {workstation_id}",
            check=False,
        )
        if merge.returncode != 0:
            conflict_files = await self._conflict_files()
            await self._git("merge", "--abort", check=False)
            engine.state.status = WorkstationStatus.CONFLICT
            engine.state.andon.active = True
            await self._publish_state(engine)
            return await self._publish_result(
                ShippingResult(
                    workstation_id=workstation_id,
                    ticket_id=engine.ticket_id,
                    action="conflict",
                    target_branch=target_branch,
                    conflict_files=conflict_files,
                )
            )

        merge_sha = (await self._git("rev-parse", "HEAD", check=True)).stdout.strip()
        await self._cleanup(engine, worktree_ref, delete_branch=self.config.cleanup_branch_after_merge)
        engine.state.status = WorkstationStatus.FINISHED
        await self._publish_state(engine)
        return await self._publish_result(
            ShippingResult(
                workstation_id=workstation_id,
                ticket_id=engine.ticket_id,
                action="merged",
                target_branch=target_branch,
                merge_sha=merge_sha,
            )
        )

    async def skip(self, workstation_id: str) -> ShippingResult:
        engine = self._require_engine(workstation_id)
        target_branch = self._target_branch(engine.ticket_path)
        worktree_ref = await self._worktree_ref(engine.state.worktree_path)
        await self._cleanup(engine, worktree_ref, delete_branch=self.config.cleanup_branch_after_merge)
        engine.state.status = WorkstationStatus.FINISHED
        await self._publish_state(engine)
        return await self._publish_result(
            ShippingResult(workstation_id=workstation_id, ticket_id=engine.ticket_id, action="skipped", target_branch=target_branch)
        )

    async def abort(self, workstation_id: str) -> ShippingResult:
        engine = self._require_engine(workstation_id)
        target_branch = self._target_branch(engine.ticket_path)
        worktree_ref = await self._worktree_ref(engine.state.worktree_path)
        await self._cleanup(engine, worktree_ref, delete_branch=self.config.cleanup_branch_after_merge, allow_dirty=True)
        engine.state.status = WorkstationStatus.STOPPED
        await self._publish_state(engine)
        return await self._publish_result(
            ShippingResult(workstation_id=workstation_id, ticket_id=engine.ticket_id, action="aborted", target_branch=target_branch)
        )

    async def resolve_conflict(self, workstation_id: str) -> ShippingResult:
        engine = self._require_engine(workstation_id)
        engine.state.andon.active = False
        engine.state.andon.signals = []
        return await self.ship(workstation_id)

    def get_queue(self) -> list[ShippingQueueEntry]:
        if self.config.shipping_mode != "operator-approved":
            return []
        return [
            ShippingQueueEntry(
                workstation_id=engine.workstation_id,
                ticket_id=engine.ticket_id,
                target_branch=self._target_branch(engine.ticket_path),
                status=engine.state.status.value,
            )
            for engine in self.manager.workstations.values()
            if self._is_ready(engine.ticket_path) and engine.state.status in {WorkstationStatus.COMPLETED, WorkstationStatus.FINISHED}
        ]

    async def handle_finished(self, workstation_id: str) -> ShippingResult | None:
        engine = self._require_engine(workstation_id)
        if not self._is_ready(engine.ticket_path):
            return None
        if self.config.shipping_mode == "operator-approved":
            return None
        return await self.ship(workstation_id)

    def _require_engine(self, workstation_id: str):
        engine = self.manager.get(workstation_id)
        if engine is None:
            raise KeyError(workstation_id)
        if engine.state.worktree_path is None:
            raise RuntimeError("workstation has no worktree")
        return engine

    def _target_branch(self, ticket_path: Path) -> str:
        if ticket_path.exists():
            match = re.search(r"^Target Branch:\s*(\S+)\s*$", ticket_path.read_text(encoding="utf-8"), re.MULTILINE)
            if match:
                return match.group(1)
        return self.config.default_target_branch

    def _is_ready(self, ticket_path: Path) -> bool:
        if not ticket_path.exists():
            return False
        match = re.search(r"^Status:\s*(\S+)\s*$", ticket_path.read_text(encoding="utf-8"), re.MULTILINE)
        return bool(match and match.group(1) in self.config.ready_to_ship_statuses)

    async def _worktree_ref(self, worktree_path: Path | None) -> str:
        if worktree_path is None:
            raise RuntimeError("workstation has no worktree")
        branch = (await self._git_cwd(worktree_path, "rev-parse", "--abbrev-ref", "HEAD", check=True)).stdout.strip()
        if branch and branch != "HEAD":
            return branch
        return (await self._git_cwd(worktree_path, "rev-parse", "HEAD", check=True)).stdout.strip()

    async def _cleanup(self, engine, worktree_ref: str, *, delete_branch: bool, allow_dirty: bool = False) -> None:
        worktree_path = engine.state.worktree_path
        if worktree_path is not None:
            dirty = (await self._git_cwd(worktree_path, "status", "--porcelain", check=True)).stdout.strip()
            if dirty and not allow_dirty:
                raise RuntimeError("worktree has uncommitted changes; abort shipping or commit them before cleanup")
            await self._git("worktree", "remove", str(worktree_path), "--force", check=True)
            engine.state.worktree_path = None
        if delete_branch and not re.fullmatch(r"[0-9a-f]{40}", worktree_ref):
            await self._git("branch", "-D", worktree_ref, check=False)

    async def _conflict_files(self) -> list[str]:
        output = await self._git("diff", "--name-only", "--diff-filter=U", check=False)
        return [line for line in output.stdout.splitlines() if line.strip()]

    async def _publish_state(self, engine) -> None:
        await self.store.replace_workstation_state(engine.workstation_id, engine.state)
        await self.store.publish(WorkstationStateChanged(workstation_id=engine.workstation_id, workstation=engine.state))

    async def _publish_result(self, result: ShippingResult) -> ShippingResult:
        await self.store.publish(
            ShippingEvent(
                workstation_id=result.workstation_id,
                ticket_id=result.ticket_id,
                action=result.action,
                target_branch=result.target_branch,
                merge_sha=result.merge_sha,
                conflict_files=result.conflict_files,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
        )
        return result

    async def _git(self, *args: str, check: bool) -> GitResult:
        return await self._git_cwd(self.workspace_root, *args, check=check)

    async def _git_cwd(self, cwd: Path, *args: str, check: bool) -> GitResult:
        process = await asyncio.create_subprocess_exec(
            "git",
            *args,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        result = GitResult(process.returncode, stdout.decode(errors="replace"), stderr.decode(errors="replace"))
        if check and result.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
        return result
