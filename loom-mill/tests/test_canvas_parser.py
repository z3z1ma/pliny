from __future__ import annotations

from loom_mill.shaping.parser import ParsedNode, ParsedResponse, parse_canvas_response


def test_single_observation_node() -> None:
    response = parse_canvas_response("<node type=\"observation\">Found a constraint.</node>")

    assert response == ParsedResponse(nodes=[ParsedNode(type="observation", content="Found a constraint.")])


def test_single_question_with_options() -> None:
    response = parse_canvas_response('<node type="question" options="tickets, specs, plans">Which surface owns this?</node>')

    assert response.nodes[0].type == "question"
    assert response.nodes[0].content == "Which surface owns this?"
    assert response.nodes[0].options == ["tickets", "specs", "plans"]


def test_single_question_without_options() -> None:
    response = parse_canvas_response('<node type="question">What should not change?</node>')

    assert response.nodes[0].type == "question"
    assert response.nodes[0].content == "What should not change?"
    assert response.nodes[0].options is None


def test_record_proposal_with_full_markdown_content() -> None:
    markdown = """# Implement Cache Invalidation

ID: ticket:20260526-cache-invalidation
Type: Ticket
Status: open

## Scope

- Add cache invalidation on record writes.
- Preserve read behavior.

```python
def invalidate(key: str) -> None:
    cache.pop(key, None)
```
"""
    response = parse_canvas_response(f'<node type="record" surface="tickets" title="Implement cache invalidation">\n{markdown}</node>')

    node = response.nodes[0]
    assert node.type == "record"
    assert node.surface == "tickets"
    assert node.title == "Implement cache invalidation"
    assert node.content == markdown.strip()


def test_option_group_with_three_options() -> None:
    response = parse_canvas_response(
        '<node type="option-group" reasoning="Three materially different approaches">'
        '<option label="Local fix">Patch only the parser.</option>'
        '<option label="Protocol rewrite">Change parser and prompt together.</option>'
        '<option label="Defer">Keep shaping before implementation.</option>'
        '</node>'
    )

    node = response.nodes[0]
    assert node.type == "option_group"
    assert node.reasoning == "Three materially different approaches"
    assert node.option_labels == ["Local fix", "Protocol rewrite", "Defer"]
    assert node.content.splitlines() == [
        "Patch only the parser.",
        "Change parser and prompt together.",
        "Keep shaping before implementation.",
    ]


def test_multiple_nodes_in_one_response() -> None:
    response = parse_canvas_response(
        '<node type="observation">The model lacks parent refs.</node>'
        '<node type="question" options="Evolve,Replace">How should the graph model change?</node>'
    )

    assert [node.type for node in response.nodes] == ["observation", "question"]
    assert response.nodes[0].content == "The model lacks parent refs."
    assert response.nodes[1].options == ["Evolve", "Replace"]


def test_explore_goal_extraction() -> None:
    response = parse_canvas_response('<explore goal="Check existing test coverage for shaping engine"/>')

    assert response.explore_goal == "Check existing test coverage for shaping engine"
    assert response.nodes == []


def test_explore_and_other_nodes_in_same_response() -> None:
    response = parse_canvas_response(
        '<node type="observation">Coverage is unclear.</node>'
        '<explore goal="Inspect parser tests"/>'
    )

    assert response.explore_goal == "Inspect parser tests"
    assert response.nodes[0].content == "Coverage is unclear."


def test_unclosed_node_tag_degrades_to_best_effort_node() -> None:
    response = parse_canvas_response('<node type="observation">The model omitted the closing tag')

    assert response.nodes == [ParsedNode(type="observation", content="The model omitted the closing tag")]


def test_no_tags_at_all_degrades_to_observation_from_raw_text() -> None:
    response = parse_canvas_response("unstructured model output")

    assert response.nodes == [ParsedNode(type="observation", content="unstructured model output")]


def test_empty_tags() -> None:
    response = parse_canvas_response('<node type="observation"></node>')

    assert response.nodes == [ParsedNode(type="observation", content="")]


def test_extra_text_outside_tags_is_ignored() -> None:
    response = parse_canvas_response('preamble <node type="observation">Keep this.</node> trailing text')

    assert response.nodes == [ParsedNode(type="observation", content="Keep this.")]


def test_partially_formed_tags_degrade_to_observation() -> None:
    response = parse_canvas_response('<node type="question" Which surface owns this?')

    assert response.nodes == [ParsedNode(type="observation", content='<node type="question" Which surface owns this?')]


def test_record_content_can_contain_xml_like_angle_brackets() -> None:
    content = """# Render Snippet

Use `<CanvasNode type="record">` in docs.

```svelte
<CanvasNode type="record" />
```
"""
    response = parse_canvas_response(f'<node type="record" surface="specs" title="Render snippet">{content}</node>')

    assert response.nodes[0].content == content.strip()


def test_record_content_preserves_literal_node_close_tag() -> None:
    content = """# XML Example

Use this closing tag in docs:

```xml
</node>
```

Then continue the record.
"""
    response = parse_canvas_response(
        f'<node type="record" surface="specs" title="XML example">{content}</node>'
        '<node type="observation">Next node.</node>'
    )

    assert response.nodes[0].type == "record"
    assert response.nodes[0].content == content.strip()
    assert response.nodes[1] == ParsedNode(type="observation", content="Next node.")


def test_very_long_content() -> None:
    long_content = "x" * 2100
    response = parse_canvas_response(f'<node type="observation">{long_content}</node>')

    assert response.nodes[0].content == long_content
    assert len(response.nodes[0].content) == 2100
