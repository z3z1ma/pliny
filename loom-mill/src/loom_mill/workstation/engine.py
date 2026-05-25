from __future__ import annotations

import asyncio
import os
import re
import shutil
import signal
from pathlib import Path

from .config import HarnessConfig
from .models import OutputEvent, WorkstationState, WorkstationStatus


class WorkstationEngine:
    def __init__(
        self,
        workspace_root: Path,
        ticket_path: Path,
        harness: HarnessConfig,
        *,
        stop_timeout: float = 5.0,
    ) -> None:
        self.workspace_root = workspace_root.resolve()
        self.ticket_path = ticket_path.resolve()
        self.harness = harness
        self.stop_timeout = stop_timeout
        self.state = WorkstationState()
        self.output_queue: asyncio.Queue[OutputEvent] = asyncio.Queue()
        self._process: asyncio.subprocess.Process | None = None
        self._capture_tasks: list[asyncio.Task[None]] = []
        self._wait_task: asyncio.Task[int] | None = None

    async def start(self) -> WorkstationState:
        if self.state.status != WorkstationStatus.IDLE:
            raise RuntimeError(f"cannot start workstation from {self.state.status}")

        worktree_path = self.workspace_root / ".mill" / "worktrees" / self._ticket_slug()
        worktree_path.parent.mkdir(parents=True, exist_ok=True)
        await self._run_git("worktree", "add", "--detach", str(worktree_path), "HEAD")

        env = os.environ.copy()
        if self.harness.env:
            env.update(self.harness.env)

        process = await asyncio.create_subprocess_exec(
            *self.harness.command_line(self.ticket_path),
            cwd=self._process_cwd(worktree_path),
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        self._process = process
        self.state.status = WorkstationStatus.RUNNING
        self.state.worktree_path = worktree_path
        self.state.process_id = process.pid
        self._capture_tasks = [
            asyncio.create_task(self._capture_stream("stdout", process.stdout)),
            asyncio.create_task(self._capture_stream("stderr", process.stderr)),
        ]
        self._wait_task = asyncio.create_task(self._wait_for_exit())
        return self.state

    async def wait(self) -> WorkstationState:
        if self._wait_task is None:
            return self.state
        await self._wait_task
        return self.state

    async def stop(self) -> WorkstationState:
        return await self._terminate(WorkstationStatus.STOPPED)

    async def pause(self) -> WorkstationState:
        return await self._terminate(WorkstationStatus.PAUSED)

    async def teardown(self) -> None:
        if self.state.status == WorkstationStatus.RUNNING:
            raise RuntimeError("cannot teardown a running workstation")
        if self.state.worktree_path is None:
            return

        worktree_path = self.state.worktree_path
        await self._run_git("worktree", "remove", "--force", str(worktree_path))
        if worktree_path.exists():
            shutil.rmtree(worktree_path)

    async def _terminate(self, status: WorkstationStatus) -> WorkstationState:
        process = self._process
        if process is None or process.returncode is not None:
            self.state.status = status
            return self.state

        self.state.status = status
        process.send_signal(signal.SIGTERM)
        try:
            await asyncio.wait_for(process.wait(), timeout=self.stop_timeout)
        except TimeoutError:
            process.kill()
            await process.wait()

        await asyncio.gather(*self._capture_tasks)
        self.state.exit_code = process.returncode
        return self.state

    async def _wait_for_exit(self) -> int:
        if self._process is None:
            raise RuntimeError("workstation process was not started")
        exit_code = await self._process.wait()
        await asyncio.gather(*self._capture_tasks)
        self.state.exit_code = exit_code
        if self.state.status == WorkstationStatus.RUNNING:
            self.state.status = WorkstationStatus.COMPLETED
        return exit_code

    async def _capture_stream(
        self,
        stream: str,
        reader: asyncio.StreamReader | None,
    ) -> None:
        if reader is None:
            return
        while chunk := await reader.read(4096):
            event = OutputEvent(stream=stream, data=chunk.decode(errors="replace"))
            self.state.output.append(event)
            await self.output_queue.put(event)

    async def _run_git(self, *args: str) -> None:
        process = await asyncio.create_subprocess_exec(
            "git",
            *args,
            cwd=self.workspace_root,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await process.communicate()
        if process.returncode != 0:
            message = stderr.decode(errors="replace").strip()
            raise RuntimeError(f"git {' '.join(args)} failed: {message}")

    def _process_cwd(self, worktree_path: Path) -> Path:
        if self.harness.cwd is None:
            return worktree_path
        cwd = Path(self.harness.cwd)
        return cwd if cwd.is_absolute() else worktree_path / cwd

    def _ticket_slug(self) -> str:
        stem = self.ticket_path.stem.lower()
        slug = re.sub(r"[^a-z0-9._-]+", "-", stem).strip("-._")
        return slug or "workstation"
