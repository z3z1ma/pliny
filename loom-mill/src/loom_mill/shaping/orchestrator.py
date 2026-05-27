from __future__ import annotations

import asyncio
from dataclasses import asdict
from uuid import uuid4

from loom_mill.state.store import MillStateStore
from loom_mill.workstation.config import HarnessConfig

from .events import ShapingEvent
from .harness import InvocationConfig, InvocationResult, run_bounded_invocation
from .models import CanvasNode, CanvasNodeType, NodeStatus
from .session import ShapingSession, utc_now


class ShapingOrchestrator:
    def __init__(
        self,
        session: ShapingSession,
        store: MillStateStore,
        harness_config: HarnessConfig,
        *,
        timeout_seconds: float = 120.0,
    ) -> None:
        self.session = session
        self.store = store
        self.harness_config = harness_config
        self.timeout_seconds = timeout_seconds
        self._active: dict[str, asyncio.Task[None]] = {}
        self._results: dict[str, InvocationResult] = {}
        self._cancelled: set[str] = set()
        self._goals: dict[str, str] = {}

    async def launch(self, goal: str, context_excerpt: str | None = None) -> str:
        invocation_id = str(uuid4())
        if context_excerpt is None:
            context_excerpt = self.session.read_context()[-4000:]

        config = InvocationConfig(
            goal=goal,
            context_excerpt=context_excerpt,
            command=self.harness_config.command,
            args=list(self.harness_config.args),
            env=dict(self.harness_config.env or {}),
            cwd=self.harness_config.cwd,
            timeout_seconds=self.timeout_seconds,
        )
        self._goals[invocation_id] = goal

        parent_id = _active_parent_id(self.session.state.nodes)
        node = CanvasNode(
            id=str(uuid4()),
            type=CanvasNodeType.PROCESSING,
            parent_id=parent_id,
            status=NodeStatus.ACTIVE,
            content={"invocation_id": invocation_id, "goal": goal, "command": config.command},
            position=None,
            timestamp=utc_now(),
        )
        self.session.state.active_explorations[node.id] = invocation_id
        await self._add_and_publish_node(node)
        await self.store.publish(
            ShapingEvent(session_id=self.session.session_id, event="exploration_start", data={"invocation_id": invocation_id, "goal": goal})
        )

        task = asyncio.create_task(self._run(invocation_id, config))
        self._active[invocation_id] = task
        return invocation_id

    async def cancel(self, invocation_id: str) -> bool:
        task = self._active.get(invocation_id)
        if task is None or task.done():
            return False
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        if invocation_id in self._active:
            await self._record_cancelled(invocation_id, self._goals.get(invocation_id, ""))
            self._finish_invocation(invocation_id)
        return True

    @property
    def active_count(self) -> int:
        return len(self._active)

    def get_result(self, invocation_id: str) -> InvocationResult | None:
        return self._results.get(invocation_id)

    def list_explorations(self) -> list[dict]:
        start_nodes = {
            node.content.get("invocation_id"): node
            for node in self.session.state.nodes.values()
            if node.type == CanvasNodeType.PROCESSING
        }
        complete_nodes = {
            node.content.get("invocation_id"): node
            for node in self.session.state.nodes.values()
            if node.content.get("event") == "exploration_complete"
        }
        ids = list(dict.fromkeys([*self._goals, *self.session.state.active_explorations.values(), *start_nodes, *complete_nodes]))
        return [
            self._exploration_payload(invocation_id, start_nodes.get(invocation_id), complete_nodes.get(invocation_id))
            for invocation_id in ids
            if invocation_id
        ]

    async def _run(self, invocation_id: str, config: InvocationConfig) -> None:
        try:
            async def on_stream(line: str) -> None:
                await self.store.publish(
                    ShapingEvent(
                        session_id=self.session.session_id,
                        event="exploration_stream",
                        data={"invocation_id": invocation_id, "delta": line},
                    )
                )

            result = await run_bounded_invocation(config, invocation_id, on_stream=on_stream)
            self._results[invocation_id] = result
            summary = result.context_summary or result.output[-2000:].strip()
            context_size = await self.session.append_context(f"Exploration: {config.goal}", summary)
            node = CanvasNode(
                id=str(uuid4()),
                type=CanvasNodeType.OBSERVATION,
                parent_id=_node_id_for_invocation(self.session.state.active_explorations, invocation_id),
                status=NodeStatus.ACTIVE,
                content={
                    "event": "exploration_complete",
                    "invocation_id": invocation_id,
                    "summary": summary or "(no summary produced)",
                    "context_added": len(summary.encode("utf-8")) if summary else 0,
                    "context_size": context_size,
                    "exit_code": result.exit_code,
                    "duration_seconds": result.duration_seconds,
                },
                position=None,
                timestamp=utc_now(),
            )
            await self._add_and_publish_node(node)
            await self.store.publish(
                ShapingEvent(
                    session_id=self.session.session_id,
                    event="exploration_complete",
                    data={"invocation_id": invocation_id, "summary": summary or "(no summary produced)", "exit_code": result.exit_code},
                )
            )
        except asyncio.CancelledError:
            await self._record_cancelled(invocation_id, config.goal)
        finally:
            self._finish_invocation(invocation_id)

    async def _record_cancelled(self, invocation_id: str, goal: str) -> None:
        self._cancelled.add(invocation_id)
        if any(node.content.get("event") == "exploration_cancelled" and node.content.get("invocation_id") == invocation_id for node in self.session.state.nodes.values()):
            return
        node = CanvasNode(
            id=str(uuid4()),
            type=CanvasNodeType.OBSERVATION,
            parent_id=_node_id_for_invocation(self.session.state.active_explorations, invocation_id),
            status=NodeStatus.ACTIVE,
            content={"invocation_id": invocation_id, "message": f"Exploration cancelled: {goal}"},
            position=None,
            timestamp=utc_now(),
        )
        node.content["event"] = "exploration_cancelled"
        await self._add_and_publish_node(node)
        await self.store.publish(
            ShapingEvent(session_id=self.session.session_id, event="exploration_cancelled", data={"invocation_id": invocation_id})
        )

    async def _add_and_publish_node(self, node: CanvasNode) -> None:
        edge = self.session.add_node_with_edge(node)
        await self.store.publish(ShapingEvent(session_id=self.session.session_id, event="node_added", data={"node": asdict(node)}))
        if edge is not None:
            await self.store.publish(ShapingEvent(session_id=self.session.session_id, event="edge_added", data={"edge": asdict(edge)}))

    def _finish_invocation(self, invocation_id: str) -> None:
        self._active.pop(invocation_id, None)
        node_id = _node_id_for_invocation(self.session.state.active_explorations, invocation_id)
        if node_id is not None:
            self.session.state.active_explorations.pop(node_id, None)
            self.session._persist_state()

    def _exploration_payload(
        self,
        invocation_id: str,
        start_node: CanvasNode | None,
        complete_node: CanvasNode | None,
    ) -> dict:
        result = self._results.get(invocation_id)
        status = "running" if invocation_id in self._active else "complete" if complete_node else "cancelled"
        if invocation_id in self._cancelled:
            status = "cancelled"
        return {
            "invocation_id": invocation_id,
            "goal": self._goals.get(invocation_id) or (start_node.content.get("goal") if start_node else ""),
            "status": status,
            "summary": complete_node.content.get("summary") if complete_node else None,
            "exit_code": result.exit_code if result else complete_node.content.get("exit_code") if complete_node else None,
        }


def _node_id_for_invocation(active_explorations: dict[str, str], invocation_id: str) -> str | None:
    for node_id, active_invocation_id in active_explorations.items():
        if active_invocation_id == invocation_id:
            return node_id
    return None


def _active_parent_id(nodes: dict[str, CanvasNode]) -> str | None:
    for node in reversed(list(nodes.values())):
        if node.status == NodeStatus.ACTIVE and node.type != CanvasNodeType.PROCESSING:
            return node.id
    return None
