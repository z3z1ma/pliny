from __future__ import annotations

from loom_mill.shaping.parser import parse_canvas_response


def test_continue_op_parsed_with_target() -> None:
    response = parse_canvas_response(
        '<op kind="continue" from="n2"/>\n'
        '<node type="tension">Two specs overlap.</node>'
    )
    assert len(response.ops) == 1
    assert response.ops[0].kind == "continue"
    assert response.ops[0].args["from"] == "n2"
    assert response.nodes[0].type == "tension"


def test_supersede_op_parsed_with_targets_list() -> None:
    response = parse_canvas_response(
        '<op kind="supersede" targets="temp:specs:a,temp:specs:b"/>\n'
        '<node type="record" surface="specs" title="Merged spec">\n# Merged\n</node>'
    )
    assert response.ops[0].kind == "supersede"
    assert response.ops[0].args["targets"] == "temp:specs:a,temp:specs:b"
    assert response.nodes[0].type == "record"


def test_discard_staged_op_parsed() -> None:
    response = parse_canvas_response('<op kind="discard-staged" temp_id="temp:specs:a"/>')
    assert response.ops[0].kind == "discard-staged"
    assert response.ops[0].args["temp_id"] == "temp:specs:a"


def test_no_ops_yields_empty_ops_list() -> None:
    response = parse_canvas_response('<node type="observation">Just a fact.</node>')
    assert response.ops == []
    assert response.nodes[0].type == "observation"


def test_framing_tension_decision_nodes_parse() -> None:
    response = parse_canvas_response(
        '<node type="framing">Treat it as a latency problem.</node>'
        '<node type="tension">Cache vs freshness.</node>'
        '<node type="decision">Go with hierarchical layout.</node>'
    )
    types = [n.type for n in response.nodes]
    assert types == ["framing", "tension", "decision"]
