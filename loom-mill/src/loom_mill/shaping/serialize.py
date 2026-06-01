from __future__ import annotations

from .models import CanvasNode, NodeStatus, SessionState

_MAX_SUMMARY = 160
_MAX_DIGEST = 200


def _summary(node: CanvasNode) -> str:
    content = node.content or {}
    for key in ("text", "question", "observation", "label", "title", "summary", "goal", "message"):
        value = content.get(key)
        if value:
            return _one_line(str(value))
    return _one_line(str(content))


def _one_line(value: str, limit: int = _MAX_SUMMARY) -> str:
    value = " ".join(value.split())
    return value if len(value) <= limit else value[: limit - 3].rstrip() + "..."


def serialize_graph(state: SessionState) -> str:
    lines: list[str] = ["# Canvas Graph", ""]
    lines.append(f"Phase: {state.phase.value}")
    lines.append(f"Active branch: {state.active_branch}")
    lines.append("")
    lines.append("## Nodes")
    # Stable ordering by timestamp then id so the view is deterministic.
    for node in sorted(state.nodes.values(), key=lambda n: (n.timestamp, n.id)):
        parent = node.parent_id or "-"
        lines.append(
            f"- id={node.id} type={node.type.value} status={node.status.value} "
            f"parent={parent} :: {_summary(node)}"
        )
    lines.append("")
    lines.append("## Staging Area")
    if not state.staged_records:
        lines.append("(empty)")
    else:
        for record in state.staged_records:
            digest = _one_line(record.content, _MAX_DIGEST)
            lines.append(
                f"- temp_id={record.temp_id} surface={record.surface} "
                f"status={record.status} title={record.title!r}"
            )
            lines.append(f"  digest: {digest}")
    lines.append("")
    return "\n".join(lines)
