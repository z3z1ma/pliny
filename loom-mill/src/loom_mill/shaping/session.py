from __future__ import annotations

import asyncio
import json
import os
import tempfile
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .models import BlockType, InteractionBlock, SessionPhase, SessionState


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_name = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp_file:
            tmp_name = tmp_file.name
            tmp_file.write(content)
        os.replace(tmp_name, path)
    finally:
        if tmp_name and os.path.exists(tmp_name):
            os.unlink(tmp_name)


class ShapingSession:
    def __init__(self, session_id: str, workspace_root: str | Path):
        self.session_id = session_id
        self.workspace_root = Path(workspace_root)
        self._base_dir = self.workspace_root / ".mill" / "shaping-sessions" / session_id
        self._state_path = self._base_dir / "state.json"
        self._context_path = self._base_dir / "context.md"
        self._context_lock = asyncio.Lock()
        self.state: SessionState

    @classmethod
    def create(cls, workspace_root: str | Path, initial_input: str) -> "ShapingSession":
        session_id = str(uuid4())
        session = cls(session_id, workspace_root)
        session._base_dir.mkdir(parents=True, exist_ok=True)
        now = utc_now()
        block = InteractionBlock(
            id=str(uuid4()),
            type=BlockType.OPERATOR_INPUT,
            timestamp=now,
            content={"text": initial_input},
        )
        session.state = SessionState(
            id=session_id,
            phase=SessionPhase.EXPLORING,
            created_at=now,
            updated_at=now,
            blocks=[block],
        )
        session._write_context(f"# Shaping Session\n\n## Operator Input\n\n{initial_input}\n")
        session._persist_state()
        return session

    @classmethod
    def load(cls, session_id: str, workspace_root: str | Path) -> "ShapingSession":
        session = cls(session_id, workspace_root)
        if not session._state_path.exists():
            raise KeyError(session_id)
        session.state = SessionState.from_dict(json.loads(session._state_path.read_text(encoding="utf-8")))
        return session

    async def append_context(self, section_heading: str, content: str) -> int:
        async with self._context_lock:
            current = self.read_context()
            section = f"\n\n## {section_heading}\n\n{content}\n"
            updated = current.rstrip() + section
            self._write_context(updated)
            return len(updated.encode("utf-8"))

    def read_context(self) -> str:
        return self._context_path.read_text(encoding="utf-8")

    def add_block(self, block: InteractionBlock) -> None:
        self.state.blocks.append(block)
        self.state.updated_at = utc_now()
        self._persist_state()

    def update_phase(self, phase: SessionPhase) -> None:
        self.state.phase = phase
        self.state.updated_at = utc_now()
        self._persist_state()

    def end(self) -> None:
        now = utc_now()
        self.state.ended_at = now
        self.state.updated_at = now
        self._persist_state()

    @property
    def staging(self):
        from .staging import StagingArea

        return StagingArea(self)

    def _persist_state(self) -> None:
        _atomic_write(self._state_path, json.dumps(asdict(self.state), indent=2) + "\n")

    def _write_context(self, content: str) -> None:
        _atomic_write(self._context_path, content)


def list_sessions(workspace_root: str | Path) -> list[SessionState]:
    base_dir = Path(workspace_root) / ".mill" / "shaping-sessions"
    if not base_dir.exists():
        return []
    sessions: list[SessionState] = []
    for path in sorted(base_dir.glob("*/state.json")):
        try:
            state = SessionState.from_dict(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError, ValueError):
            continue
        if state.ended_at is None:
            sessions.append(state)
    return sessions
