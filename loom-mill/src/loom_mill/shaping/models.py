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


class CanvasNodeType(StrEnum):
    INPUT = "input"
    PROCESSING = "processing"
    QUESTION = "question"
    OBSERVATION = "observation"
    FRAMING = "framing"
    TENSION = "tension"
    DECISION = "decision"
    OPTION_GROUP = "option_group"
    OPTION = "option"
    RECORD = "record"


class NodeStatus(StrEnum):
    ACTIVE = "active"
    DEAD = "dead"
    STALE = "stale"
    REJECTED = "rejected"


@dataclass
class CanvasNode:
    id: str
    type: CanvasNodeType
    parent_id: str | None
    status: NodeStatus
    content: dict[str, Any]
    position: dict[str, float] | None
    timestamp: str
    option_group_id: str | None = None
    selected: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "CanvasNode":
        position = data.get("position")
        if position is not None:
            position = {str(key): float(value) for key, value in dict(position).items()}
        return cls(
            id=str(data.get("id") or ""),
            type=CanvasNodeType(str(data.get("type") or CanvasNodeType.OBSERVATION)),
            parent_id=data.get("parent_id"),
            status=NodeStatus(str(data.get("status") or NodeStatus.ACTIVE)),
            content=dict(data.get("content") or {}),
            position=position,
            timestamp=str(data.get("timestamp") or ""),
            option_group_id=data.get("option_group_id"),
            selected=bool(data.get("selected", False)),
        )


@dataclass
class CanvasEdge:
    id: str
    source_id: str
    target_id: str
    type: str

    @classmethod
    def from_dict(cls, data: dict) -> "CanvasEdge":
        return cls(
            id=str(data.get("id") or ""),
            source_id=str(data.get("source_id") or ""),
            target_id=str(data.get("target_id") or ""),
            type=str(data.get("type") or "causal"),
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
    nodes: dict[str, CanvasNode] = field(default_factory=dict)
    edges: list[CanvasEdge] = field(default_factory=list)
    staged_records: list[StagedRecord] = field(default_factory=list)
    active_branch: str = "main"
    branches: list[str] = field(default_factory=lambda: ["main"])
    active_explorations: dict[str, str] = field(default_factory=dict)
    ended_at: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "SessionState":
        active_explorations = data.get("active_explorations") or {}
        if isinstance(active_explorations, list):
            active_explorations = {str(item): str(item) for item in active_explorations}
        return cls(
            id=str(data.get("id") or ""),
            phase=SessionPhase(str(data.get("phase") or SessionPhase.EXPLORING)),
            created_at=str(data.get("created_at") or ""),
            updated_at=str(data.get("updated_at") or ""),
            nodes={str(node_id): CanvasNode.from_dict(item) for node_id, item in dict(data.get("nodes") or {}).items()},
            edges=[CanvasEdge.from_dict(item) for item in data.get("edges", [])],
            staged_records=[StagedRecord.from_dict(item) for item in data.get("staged_records", [])],
            active_branch=str(data.get("active_branch") or "main"),
            branches=list(data.get("branches") or ["main"]),
            active_explorations={str(key): str(value) for key, value in dict(active_explorations).items()},
            ended_at=data.get("ended_at"),
        )
