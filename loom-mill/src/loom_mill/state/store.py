from __future__ import annotations

import asyncio

from loom_mill.parser import LoomRecord

from loom_mill.workstation import WorkstationState

from .models import GitState, MillEvent, MillState


class MillEventSubscription:
    def __init__(self, store: "MillStateStore", queue: asyncio.Queue[MillEvent]) -> None:
        self._store = store
        self._queue = queue

    def __aiter__(self) -> "MillEventSubscription":
        return self

    async def __anext__(self) -> MillEvent:
        return await self._queue.get()

    async def aclose(self) -> None:
        self._store._subscribers.discard(self._queue)


class MillStateStore:
    def __init__(self) -> None:
        self._records: dict[str, LoomRecord] = {}
        self._git = GitState()
        self._workstations: dict[str, WorkstationState] = {}
        self._subscribers: set[asyncio.Queue[MillEvent]] = set()
        self._lock = asyncio.Lock()

    async def snapshot(self) -> MillState:
        async with self._lock:
            return MillState(
                records=tuple(self._records[path] for path in sorted(self._records)),
                git=self._git,
                workstations=dict(self._workstations),
            )

    async def record(self, path: str) -> LoomRecord | None:
        async with self._lock:
            return self._records.get(path)

    async def upsert_record(self, record: LoomRecord) -> LoomRecord | None:
        async with self._lock:
            return self._records.setdefault(record.path, record)

    async def replace_record(self, record: LoomRecord) -> LoomRecord | None:
        async with self._lock:
            previous = self._records.get(record.path)
            self._records[record.path] = record
            return previous

    async def remove_record(self, path: str) -> LoomRecord | None:
        async with self._lock:
            return self._records.pop(path, None)

    async def replace_all_records(self, records: tuple[LoomRecord, ...]) -> None:
        async with self._lock:
            self._records = {record.path: record for record in records}

    async def git_state(self) -> GitState:
        async with self._lock:
            return self._git

    async def replace_git_state(self, git: GitState) -> GitState:
        async with self._lock:
            previous = self._git
            self._git = git
            return previous

    async def replace_workstation_state(self, ticket_id: str, workstation: WorkstationState) -> WorkstationState | None:
        async with self._lock:
            previous = self._workstations.get(ticket_id)
            self._workstations[ticket_id] = workstation
            return previous

    async def publish(self, event: MillEvent) -> None:
        for queue in tuple(self._subscribers):
            await queue.put(event)

    def subscribe(self) -> MillEventSubscription:
        queue: asyncio.Queue[MillEvent] = asyncio.Queue()
        self._subscribers.add(queue)
        return MillEventSubscription(self, queue)
