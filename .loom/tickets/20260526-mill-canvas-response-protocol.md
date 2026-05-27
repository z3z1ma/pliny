# Model Response Protocol for Multi-Node Output

ID: ticket:20260526-mill-canvas-response-protocol
Type: Ticket
Status: closed
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - AI output format reliability is uncertain; parser must be robust to malformed/partial responses

Depends On: ticket:20260526-mill-canvas-svelvet-proof

## Summary

Design and implement a response protocol that allows the AI model to produce
MULTIPLE typed nodes in a single response. The current format (single
` ```action ` block) supports only one decision per invocation. The canvas needs
the model to emit combinations: observation + question, multiple options,
observation + record proposal, etc.

The format uses XML-like tags that the parser extracts. The prompt template
instructs the model on the format. The parser is tolerant of malformed output.
The old ` ```action ` format and `parse_decision()` function are deleted — we own
the entire stack and do not carry dead code paths.

Single closure claim: The parser correctly extracts multiple typed nodes from model
XML output, with tested robustness for malformed responses.

## Related Records

- `spec:mill-shaping-canvas` — REQ-002 defines node types; REQ-011 requires
  parallel processing
- `plan:20260526-mill-shaping-canvas` — parent plan; this is Unit 3
- `loom-mill/src/loom_mill/shaping/parser.py` — current parser being replaced
- `loom-mill/src/loom_mill/shaping/prompts.py` — current prompt being rewritten
- `loom-mill/src/loom_mill/shaping/engine.py` — consumer of parsed output

## Scope

**What changes:**

`loom-mill/src/loom_mill/shaping/parser.py`:
- New `ParsedNode` dataclass:
  - `type: str` (observation, question, record, option_group)
  - `content: str` (node body text)
  - `options: list[str] | None` (for questions with options)
  - `surface: str | None` (for record nodes)
  - `title: str | None` (for record nodes)
  - `reasoning: str | None` (for option groups)
  - `option_labels: list[str] | None` (for option groups)
- New `ParsedResponse` dataclass:
  - `nodes: list[ParsedNode]`
  - `explore_goal: str | None` (if model wants to explore)
- New `parse_canvas_response(output: str) -> ParsedResponse` function (replaces
  `parse_decision()` entirely — delete the old function and its tests)
- Parser extraction rules:
  - Find all `<node type="...">...</node>` blocks
  - Find `<node type="option-group" ...><option ...>...</option>...</node>` blocks
  - If no XML tags found, treat the entire output as a single observation node
    (graceful degradation, not backward compat)
  - If `<explore goal="..."/>` self-closing tag found, set explore_goal
  - Gracefully handle: unclosed tags, nested tags, extra whitespace, mixed
    content outside tags

`loom-mill/src/loom_mill/shaping/prompts.py`:
- Replace `build_decision_prompt()` with `build_canvas_prompt()` (delete the old
  function entirely):
  - Format specification with examples for each node type
  - Clear instruction that multiple nodes are allowed/encouraged
  - Instruction to emit observation + question together when appropriate
  - Instruction for option-group format
  - Instruction for record proposals with full content
  - Instruction for `<explore goal="..."/>` when codebase exploration is needed
  - Guidelines: be specific, produce complete records not stubs, ask focused
    questions, observe contradictions

**Response format specification:**

```xml
<!-- Single observation -->
<node type="observation">
Discovered that GraphView.svelte uses d3-force for layout positioning.
The existing pattern handles ~50 nodes before performance degrades.
</node>

<!-- Question with options -->
<node type="question" options="Force-directed,Hierarchical DAG,Hybrid">
Which layout algorithm should the canvas use for auto-positioning?
</node>

<!-- Question with open response -->
<node type="question">
What quality bar matters most: visual polish or interaction speed?
</node>

<!-- Record proposal -->
<node type="record" surface="tickets" title="Implement canvas zoom controls">
# Implement canvas zoom controls

ID: ticket:20260526-canvas-zoom
Type: Ticket
Status: closed
...full Markdown content...
</node>

<!-- Option group (branching) -->
<node type="option-group" reasoning="Two architecturally different approaches">
<option label="Svelvet library">Use Svelvet for reactive node rendering</option>
<option label="Custom SVG">Build from scratch with d3 and raw SVG</option>
</node>

<!-- Exploration request -->
<explore goal="Check existing test coverage for shaping engine"/>

<!-- Multiple nodes in one response (the common case) -->
<node type="observation">
The session model currently uses a flat block list with no parent references.
</node>
<node type="question" options="Evolve existing model,Replace entirely">
Should we migrate the existing model or create a clean replacement?
</node>
```

**What must NOT change:**
- Harness invocation mechanism (this ticket only changes what we PARSE from output)
- Session persistence format (that's the graph model ticket)

**What gets deleted:**
- `parse_decision()` function and its `Decision` dataclass
- `build_decision_prompt()` function
- All tests that verify the old ` ```action ` format
- The `_parse_fields`, `_parse_options`, `_parse_branches` helper functions

**Stop condition:** If testing with real LLMs shows the XML format is unreliable
(models frequently produce malformed output that the parser can't recover from),
simplify to one-node-per-advance with a `type` prefix line instead of XML.

## Acceptance

- ACC-001: Parser extracts multiple nodes from well-formed XML output
  - Evidence: Unit tests: input with 2 observations → parses to 2 ParsedNodes.
    Input with observation + question → parses both. Input with option-group
    containing 3 options → parses group with labels.
  - Audit: Verify all spec node types are parseable

- ACC-002: Parser handles record proposals with full Markdown content (including
  code blocks, headings, lists inside the XML)
  - Evidence: Unit test: record node containing ` ``` ` code blocks, `#` headings,
    `- ` lists → content preserved exactly
  - Audit: Verify no content truncation or escaping corruption

- ACC-003: Parser is tolerant of malformed output
  - Evidence: Unit tests for: unclosed tags, extra text outside tags, partially
    formed tags, empty tags, duplicate attributes, no tags at all (degrades to
    single observation node from raw text)
  - Audit: Verify graceful degradation (always produces at least one node)

- ACC-004: Old parser code is fully deleted (no backward compat dead code)
  - Evidence: `parse_decision`, `Decision`, `build_decision_prompt`,
    `_parse_fields`, `_parse_options`, `_parse_branches` are all gone from the
    codebase. Old tests are replaced, not maintained.
  - Audit: `grep -r "parse_decision\|Decision\|build_decision_prompt" loom-mill/src/`
    returns nothing

- ACC-005: Prompt template clearly instructs the model with examples and constraints
  - Evidence: Prompt text includes format specification, examples for each type,
    multi-node encouragement, and exploration syntax
  - Audit: Manual review that prompt is unambiguous and complete

- ACC-006: Explore goal extraction works
  - Evidence: Unit test: `<explore goal="..."/>` self-closing tag → ParsedResponse
    with explore_goal set
  - Audit: Verify explore + other nodes can coexist in one response

## Current State

Implementation is complete and ready for audit/review. `parser.py` now exposes
`ParsedNode`, `ParsedResponse`, and `parse_canvas_response()`. `prompts.py` now
exposes `build_canvas_prompt()` and `format_node_history()`. The shaping engine
consumer uses the new parser/prompt API, creates canvas nodes from parsed nodes,
and launches exploration from `<explore goal="..."/>`. Parser and full Mill tests
pass; evidence is recorded in
`evidence:20260526-mill-canvas-response-protocol-validation`.

## Journal

- 2026-05-26: Created ticket with Status `open`. Contract-first: defines how model
  output becomes graph nodes. Parser robustness is critical — AI output is noisy.
- 2026-05-26: Status set to `active`; implementation run began for parser, prompt,
  engine consumer updates, and parser-focused tests.
- 2026-05-26: Implementation completed and status moved to `review`. Evidence
  recorded in `evidence:20260526-mill-canvas-response-protocol-validation`:
  parser tests `15 passed`, full Mill suite `111 passed` with one unrelated
  asyncio subprocess warning, old action-block parser/prompt identifiers removed
  from shaping source/tests, and `git diff --check` clean.
