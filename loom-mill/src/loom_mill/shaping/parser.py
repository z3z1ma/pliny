from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Decision:
    action: str
    goal: str | None = None
    context_excerpt: str | None = None
    question: str | None = None
    options: list[str] | None = None
    context_ref: str | None = None
    observation: str | None = None
    evidence: list[str] | None = None
    record_surface: str | None = None
    record_title: str | None = None
    record_content: str | None = None
    branches: list[dict[str, str]] | None = None
    reasoning: str | None = None


def parse_decision(output: str) -> Decision:
    match = re.search(r"```action\s*\n(.+?)```", output, re.DOTALL | re.IGNORECASE)
    if not match:
        return Decision(action="observation", observation=output[:2000])

    fields = _parse_fields(match.group(1))
    action = fields.get("type", "observation").strip().lower() or "observation"
    if action not in {"explore", "question", "observation", "propose", "branch"}:
        return Decision(action="observation", observation=output[:2000])

    return Decision(
        action=action,
        goal=_blank_to_none(fields.get("goal")),
        context_excerpt=_blank_to_none(fields.get("context_excerpt")),
        question=_blank_to_none(fields.get("question")),
        options=_parse_options(fields.get("options")),
        context_ref=_blank_to_none(fields.get("context_ref")),
        observation=_blank_to_none(fields.get("observation")),
        evidence=_parse_lines(fields.get("evidence")),
        record_surface=_blank_to_none(fields.get("surface")),
        record_title=_blank_to_none(fields.get("title")),
        record_content=_blank_to_none(fields.get("content")),
        branches=_parse_branches(fields.get("branches")),
        reasoning=_blank_to_none(fields.get("reasoning")),
    )


def _parse_fields(block: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    current_key: str | None = None
    current_value: list[str] = []

    for line in block.splitlines():
        kv = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if kv:
            if current_key is not None:
                fields[current_key] = "\n".join(current_value).strip()
            current_key = kv.group(1).lower()
            current_value = [kv.group(2)]
        elif current_key is not None:
            current_value.append(line)

    if current_key is not None:
        fields[current_key] = "\n".join(current_value).strip()
    return fields


def _blank_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _parse_options(value: str | None) -> list[str] | None:
    value = _blank_to_none(value)
    if value is None or value.lower() == "open":
        return None
    return [option.strip() for option in value.split(",") if option.strip()]


def _parse_lines(value: str | None) -> list[str] | None:
    value = _blank_to_none(value)
    if value is None:
        return None
    return [line.strip() for line in value.splitlines() if line.strip()]


def _parse_branches(value: str | None) -> list[dict[str, str]] | None:
    value = _blank_to_none(value)
    if value is None:
        return None
    branches = []
    for index, label in enumerate(part.strip() for part in value.split("|")):
        if label:
            branches.append({"id": f"branch-{index + 1}", "label": label})
    return branches or None
