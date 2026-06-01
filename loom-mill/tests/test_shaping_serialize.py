from __future__ import annotations

from loom_mill.shaping.models import (
    CanvasEdge,
    CanvasNode,
    CanvasNodeType,
    NodeStatus,
    SessionPhase,
    SessionState,
    StagedRecord,
)
from loom_mill.shaping.serialize import serialize_graph


def _node(node_id, node_type, parent_id, text, status=NodeStatus.ACTIVE):
    return CanvasNode(
        id=node_id,
        type=node_type,
        parent_id=parent_id,
        status=status,
        content={"text": text} if node_type == CanvasNodeType.INPUT else {"observation": text},
        position=None,
        timestamp="2026-05-31T00:00:00+00:00",
    )


def _state() -> SessionState:
    root = _node("n1", CanvasNodeType.INPUT, None, "build a graph feature")
    obs = _node("n2", CanvasNodeType.OBSERVATION, "n1", "uses d3-force")
    dead = _node("n3", CanvasNodeType.OBSERVATION, "n1", "rejected path", status=NodeStatus.DEAD)
    state = SessionState(
        id="s1",
        phase=SessionPhase.EXPLORING,
        created_at="t",
        updated_at="t",
        nodes={"n1": root, "n2": obs, "n3": dead},
        edges=[CanvasEdge(id="e1", source_id="n1", target_id="n2", type="causal")],
        staged_records=[
            StagedRecord(
                temp_id="temp:specs:graph-view",
                surface="specs",
                title="Graph View",
                content="# Graph View\n\nLong body...",
                branch="main",
                status="proposed",
                proposed_at="t",
            )
        ],
    )
    return state


def test_serialize_includes_all_active_nodes_with_ids_types_status() -> None:
    text = serialize_graph(_state())
    assert "n1" in text and "input" in text
    assert "n2" in text and "observation" in text
    assert "uses d3-force" in text


def test_serialize_marks_dead_nodes() -> None:
    text = serialize_graph(_state())
    assert "n3" in text
    assert "dead" in text


def test_serialize_includes_staging_area_with_temp_ids() -> None:
    text = serialize_graph(_state())
    assert "Staging Area" in text
    assert "temp:specs:graph-view" in text
    assert "specs" in text
    assert "Graph View" in text


def test_serialize_includes_parent_edges() -> None:
    text = serialize_graph(_state())
    assert "parent=n1" in text
