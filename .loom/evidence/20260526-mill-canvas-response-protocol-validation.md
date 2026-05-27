# Mill Canvas Response Protocol Validation

ID: evidence:20260526-mill-canvas-response-protocol-validation
Type: Evidence Dossier
Status: recorded
Created: 2026-05-26
Updated: 2026-05-26
Observed: 2026-05-26

## Summary

Validation observations for `ticket:20260526-mill-canvas-response-protocol` after replacing the shaping response parser and prompt with the multi-node XML protocol.

## Observations

- Observation: Parser-focused tests passed.
  Procedure/source: `cd loom-mill && uv run pytest tests/test_canvas_parser.py -v`.
  Actual result: `15 passed in 0.21s`.
- Observation: Full Mill test suite passed after parser, prompt, engine, and shaping test updates.
  Procedure/source: `cd loom-mill && uv run pytest tests/ -v`.
  Actual result: `111 passed in 34.83s`.
- Observation: Requested full-suite tail command also reported the same passing count with one warning.
  Procedure/source: `cd loom-mill && uv run pytest tests/ -v 2>&1 | tail -30`.
  Actual result: `111 passed, 1 warning in 34.79s`; warning was a pre-existing style asyncio subprocess transport warning from `tests/test_workstation_engine.py::test_workstation_records_failed_exit`.
- Observation: Old action-block parser and prompt identifiers were absent from Mill source and tests.
  Procedure/source: grep scans for `parse_decision`, `build_decision_prompt`, action-block strings, and old parser helper names under `loom-mill/src` and `loom-mill/tests`.
  Actual result: no matches for removed shaping parser/prompt identifiers or old action-block tests.
- Observation: Diff whitespace check passed.
  Procedure/source: `git diff --check` from repository root.
  Actual result: no output.

## Artifacts

- Command outputs are preserved in the current session transcript; no separate raw artifact files were created.

## What This Shows

- `ticket:20260526-mill-canvas-response-protocol#ACC-001` - supports - parser tests cover multi-node XML extraction, including observation plus question and option groups.
- `ticket:20260526-mill-canvas-response-protocol#ACC-002` - supports - parser tests cover record Markdown content with headings, lists, and fenced code blocks.
- `ticket:20260526-mill-canvas-response-protocol#ACC-003` - supports - parser tests cover unclosed tags, no tags, empty tags, extra text, partially formed tags, XML-like angle brackets, and long content.
- `ticket:20260526-mill-canvas-response-protocol#ACC-004` - supports - grep scans found no removed shaping parser/prompt identifiers or old action-block tests.
- `ticket:20260526-mill-canvas-response-protocol#ACC-005` - partially supports - prompt code includes XML format examples and constraints; sufficiency still depends on review.
- `ticket:20260526-mill-canvas-response-protocol#ACC-006` - supports - parser tests cover explore extraction and explore with other nodes.

## What This Does Not Show

This evidence does not prove real LLM compliance with the XML format, frontend rendering behavior, or audit acceptance. The full-suite warning should be rechecked only if subprocess lifecycle behavior becomes part of this ticket's claim.

## Related Records

- `ticket:20260526-mill-canvas-response-protocol` - consuming ticket.
- `spec:mill-shaping-canvas` - canvas node behavior and bounded processing requirements.
- `plan:20260526-mill-shaping-canvas` - parent plan Unit 3.
