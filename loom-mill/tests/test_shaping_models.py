from __future__ import annotations

from loom_mill.shaping.models import CanvasNodeType


def test_new_intent_node_types_exist() -> None:
    assert CanvasNodeType.FRAMING == "framing"
    assert CanvasNodeType.TENSION == "tension"
    assert CanvasNodeType.DECISION == "decision"


def test_existing_node_types_unchanged() -> None:
    assert CanvasNodeType.OBSERVATION == "observation"
    assert CanvasNodeType.RECORD == "record"
    assert CanvasNodeType.OPTION_GROUP == "option_group"
