from __future__ import annotations

from loom_mill.shaping.prompts import build_canvas_prompt


def test_prompt_documents_new_node_types() -> None:
    prompt = build_canvas_prompt("ctx", "graph-text", [], "exploring")
    assert "framing" in prompt.lower()
    assert "tension" in prompt.lower()
    assert "decision" in prompt.lower()


def test_prompt_documents_ops() -> None:
    prompt = build_canvas_prompt("ctx", "graph-text", [], "exploring")
    assert "supersede" in prompt.lower()
    assert "continue" in prompt.lower()


def test_prompt_includes_graph_view() -> None:
    prompt = build_canvas_prompt("ctx", "GRAPH-SENTINEL", [], "exploring")
    assert "GRAPH-SENTINEL" in prompt


def test_exploring_phase_disposition_favors_branching() -> None:
    prompt = build_canvas_prompt("ctx", "g", [], "exploring")
    assert "branch" in prompt.lower()
    assert "as quickly as certainty allows" not in prompt
