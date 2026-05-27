from __future__ import annotations

from dataclasses import asdict
from uuid import uuid4

from loom_mill.state.store import MillStateStore

from .events import ShapingEvent
from .harness import InvocationConfig, run_bounded_invocation
from .models import BlockType, InteractionBlock, SessionPhase
from .orchestrator import ShapingOrchestrator
from .parser import Decision, parse_decision
from .prompts import build_decision_prompt
from .session import ShapingSession, utc_now


class ShapingEngine:
    def __init__(self, session: ShapingSession, orchestrator: ShapingOrchestrator, store: MillStateStore) -> None:
        self.session = session
        self.orchestrator = orchestrator
        self.store = store

    async def advance(self) -> list[InteractionBlock]:
        await self._transition_for_operator_feedback()
        context = self.session.read_context()
        recent_blocks = self.session.state.blocks[-20:]
        decision = await self._decide_next_action(context, recent_blocks, self.session.state.phase)

        if decision.action == "explore":
            await self.orchestrator.launch(decision.goal or "Explore context needed for shaping", decision.context_excerpt)
            return []

        block = self._block_from_decision(decision)
        if block.type == BlockType.AGENT_PROPOSAL:
            staged = self.session.staging.propose(
                str(block.content.get("surface") or "tickets"),
                str(block.content.get("title") or "Untitled proposal"),
                str(block.content.get("content") or ""),
                self.session.state.active_branch,
            )
            block.content["temp_id"] = staged.temp_id
        self.session.add_block(block)
        await self._publish_block(block)
        await self._transition_after_block(block)
        return [block]

    async def _decide_next_action(
        self,
        context: str,
        recent_blocks: list[InteractionBlock],
        phase: SessionPhase,
    ) -> Decision:
        prompt = build_decision_prompt(context, recent_blocks, phase)
        config = InvocationConfig(
            goal="Decide next shaping action",
            context_excerpt="",
            command=self.orchestrator.harness_config.command,
            args=list(self.orchestrator.harness_config.args),
            env=dict(self.orchestrator.harness_config.env or {}),
            cwd=self.orchestrator.harness_config.cwd,
            timeout_seconds=60.0,
        )
        try:
            result = await run_bounded_invocation(
                config,
                invocation_id=f"decision-{uuid4().hex[:8]}",
                on_stream=None,
                prompt_override=prompt,
            )
        except Exception as error:
            return Decision(action="observation", observation=f"Decision harness failed: {error}")

        output = result.output.strip()
        if result.exit_code != 0 and not output:
            message = result.stderr.strip() or f"decision harness exited with code {result.exit_code}"
            return Decision(action="observation", observation=f"Decision harness failed: {message}")
        return parse_decision(output or result.stderr.strip())

    def _block_from_decision(self, decision: Decision) -> InteractionBlock:
        block_type = {
            "question": BlockType.AGENT_QUESTION,
            "observation": BlockType.AGENT_OBSERVATION,
            "propose": BlockType.AGENT_PROPOSAL,
            "branch": BlockType.BRANCH_POINT,
        }.get(decision.action, BlockType.AGENT_OBSERVATION)
        return InteractionBlock(id=str(uuid4()), type=block_type, timestamp=utc_now(), content=self._content_from_decision(decision))

    def _content_from_decision(self, decision: Decision) -> dict:
        if decision.action == "question":
            return {
                "question": decision.question or "What should we clarify next?",
                "options": decision.options,
                "context_ref": decision.context_ref,
            }
        if decision.action == "propose":
            return {
                "temp_id": f"proposal-{uuid4().hex[:8]}",
                "surface": decision.record_surface or "tickets",
                "title": decision.record_title or "Untitled proposal",
                "content": decision.record_content or "",
            }
        if decision.action == "branch":
            return {"branches": decision.branches or [], "reasoning": decision.reasoning}
        return {"observation": decision.observation or "No structured decision was produced.", "evidence": decision.evidence}

    async def _transition_for_operator_feedback(self) -> None:
        if self.session.state.phase != SessionPhase.PROPOSING:
            return
        last_proposal = _last_index(self.session.state.blocks, BlockType.AGENT_PROPOSAL)
        last_input = _last_index(self.session.state.blocks, BlockType.OPERATOR_INPUT)
        if last_proposal is not None and last_input is not None and last_input > last_proposal:
            await self._update_phase(SessionPhase.REFINING)

    async def _transition_after_block(self, block: InteractionBlock) -> None:
        if self.session.state.phase == SessionPhase.EXPLORING and block.type == BlockType.AGENT_QUESTION:
            await self._update_phase(SessionPhase.NARROWING)
        elif block.type == BlockType.AGENT_PROPOSAL and self.session.state.phase != SessionPhase.REFINING:
            await self._update_phase(SessionPhase.PROPOSING)

    async def _update_phase(self, phase: SessionPhase) -> None:
        if self.session.state.phase == phase:
            return
        self.session.update_phase(phase)
        await self.store.publish(ShapingEvent(session_id=self.session.session_id, event="phase_changed", data={"phase": phase.value}))

    async def _publish_block(self, block: InteractionBlock) -> None:
        await self.store.publish(ShapingEvent(session_id=self.session.session_id, event="block_added", data={"block": asdict(block)}))


def _last_index(blocks: list[InteractionBlock], block_type: BlockType) -> int | None:
    for index in range(len(blocks) - 1, -1, -1):
        if blocks[index].type == block_type:
            return index
    return None
