from __future__ import annotations

import json
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class ChatContext:
    path: str
    selected_text: str
    line_range: tuple[int, int] | None = None

    @classmethod
    def from_dict(cls, data: dict | None) -> "ChatContext | None":
        if data is None:
            return None
        line_range = data.get("line_range")
        return cls(
            path=str(data.get("path") or ""),
            selected_text=str(data.get("selected_text") or ""),
            line_range=tuple(line_range) if line_range is not None else None,
        )


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str
    timestamp: str
    context: ChatContext | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "ChatMessage":
        return cls(
            role=str(data.get("role") or ""),
            content=str(data.get("content") or ""),
            timestamp=str(data.get("timestamp") or ""),
            context=ChatContext.from_dict(data.get("context")),
        )


@dataclass(frozen=True)
class ChatSession:
    id: str
    harness_command: str
    document_path: str | None
    messages: list[ChatMessage] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    ended_at: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "ChatSession":
        return cls(
            id=str(data.get("id") or ""),
            harness_command=str(data.get("harness_command") or ""),
            document_path=data.get("document_path"),
            messages=[ChatMessage.from_dict(item) for item in data.get("messages", [])],
            created_at=str(data.get("created_at") or ""),
            ended_at=data.get("ended_at"),
        )


class SessionStore:
    def __init__(self, base_dir: str | Path = ".mill/chat-sessions") -> None:
        self.base_dir = Path(base_dir)
        os.makedirs(self.base_dir, exist_ok=True)

    def create(self, harness_command: str, document_path: str | None = None) -> ChatSession:
        session = ChatSession(
            id=str(uuid.uuid4())[:8],
            harness_command=harness_command,
            document_path=document_path,
        )
        self._save(session)
        return session

    def get(self, session_id: str) -> ChatSession | None:
        path = self._path(session_id)
        if not path.exists():
            return None
        return ChatSession.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def add_message(self, session_id: str, message: ChatMessage) -> None:
        session = self.get(session_id)
        if session is None:
            raise KeyError(session_id)
        self._save(
            ChatSession(
                id=session.id,
                harness_command=session.harness_command,
                document_path=session.document_path,
                messages=[*session.messages, message],
                created_at=session.created_at,
                ended_at=session.ended_at,
            )
        )

    def end(self, session_id: str) -> ChatSession:
        session = self.get(session_id)
        if session is None:
            raise KeyError(session_id)
        ended = ChatSession(
            id=session.id,
            harness_command=session.harness_command,
            document_path=session.document_path,
            messages=session.messages,
            created_at=session.created_at,
            ended_at=datetime.now().isoformat(),
        )
        self._save(ended)
        return ended

    def _save(self, session: ChatSession) -> None:
        self._path(session.id).write_text(json.dumps(asdict(session), indent=2) + "\n", encoding="utf-8")

    def _path(self, session_id: str) -> Path:
        return self.base_dir / f"{session_id}.json"
