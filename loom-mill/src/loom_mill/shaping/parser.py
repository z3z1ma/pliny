from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ParsedNode:
    type: str
    content: str
    options: list[str] | None = None
    surface: str | None = None
    title: str | None = None
    reasoning: str | None = None
    option_labels: list[str] | None = None


@dataclass
class ParsedResponse:
    nodes: list[ParsedNode]
    explore_goal: str | None = None


_NODE_OPEN_RE = re.compile(r"<node\b(?P<attrs>[^>]*)>", re.IGNORECASE | re.DOTALL)
_NODE_CLOSE_RE = re.compile(r"</node\s*>", re.IGNORECASE)
_OPTION_RE = re.compile(r"<option\b(?P<attrs>[^>]*)>(?P<body>.*?)</option\s*>", re.IGNORECASE | re.DOTALL)
_EXPLORE_RE = re.compile(r"<explore\b(?P<attrs>[^>]*)/\s*>", re.IGNORECASE | re.DOTALL)
_XML_TAG_RE = re.compile(r"</?\w+\b|<\w+\b[^>]*/\s*>")
_ATTR_RE = re.compile(
    r"(?P<name>[\w:-]+)\s*=\s*(?:\"(?P<double>.*?)\"|'(?P<single>.*?)'|(?P<bare>[^\s>]+))",
    re.DOTALL,
)


def parse_canvas_response(output: str) -> ParsedResponse:
    explore_goal = _first_explore_goal(output)
    nodes = [_parse_node(attrs, body) for attrs, body in _node_blocks(output)]

    if not nodes and not _XML_TAG_RE.search(output):
        nodes.append(ParsedNode(type="observation", content=output.strip()))
    elif not nodes and explore_goal is None:
        nodes.append(ParsedNode(type="observation", content=output.strip()))

    return ParsedResponse(nodes=nodes, explore_goal=explore_goal)


def _node_blocks(output: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    position = 0
    while match := _NODE_OPEN_RE.search(output, position):
        body_start = match.end()
        attrs = match.group("attrs")
        node_type = _normalize_type(_parse_attrs(attrs).get("type") or "observation")
        next_open = _NODE_OPEN_RE.search(output, body_start)
        next_start = next_open.start() if next_open else len(output)

        if node_type == "record":
            close_matches = list(_NODE_CLOSE_RE.finditer(output, body_start, next_start))
            close = close_matches[-1] if close_matches else None
        else:
            close = _NODE_CLOSE_RE.search(output, body_start, next_start)

        if close:
            body_end = close.start()
            position = close.end()
        else:
            explore = _EXPLORE_RE.search(output, body_start)
            body_end = min(
                candidate
                for candidate in [next_start, explore.start() if explore else len(output), len(output)]
                if candidate >= body_start
            )
            position = body_end if body_end > match.start() else match.end()
        blocks.append((attrs, output[body_start:body_end]))
    return blocks


def _parse_node(attrs_text: str, body: str) -> ParsedNode:
    attrs = _parse_attrs(attrs_text)
    node_type = _normalize_type(attrs.get("type") or "observation")
    content = body.strip()

    if node_type == "question":
        return ParsedNode(type=node_type, content=content, options=_split_options(attrs.get("options")))
    if node_type == "record":
        return ParsedNode(type=node_type, content=content, surface=_blank_to_none(attrs.get("surface")), title=_blank_to_none(attrs.get("title")))
    if node_type == "option_group":
        options = list(_OPTION_RE.finditer(body))
        option_labels = [_blank_to_none(_parse_attrs(option.group("attrs")).get("label")) or "" for option in options]
        option_contents = [option.group("body").strip() for option in options]
        content_without_options = _OPTION_RE.sub("", body).strip()
        return ParsedNode(
            type=node_type,
            content=content_without_options or "\n".join(option_contents),
            reasoning=_blank_to_none(attrs.get("reasoning")),
            option_labels=option_labels or None,
        )
    return ParsedNode(type=node_type, content=content)


def _first_explore_goal(output: str) -> str | None:
    match = _EXPLORE_RE.search(output)
    if not match:
        return None
    return _blank_to_none(_parse_attrs(match.group("attrs")).get("goal"))


def _parse_attrs(attrs_text: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    for match in _ATTR_RE.finditer(attrs_text):
        value = match.group("double")
        if value is None:
            value = match.group("single")
        if value is None:
            value = match.group("bare") or ""
        attrs[match.group("name").lower()] = value
    return attrs


def _split_options(value: str | None) -> list[str] | None:
    value = _blank_to_none(value)
    if value is None:
        return None
    options = [option.strip() for option in value.split(",") if option.strip()]
    return options or None


def _blank_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _normalize_type(value: str) -> str:
    return value.strip().lower().replace("-", "_") or "observation"
