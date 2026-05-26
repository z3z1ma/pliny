from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import signal
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from loom_mill.iterations import IterationRecord, IterationStore
from loom_mill.processes import summarize_iteration
from loom_mill.processes.backpressure import IterationRecord as BackpressureIterationRecord, detect_backpressure

from .config import HarnessConfig
from .models import OutputEvent, WorkstationState, WorkstationStatus

MAX_LOG_LINE_BYTES = 10_000


class WorkstationEngine:
    def __init__(
        self,
        workspace_root: Path,
        ticket_path: Path,
        harness: HarnessConfig,
        *,
        workstation_id: str | None = None,
        ticket_id: str | None = None,
        stop_timeout: float = 5.0,
        commit_poll_interval: float = 2.0,
    ) -> None:
        self.workspace_root = workspace_root.resolve()
        self.ticket_path = ticket_path.resolve()
        self.workstation_id = workstation_id or self._ticket_slug()
        self.ticket_id = ticket_id or self._ticket_slug()
        self.harness = harness
        self.stop_timeout = stop_timeout
        self.commit_poll_interval = commit_poll_interval
        self.state = WorkstationState(id=self.workstation_id, ticket_id=self.ticket_id)
        self.output_queue: asyncio.Queue[OutputEvent] = asyncio.Queue()
        self.iteration_queue: asyncio.Queue[IterationRecord] = asyncio.Queue()
        self._process: asyncio.subprocess.Process | None = None
        self._capture_tasks: list[asyncio.Task[None]] = []
        self._wait_task: asyncio.Task[int] | None = None
        self._commit_poll_task: asyncio.Task[None] | None = None
        self._iteration = 0
        self._iteration_started_at: float | None = None
        self._iteration_started_wall: datetime | None = None
        self._iteration_base_sha: str | None = None
        self._iteration_lock = asyncio.Lock()
        self._log_tail: list[str] = []

    async def start(self) -> WorkstationState:
        if self.state.status != WorkstationStatus.IDLE:
            raise RuntimeError(f"cannot start workstation from {self.state.status}")

        worktree_path = self.workspace_root / ".mill" / "worktrees" / self.workstation_id
        worktree_path.parent.mkdir(parents=True, exist_ok=True)
        await self._run_git("worktree", "add", "--detach", str(worktree_path), "HEAD")
        return await self._launch(worktree_path)

    async def resume(self) -> WorkstationState:
        if self.state.status != WorkstationStatus.PAUSED:
            raise RuntimeError(f"cannot resume workstation from {self.state.status}")
        if self.state.worktree_path is None:
            raise RuntimeError("cannot resume workstation without a worktree")
        if self._wait_task is not None:
            await self._wait_task

        self.state.andon.active = False
        self.state.andon.signals = []
        return await self._launch(self.state.worktree_path)

    def acknowledge_andon(self) -> WorkstationState:
        self.state.andon.active = False
        self.state.andon.signals = []
        return self.state

    async def _launch(self, worktree_path: Path) -> WorkstationState:
        if not worktree_path.exists():
            raise RuntimeError("cannot launch workstation without an existing worktree")

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
        self._iteration = IterationStore(self.workspace_root, self.workstation_id).next_iteration()
        self._iteration_started_at = time.monotonic()
        self._iteration_started_wall = datetime.now(timezone.utc)
        self._iteration_base_sha = (await self._git_output(worktree_path, "rev-parse", "HEAD")).strip()
        now = self._utc_now()
        self.state.status = WorkstationStatus.RUNNING
        self.state.worktree_path = worktree_path
        self.state.started_at = self.state.started_at or now
        self.state.iteration_count = self._iteration
        self.state.last_event_at = now
        self.state.process_id = process.pid
        self.state.exit_code = None
        self.state.iteration_summary = None
        self.state.backpressure_signals = []
        self._log_dir().mkdir(parents=True, exist_ok=True)
        self._capture_tasks = [
            asyncio.create_task(self._capture_stream("stdout", process.stdout)),
            asyncio.create_task(self._capture_stream("stderr", process.stderr)),
        ]
        self._wait_task = asyncio.create_task(self._wait_for_exit())
        self._commit_poll_task = asyncio.create_task(self._poll_commits())
        return self.state

    async def wait(self) -> WorkstationState:
        if self._wait_task is None:
            return self.state
        await self._wait_task
        return self.state

    def wait_done(self) -> bool:
        return self._wait_task is None or self._wait_task.done()

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
            if self._wait_task is not None and self._wait_task is not asyncio.current_task():
                await self._wait_task
            return self.state

        self.state.status = status
        process.send_signal(signal.SIGTERM)
        try:
            await asyncio.wait_for(process.wait(), timeout=self.stop_timeout)
        except TimeoutError:
            process.kill()
            await process.wait()

        if self._wait_task is not None and self._wait_task is not asyncio.current_task():
            await self._wait_task
            return self.state

        await asyncio.gather(*self._capture_tasks)
        self.state.exit_code = process.returncode
        self._process = None
        await self._summarize_exit()
        await self._record_iteration_boundary(process.returncode)
        await self._stop_commit_poll()
        return self.state

    async def _wait_for_exit(self) -> int:
        if self._process is None:
            raise RuntimeError("workstation process was not started")
        exit_code = await self._process.wait()
        await asyncio.gather(*self._capture_tasks)
        self.state.exit_code = exit_code
        self._process = None
        if self.state.status == WorkstationStatus.RUNNING:
            self.state.status = WorkstationStatus.COMPLETED
            await self._check_backpressure(exit_code)
        await self._summarize_exit()
        await self._record_iteration_boundary(exit_code)
        await self._stop_commit_poll()
        return exit_code

    async def _capture_stream(
        self,
        stream: str,
        reader: asyncio.StreamReader | None,
    ) -> None:
        if reader is None:
            return
        log_path = self.log_path(stream)
        with log_path.open("a", encoding="utf-8") as log_file:
            while line := await reader.readline():
                line = line[:MAX_LOG_LINE_BYTES]
                text = line.decode(errors="replace").rstrip("\r\n")
                log_file.write(text + "\n")
                log_file.flush()
                timestamp = self._utc_now()
                self._log_tail.append(text)
                self._log_tail = self._log_tail[-200:]
                self.state.last_event_at = timestamp
                await self.output_queue.put(OutputEvent(stream=stream, line=text, timestamp=timestamp))

    def log_path(self, stream: str) -> Path:
        if stream not in {"stdout", "stderr"}:
            raise ValueError("stream must be stdout or stderr")
        return self._log_dir() / f"{stream}.log"

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

    async def _git_output(self, cwd: Path, *args: str) -> str:
        process = await asyncio.create_subprocess_exec(
            "git",
            *args,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            message = stderr.decode(errors="replace").strip()
            raise RuntimeError(f"git {' '.join(args)} failed: {message}")
        return stdout.decode(errors="replace")

    async def _poll_commits(self) -> None:
        try:
            while self.state.status == WorkstationStatus.RUNNING and self.state.worktree_path is not None:
                await asyncio.sleep(self.commit_poll_interval)
                head = (await self._git_output(self.state.worktree_path, "rev-parse", "HEAD")).strip()
                if self._iteration_base_sha is not None and head != self._iteration_base_sha:
                    await self._record_iteration_boundary(None, new_sha=head)
        except asyncio.CancelledError:
            pass

    async def _stop_commit_poll(self) -> None:
        task = self._commit_poll_task
        if task is None or task.done():
            return
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)

    async def _record_iteration_boundary(self, exit_code: int | None, *, new_sha: str | None = None) -> IterationRecord | None:
        async with self._iteration_lock:
            if self.state.worktree_path is None or self._iteration_started_at is None or self._iteration_started_wall is None:
                return None

            previous_sha = self._iteration_base_sha
            head = new_sha or (await self._git_output(self.state.worktree_path, "rev-parse", "HEAD")).strip()
            ended_wall = datetime.now(timezone.utc)
            duration_seconds = time.monotonic() - self._iteration_started_at
            diff = await self._diff(previous_sha, head)
            files_changed, lines_added, lines_removed = await self._diff_numstat(previous_sha, head)
            record = IterationRecord(
                iteration=self._iteration,
                started_at=self._format_time(self._iteration_started_wall),
                ended_at=self._format_time(ended_wall),
                duration_seconds=duration_seconds,
                exit_code=exit_code,
                commit_sha=head,
                files_changed=files_changed,
                lines_added=lines_added,
                lines_removed=lines_removed,
                diff_stat=self._diff_stat(lines_added, lines_removed, len(files_changed)),
                previous_commit_sha=previous_sha,
            )
            IterationStore(self.workspace_root, self.workstation_id).save(record, diff)
            await self.iteration_queue.put(record)

            self._iteration += 1
            self._iteration_started_at = time.monotonic()
            self._iteration_started_wall = ended_wall
            self._iteration_base_sha = head
            self.state.iteration_count = self._iteration
            self.state.last_event_at = self._utc_now()
            return record

    async def _diff(self, previous_sha: str | None, head: str) -> str:
        if previous_sha is None or previous_sha == head:
            return ""
        return await self._git_output(self.state.worktree_path, "diff", f"{previous_sha}..{head}")

    async def _diff_numstat(self, previous_sha: str | None, head: str) -> tuple[list[str], int, int]:
        if previous_sha is None or previous_sha == head:
            return [], 0, 0
        output = await self._git_output(self.state.worktree_path, "diff", "--numstat", f"{previous_sha}..{head}")
        files_changed: list[str] = []
        lines_added = 0
        lines_removed = 0
        for line in output.splitlines():
            added, removed, path = line.split("\t", 2)
            files_changed.append(path)
            if added.isdigit():
                lines_added += int(added)
            if removed.isdigit():
                lines_removed += int(removed)
        return files_changed, lines_added, lines_removed

    def _diff_stat(self, lines_added: int, lines_removed: int, file_count: int) -> str:
        file_word = "file" if file_count == 1 else "files"
        return f"+{lines_added} -{lines_removed} across {file_count} {file_word}"

    async def _check_backpressure(self, exit_code: int) -> None:
        if self.state.worktree_path is None:
            return

        started_at = self._iteration_started_at or time.monotonic()
        duration_seconds = time.monotonic() - started_at
        history = self._load_iteration_history()
        output_tail = "\n".join(self._log_tail)[-4000:]
        loom_changed = bool((await self._git_output(self.state.worktree_path, "status", "--porcelain", "--", ".loom")).strip())
        history.append(
            BackpressureIterationRecord(
                exit_code=exit_code,
                duration_seconds=duration_seconds,
                loom_changed=loom_changed,
                output_tail=output_tail,
            )
        )
        self._save_iteration_history(history)
        signals = detect_backpressure(history)
        self.state.backpressure_signals = signals
        alerts = [signal for signal in signals if signal.severity == "alert"]
        if alerts:
            self.state.andon.active = True
            self.state.andon.signals = alerts
            self.state.status = WorkstationStatus.PAUSED

    async def _summarize_exit(self) -> None:
        if self.state.iteration_summary is not None:
            return
        if self.state.worktree_path is None or self._iteration_started_at is None:
            return
        duration = time.monotonic() - self._iteration_started_at
        self.state.iteration_summary = await summarize_iteration(
            workspace_root=self.workspace_root,
            worktree_path=self.state.worktree_path,
            ticket_slug=self._ticket_slug(),
            iteration=self._iteration,
            exit_code=self.state.exit_code,
            duration_seconds=duration,
        )

    def _pattern_path(self) -> Path:
        return self.workspace_root / ".mill" / "patterns" / f"{self._ticket_slug()}.json"

    def _log_dir(self) -> Path:
        return self.workspace_root / ".mill" / "workstations" / self.workstation_id / "logs"

    def _load_iteration_history(self) -> list[BackpressureIterationRecord]:
        path = self._pattern_path()
        if not path.exists():
            return []
        data = json.loads(path.read_text(encoding="utf-8"))
        return [BackpressureIterationRecord(**item) for item in data]

    def _save_iteration_history(self, history: list[BackpressureIterationRecord]) -> None:
        path = self._pattern_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps([asdict(record) for record in history], indent=2) + "\n", encoding="utf-8")

    def _process_cwd(self, worktree_path: Path) -> Path:
        if self.harness.cwd is None:
            return worktree_path
        cwd = Path(self.harness.cwd)
        return cwd if cwd.is_absolute() else worktree_path / cwd

    def _ticket_slug(self) -> str:
        stem = self.ticket_path.stem.lower()
        slug = re.sub(r"[^a-z0-9._-]+", "-", stem).strip("-._")
        return slug or "workstation"

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _format_time(self, value: datetime) -> str:
        return value.isoformat().replace("+00:00", "Z")
