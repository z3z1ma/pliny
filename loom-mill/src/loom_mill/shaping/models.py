from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class SessionPhase(StrEnum):
    EXPLORING = "exploring"
    NARROWING = "narrowing"
    PROPOSING = "proposing"
    REFINING = "refining"
    READY = "ready"


class BlockType(StrEnum):
    OPERATOR_INPUT = "operator_input"
    AGENT_QUESTION = "agent_question"
    AGENT_OBSERVATION = "agent_observation"
    AGENT_PROPOSAL = "agent_proposal"
    EXPLORATION_START = "exploration_start"
    EXPLORATION_COMPLETE = "exploration_complete"
    BRANCH_POINT = "branch_point"
    SYSTEM = "system"


@dataclass
class InteractionBlock:
    id: str
    type: BlockType
    timestamp: str
    content: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict) -> "InteractionBlock":
        return cls(
            id=str(data.get("id") or ""),
            type=BlockType(str(data.get("type") or BlockType.SYSTEM)),
            timestamp=str(data.get("timestamp") or ""),
            content=dict(data.get("content") or {}),
        )


@dataclass
class StagedRecord:
    temp_id: str
    surface: str
    title: str
    content: str
    branch: str
    status: str
    proposed_at: str
    modified_at: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "StagedRecord":
        return cls(
            temp_id=str(data.get("temp_id") or ""),
            surface=str(data.get("surface") or ""),
            title=str(data.get("title") or ""),
            content=str(data.get("content") or ""),
            branch=str(data.get("branch") or "main"),
            status=str(data.get("status") or "proposed"),
            proposed_at=str(data.get("proposed_at") or ""),
            modified_at=data.get("modified_at"),
        )


@dataclass
class SessionState:
    id: str
    phase: SessionPhase
    created_at: str
    updated_at: str
    blocks: list[InteractionBlock] = field(default_factory=list)
    staged_records: list[StagedRecord] = field(default_factory=list)
    active_branch: str = "main"
    branches: list[str] = field(default_factory=lambda: ["main"])
    active_explorations: list[str] = field(default_factory=list)
    ended_at: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "SessionState":
        return cls(
            id=str(data.get("id") or ""),
            phase=SessionPhase(str(data.get("phase") or SessionPhase.EXPLORING)),
            created_at=str(data.get("created_at") or ""),
            updated_at=str(data.get("updated_at") or ""),
            blocks=[InteractionBlock.from_dict(item) for item in data.get("blocks", [])],
            staged_records=[StagedRecord.from_dict(item) for item in data.get("staged_records", [])],
            active_branch=str(data.get("active_branch") or "main"),
            branches=list(data.get("branches") or ["main"]),
            active_explorations=list(data.get("active_explorations") or []),
            ended_at=data.get("ended_at"),
        )
