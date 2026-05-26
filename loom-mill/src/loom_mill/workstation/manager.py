from __future__ import annotations

import asyncio
import re
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

from loom_mill.state.models import WorkstationIterationCompleted, WorkstationOutput, WorkstationStateChanged, WorkstationTakt

from .config import FactoryConfig, HarnessConfig
from .engine import WorkstationEngine
from .models import WorkstationState, WorkstationStatus

if TYPE_CHECKING:
    from loom_mill.state.store import MillStateStore


class WorkstationManager:
    def __init__(self, workspace_root: Path, store: MillStateStore, config: FactoryConfig) -> None:
        self.workspace_root = workspace_root.resolve()
        self.store = store
        self.config = config
        self.workstations: dict[str, WorkstationEngine] = {}
        self._tasks: dict[str, set[asyncio.Task[None]]] = {}
        self._lock = asyncio.Lock()

    def update_config(self, config: FactoryConfig) -> None:
        self.config = config

    def list(self) -> list[WorkstationState]:
        return [engine.state for engine in self.workstations.values()]

    def get(self, workstation_id: str) -> WorkstationEngine | None:
        return self.workstations.get(workstation_id)

    def get_by_ticket(self, ticket_id: str) -> WorkstationEngine | None:
        ticket_id = ticket_id.removeprefix("ticket:")
        for engine in self.workstations.values():
            if engine.ticket_id == ticket_id:
                return engine
        return None

    async def start(self, ticket_path: Path, ticket_id: str, harness: HarnessConfig | None = None) -> WorkstationEngine:
        async with self._lock:
            if self._active_count() >= self.config.max_workstations:
                raise RuntimeError(f"WIP limit reached: max_workstations={self.config.max_workstations}")
            workstation_id = f"ws-{uuid.uuid4().hex[:12]}"
            engine = WorkstationEngine(
                self.workspace_root,
                ticket_path,
                harness or self.config.harness,
                workstation_id=workstation_id,
                ticket_id=ticket_id.removeprefix("ticket:"),
            )
            self.workstations[workstation_id] = engine
            await engine.start()
            await self._publish_state(engine)
            self._tasks[workstation_id] = {
                asyncio.create_task(self._monitor_exit(engine)),
                asyncio.create_task(self._pump_iterations(engine)),
                asyncio.create_task(self._pump_output(engine)),
            }
            return engine

    async def pause(self, workstation_id: str) -> WorkstationState:
        engine = self._require(workstation_id)
        state = await engine.pause()
        await self._publish_state(engine)
        return state

    async def resume(self, workstation_id: str) -> WorkstationState:
        engine = self._require(workstation_id)
        state = await engine.resume()
        await self._publish_state(engine)
        tasks = self._tasks.setdefault(workstation_id, set())
        tasks.add(asyncio.create_task(self._monitor_exit(engine)))
        tasks.add(asyncio.create_task(self._pump_iterations(engine)))
        tasks.add(asyncio.create_task(self._pump_output(engine)))
        return state

    async def stop(self, workstation_id: str, *, remove: bool = True) -> WorkstationState:
        engine = self._require(workstation_id)
        state = await engine.stop()
        await self._publish_state(engine)
        if remove:
            await engine.teardown()
            self.workstations.pop(workstation_id, None)
            for task in self._tasks.pop(workstation_id, set()):
                task.cancel()
            await self.store.remove_workstation_state(workstation_id)
        return state

    async def shutdown(self) -> None:
        for workstation_id in list(self.workstations):
            engine = self.workstations[workstation_id]
            if engine.state.status == WorkstationStatus.RUNNING:
                await engine.stop()
            else:
                await engine.wait()
        for tasks in self._tasks.values():
            for task in tasks:
                task.cancel()
        await asyncio.gather(*(task for tasks in self._tasks.values() for task in tasks), return_exceptions=True)

    def _active_count(self) -> int:
        return sum(
            1
            for engine in self.workstations.values()
            if engine.state.status in {WorkstationStatus.RUNNING, WorkstationStatus.PAUSED}
        )

    def _require(self, workstation_id: str) -> WorkstationEngine:
        engine = self.workstations.get(workstation_id)
        if engine is None:
            raise KeyError(workstation_id)
        return engine

    async def _publish_state(self, engine: WorkstationEngine) -> None:
        await self.store.replace_workstation_state(engine.workstation_id, engine.state)
        await self.store.publish(WorkstationStateChanged(workstation_id=engine.workstation_id, workstation=engine.state))

    async def _pump_output(self, engine: WorkstationEngine) -> None:
        while True:
            try:
                output = await asyncio.wait_for(engine.output_queue.get(), timeout=0.1)
            except TimeoutError:
                if engine.state.status != WorkstationStatus.RUNNING and engine.output_queue.empty() and self._engine_wait_done(engine):
                    break
                continue
            await self.store.publish(WorkstationOutput(workstation_id=engine.workstation_id, output=output))

    async def _pump_iterations(self, engine: WorkstationEngine) -> None:
        while True:
            try:
                iteration = await asyncio.wait_for(engine.iteration_queue.get(), timeout=0.1)
            except TimeoutError:
                if engine.state.status != WorkstationStatus.RUNNING and engine.iteration_queue.empty() and self._engine_wait_done(engine):
                    break
                continue
            await self.store.publish(WorkstationIterationCompleted(workstation_id=engine.workstation_id, iteration=iteration))
            await self.store.publish(
                WorkstationTakt(
                    workstation_id=engine.workstation_id,
                    iteration=iteration.iteration,
                    duration_seconds=iteration.duration_seconds,
                )
            )

    def _engine_wait_done(self, engine: WorkstationEngine) -> bool:
        return engine.wait_done()

    async def _monitor_exit(self, engine: WorkstationEngine) -> None:
        await engine.wait()
        await self._publish_state(engine)
        if engine.state.status == WorkstationStatus.COMPLETED:
            from loom_mill.scheduling import SchedulingAgent

            if self._ticket_ready_to_ship(engine.ticket_path):
                from loom_mill.shipping import ShippingDock

                await ShippingDock(self.workspace_root, self).handle_finished(engine.workstation_id)
            await SchedulingAgent(self.workspace_root, self).on_workstation_finished(engine.workstation_id)

    def _ticket_ready_to_ship(self, ticket_path: Path) -> bool:
        if not ticket_path.exists():
            return False
        match = re.search(r"^Status:\s*(\S+)\s*$", ticket_path.read_text(encoding="utf-8"), re.MULTILINE)
        return bool(match and match.group(1) in self.config.ready_to_ship_statuses)
