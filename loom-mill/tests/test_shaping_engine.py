from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from types import SimpleNamespace

import pytest

from loom_mill.api import shaping
from loom_mill.api.ws import _event_payload
from loom_mill.app import create_app
from loom_mill.shaping import BlockType, InteractionBlock, SessionPhase, ShapingSession
from loom_mill.shaping.engine import ShapingEngine
from loom_mill.shaping.orchestrator import ShapingOrchestrator
from loom_mill.shaping.parser import parse_decision
from loom_mill.shaping.prompts import build_decision_prompt
from loom_mill.shaping.session import utc_now
from loom_mill.state import MillStateStore
from loom_mill.workstation.config import HarnessConfig


class Request:
    def __init__(
        self,
        workspace_root: Path,
        store: MillStateStore,
        body: dict | None = None,
        path_params: dict | None = None,
        harness_config: HarnessConfig | None = None,
    ):
        self.app = SimpleNamespace(
            state=SimpleNamespace(
                workspace_root=str(workspace_root),
                store=store,
                harness_config=harness_config or _printf_harness("```action\ntype: observation\nobservation: default\n```"),
            )
        )
        self._body = body or {}
        self.path_params = path_params or {}

    async def json(self):
        return self._body


def _body(response) -> dict:
    return json.loads(response.body)


def _printf_harness(output: str) -> HarnessConfig:
    return HarnessConfig(command="printf", args=[output])


def test_parse_decision_question_block() -> None:
    decision = parse_decision(
        "```action\n"
        "type: question\n"
        "question: Which boundary should this reinforce?\n"
        "options: tickets, specs, plans\n"
        "context_ref: current plan\n"
        "```"
    )

    assert decision.action == "question"
    assert decision.question == "Which boundary should this reinforce?"
    assert decision.options == ["tickets", "specs", "plans"]
    assert decision.context_ref == "current plan"


def test_parse_decision_proposal_block_with_multiline_content() -> None:
    decision = parse_decision(
        "```action\n"
        "type: propose\n"
        "surface: tickets\n"
        "title: Implement cache invalidation\n"
        "content: # Implement cache invalidation\n"
        "\n"
        "ID: ticket:20260526-cache-invalidation\n"
        "Type: Ticket\n"
        "Status: open\n"
        "```"
    )

    assert decision.action == "propose"
    assert decision.record_surface == "tickets"
    assert decision.record_title == "Implement cache invalidation"
    assert "ID: ticket:20260526-cache-invalidation" in (decision.record_content or "")


def test_parse_decision_branch_and_explore_blocks() -> None:
    branch = parse_decision("```action\ntype: branch\nbranches: local fix | durable spec\nreasoning: different closure stories\n```")
    explore = parse_decision("```action\ntype: explore\ngoal: inspect records\ncontext_excerpt: auth area\n```")

    assert branch.branches == [{"id": "branch-1", "label": "local fix"}, {"id": "branch-2", "label": "durable spec"}]
    assert branch.reasoning == "different closure stories"
    assert explore.action == "explore"
    assert explore.goal == "inspect records"
    assert explore.context_excerpt == "auth area"


def test_parse_decision_falls_back_to_observation() -> None:
    decision = parse_decision("unstructured model output")

    assert decision.action == "observation"
    assert decision.observation == "unstructured model output"


def test_decision_prompt_includes_context_history_and_phase() -> None:
    block = InteractionBlock(id="b1", type=BlockType.OPERATOR_INPUT, timestamp=utc_now(), content={"text": "shape graph mode"})

    prompt = build_decision_prompt("context facts", [block], SessionPhase.EXPLORING)

    assert "## Current Phase: exploring" in prompt
    assert "context facts" in prompt
    assert "operator_input: shape graph mode" in prompt
    assert "Output EXACTLY ONE structured ```action block" in prompt


@pytest.mark.asyncio
async def test_engine_advance_with_question_publishes_block_and_moves_to_narrowing(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape a graph view")
    store = MillStateStore()
    output = "```action\ntype: question\nquestion: Is this for navigation or analysis?\noptions: navigation, analysis\ncontext_ref: operator input\n```"
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)
    subscription = store.subscribe()
    try:
        blocks = await engine.advance()
        events = [await subscription.__anext__(), await subscription.__anext__()]
    finally:
        await subscription.aclose()

    assert len(blocks) == 1
    assert blocks[0].type == BlockType.AGENT_QUESTION
    assert blocks[0].content["question"] == "Is this for navigation or analysis?"
    assert session.state.phase == SessionPhase.NARROWING
    assert [_event_payload(event)["type"] for event in events] == ["shaping:block_added", "shaping:phase_changed"]


@pytest.mark.asyncio
async def test_engine_advance_with_proposal_publishes_block_and_moves_to_proposing(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape notification bug")
    session.update_phase(SessionPhase.NARROWING)
    store = MillStateStore()
    output = (
        "```action\n"
        "type: propose\n"
        "surface: tickets\n"
        "title: Fix notification label\n"
        "content: # Fix notification label\n\nID: ticket:20260526-fix-notification-label\nType: Ticket\nStatus: open\n"
        "```"
    )
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)

    blocks = await engine.advance()

    assert blocks[0].type == BlockType.AGENT_PROPOSAL
    assert blocks[0].content["surface"] == "tickets"
    assert blocks[0].content["title"] == "Fix notification label"
    assert "Type: Ticket" in blocks[0].content["content"]
    assert blocks[0].content["temp_id"] == "temp:tickets:fix-notification-label"
    assert session.state.staged_records[0].temp_id == blocks[0].content["temp_id"]
    assert session.state.phase == SessionPhase.PROPOSING


@pytest.mark.asyncio
async def test_engine_transitions_to_refining_after_operator_feedback_on_proposal(tmp_path: Path) -> None:
    session = ShapingSession.create(tmp_path, "shape notification bug")
    session.update_phase(SessionPhase.PROPOSING)
    session.add_block(
        InteractionBlock(
            id="proposal-1",
            type=BlockType.AGENT_PROPOSAL,
            timestamp=utc_now(),
            content={"surface": "tickets", "title": "Fix notification label", "content": "# Fix"},
        )
    )
    session.add_block(InteractionBlock(id="input-2", type=BlockType.OPERATOR_INPUT, timestamp=utc_now(), content={"text": "split this"}))
    store = MillStateStore()
    output = "```action\ntype: observation\nobservation: I will refine the proposal around the split.\n```"
    engine = ShapingEngine(session, ShapingOrchestrator(session, store, _printf_harness(output)), store)

    blocks = await engine.advance()

    assert session.state.phase == SessionPhase.REFINING
    assert blocks[0].type == BlockType.AGENT_OBSERVATION


@pytest.mark.asyncio
async def test_advance_endpoint_returns_blocks(tmp_path: Path) -> None:
    store = MillStateStore()
    harness = _printf_harness("```action\ntype: observation\nobservation: Existing context is enough to proceed.\nevidence: .loom/specs/example.md\n```")
    create_response = await shaping.create_shaping_session(Request(tmp_path, store, {"input": "initial"}, harness_config=harness))
    session_id = _body(create_response)["session_id"]

    response = await shaping.advance_shaping_session(Request(tmp_path, store, path_params={"session_id": session_id}, harness_config=harness))

    payload = _body(response)
    assert response.status_code == 200
    assert payload["session_id"] == session_id
    assert payload["blocks"][0]["type"] == "agent_observation"
    assert payload["blocks"][0]["content"]["evidence"] == [".loom/specs/example.md"]


def test_advance_route_is_registered() -> None:
    routes = [(route.path, route.methods or set()) for route in create_app().routes if hasattr(route, "methods")]

    assert any(route_path == "/shaping/sessions/{session_id}/advance" and "POST" in methods for route_path, methods in routes)
