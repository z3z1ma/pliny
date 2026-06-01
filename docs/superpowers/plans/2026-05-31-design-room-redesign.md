# Design Room Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Loom Mill Design Room a genuinely useful divergent-then-convergent shaping surface by giving the agent full graph + staging awareness with structured mutation ops, a differentiated intent-coded node vocabulary, a legible canvas (tidy layout, elbow edges, record modal), visible thinking/context, and real staging control.

**Architecture:** The keystone is a serialized full-graph view plus a structured-op vocabulary the one-shot harness agent emits (parsed in `parser.py`, applied in `engine.py`). Node types extend `CanvasNodeType`. The Svelte/Svelvet canvas (`frontend/src/lib/design/canvas/`) gains a width-aware layered-tree layout, orthogonal edges, and a record summary-card + modal. Transparency adds a decision-step thinking stream over the existing WebSocket and a context-peek panel.

**Tech Stack:** Python 3.12 (Starlette routes, dataclasses, `asyncio`), pytest + pytest-asyncio. Svelte 5 (runes) + Svelvet canvas, Vite, Tailwind. WebSocket event bus (`MillStateStore`).

**Spec:** `docs/superpowers/specs/2026-05-31-design-room-redesign.md`

## Conventions

- **Backend tests:** `cd loom-mill && uv run pytest tests/<file>::<test> -v`. Tests live in `loom-mill/tests/`, flat, named `test_*.py`, plain functions; async tests use `@pytest.mark.asyncio`.
- **Frontend:** no JS test runner is installed. Verify frontend tasks with `cd loom-mill/frontend && npm run build` (must succeed with no type/Svelte errors) plus the manual observation noted per task. Do **not** add a test runner.
- **Commit cadence:** one commit per task (after its tests pass / build succeeds). Use the message shown in each task's final step.
- **All paths are relative to repo root** `/Users/alexanderbutler/code_projects/personal/agent-loom` unless absolute.

## File Structure

**Backend (`loom-mill/src/loom_mill/shaping/`):**
- `models.py` — extend `CanvasNodeType` with `FRAMING`, `TENSION`, `DECISION`.
- `serialize.py` *(new)* — `serialize_graph(state)` full-graph + staging text view.
- `parser.py` — parse new node types + structured ops (`continue`, `supersede`, `edit-staged`, `discard-staged`, `revise`).
- `engine.py` — feed serialized graph to prompt; apply ops; phase retune; stream decision step.
- `prompts.py` — new node-type docs, op docs, phase-aware disposition.
- `staging.py` — `consolidate()` helper used by the `supersede` op.

**Backend API (`loom-mill/src/loom_mill/api/shaping.py`):** new `advance_stream` event already flows through the store; add a `consolidate` endpoint for the frontend "Ask agent to consolidate" button.

**Frontend (`loom-mill/frontend/src/lib/`):**
- `design/canvas/layout.ts` — replace with width-aware layered tree.
- `design/canvas/ShapingCanvas.svelte` — elbow edges, new node-type rendering, thinking-stream region, render context-peek + consolidate wiring.
- `design/canvas/RecordNode.svelte` — compact card + open-modal (reuse modal pattern).
- `design/canvas/RecordModal.svelte` *(new)* — full document modal.
- `design/canvas/FramingNode.svelte`, `TensionNode.svelte`, `DecisionNode.svelte` *(new)* — intent-coded node components.
- `design/canvas/ContextPeekPanel.svelte` *(new)* — context.md + last-prompt-slice viewer.
- `design/StagingPanel.svelte` — discard/edit controls + multi-select consolidate.
- `ws.svelte.ts` — handle `shaping:advance_stream`.
- `types.ts` — extend node-type union.

---

## PHASE 1 — Keystone: graph-aware agent

### Task 1: Add new node types to the backend enum

**Files:**
- Modify: `loom-mill/src/loom_mill/shaping/models.py:16-24`
- Test: `loom-mill/tests/test_shaping_models.py` (new)

- [ ] **Step 1: Write the failing test**

Create `loom-mill/tests/test_shaping_models.py`:

```python
from __future__ import annotations

from loom_mill.shaping.models import CanvasNodeType


def test_new_intent_node_types_exist() -> None:
    assert CanvasNodeType.FRAMING == "framing"
    assert CanvasNodeType.TENSION == "tension"
    assert CanvasNodeType.DECISION == "decision"


def test_existing_node_types_unchanged() -> None:
    assert CanvasNodeType.OBSERVATION == "observation"
    assert CanvasNodeType.RECORD == "record"
    assert CanvasNodeType.OPTION_GROUP == "option_group"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd loom-mill && uv run pytest tests/test_shaping_models.py -v`
Expected: FAIL with `AttributeError: FRAMING`

- [ ] **Step 3: Add the enum members**

In `models.py`, extend `CanvasNodeType` (insert after `OBSERVATION = "observation"`):

```python
class CanvasNodeType(StrEnum):
    INPUT = "input"
    PROCESSING = "processing"
    QUESTION = "question"
    OBSERVATION = "observation"
    FRAMING = "framing"
    TENSION = "tension"
    DECISION = "decision"
    OPTION_GROUP = "option_group"
    OPTION = "option"
    RECORD = "record"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd loom-mill && uv run pytest tests/test_shaping_models.py -v`
Expected: PASS (2 passed)

- [ ] **Step 5: Commit**

```bash
git add loom-mill/src/loom_mill/shaping/models.py loom-mill/tests/test_shaping_models.py
git commit -m "feat(mill): add FRAMING/TENSION/DECISION node types"
```

---

### Task 2: Serialize the full graph + staging area

**Files:**
- Create: `loom-mill/src/loom_mill/shaping/serialize.py`
- Test: `loom-mill/tests/test_shaping_serialize.py` (new)

- [ ] **Step 1: Write the failing test**

Create `loom-mill/tests/test_shaping_serialize.py`:

```python
from __future__ import annotations

from loom_mill.shaping.models import (
    CanvasEdge,
    CanvasNode,
    CanvasNodeType,
    NodeStatus,
    SessionPhase,
    SessionState,
    StagedRecord,
)
from loom_mill.shaping.serialize import serialize_graph


def _node(node_id, node_type, parent_id, text, status=NodeStatus.ACTIVE):
    return CanvasNode(
        id=node_id,
        type=node_type,
        parent_id=parent_id,
        status=status,
        content={"text": text} if node_type == CanvasNodeType.INPUT else {"observation": text},
        position=None,
        timestamp="2026-05-31T00:00:00+00:00",
    )


def _state() -> SessionState:
    root = _node("n1", CanvasNodeType.INPUT, None, "build a graph feature")
    obs = _node("n2", CanvasNodeType.OBSERVATION, "n1", "uses d3-force")
    dead = _node("n3", CanvasNodeType.OBSERVATION, "n1", "rejected path", status=NodeStatus.DEAD)
    state = SessionState(
        id="s1",
        phase=SessionPhase.EXPLORING,
        created_at="t",
        updated_at="t",
        nodes={"n1": root, "n2": obs, "n3": dead},
        edges=[CanvasEdge(id="e1", source_id="n1", target_id="n2", type="causal")],
        staged_records=[
            StagedRecord(
                temp_id="temp:specs:graph-view",
                surface="specs",
                title="Graph View",
                content="# Graph View\n\nLong body...",
                branch="main",
                status="proposed",
                proposed_at="t",
            )
        ],
    )
    return state


def test_serialize_includes_all_active_nodes_with_ids_types_status() -> None:
    text = serialize_graph(_state())
    assert "n1" in text and "input" in text
    assert "n2" in text and "observation" in text
    assert "uses d3-force" in text


def test_serialize_marks_dead_nodes() -> None:
    text = serialize_graph(_state())
    assert "n3" in text
    assert "dead" in text


def test_serialize_includes_staging_area_with_temp_ids() -> None:
    text = serialize_graph(_state())
    assert "Staging Area" in text
    assert "temp:specs:graph-view" in text
    assert "specs" in text
    assert "Graph View" in text


def test_serialize_includes_parent_edges() -> None:
    text = serialize_graph(_state())
    # n2's line should reference its parent n1
    assert "parent=n1" in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd loom-mill && uv run pytest tests/test_shaping_serialize.py -v`
Expected: FAIL with `ModuleNotFoundError: loom_mill.shaping.serialize`

- [ ] **Step 3: Write the serializer**

Create `loom-mill/src/loom_mill/shaping/serialize.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd loom-mill && uv run pytest tests/test_shaping_serialize.py -v`
Expected: PASS (4 passed)

- [ ] **Step 5: Commit**

```bash
git add loom-mill/src/loom_mill/shaping/serialize.py loom-mill/tests/test_shaping_serialize.py
git commit -m "feat(mill): serialize full graph + staging area for shaping prompt"
```

---

### Task 3: Parse structured mutation ops

**Files:**
- Modify: `loom-mill/src/loom_mill/shaping/parser.py`
- Test: `loom-mill/tests/test_shaping_ops_parser.py` (new)

The agent emits ops as self-closing tags alongside nodes, e.g.
`<op kind="supersede" targets="temp:specs:a,temp:specs:b"/>`,
`<op kind="continue" from="n2"/>`, `<op kind="discard-staged" temp_id="temp:specs:a"/>`,
`<op kind="edit-staged" temp_id="temp:specs:a"/>`, `<op kind="revise" node="n5"/>`.
A `continue` / `revise` op pairs with the nodes that follow in the same response;
`supersede` pairs with the single `record` node in the same response.

- [ ] **Step 1: Write the failing test**

Create `loom-mill/tests/test_shaping_ops_parser.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd loom-mill && uv run pytest tests/test_shaping_ops_parser.py -v`
Expected: FAIL with `AttributeError: 'ParsedResponse' object has no attribute 'ops'`

- [ ] **Step 3: Add op parsing**

In `parser.py`, add the `ParsedOp` dataclass after `ParsedNode` (around line 16):

```python
@dataclass
class ParsedOp:
    kind: str
    args: dict[str, str]
```

Add `ops` to `ParsedResponse` (replace the existing dataclass at lines 18-21):

```python
@dataclass
class ParsedResponse:
    nodes: list[ParsedNode]
    explore_goal: str | None = None
    ops: list["ParsedOp"] = field(default_factory=list)
```

Add the import for `field` at the top (line 4 currently `from dataclasses import dataclass`):

```python
from dataclasses import dataclass, field
```

Add the op regex after `_EXPLORE_RE` (line 27):

```python
_OP_RE = re.compile(r"<op\b(?P<attrs>[^>]*)/\s*>", re.IGNORECASE | re.DOTALL)
```

Add a parse helper and wire it into `parse_canvas_response`. Replace the body of `parse_canvas_response` (lines 35-44) with:

```python
def parse_canvas_response(output: str) -> ParsedResponse:
    explore_goal = _first_explore_goal(output)
    ops = _parse_ops(output)
    nodes = [_parse_node(attrs, body) for attrs, body in _node_blocks(output)]

    if not nodes and not ops and not _XML_TAG_RE.search(output):
        nodes.append(ParsedNode(type="observation", content=output.strip()))
    elif not nodes and not ops and explore_goal is None:
        nodes.append(ParsedNode(type="observation", content=output.strip()))

    return ParsedResponse(nodes=nodes, explore_goal=explore_goal, ops=ops)


def _parse_ops(output: str) -> list[ParsedOp]:
    ops: list[ParsedOp] = []
    for match in _OP_RE.finditer(output):
        attrs = _parse_attrs(match.group("attrs"))
        kind = (attrs.pop("kind", "") or "").strip().lower()
        if kind:
            ops.append(ParsedOp(kind=kind, args=attrs))
    return ops
```

Note: `_XML_TAG_RE` (line 28) already matches self-closing tags, so an op-only
response will not be treated as raw text — but the explicit `not ops` guards make
that intent clear and robust.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd loom-mill && uv run pytest tests/test_shaping_ops_parser.py tests/test_canvas_parser.py tests/test_parser.py -v`
Expected: PASS (new tests pass; existing parser tests still pass)

- [ ] **Step 5: Commit**

```bash
git add loom-mill/src/loom_mill/shaping/parser.py loom-mill/tests/test_shaping_ops_parser.py
git commit -m "feat(mill): parse structured mutation ops in shaping responses"
```

---

### Task 4: Parse new node types (framing/tension/decision)

**Files:**
- Modify: `loom-mill/src/loom_mill/shaping/parser.py:135-137` (`_normalize_type` already lowercases/dashes); engine mapping in Task 6.
- Test: `loom-mill/tests/test_shaping_ops_parser.py` (extend)

The parser already returns whatever `type` string it sees (via `_parse_node` fallthrough at line 98). We only need a test locking in that framing/tension/decision survive parsing; the engine maps them in Task 6.

- [ ] **Step 1: Write the failing test (extend the ops parser test file)**

Append to `loom-mill/tests/test_shaping_ops_parser.py`:

```python
def test_framing_tension_decision_nodes_parse() -> None:
    response = parse_canvas_response(
        '<node type="framing">Treat it as a latency problem.</node>'
        '<node type="tension">Cache vs freshness.</node>'
        '<node type="decision">Go with hierarchical layout.</node>'
    )
    types = [n.type for n in response.nodes]
    assert types == ["framing", "tension", "decision"]
```

- [ ] **Step 2: Run test to verify it passes (already supported)**

Run: `cd loom-mill && uv run pytest tests/test_shaping_ops_parser.py::test_framing_tension_decision_nodes_parse -v`
Expected: PASS (the generic `_parse_node` fallthrough already returns these types)

If it FAILS, inspect `_normalize_type` — it must not whitelist types. It currently does `value.strip().lower().replace("-", "_")`, which passes these through. No code change expected.

- [ ] **Step 3: Commit**

```bash
git add loom-mill/tests/test_shaping_ops_parser.py
git commit -m "test(mill): lock in framing/tension/decision node parsing"
```

---

### Task 5: Add `consolidate` to the staging area

**Files:**
- Modify: `loom-mill/src/loom_mill/shaping/staging.py`
- Test: `loom-mill/tests/test_shaping_staging.py` (extend)

`consolidate(targets, surface, title, content)` stages a new merged record and
discards the targets — but refuses if any target is already `accepted` (fail-closed
per spec).

- [ ] **Step 1: Write the failing test**

Append to `loom-mill/tests/test_shaping_staging.py` (match the existing fixture style in that file — it constructs a `ShapingSession` in a tmp workspace; reuse whatever helper/fixture it already defines for building a session with staged records):

```python
import pytest

from loom_mill.shaping.session import ShapingSession


def _session_with_two_specs(tmp_path) -> ShapingSession:
    session = ShapingSession.create(tmp_path, "shape a feature")
    session.staging.propose("specs", "Spec A", "# Spec A\nbody a", "main")
    session.staging.propose("specs", "Spec B", "# Spec B\nbody b", "main")
    return session


def test_consolidate_stages_merged_and_discards_targets(tmp_path) -> None:
    session = _session_with_two_specs(tmp_path)
    merged = session.staging.consolidate(
        ["temp:specs:spec-a", "temp:specs:spec-b"],
        surface="specs",
        title="Spec Combined",
        content="# Spec Combined\nmerged body",
    )
    temp_ids = {r.temp_id for r in session.state.staged_records}
    assert merged.temp_id in temp_ids
    assert "temp:specs:spec-a" not in temp_ids
    assert "temp:specs:spec-b" not in temp_ids


def test_consolidate_refuses_accepted_target(tmp_path) -> None:
    session = _session_with_two_specs(tmp_path)
    session.staging.accept("temp:specs:spec-a")
    with pytest.raises(ValueError, match="accepted"):
        session.staging.consolidate(
            ["temp:specs:spec-a", "temp:specs:spec-b"],
            surface="specs",
            title="Spec Combined",
            content="# merged",
        )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd loom-mill && uv run pytest tests/test_shaping_staging.py::test_consolidate_stages_merged_and_discards_targets -v`
Expected: FAIL with `AttributeError: 'StagingArea' object has no attribute 'consolidate'`

- [ ] **Step 3: Implement `consolidate`**

In `staging.py`, add this method to `StagingArea` (after `reject`, around line 70):

```python
    def consolidate(self, targets: list[str], surface: str, title: str, content: str) -> StagedRecord:
        records = [self._find(temp_id) for temp_id in targets]
        for record in records:
            if record.status == "accepted":
                raise ValueError(f"Cannot consolidate accepted record {record.temp_id}")
        branch = records[0].branch if records else self.session.state.active_branch
        merged = self.propose(surface, title, content, branch)
        for temp_id in targets:
            if temp_id != merged.temp_id:
                self.reject(temp_id)
        return merged
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd loom-mill && uv run pytest tests/test_shaping_staging.py -v`
Expected: PASS (new + existing staging tests)

- [ ] **Step 5: Commit**

```bash
git add loom-mill/src/loom_mill/shaping/staging.py loom-mill/tests/test_shaping_staging.py
git commit -m "feat(mill): staging consolidate() merges records, fails closed on accepted"
```

---

### Task 6: Map new node types + apply ops in the engine

**Files:**
- Modify: `loom-mill/src/loom_mill/shaping/engine.py` (`_node_from_parsed_node:188-195`, `_content_from_parsed_node:208-231`, `_advance_from:65-105`)
- Test: `loom-mill/tests/test_shaping_engine.py` (extend)

- [ ] **Step 1: Write the failing test**

Append to `loom-mill/tests/test_shaping_engine.py` (reuse the file's existing fixtures for building an engine with a stubbed harness response; the file already constructs `ShapingEngine` with a fake orchestrator/decision — mirror that). Two behaviors to lock in:

```python
import pytest

from loom_mill.shaping.models import CanvasNodeType, NodeStatus


@pytest.mark.asyncio
async def test_advance_maps_tension_node_type(engine_with_response):
    # engine_with_response: helper from this test file that stubs the decision
    # output and returns the engine. See existing tests for its exact name; if it
    # differs, adapt. Stub the harness to return a tension node.
    engine = engine_with_response('<node type="tension">Cache vs freshness.</node>')
    nodes = await engine.advance()
    assert nodes[0].type == CanvasNodeType.TENSION


@pytest.mark.asyncio
async def test_advance_applies_discard_staged_op(engine_factory):
    # engine_factory: helper that builds an engine on a session; adapt to the
    # file's actual helper. Pre-stage a record, then stub a discard op.
    engine = engine_factory()
    engine.session.staging.propose("specs", "Doomed", "# doomed", "main")
    engine._stub_decision('<op kind="discard-staged" temp_id="temp:specs:doomed"/>')
    await engine.advance()
    temp_ids = {r.temp_id for r in engine.session.state.staged_records}
    assert "temp:specs:doomed" not in temp_ids
```

> If `test_shaping_engine.py` does not already expose reusable fixtures/helpers, first read the file and add minimal module-level helpers (`engine_factory`, `engine_with_response`, and a `_stub_decision` monkeypatch on `_decide_next_action`) following the patterns already used there. Keep helpers in the test file, not in `src`.

- [ ] **Step 2: Run test to verify it fails**

Run: `cd loom-mill && uv run pytest tests/test_shaping_engine.py -k "tension or discard_staged" -v`
Expected: FAIL — tension maps to `OBSERVATION` (default), and discard op is ignored.

- [ ] **Step 3a: Map the new node types**

In `engine.py`, extend the mapping dict in `_node_from_parsed_node` (lines 189-194):

```python
        node_type = {
            "question": CanvasNodeType.QUESTION,
            "observation": CanvasNodeType.OBSERVATION,
            "framing": CanvasNodeType.FRAMING,
            "tension": CanvasNodeType.TENSION,
            "decision": CanvasNodeType.DECISION,
            "record": CanvasNodeType.RECORD,
            "option_group": CanvasNodeType.OPTION_GROUP,
        }.get(parsed_node.type, CanvasNodeType.OBSERVATION)
```

In `_content_from_parsed_node` (lines 208-231), the generic fallthrough at line 231 already returns `{"observation": ...}`. Add framing/tension/decision branches before the final return so their content key matches its type:

```python
        if parsed_node.type in ("framing", "tension", "decision"):
            return {parsed_node.type: parsed_node.content or "", "evidence": None}
```

- [ ] **Step 3b: Apply ops in `_advance_from`**

In `engine.py`, after computing `response` (line 75) and before the explore-only
early return, add op application. Insert a new method and call it:

Add the call right after `response = await self._decide_next_action(...)` (line 75):

```python
        op_nodes = await self._apply_ops(response.ops, response.nodes, parent_id)
```

Then change the `continue`/`supersede` semantics: ops that consume the response's
record/nodes set a flag so we don't double-add. Implement `_apply_ops`:

```python
    async def _apply_ops(self, ops, parsed_nodes, parent_id):
        """Apply structured mutation ops. Returns nodes created as a side effect.

        Fail-closed: an op referencing an unknown/stale/accepted target is dropped
        and an OBSERVATION explaining why is emitted instead of mutating wrongly.
        """
        created = []
        for op in ops:
            try:
                if op.kind == "discard-staged":
                    self.session.staging.reject(op.args["temp_id"])
                elif op.kind == "edit-staged":
                    # content/title come from the paired record node if present
                    record = next((n for n in parsed_nodes if n.type == "record"), None)
                    if record is None:
                        raise ValueError("edit-staged requires a paired record node")
                    self.session.staging.update(
                        op.args["temp_id"],
                        content=record.content,
                        title=record.title,
                    )
                elif op.kind == "supersede":
                    record = next((n for n in parsed_nodes if n.type == "record"), None)
                    if record is None:
                        raise ValueError("supersede requires a paired record node")
                    targets = [t.strip() for t in op.args.get("targets", "").split(",") if t.strip()]
                    self.session.staging.consolidate(
                        targets,
                        surface=record.surface or "specs",
                        title=record.title or "Consolidated record",
                        content=record.content,
                    )
                # continue/revise affect where subsequent nodes attach; handled
                # by the caller via _resolve_parent_for_ops.
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
```

Because `supersede`/`edit-staged` consume the record node, skip re-adding it in the
node loop. Add a guard at the top of the `for parsed_node in response.nodes:` loop
(line 83):

```python
        consuming_ops = {op.kind for op in response.ops} & {"supersede", "edit-staged"}
        for parsed_node in response.nodes:
            if parsed_node.type == "record" and consuming_ops:
                continue
            ...
```

For `continue`/`revise`, override `parent_id` for the node loop when present:

```python
        for op in response.ops:
            if op.kind == "continue" and op.args.get("from") in self.session.state.nodes:
                parent_id = op.args["from"]
            elif op.kind == "revise" and op.args.get("node") in self.session.state.nodes:
                # mark the node's subtree stale, then attach fresh nodes under it
                self.session.invalidate_nodes(
                    [n.id for n in self.session.state.nodes.values() if n.parent_id == op.args["node"]]
                )
                parent_id = op.args["node"]
```

Place this `continue`/`revise` parent-resolution block immediately before the node
loop. Finally, return `nodes + op_nodes` instead of just `nodes` (line 105):

```python
        return nodes + op_nodes
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd loom-mill && uv run pytest tests/test_shaping_engine.py -v`
Expected: PASS (tension maps correctly; discard op removes the staged record)

- [ ] **Step 5: Commit**

```bash
git add loom-mill/src/loom_mill/shaping/engine.py loom-mill/tests/test_shaping_engine.py
git commit -m "feat(mill): map intent node types and apply structured ops in engine"
```

---

### Task 7: Feed the serialized graph to the prompt + disposition shift

**Files:**
- Modify: `loom-mill/src/loom_mill/shaping/engine.py:73-75,156-162`, `loom-mill/src/loom_mill/shaping/prompts.py`
- Test: `loom-mill/tests/test_shaping_prompts.py` (new)

- [ ] **Step 1: Write the failing test**

Create `loom-mill/tests/test_shaping_prompts.py`:

```python
from __future__ import annotations

from loom_mill.shaping.prompts import build_canvas_prompt


def test_prompt_documents_new_node_types() -> None:
    prompt = build_canvas_prompt("ctx", "graph-text", [], "exploring")
    assert "framing" in prompt.lower()
    assert "tension" in prompt.lower()
    assert "decision" in prompt.lower()


def test_prompt_documents_ops() -> None:
    prompt = build_canvas_prompt("ctx", "graph-text", [], "exploring")
    assert "supersede" in prompt.lower()
    assert "continue" in prompt.lower()


def test_prompt_includes_graph_view() -> None:
    prompt = build_canvas_prompt("ctx", "GRAPH-SENTINEL", [], "exploring")
    assert "GRAPH-SENTINEL" in prompt


def test_exploring_phase_disposition_favors_branching() -> None:
    prompt = build_canvas_prompt("ctx", "g", [], "exploring")
    assert "branch" in prompt.lower()
    # Must NOT carry the old "as quickly as certainty allows" funnel bias verbatim.
    assert "as quickly as certainty allows" not in prompt
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd loom-mill && uv run pytest tests/test_shaping_prompts.py -v`
Expected: FAIL — `build_canvas_prompt` takes 3 args, not 4, and lacks the new content.

- [ ] **Step 3: Update `build_canvas_prompt`**

In `prompts.py`, change the signature (line 6) to accept the serialized graph and
make disposition phase-aware. Replace lines 6-21 with:

```python
def build_canvas_prompt(context: str, graph_view: str, recent_nodes: list[CanvasNode], phase: str) -> str:
    context_excerpt = context[-8000:] if context else "(no context yet)"
    history = format_node_history(recent_nodes)
    phase_value = getattr(phase, "value", phase)
    disposition = _disposition_for_phase(str(phase_value))
    return f"""You are a shaping agent in a Loom session. Your job is to help the operator shape fuzzy intent into concrete Loom records (tickets, specs, plans, research) using a branching canvas.

## Current Phase: {phase_value}

## Disposition
{disposition}

## Internal Context Document
{context_excerpt}

## Current Canvas Graph (all nodes, statuses, and the staging area)
{graph_view}

## Recent Path
{history}

## Response Format
Respond with XML-like nodes and optional mutation ops. Multiple nodes in one response are allowed and encouraged when they help the canvas branch. Output only the nodes/ops and optional exploration request; do not wrap the response in Markdown fences.
"""
```

Then, in the body section of the prompt (the part documenting node types, currently
lines 22-112), add documentation for the three new node types and the ops. Insert
after the Observation Node block (after line 29) the following blocks:

```python
```

Concretely, edit the long docstring to include these sections (add them before
`### Record Proposal Node`):

```
### Framing Node
Use a framing node to name a distinct lens on the problem. Framings invite parallel exploration; emit two or three competing framings early rather than committing immediately.

<node type="framing">Treat the canvas as a latency problem: the bottleneck is render time, not model quality.</node>

### Tension Node
Use a tension node for a contradiction, risk, or constraint that should stay open rather than be resolved away. A tension is an invitation to continue, not a dead end.

<node type="tension">Operators want full document context on the canvas, but full inline documents make the canvas unreadable.</node>

### Decision Node
Use a decision node when a choice is resolved and branches should be pruned. A decision marks convergence.

<node type="decision">Use a layered tree layout with orthogonal edges; the force-directed option is rejected for legibility.</node>

### Mutation Ops
You can see the full graph and staging area above. Mutate them with self-closing ops:

- Continue from any existing node (including an observation or tension):
  <op kind="continue" from="<node_id>"/> followed by the new nodes.
- Consolidate duplicate staged records into one (pair with a single record node):
  <op kind="supersede" targets="temp:specs:a,temp:specs:b"/>
  <node type="record" surface="specs" title="Merged">...full markdown...</node>
- Rewrite one staged record (pair with a record node carrying the new content):
  <op kind="edit-staged" temp_id="temp:specs:a"/>
  <node type="record" surface="specs" title="Spec A">...</node>
- Drop a staged record: <op kind="discard-staged" temp_id="temp:specs:a"/>
- Revise a prior node's subtree: <op kind="revise" node="<node_id>"/> followed by replacement nodes.

Use these to keep the graph coherent: when two staged records cover the same thing, supersede them; when a thread ended in an observation that should continue, continue from it.
```

Replace the final guideline line (line 111, `- Move toward proposing records as
quickly as certainty allows.`) with:

```
- Branch and surface tensions while exploring and narrowing. Converge to decisions and records when the operator signals readiness or certainty is genuinely high — do not rush to records.
```

Add the `_disposition_for_phase` helper at the end of the file:

```python
def _disposition_for_phase(phase: str) -> str:
    if phase in ("exploring", "narrowing"):
        return (
            "You are in divergent mode. Prefer framing and tension nodes, options, and one "
            "focused question at a time. Branch the canvas. Do not propose records yet unless "
            "the operator has clearly signalled readiness."
        )
    return (
        "You are in convergent mode. Resolve open tensions into decisions and propose complete, "
        "coherent records. Consolidate duplicate staged records with the supersede op."
    )
```

- [ ] **Step 4a: Wire the serialized graph into the engine**

In `engine.py`, import the serializer (top, after line 13):

```python
from .serialize import serialize_graph
```

Update `_decide_next_action` (lines 156-162) to take and pass the graph view:

```python
    async def _decide_next_action(
        self,
        context: str,
        graph_view: str,
        recent_nodes: list[CanvasNode],
        phase: SessionPhase,
    ) -> ParsedResponse:
        prompt = build_canvas_prompt(context, graph_view, recent_nodes, phase)
```

Update the call site in `_advance_from` (line 75):

```python
        graph_view = serialize_graph(self.session.state)
        response = await self._decide_next_action(context, graph_view, recent_nodes, self.session.state.phase)
```

- [ ] **Step 4b: Run tests**

Run: `cd loom-mill && uv run pytest tests/test_shaping_prompts.py tests/test_shaping_engine.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add loom-mill/src/loom_mill/shaping/prompts.py loom-mill/src/loom_mill/shaping/engine.py loom-mill/tests/test_shaping_prompts.py
git commit -m "feat(mill): feed full graph to prompt, document ops, divergent disposition"
```

---

### Task 8: Retune the phase machine for divergent-first

**Files:**
- Modify: `loom-mill/src/loom_mill/shaping/engine.py:242-246`
- Test: `loom-mill/tests/test_shaping_engine.py` (extend)

Today `EXPLORING → NARROWING` triggers on the first QUESTION. With divergent-first,
a FRAMING or TENSION node is the more natural early signal, and we must not push to
PROPOSING just because a record appeared if the operator hasn't engaged.

- [ ] **Step 1: Write the failing test**

Append to `loom-mill/tests/test_shaping_engine.py`:

```python
@pytest.mark.asyncio
async def test_framing_node_does_not_force_narrowing(engine_factory):
    engine = engine_factory()  # starts in EXPLORING
    engine._stub_decision('<node type="framing">A lens.</node>')
    await engine.advance()
    from loom_mill.shaping.models import SessionPhase
    assert engine.session.state.phase == SessionPhase.EXPLORING


@pytest.mark.asyncio
async def test_question_still_transitions_to_narrowing(engine_factory):
    engine = engine_factory()
    engine._stub_decision('<node type="question">Which path?</node>')
    await engine.advance()
    from loom_mill.shaping.models import SessionPhase
    assert engine.session.state.phase == SessionPhase.NARROWING
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd loom-mill && uv run pytest tests/test_shaping_engine.py -k "framing_node_does_not or question_still" -v`
Expected: the framing test may already pass (framing isn't QUESTION); the second should pass too. If both pass, this task is a no-op confirmation — proceed to Step 4. If the framing test FAILS (because some code transitions on any non-input node), fix in Step 3.

- [ ] **Step 3: Confirm/adjust `_transition_after_node`**

The current logic (lines 242-246) only transitions on QUESTION and RECORD, so
framing/tension/decision correctly do not force a transition. No change required
unless Step 2 surfaced an issue. If it did, ensure the method reads exactly:

```python
    async def _transition_after_node(self, node: CanvasNode) -> None:
        if self.session.state.phase == SessionPhase.EXPLORING and node.type == CanvasNodeType.QUESTION:
            await self._update_phase(SessionPhase.NARROWING)
        elif node.type == CanvasNodeType.RECORD and self.session.state.phase != SessionPhase.REFINING:
            await self._update_phase(SessionPhase.PROPOSING)
```

- [ ] **Step 4: Run tests**

Run: `cd loom-mill && uv run pytest tests/test_shaping_engine.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add loom-mill/tests/test_shaping_engine.py loom-mill/src/loom_mill/shaping/engine.py
git commit -m "test(mill): divergent node types do not force phase transitions"
```

---

## PHASE 2 — Staging control API + consolidate endpoint

### Task 9: Add a `consolidate` API endpoint

**Files:**
- Modify: `loom-mill/src/loom_mill/api/shaping.py` (add handler after `delete_staged_record`, line 467)
- Modify: `loom-mill/src/loom_mill/app.py` (import the handler at line 13; register the route in the route list at lines 96-99)
- Test: `loom-mill/tests/test_design_api.py` (extend)

The shaping routes are registered in `app.py` (lines 87-105), and the handler names
are imported in the `from loom_mill.api.shaping import ...` statement at line 13.
You will edit both.

- [ ] **Step 1: Confirm the route table**

Run: `cd loom-mill && sed -n '96,99p' src/loom_mill/app.py`
Expected: the existing `/staged`, `/staged/{temp_id}` (PUT, DELETE), and
`/staged/{temp_id}/accept` routes. You will add `/staged/consolidate` **above** the
`/staged/{temp_id}` lines so the literal path is matched before the param route.

- [ ] **Step 2: Write the failing test**

Append to `loom-mill/tests/test_design_api.py` (reuse the file's existing test
client fixture and session-creation helper — it already exercises
create/advance/staged endpoints; mirror that style):

```python
def test_consolidate_endpoint_merges_two_staged(client, created_session):
    sid = created_session
    client.post(f"/shaping/sessions/{sid}/staged", json={"surface": "specs", "title": "Spec A", "content": "# A"})
    client.post(f"/shaping/sessions/{sid}/staged", json={"surface": "specs", "title": "Spec B", "content": "# B"})
    resp = client.post(
        f"/shaping/sessions/{sid}/staged/consolidate",
        json={
            "targets": ["temp:specs:spec-a", "temp:specs:spec-b"],
            "surface": "specs",
            "title": "Spec Combined",
            "content": "# Combined",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    temp_ids = {r["temp_id"] for r in body["staged_records"]}
    assert "temp:specs:spec-combined" in temp_ids
    assert "temp:specs:spec-a" not in temp_ids
```

> If `test_design_api.py`'s fixtures are named differently, adapt `client`/`created_session` to the actual fixtures after reading the file. The endpoint must return the updated staged list under `staged_records`.

- [ ] **Step 3: Run test to verify it fails**

Run: `cd loom-mill && uv run pytest tests/test_design_api.py -k consolidate -v`
Expected: FAIL with 404 (route not registered)

- [ ] **Step 4: Implement the handler**

In `api/shaping.py`, add after `delete_staged_record` (line 467):

```python
async def consolidate_staged_records(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    if session.state.ended_at is not None:
        return JSONResponse({"error": "Session has ended"}, status_code=409)
    try:
        body = await _json_body(request)
        targets = body["targets"]
        surface = body["surface"]
        title = body["title"]
        content = body["content"]
        if not isinstance(targets, list) or len(targets) < 2:
            raise ValueError("targets must be a list of at least two temp_ids")
        if not isinstance(surface, str) or not surface.strip():
            raise ValueError("surface must be a non-empty string")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        if not isinstance(content, str):
            raise ValueError("content must be a string")
        session.staging.consolidate([str(t) for t in targets], surface.strip(), title.strip(), content)
    except (KeyError, ValueError) as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    return JSONResponse({"session_id": session.session_id, "staged_records": [asdict(r) for r in session.state.staged_records]})
```

Then register it in `app.py`. First add `consolidate_staged_records` to the import
list at line 13 (the `from loom_mill.api.shaping import ...` statement). Then insert
the route in the route list **immediately after** the `/staged` POST route (line 96)
and **before** the `/staged/{temp_id}` routes (lines 97-98), so Starlette matches the
literal `consolidate` path before the `{temp_id}` param route:

```python
            Route("/shaping/sessions/{session_id}/staged/consolidate", consolidate_staged_records, methods=["POST"]),
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd loom-mill && uv run pytest tests/test_design_api.py -k consolidate -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add loom-mill/src/loom_mill/api/shaping.py loom-mill/tests/test_design_api.py
git commit -m "feat(mill): POST /staged/consolidate endpoint"
```

---

## PHASE 3 — Transparency

### Task 10: Stream the decision step as a thinking trace

**Files:**
- Modify: `loom-mill/src/loom_mill/shaping/engine.py:156-186` (`_decide_next_action`)
- Test: `loom-mill/tests/test_shaping_engine.py` (extend)

- [ ] **Step 1: Write the failing test**

Append to `loom-mill/tests/test_shaping_engine.py`:

```python
@pytest.mark.asyncio
async def test_decision_step_publishes_advance_stream(engine_factory, captured_events):
    # captured_events: helper that records ShapingEvents published to the store.
    # Adapt to the file's existing store/event-capture fixture.
    engine = engine_factory()
    engine._stub_decision_streaming("thinking line 1\n", '<node type="observation">done</node>')
    await engine.advance()
    stream_events = [e for e in captured_events() if e.event == "advance_stream"]
    assert stream_events
    assert any("thinking line 1" in e.data.get("delta", "") for e in stream_events)
```

> Add `_stub_decision_streaming(stream_text, final_output)` to the test helpers: it
> should monkeypatch `run_bounded_invocation` so the `on_stream` callback is invoked
> with `stream_text` and the result `.output` is `final_output`. Model it on how the
> existing engine tests stub the harness.

- [ ] **Step 2: Run test to verify it fails**

Run: `cd loom-mill && uv run pytest tests/test_shaping_engine.py -k advance_stream -v`
Expected: FAIL — no `advance_stream` events are published (decision passes `on_stream=None`).

- [ ] **Step 3: Add streaming to the decision call**

In `engine.py` `_decide_next_action` (lines 172-178), replace the
`run_bounded_invocation` call to supply an `on_stream` callback:

```python
        async def on_stream(line: str) -> None:
            await self.store.publish(
                ShapingEvent(
                    session_id=self.session.session_id,
                    event="advance_stream",
                    data={"delta": line},
                )
            )

        try:
            result = await run_bounded_invocation(
                config,
                invocation_id=f"decision-{uuid4().hex[:8]}",
                on_stream=on_stream,
                prompt_override=prompt,
            )
        except Exception as error:
            return ParsedResponse(nodes=[ParsedNode(type="observation", content=f"Decision harness failed: {error}")])
```

(The `ShapingEvent` import already exists at line 8.)

- [ ] **Step 4: Run test to verify it passes**

Run: `cd loom-mill && uv run pytest tests/test_shaping_engine.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add loom-mill/src/loom_mill/shaping/engine.py loom-mill/tests/test_shaping_engine.py
git commit -m "feat(mill): stream decision-step reasoning as advance_stream events"
```

---

### Task 11: Handle `advance_stream` in the WebSocket client

**Files:**
- Modify: `loom-mill/frontend/src/lib/ws.svelte.ts:328-346`
- Verify: `cd loom-mill/frontend && npm run build`

- [ ] **Step 1: Read the existing advance handlers**

Read `loom-mill/frontend/src/lib/ws.svelte.ts` lines 320-350 to see the
`store.shapingThinking` / advance-state shape used by `advance_started` /
`advance_completed`. Note the exact state field names they set.

- [ ] **Step 2: Add the `advance_stream` case**

In the `switch` (after the `advance_started` case near line 333), add:

```typescript
      case 'shaping:advance_stream': {
        const delta = msg.data?.delta ?? '';
        store.shapingThinking = (store.shapingThinking ?? '') + delta;
        break;
      }
```

In the `advance_started` case, reset the buffer:

```typescript
      case 'shaping:advance_started':
        store.advancing = true;
        store.shapingThinking = '';
        break;
```

Declare `shapingThinking` on the store object (find the store state declaration near
the top of the file where `advancing` is declared) and add:

```typescript
  shapingThinking: '' as string,
```

- [ ] **Step 3: Verify build**

Run: `cd loom-mill/frontend && npm run build`
Expected: build succeeds, no TS/Svelte errors.

- [ ] **Step 4: Commit**

```bash
git add loom-mill/frontend/src/lib/ws.svelte.ts
git commit -m "feat(mill): buffer decision thinking stream in ws store"
```

---

### Task 12: Render the thinking-stream region on the canvas

**Files:**
- Modify: `loom-mill/frontend/src/lib/design/canvas/ShapingCanvas.svelte`
- Verify: build + manual observation

- [ ] **Step 1: Add a dismissible thinking panel**

In `ShapingCanvas.svelte`, add a derived value near the other `$derived` decls:

```typescript
  let thinking = $derived(store.shapingThinking ?? '');
```

Add markup inside the canvas container (above `<Svelvet ...>` or as an overlay),
shown only while advancing and there is thinking text:

```svelte
{#if advancing && thinking}
  <div class="absolute bottom-4 left-4 z-20 max-w-[420px] max-h-[40vh] overflow-auto
    bg-bg-surface/95 border border-border-default rounded-lg shadow-lg p-3 text-[11px]
    font-mono text-text-secondary whitespace-pre-wrap">
    <div class="text-[10px] uppercase tracking-wider text-text-tertiary mb-1">Thinking…</div>
    {thinking}
  </div>
{/if}
```

- [ ] **Step 2: Verify build**

Run: `cd loom-mill/frontend && npm run build`
Expected: build succeeds.

- [ ] **Step 3: Manual observation**

Per `AGENTS.md` Mill dev-server rules, run the dev server, open the Design Room,
start a shaping session, and confirm a "Thinking…" panel appears with streaming
text during an advance and disappears when it completes. Capture a screenshot.

- [ ] **Step 4: Commit**

```bash
git add loom-mill/frontend/src/lib/design/canvas/ShapingCanvas.svelte
git commit -m "feat(mill): show live decision thinking stream on canvas"
```

---

### Task 13: Add a context-peek panel

**Files:**
- Create: `loom-mill/frontend/src/lib/design/canvas/ContextPeekPanel.svelte`
- Modify: `loom-mill/frontend/src/lib/design/canvas/ShapingCanvas.svelte` (toggle + mount)
- Backend: a `GET /shaping/sessions/{id}/context` route already exists (`get_shaping_context`, `api/shaping.py:153`).
- Verify: build + manual observation

- [ ] **Step 1: Create the panel component**

Create `ContextPeekPanel.svelte`:

```svelte
<script lang="ts">
  import { apiUrl } from '../../api';

  let { sessionId }: { sessionId: string } = $props();

  let open = $state(false);
  let context = $state('');
  let loading = $state(false);

  async function load() {
    loading = true;
    try {
      const resp = await fetch(apiUrl(`/shaping/sessions/${sessionId}/context`));
      if (resp.ok) {
        const body = await resp.json();
        context = body.context ?? body.content ?? '';
      }
    } finally {
      loading = false;
    }
  }

  function toggle() {
    open = !open;
    if (open) load();
  }
</script>

<button
  class="absolute top-4 left-4 z-20 px-3 py-1.5 text-[11px] rounded border border-border-default
    bg-bg-surface text-text-secondary hover:text-text-primary"
  onclick={toggle}
>
  {open ? 'Hide context' : 'Context'}
</button>

{#if open}
  <div class="absolute top-14 left-4 z-20 w-[420px] max-h-[60vh] overflow-auto
    bg-bg-surface border border-border-default rounded-lg shadow-lg p-3">
    <div class="text-[10px] uppercase tracking-wider text-text-tertiary mb-2">Context document</div>
    {#if loading}
      <div class="text-[11px] text-text-tertiary">Loading…</div>
    {:else}
      <pre class="text-[11px] font-mono text-text-secondary whitespace-pre-wrap break-words">{context}</pre>
    {/if}
  </div>
{/if}
```

> Confirm the `get_shaping_context` JSON key by reading `api/shaping.py:153-160`;
> set the fallback in `body.context ?? body.content` to match the actual key.

- [ ] **Step 2: Mount it in the canvas**

In `ShapingCanvas.svelte`, import and render the panel inside the canvas container:

```svelte
  import ContextPeekPanel from './ContextPeekPanel.svelte';
```

```svelte
<ContextPeekPanel {sessionId} />
```

- [ ] **Step 3: Verify build**

Run: `cd loom-mill/frontend && npm run build`
Expected: build succeeds.

- [ ] **Step 4: Manual observation**

Open a session, click "Context", confirm the context document renders and scrolls.
Screenshot it.

- [ ] **Step 5: Commit**

```bash
git add loom-mill/frontend/src/lib/design/canvas/ContextPeekPanel.svelte loom-mill/frontend/src/lib/design/canvas/ShapingCanvas.svelte
git commit -m "feat(mill): context-peek panel exposes the shaping context document"
```

---

## PHASE 3 (parallel) — Canvas legibility

### Task 14: Width-aware layered-tree layout

**Files:**
- Modify: `loom-mill/frontend/src/lib/design/canvas/layout.ts`
- Verify: build + manual observation

- [ ] **Step 1: Replace the X-assignment with non-overlapping slot allocation**

The current `assignX` (layout.ts:42-79) centers parents over children but uses a
single shared `nextLeafX` cursor with no per-layer collision handling, so subtrees
overlap. Replace the whole file with a tidy-tree pass that (a) lays out leaves left
to right with a fixed gap, (b) centers parents over their children's span, and
(c) shifts subtrees right to remove overlap. Full replacement:

```typescript
export interface LayoutNode {
  id: string;
  parent_id: string | null;
  position: { x: number; y: number } | null;
  status?: string;
}

export interface LayoutResult {
  positions: Record<string, { x: number; y: number }>;
}

const NODE_WIDTH = 280;
const H_GAP = 48;
const V_GAP = 150;
const Y_OFFSET = 50;
const X_ORIGIN = 400;

export function computeTreeLayout(nodes: LayoutNode[], _edges: any[]): LayoutResult {
  const positions: Record<string, { x: number; y: number }> = {};
  const childrenMap: Record<string, string[]> = {};
  const nodeMap: Record<string, LayoutNode> = {};

  nodes.forEach((n) => {
    nodeMap[n.id] = n;
    childrenMap[n.id] = [];
  });

  const roots: string[] = [];
  nodes.forEach((n) => {
    if (n.parent_id && nodeMap[n.parent_id]) {
      childrenMap[n.parent_id].push(n.id);
    } else {
      roots.push(n.id);
    }
  });

  const depths: Record<string, number> = {};
  function assignDepth(nodeId: string, depth: number) {
    depths[nodeId] = depth;
    childrenMap[nodeId].forEach((c) => assignDepth(c, depth + 1));
  }
  roots.forEach((r) => assignDepth(r, 0));

  // Post-order X assignment with a single advancing cursor for leaves.
  // Each subtree occupies a contiguous horizontal band, so siblings never overlap.
  let cursor = 0;
  const slot = NODE_WIDTH + H_GAP;

  function assignX(nodeId: string): number {
    const children = childrenMap[nodeId];
    let x: number;
    if (children.length === 0) {
      x = cursor;
      cursor += slot;
    } else {
      const childXs = children.map((c) => assignX(c));
      x = (childXs[0] + childXs[childXs.length - 1]) / 2;
    }
    positions[nodeId] = { x, y: depths[nodeId] * V_GAP + Y_OFFSET };
    return x;
  }

  roots.forEach((r) => {
    assignX(r);
    cursor += slot; // gap between separate root trees
  });

  // Honor pinned (manually dragged) positions: override after layout.
  nodes.forEach((n) => {
    if (n.position) {
      positions[n.id] = { x: n.position.x, y: n.position.y };
    }
  });

  // Shift the whole (unpinned) graph so the first root sits at X_ORIGIN.
  if (roots.length > 0 && !nodeMap[roots[0]].position) {
    const shift = X_ORIGIN - positions[roots[0]].x;
    nodes.forEach((n) => {
      if (!n.position) positions[n.id].x += shift;
    });
  }

  return { positions };
}
```

- [ ] **Step 2: Verify build**

Run: `cd loom-mill/frontend && npm run build`
Expected: build succeeds.

- [ ] **Step 3: Manual observation**

Open a session that already has branches (or create branching via a question with
options). Confirm: no node overlaps a sibling subtree, parents are centered over
children, and dragging a node still pins it. Screenshot before/after if a prior
screenshot exists.

- [ ] **Step 4: Commit**

```bash
git add loom-mill/frontend/src/lib/design/canvas/layout.ts
git commit -m "feat(mill): width-aware layered-tree layout, no sibling overlap"
```

---

### Task 15: Orthogonal (elbow) edges

**Files:**
- Modify: `loom-mill/frontend/src/lib/design/canvas/ShapingCanvas.svelte` (Svelvet `<Edge>` / anchor config)
- Verify: build + manual observation

- [ ] **Step 1: Determine how edges are currently styled**

Read `ShapingCanvas.svelte` for `<Edge`, `Anchor`, or edge `step`/`type` props.
Svelvet supports an edge `step` curve. The goal: render right-angle connectors.

- [ ] **Step 2: Apply step edges**

If the canvas renders Svelvet `<Edge>` components, set the `step` prop (rounded
orthogonal). If edges are implicit via `Anchor` connections, wrap them with an
`<Edge let:... >` using `step` and a low-contrast `color`. Concretely, for each
edge rendered, pass:

```svelte
<Edge {source} {target} step color="var(--border-default, #d8d8d8)" width={1.5} />
```

For branch (`option_group`) edges, use a distinct dashed style:

```svelte
<Edge {source} {target} step color="var(--border-subtle, #c4b5fd)" width={1.5} edgeClick={null} />
```

> Adapt prop names to the installed Svelvet version after reading the component;
> the requirement is: orthogonal/step routing, thin, low-contrast, with branch edges
> visually distinct from causal edges.

- [ ] **Step 3: Verify build**

Run: `cd loom-mill/frontend && npm run build`
Expected: build succeeds.

- [ ] **Step 4: Manual observation**

Confirm edges render as crisp right angles (not wandering beziers), stay clean at
multiple zoom levels, and branch edges look different from normal edges. Screenshot.

- [ ] **Step 5: Commit**

```bash
git add loom-mill/frontend/src/lib/design/canvas/ShapingCanvas.svelte
git commit -m "feat(mill): orthogonal elbow edges with distinct branch styling"
```

---

### Task 16: Frontend node-type union + intent-coded node components

**Files:**
- Modify: `loom-mill/frontend/src/lib/types.ts` (node-type union)
- Create: `loom-mill/frontend/src/lib/design/canvas/FramingNode.svelte`, `TensionNode.svelte`, `DecisionNode.svelte`
- Modify: `loom-mill/frontend/src/lib/design/canvas/ShapingCanvas.svelte` (render the new types)
- Verify: build + manual observation

- [ ] **Step 1: Extend the type union**

In `types.ts`, find the `CanvasNode` type/`type` field union and add
`'framing' | 'tension' | 'decision'`.

- [ ] **Step 2: Create the three components**

Model them on `ObservationNode.svelte` (read it first for the exact Svelvet `<Node>`
+ `<Anchor>` slot structure). Each differs only in label, glyph, and intent color
(purple = framing, orange = tension, green = decision). `FramingNode.svelte`:

```svelte
<script lang="ts">
  import { Node, Anchor } from 'svelvet';
  let { node, position, connections = [], highlighted = false } = $props();
  let text = $derived(node.content.framing ?? node.content.text ?? '');
</script>

<Node id={node.id} {position} let:selected>
  <div class="bg-bg-surface border border-l-4 rounded-lg p-3 min-w-[220px] max-w-[320px] shadow-sm
    border-l-purple-500 {selected ? 'ring-2 ring-accent-primary/50' : ''}
    {node.status === 'dead' ? 'opacity-40 grayscale' : ''}
    {node.status === 'stale' ? 'border-dashed opacity-60' : ''}">
    <div class="text-[9px] font-bold uppercase tracking-wider text-purple-400 mb-1">◆ Framing</div>
    <div class="text-[12px] text-text-primary whitespace-pre-wrap break-words">{text}</div>
  </div>
  <div slot="anchorNorth"><Anchor id="{node.id}-in" input /></div>
  <div slot="anchorSouth">
    {#if connections && connections.length > 0}
      <Anchor id="{node.id}-out" output {connections} />
    {:else}
      <Anchor id="{node.id}-out" output />
    {/if}
  </div>
</Node>
```

`TensionNode.svelte` — identical structure, but: label `⚠ Tension`, color
`border-l-amber-500` / `text-amber-400`, `text` from `node.content.tension`, and add
a "Continue from here" affordance (a button that calls an `onContinue` prop):

```svelte
<script lang="ts">
  import { Node, Anchor } from 'svelvet';
  let { node, position, connections = [], onContinue } = $props();
  let text = $derived(node.content.tension ?? node.content.text ?? '');
</script>

<Node id={node.id} {position} let:selected>
  <div class="bg-bg-surface border border-l-4 border-l-amber-500 rounded-lg p-3 min-w-[220px] max-w-[320px] shadow-sm
    {selected ? 'ring-2 ring-accent-primary/50' : ''}">
    <div class="text-[9px] font-bold uppercase tracking-wider text-amber-400 mb-1">⚠ Tension</div>
    <div class="text-[12px] text-text-primary whitespace-pre-wrap break-words">{text}</div>
    {#if node.status === 'active'}
      <button class="mt-2 text-[10px] text-amber-400 hover:text-amber-300"
        onclick={() => onContinue && onContinue(node.id)}>Continue from here →</button>
    {/if}
  </div>
  <div slot="anchorNorth"><Anchor id="{node.id}-in" input /></div>
  <div slot="anchorSouth">
    {#if connections && connections.length > 0}
      <Anchor id="{node.id}-out" output {connections} />
    {:else}
      <Anchor id="{node.id}-out" output />
    {/if}
  </div>
</Node>
```

`DecisionNode.svelte` — identical to `FramingNode` but label `✓ Decision`, color
`border-l-emerald-500` / `text-emerald-400`, `text` from `node.content.decision`.

- [ ] **Step 3: Render the new types in the canvas**

In `ShapingCanvas.svelte`, import the three components and add branches to whatever
construct maps `node.type` to a component (an `{#if}`/`{:else if}` chain or a
lookup). Add cases for `'framing'`, `'tension'`, `'decision'`. Wire `TensionNode`'s
`onContinue` to a handler that POSTs to the advance endpoint with the node as
parent (reuse the existing "continue from node" / advance call — observations should
get the same affordance, so also add a "Continue" control to `ObservationNode.svelte`
calling the same handler).

> Read how the existing canvas triggers an advance (it already has an advance/
> continue path used by `CanvasInputBar` or option selection). Reuse it; do not
> invent a new endpoint. The `continue` op (Task 6/7) lets the agent continue
> autonomously; this affordance lets the operator request a continue from a specific
> node.

- [ ] **Step 4: Verify build**

Run: `cd loom-mill/frontend && npm run build`
Expected: build succeeds.

- [ ] **Step 5: Manual observation**

Drive a session until framing/tension/decision nodes appear (the new prompt favors
them early). Confirm each renders with its intent color and glyph, and that
"Continue from here" on a tension/observation triggers another advance. Screenshot.

- [ ] **Step 6: Commit**

```bash
git add loom-mill/frontend/src/lib/types.ts loom-mill/frontend/src/lib/design/canvas/FramingNode.svelte loom-mill/frontend/src/lib/design/canvas/TensionNode.svelte loom-mill/frontend/src/lib/design/canvas/DecisionNode.svelte loom-mill/frontend/src/lib/design/canvas/ShapingCanvas.svelte loom-mill/frontend/src/lib/design/canvas/ObservationNode.svelte
git commit -m "feat(mill): intent-coded framing/tension/decision nodes + continue affordance"
```

---

### Task 17: Record node → compact card + document modal

**Files:**
- Create: `loom-mill/frontend/src/lib/design/canvas/RecordModal.svelte`
- Modify: `loom-mill/frontend/src/lib/design/canvas/RecordNode.svelte`
- Verify: build + manual observation

- [ ] **Step 1: Create the modal**

Create `RecordModal.svelte` (reuse the app's modal pattern — read
`ProcessingLogModal.svelte` for the existing overlay/z-index/escape approach and
mirror it):

```svelte
<script lang="ts">
  let { node, onClose, onSave } = $props();
  let editContent = $state(node.content.content ?? '');
  let saving = $state(false);
</script>

<div class="fixed inset-0 z-[1000] flex items-center justify-center bg-black/50" onclick={onClose}>
  <div class="bg-bg-surface border border-border-default rounded-lg shadow-2xl w-[720px] max-w-[92vw] max-h-[85vh] flex flex-col"
    onclick={(e) => e.stopPropagation()}>
    <div class="flex justify-between items-center p-4 border-b border-border-subtle">
      <div class="text-[14px] font-bold text-text-primary">{node.content.title}</div>
      <button class="text-text-tertiary hover:text-text-primary" onclick={onClose} aria-label="Close">✕</button>
    </div>
    <div class="flex-1 overflow-auto p-4">
      <textarea bind:value={editContent}
        class="w-full h-[55vh] p-3 rounded border border-border-default bg-bg-primary text-[12px] font-mono text-text-primary resize-none focus:outline-none focus:border-accent-primary"></textarea>
    </div>
    <div class="flex justify-end gap-2 p-4 border-t border-border-subtle">
      <button class="px-3 py-1.5 text-[12px] rounded border border-border-default text-text-secondary hover:text-text-primary" onclick={onClose}>Close</button>
      <button class="px-3 py-1.5 text-[12px] rounded bg-accent-primary text-white disabled:opacity-50"
        disabled={saving || editContent === node.content.content}
        onclick={async () => { if (!onSave) return; saving = true; try { await onSave(node.id, editContent); onClose(); } finally { saving = false; } }}>
        {saving ? 'Saving…' : 'Save'}
      </button>
    </div>
  </div>
</div>

<svelte:window onkeydown={(e) => { if (e.key === 'Escape') onClose(); }} />
```

> Match `z-[1000]` to whatever the app uses for top-most modals (the recent commit
> "log modal z-index" fixed stacking — read `ProcessingLogModal.svelte` and reuse
> the same z-index/portal approach so the modal escapes the canvas stacking context).

- [ ] **Step 2: Make the record node a compact card that opens the modal**

In `RecordNode.svelte`, replace the inline full-markdown block + Expand button
(lines 50-95) with a one-line summary and an Open button. Replace the `{#if editing}
… {/if}` ... Expand block (lines 50-95) with:

```svelte
    <div class="text-[11px] text-text-secondary line-clamp-2 mt-1">
      {(node.content.content || '').split('\n').find((l) => l.trim() && !l.startsWith('#')) || ''}
    </div>
    <button
      class="mt-2 text-[11px] text-accent-primary hover:underline"
      onclick={() => (modalOpen = true)}
    >Open document</button>
```

Add modal state + import at the top of the `<script>`:

```typescript
  import RecordModal from './RecordModal.svelte';
  let modalOpen = $state(false);
```

Remove the now-unused `expanded`/`editing`/`editContent` inline-edit machinery
(lines 6-9 and the inline editing block) — editing now lives in the modal. Keep the
Accept/Reject buttons (lines 97-121). Render the modal at the end of the component
markup, after `</Node>` is **not** valid (it must be inside the DOM but the overlay
is fixed) — render it just before the closing of the outer node `<div>` content,
guarded:

```svelte
{#if modalOpen}
  <RecordModal {node} onClose={() => (modalOpen = false)} onSave={onEdit} />
{/if}
```

> `onEdit(id, content)` is already a prop on this component (line 4) and is wired to
> the staging update endpoint upstream; reuse it as the modal's `onSave`.

- [ ] **Step 3: Verify build**

Run: `cd loom-mill/frontend && npm run build`
Expected: build succeeds.

- [ ] **Step 4: Manual observation**

Confirm a record node is now a compact card (badge + title + 2-line summary +
Open), clicking Open shows the full document in a centered modal that closes on ✕,
Escape, and backdrop click; editing + Save persists. Confirm the canvas no longer
grows a tall scroll for long documents. Screenshot.

- [ ] **Step 5: Commit**

```bash
git add loom-mill/frontend/src/lib/design/canvas/RecordModal.svelte loom-mill/frontend/src/lib/design/canvas/RecordNode.svelte
git commit -m "feat(mill): record nodes are compact cards that open a document modal"
```

---

### Task 18: Staging panel — discard/edit + multi-select consolidate

**Files:**
- Modify: `loom-mill/frontend/src/lib/design/StagingPanel.svelte`
- Verify: build + manual observation

- [ ] **Step 1: Read the panel and its data flow**

Read `StagingPanel.svelte` for how it lists staged records and what props/handlers
it has (it shows the "0 / 2 Ready" staging area from the screenshot). Note how it
reaches the API (`apiUrl`) and the session id.

- [ ] **Step 2: Add per-item Discard control**

For each staged item, add a Discard button that calls
`DELETE /shaping/sessions/{sessionId}/staged/{temp_id}` (the existing
`delete_staged_record` route):

```svelte
<button
  class="text-[11px] text-red-400 hover:text-red-300"
  onclick={async () => {
    await fetch(apiUrl(`/shaping/sessions/${sessionId}/staged/${encodeURIComponent(record.temp_id)}`), { method: 'DELETE' });
  }}
>Discard</button>
```

(State updates arrive via the existing WebSocket staging events; no local mutation
needed. If the panel reads staged records from `store`, confirm a staging-changed
event refreshes it — if not, refetch the session state after the call.)

- [ ] **Step 3: Add multi-select + Consolidate**

Add a selection set and a Consolidate action that calls the Task 9 endpoint. When
2+ items are selected, show a "Consolidate selected" button that POSTs to
`/shaping/sessions/{sessionId}/staged/consolidate`. Because the merged title/content
should be authored by the agent, send the targets and let the user provide a title,
or (preferred) trigger an agent consolidation: POST the targets with a placeholder
title/content is wrong — instead, this button should ask the **agent** to
consolidate. Implement it as: POST to consolidate with the user-confirmed merged
title and a content body that concatenates the targets' bodies under a single
heading as a first pass:

```svelte
<script lang="ts">
  let selected = $state<Set<string>>(new Set());
  function toggle(tempId: string) {
    const next = new Set(selected);
    next.has(tempId) ? next.delete(tempId) : next.add(tempId);
    selected = next;
  }
  async function consolidate() {
    const targets = [...selected];
    if (targets.length < 2) return;
    const records = stagedRecords.filter((r) => targets.includes(r.temp_id));
    const surface = records[0].surface;
    const title = `${records[0].title} (consolidated)`;
    const content = records.map((r) => r.content).join('\n\n---\n\n');
    await fetch(apiUrl(`/shaping/sessions/${sessionId}/staged/consolidate`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ targets, surface, title, content }),
    });
    selected = new Set();
  }
</script>
```

Add a checkbox per item bound to `toggle(record.temp_id)` and a button:

```svelte
{#if selected.size >= 2}
  <button class="text-[12px] px-3 py-1.5 rounded bg-accent-primary text-white" onclick={consolidate}>
    Consolidate {selected.size} records
  </button>
{/if}
```

> `stagedRecords` and `sessionId` must match the names the panel already uses; adapt
> after reading the file. The first-pass mechanical merge gives an immediate result;
> the operator can then open the consolidated record's modal and ask the agent to
> refine it via the normal advance loop (the agent now sees the staging area and can
> `edit-staged` it).

- [ ] **Step 4: Verify build**

Run: `cd loom-mill/frontend && npm run build`
Expected: build succeeds.

- [ ] **Step 5: Manual observation**

Reproduce the two-duplicate-specs scenario from the original report. Confirm: each
staged item has a Discard button that removes it; selecting two and clicking
Consolidate replaces them with a single merged record in staging. Screenshot.

- [ ] **Step 6: Commit**

```bash
git add loom-mill/frontend/src/lib/design/StagingPanel.svelte
git commit -m "feat(mill): staging discard + multi-select consolidate controls"
```

---

## Final verification

### Task 19: Full backend test sweep + integration check

- [ ] **Step 1: Run the whole backend suite**

Run: `cd loom-mill && uv run pytest -q`
Expected: all tests pass (including pre-existing `test_shaping_integration.py`).

- [ ] **Step 2: Frontend build**

Run: `cd loom-mill/frontend && npm run build`
Expected: succeeds with no errors.

- [ ] **Step 3: End-to-end manual session (the acceptance scenario)**

Following `AGENTS.md` Mill dev-server rules, run a full shaping session and verify
against the original report's complaints:
1. Branching options appear early (framing/tension/options) — divergent behavior.
2. A tension/observation can be continued (no dead ends).
3. Layout is tidy, no overlap; edges are clean elbows.
4. Records are compact cards opening a modal; no tall scroll.
5. Thinking stream is visible during advances; context panel shows the doc.
6. Two duplicate specs can be discarded and/or consolidated.
Capture screenshots for the review record.

- [ ] **Step 4: Commit any final fixes**

```bash
git add -A
git commit -m "chore(mill): final fixes from end-to-end Design Room verification"
```

---

## Self-Review Notes (author)

- **Spec coverage:** §1 keystone → Tasks 1-8; §2 vocabulary → Tasks 1,6,7,16; §3
  legibility → Tasks 14,15,17; §4 transparency → Tasks 10-13; §5 staging control →
  Tasks 5,9,18. All spec sections map to tasks.
- **Type/name consistency:** `serialize_graph(state)` defined Task 2, used Task 7;
  `ParsedOp`/`ParsedResponse.ops` defined Task 3, used Tasks 6-7; `consolidate()`
  defined Task 5, used Tasks 6,9; `advance_stream` event defined Task 10, consumed
  Tasks 11-12; `shapingThinking` store field defined Task 11, used Task 12;
  `RecordModal` defined Task 17. `build_canvas_prompt` signature changes in Task 7
  and its only caller (`engine.py`) is updated in the same task.
- **Known adaptation points (flagged inline, not placeholders):** several frontend
  tasks and the engine/staging/api test tasks must adapt to existing fixture and
  prop names in files the worker reads first. These are real "read then match"
  instructions, not deferred work; the required behavior and verification are fully
  specified.
