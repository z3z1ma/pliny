from __future__ import annotations

from dataclasses import asdict
from uuid import uuid4

from loom_mill.state.store import MillStateStore

from .events import ShapingEvent
from .harness import InvocationConfig, harness_command_error, run_bounded_invocation
from .models import CanvasEdge, CanvasNode, CanvasNodeType, NodeStatus, SessionPhase
from .orchestrator import ShapingOrchestrator
from .parser import ParsedNode, ParsedResponse, parse_canvas_response
from .prompts import build_canvas_prompt
from .serialize import serialize_graph
from .session import ShapingSession, utc_now


class ShapingEngine:
    def __init__(self, session: ShapingSession, orchestrator: ShapingOrchestrator, store: MillStateStore) -> None:
        self.session = session
        self.orchestrator = orchestrator
        self.store = store

    async def advance(self) -> list[CanvasNode]:
        await self._transition_for_operator_feedback()
        parent_id = _active_parent_id(self.session.state.nodes)
        return await self._advance_from(parent_id)

    async def regenerate(self, from_node_id: str, max_depth: int = 3) -> list[CanvasNode]:
        """Re-invoke from a specific node, replacing stale direct child subtrees."""
        if max_depth <= 0:
            return []
        stale_ids = [
            node.id
            for node in list(self.session.state.nodes.values())
            if node.parent_id == from_node_id and node.status == NodeStatus.STALE
        ]
        removed_ids: list[str] = []
        for stale_id in stale_ids:
            removed_ids.extend(self._remove_subtree(stale_id))
        if removed_ids:
            self.session.state.updated_at = utc_now()
            self.session._persist_state()
            await self.store.publish(
                ShapingEvent(
                    session_id=self.session.session_id,
                    event="nodes_removed",
                    data={"node_ids": removed_ids},
                )
            )
        return await self._advance_from(from_node_id)

    async def _apply_ops(self, ops: list, parsed_nodes: list[ParsedNode], parent_id: str | None) -> list[CanvasNode]:
        """Apply structured mutation ops and return any error observation nodes."""
        created: list[CanvasNode] = []
        for op in ops:
            try:
                if op.kind == "discard-staged":
                    self.session.staging.reject(op.args["temp_id"])
                elif op.kind == "edit-staged":
                    record = next((n for n in parsed_nodes if n.type == "record"), None)
                    if record is None:
                        raise ValueError("edit-staged requires a paired record node")
                    self.session.staging.update(op.args["temp_id"], content=record.content, title=record.title)
                elif op.kind == "supersede":
                    record = next((n for n in parsed_nodes if n.type == "record"), None)
                    if record is None:
                        raise ValueError("supersede requires a paired record node")
                    targets = [t.strip() for t in op.args.get("targets", "").split(",") if t.strip()]
                    self.session.staging.consolidate(
                        targets,
                        surface=record.surface or "specs",
                        title=record.title or "Consolidated record",
                        content=record.content or "",
                    )
            except (KeyError, ValueError) as error:
                node = self._new_node(
                    CanvasNodeType.OBSERVATION,
                    {"observation": f"Op '{op.kind}' could not be applied: {error}", "evidence": None},
                    parent_id=parent_id,
                )
                edge = self.session.add_node_with_edge(node)
                await self._publish_node(node)
                if edge is not None:
                    await self._publish_edge(edge)
                created.append(node)
        return created

    def _remove_subtree(self, node_id: str) -> list[str]:
        """Remove a node and all descendants from session state."""
        removed: list[str] = []
        children = [node.id for node in list(self.session.state.nodes.values()) if node.parent_id == node_id]
        for child_id in children:
            removed.extend(self._remove_subtree(child_id))
        if self.session.state.nodes.pop(node_id, None) is not None:
            removed.append(node_id)
        self.session.state.edges = [
            edge for edge in self.session.state.edges if edge.source_id != node_id and edge.target_id != node_id
        ]
        return removed

    async def _advance_from(self, parent_id: str | None) -> list[CanvasNode]:
        if error := harness_command_error(self.orchestrator.harness_config.command):
            node = self._new_node(CanvasNodeType.OBSERVATION, {"message": error}, parent_id=parent_id)
            edge = self.session.add_node_with_edge(node)
            await self._publish_node(node)
            if edge is not None:
                await self._publish_edge(edge)
            return [node]
        context = self._context_for_node(parent_id)
        graph_view = serialize_graph(self.session.state)
        recent_nodes = self._path_to_node(parent_id)[-20:] if parent_id else list(self.session.state.nodes.values())[-20:]
        response = await self._decide_next_action(context, graph_view, recent_nodes, self.session.state.phase)

        if response.explore_goal and not response.nodes:
            node_count = len(self.session.state.nodes)
            await self.orchestrator.launch(response.explore_goal)
            return list(self.session.state.nodes.values())[node_count:]

        # Resolve parent override for continue/revise ops; fail closed on unknown nodes
        pre_op_nodes: list[CanvasNode] = []
        for op in response.ops:
            if op.kind == "continue":
                target_id = op.args.get("from")
                if target_id in self.session.state.nodes:
                    parent_id = target_id
                elif target_id:
                    node = self._new_node(
                        CanvasNodeType.OBSERVATION,
                        {"observation": f"Op 'continue' references unknown node {target_id}", "evidence": None},
                        parent_id=parent_id,
                    )
                    edge = self.session.add_node_with_edge(node)
                    await self._publish_node(node)
                    if edge is not None:
                        await self._publish_edge(edge)
                    pre_op_nodes.append(node)
            elif op.kind == "revise":
                target_id = op.args.get("node")
                if target_id in self.session.state.nodes:
                    self.session.invalidate_nodes(
                        [n.id for n in self.session.state.nodes.values() if n.parent_id == target_id]
                    )
                    parent_id = target_id
                elif target_id:
                    node = self._new_node(
                        CanvasNodeType.OBSERVATION,
                        {"observation": f"Op 'revise' references unknown node {target_id}", "evidence": None},
                        parent_id=parent_id,
                    )
                    edge = self.session.add_node_with_edge(node)
                    await self._publish_node(node)
                    if edge is not None:
                        await self._publish_edge(edge)
                    pre_op_nodes.append(node)

        # Identify records consumed by supersede/edit-staged ops
        consuming_ops = {op.kind for op in response.ops} & {"supersede", "edit-staged"}

        nodes: list[CanvasNode] = []
        for parsed_node in response.nodes:
            # Skip record nodes that will be consumed by supersede/edit-staged
            if parsed_node.type == "record" and consuming_ops:
                continue
            if parsed_node.type == "option_group":
                nodes.extend(await self._add_option_group(parsed_node, parent_id))
                continue
            node = self._node_from_parsed_node(parsed_node, parent_id)
            if node.type == CanvasNodeType.RECORD:
                staged = self.session.staging.propose(
                    str(node.content.get("surface") or "tickets"),
                    str(node.content.get("title") or "Untitled proposal"),
                    str(node.content.get("content") or ""),
                    self.session.state.active_branch,
                )
                node.content["temp_id"] = staged.temp_id
            edge = self.session.add_node_with_edge(node)
            await self._publish_node(node)
            if edge is not None:
                await self._publish_edge(edge)
            await self._transition_after_node(node)
            nodes.append(node)

        # Apply structured mutation ops
        op_nodes = await self._apply_ops(response.ops, response.nodes, parent_id)

        if response.explore_goal:
            await self.orchestrator.launch(response.explore_goal)
        return nodes + op_nodes + pre_op_nodes

    def _path_to_node(self, node_id: str | None) -> list[CanvasNode]:
        path: list[CanvasNode] = []
        current_id = node_id
        seen: set[str] = set()
        while current_id and current_id not in seen:
            seen.add(current_id)
            node = self.session.state.nodes.get(current_id)
            if node is None:
                break
            path.append(node)
            current_id = node.parent_id
        return list(reversed(path))

    def _context_for_node(self, node_id: str | None) -> str:
        path = self._path_to_node(node_id)
        if not path:
            return self.session.read_context()
        lines = ["# Shaping Session", "", "## Context Path"]
        for node in path:
            lines.append(f"- {node.type.value}: {_node_summary(node)}")
        return "\n".join(lines) + "\n"

    async def _add_option_group(self, parsed_node: ParsedNode, parent_id: str | None) -> list[CanvasNode]:
        group = self._new_node(CanvasNodeType.OPTION_GROUP, self._content_from_parsed_node(parsed_node), parent_id=parent_id)
        group_edge = self.session.add_node_with_edge(group)
        await self._publish_node(group)
        if group_edge is not None:
            await self._publish_edge(group_edge)

        nodes = [group]
        option_contents = [part.strip() for part in parsed_node.content.splitlines() if part.strip()]
        for index, label in enumerate(parsed_node.option_labels or []):
            option = CanvasNode(
                id=str(uuid4()),
                type=CanvasNodeType.OPTION,
                parent_id=group.id,
                status=NodeStatus.ACTIVE,
                content={"label": label, "content": option_contents[index] if index < len(option_contents) else ""},
                position=None,
                timestamp=utc_now(),
                option_group_id=group.id,
            )
            edge = self.session.add_node_with_edge(option, edge_type="option_group")
            await self._publish_node(option)
            if edge is not None:
                await self._publish_edge(edge)
            nodes.append(option)
        return nodes

    async def _decide_next_action(
        self,
        context: str,
        graph_view: str,
        recent_nodes: list[CanvasNode],
        phase: SessionPhase,
    ) -> ParsedResponse:
        prompt = build_canvas_prompt(context, graph_view, recent_nodes, phase)
        config = InvocationConfig(
            goal="Decide next shaping action",
            context_excerpt="",
            command=self.orchestrator.harness_config.command,
            args=list(self.orchestrator.harness_config.args),
            env=dict(self.orchestrator.harness_config.env or {}),
            cwd=self.orchestrator.harness_config.cwd,
            timeout_seconds=300.0,
        )
        try:
            result = await run_bounded_invocation(
                config,
                invocation_id=f"decision-{uuid4().hex[:8]}",
                on_stream=None,
                prompt_override=prompt,
            )
        except Exception as error:
            return ParsedResponse(nodes=[ParsedNode(type="observation", content=f"Decision harness failed: {error}")])

        output = result.output.strip()
        if result.exit_code != 0 and not output:
            message = result.stderr.strip() or f"decision harness exited with code {result.exit_code}"
            return ParsedResponse(nodes=[ParsedNode(type="observation", content=f"Decision harness failed: {message}")])
        return parse_canvas_response(output or result.stderr.strip())

    def _node_from_parsed_node(self, parsed_node: ParsedNode, parent_id: str | None) -> CanvasNode:
        node_type = {
            "question": CanvasNodeType.QUESTION,
            "observation": CanvasNodeType.OBSERVATION,
            "framing": CanvasNodeType.FRAMING,
            "tension": CanvasNodeType.TENSION,
            "decision": CanvasNodeType.DECISION,
            "record": CanvasNodeType.RECORD,
            "option_group": CanvasNodeType.OPTION_GROUP,
        }.get(parsed_node.type, CanvasNodeType.OBSERVATION)
        return self._new_node(node_type, self._content_from_parsed_node(parsed_node), parent_id=parent_id)

    def _new_node(self, node_type: CanvasNodeType, content: dict, parent_id: str | None = None) -> CanvasNode:
        return CanvasNode(
            id=str(uuid4()),
            type=node_type,
            parent_id=parent_id,
            status=NodeStatus.ACTIVE,
            content=content,
            position=None,
            timestamp=utc_now(),
        )

    def _content_from_parsed_node(self, parsed_node: ParsedNode) -> dict:
        if parsed_node.type == "question":
            return {
                "question": parsed_node.content or "What should we clarify next?",
                "options": parsed_node.options,
                "context_ref": None,
            }
        if parsed_node.type == "record":
            return {
                "temp_id": f"proposal-{uuid4().hex[:8]}",
                "surface": parsed_node.surface or "tickets",
                "title": parsed_node.title or "Untitled proposal",
                "content": parsed_node.content,
            }
        if parsed_node.type == "option_group":
            option_contents = [part.strip() for part in parsed_node.content.splitlines() if part.strip()]
            return {
                "branches": [
                    {"id": f"branch-{index + 1}", "label": label, "content": option_contents[index] if index < len(option_contents) else ""}
                    for index, label in enumerate(parsed_node.option_labels or [])
                ],
                "reasoning": parsed_node.reasoning,
            }
        if parsed_node.type in ("framing", "tension", "decision"):
            return {parsed_node.type: parsed_node.content or "", "evidence": None}
        return {"observation": parsed_node.content or "No structured response was produced.", "evidence": None}

    async def _transition_for_operator_feedback(self) -> None:
        if self.session.state.phase != SessionPhase.PROPOSING:
            return
        nodes = list(self.session.state.nodes.values())
        last_proposal = _last_index(nodes, CanvasNodeType.RECORD)
        last_input = _last_index(nodes, CanvasNodeType.INPUT)
        if last_proposal is not None and last_input is not None and last_input > last_proposal:
            await self._update_phase(SessionPhase.REFINING)

    async def _transition_after_node(self, node: CanvasNode) -> None:
        if self.session.state.phase == SessionPhase.EXPLORING and node.type == CanvasNodeType.QUESTION:
            await self._update_phase(SessionPhase.NARROWING)
        elif node.type == CanvasNodeType.RECORD and self.session.state.phase != SessionPhase.REFINING:
            await self._update_phase(SessionPhase.PROPOSING)

    async def _update_phase(self, phase: SessionPhase) -> None:
        if self.session.state.phase == phase:
            return
        self.session.update_phase(phase)
        await self.store.publish(ShapingEvent(session_id=self.session.session_id, event="phase_changed", data={"phase": phase.value}))

    async def _publish_node(self, node: CanvasNode) -> None:
        await self.store.publish(ShapingEvent(session_id=self.session.session_id, event="node_added", data={"node": asdict(node)}))

    async def _publish_edge(self, edge: CanvasEdge) -> None:
        await self.store.publish(ShapingEvent(session_id=self.session.session_id, event="edge_added", data={"edge": asdict(edge)}))


def _last_index(nodes: list[CanvasNode], node_type: CanvasNodeType) -> int | None:
    for index in range(len(nodes) - 1, -1, -1):
        if nodes[index].type == node_type:
            return index
    return None


def _active_parent_id(nodes: dict[str, CanvasNode]) -> str | None:
    for node in reversed(list(nodes.values())):
        if node.status == NodeStatus.ACTIVE and node.type != CanvasNodeType.PROCESSING:
            return node.id
    return None


def _node_summary(node: CanvasNode) -> str:
    for key in ("text", "question", "observation", "label", "title", "message"):
        value = node.content.get(key)
        if value:
            return str(value)
    return str(node.content)
