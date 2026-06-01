# Design Room Redesign — Graph-Aware Shaping

**Date:** 2026-05-31
**Status:** Approved design, pre-implementation
**Component:** Loom Mill — Design Room / shaping canvas (`loom-mill/`)

## Problem

The Design Room presents a novel interaction model — an AI shapes fuzzy intent
into Loom records on a branching canvas — but in practice it does not feel
genuinely useful. Operator-observed friction:

- Branching options never appear, despite being the canvas's main advantage.
- Some threads end terminally in observations with no way to continue them.
- Default node placement is weird and nodes overlap.
- Edge curves look unpolished.
- Record nodes render their full document inline, creating long vertical scroll.
- Agent "thinking" is invisible — no evidence of progress or sequential thought.
- The internal context document is invisible and its effect is opaque.
- It is unclear whether the graph feeds back into the prompt.
- Duplicate/overlapping specs can pile up in staging with no way to remove a
  staged item or ask the AI to consolidate two of them.
- The AI appears unaware of the graph it is creating.

## Root-Cause Analysis (grounded in current code)

| Symptom | Root cause in code |
|---|---|
| No branching | Prompt's final guideline biases to records (`prompts.py:111`); agent only sees a **linear path** (`engine.py:73-74`), never the branching graph. `option-group` is supported but rarely chosen. |
| Dead-end observations | `_active_parent_id` (`engine.py:268-272`) *can* continue from an observation, but no UI affordance invites it. |
| Weird placement / overlap | `layout.ts` is a naive `y = depth*150` grid with sibling X spread and **no collision handling**. |
| Curvy edges | Svelvet default bezier edges, unstyled. |
| Tall record scroll | `RecordNode.svelte:83-94` renders full markdown inline, line-clamped, expanding in place. |
| No thinking traces | Decision call passes `on_stream=None` (`engine.py:177`); only explorations stream. |
| Opaque context doc | `context.md` is read into the prompt (`engine.py:120-127`) but never surfaced to the operator. |
| AI not graph-aware | Prompt receives `context.md[-8000:]` + 20-node linear summary only; never the full DAG or the staging area. |
| No staging control | `DELETE`/`PUT /staged/{temp_id}` endpoints exist (`shaping.py`) but have no UI; no consolidation op exists. |

**Keystone insight:** most symptoms are downstream of one limitation — the agent
cannot perceive the whole graph or the staging area, and its only mutation is
"append a child." Fix that, and branching, continue-from-observation, and
consolidation become emergent behaviors rather than separate features.

## Goals

1. Make the agent perceive the full graph + staging area and mutate them with
   explicit, parseable operations.
2. Shift the shaping disposition from a convergent funnel to
   **divergent-then-convergent**.
3. Give nodes a differentiated, intent-coded vocabulary so the canvas reads as a
   thinking process.
4. Make the canvas legible: tidy layout, clean edges, record nodes as compact
   cards that open a modal.
5. Make the invisible machinery visible: live thinking stream + a context peek
   panel.
6. Give the operator real staging control: manual discard/edit + AI consolidation.

## Non-Goals

- Migrating the shaping agent to a true tool-using filesystem loop. This design
  uses a **serialized graph view + structured ops** that fit the existing
  one-shot harness. The op vocabulary is explicitly intended as the proving
  ground / spec for a future tools-based version, but that migration is out of
  scope here.
- Multi-operator real-time collaboration semantics beyond what the current
  WebSocket broadcast already provides.
- Changing the commit pipeline or the `.loom` record formats.

## Design

### 1. Keystone — graph-aware agent (serialized view + structured ops)

**1a. Full-graph serialization.** Add `serialize_graph(session)` that renders the
entire session as compact, stable text for the prompt, replacing the linear
`format_node_history`:

- Every node: short stable ID, type, status (`active`/`stale`/`dead`), parent ID,
  branch, and a one-line summary.
- A **Staging Area** section: each staged doc by `temp_id`, surface, title, and a
  short content digest.
- Size control: cap the rendered graph; when a session grows large, digest older
  / dead subtrees and rely on `context.md` for deep history. The serialized view
  always includes all *active* nodes and the full staging list.

**1b. Structured mutation ops.** Extend the response vocabulary parsed in
`parser.py`. In addition to today's node emission, the agent may emit ops that
reference existing node/temp IDs:

- `continue from="<node_id>"` — append children to any node, including
  OBSERVATION/TENSION. Removes dead-ends.
- `supersede targets="<temp_id>[,<temp_id>...]"` + replacement RECORD — the
  consolidation primitive; discards targets, stages the merged record.
- `edit-staged temp_id="..."` — rewrite a staged doc's title/content.
- `discard-staged temp_id="..."` — remove a staged doc.
- `revise node="<id>"` — mark a node stale and replace its subtree, reusing the
  existing `regenerate` / `_remove_subtree` machinery (`engine.py:28-63`).

Ops resolve against current session state server-side; unknown/stale IDs fail
closed (op is dropped with an OBSERVATION explaining why, never a silent no-op).

**1c. Disposition shift.** The prompt's closing guideline changes from
"move toward proposing records as quickly as certainty allows" to a phase-aware
disposition: **branch and surface tensions while EXPLORING/NARROWING; converge to
records only when the operator signals readiness or certainty is genuinely high.**

### 2. Node vocabulary & divergent→convergent arc

Extend `CanvasNodeType` (`models.py:16-24`). Types are color-coded by intent so
the canvas reads as a thinking process:

| Type | Intent (color) | Role |
|---|---|---|
| `INPUT` | neutral (grey) | operator intent / steer |
| `PROCESSING` | neutral (grey) | live exploration **and** live thinking (see §4) |
| `FRAMING` | divergent (purple) | a distinct lens on the problem; invites parallel framings |
| `QUESTION` | divergent (purple) | one decision that narrows the work |
| `OPTION_GROUP` / `OPTION` | divergent (purple) | materially different paths as live branches |
| `TENSION` | holds (orange) | a contradiction / risk / constraint held open — inherently continuable |
| `OBSERVATION` | neutral (grey) | a fact/finding — **now always continuable** |
| `DECISION` | convergent (green) | a resolved choice that prunes branches |
| `RECORD` | convergent (green) | complete Loom record → staging |

- `TENSION` and continuable `OBSERVATION` cure the dead-end problem: both render a
  "continue / branch from here" affordance backed by the `continue from=` op.
- `FRAMING` + the disposition shift make branching the natural early move.
- `DECISION` gives convergence a visible moment instead of a silent option-select.

**Phase coupling.** The phase machine (`EXPLORING→NARROWING→PROPOSING→REFINING`,
`engine.py:242-252`) is retuned so divergent types are encouraged early and the
agent is not pushed to propose a record prematurely. The prompt states the
current phase and its matching disposition.

### 3. Canvas legibility

**3a. Layout — layered tree (replaces `layout.ts`).** Strict layers by depth, but
siblings packed with **width-aware collision avoidance**: measure each node's box,
allocate non-overlapping horizontal slots per layer, center parents over their
children's span (tidy-tree / dagre-style). Dead/collapsed branches reserve no
space (ties into the existing "Collapse dead branches" toggle). Manual
drag-to-pin overrides are still honored; the default is always non-overlapping.

**3b. Edges — orthogonal elbows.** Replace Svelvet default bezier with right-angle
connectors with rounded corners, thin and low-contrast. Branch-point
(`option_group`) edges get a subtle distinct treatment from normal `causal`
edges. Crisp at any zoom.

**3c. Record node → compact card + modal.** Replace inline full-markdown rendering
(`RecordNode.svelte:83-94`) with:

- A **compact summary card**: surface badge (color-coded by surface), title, a
  one-line intent/summary, Accept/Reject/Edit controls. Bounded, uniform height.
- Clicking the card / "Open" launches a **document modal** with full markdown, an
  editor, and accept/reject — reusing the app's existing modal pattern (the
  processing-log modal and its z-index/stacking fixes from recent commits).

### 4. Transparency

**4a. Live thinking stream.** Thread a stream callback into the decision
invocation (`engine.py:177`, currently `on_stream=None`) so the agent's reasoning
streams during the decision step, not just during explorations. Surface it via a
`shaping:advance_stream` WebSocket event alongside the existing
`advance_started`/`advance_completed` events (`ws.svelte.ts:328-346`), rendered in
a dedicated, dismissible stream region (not jammed into a node body, since raw
thinking can be noisy).

**4b. Context peek panel.** A collapsible side panel (mirroring the Staging Area
panel) exposes:

- the current context document (`context.md`) for the session,
- a note of what graph slice was fed to the prompt on the last advance (now the
  full serialized graph from §1).

This answers the operator's open questions about how continuity is maintained and
how the graph feeds the prompt.

### 5. Staging control

- **Manual:** each staged item gets **Discard** and **Edit** controls in the
  Staging Area panel, wiring the existing `DELETE` / `PUT /staged/{temp_id}`
  endpoints (`shaping.py`) that currently lack UI.
- **AI consolidate:** select 2+ staged docs → "Ask agent to consolidate" issues
  the `supersede targets=...` op (§1b). The agent reads both docs (it can now see
  staging), produces one merged RECORD, and discards the originals. Direct fix for
  duplicate/overlapping specs.

## Data Flow

1. Operator adds INPUT (or selects/continues a node) → `POST .../advance`.
2. Engine assembles context: `serialize_graph(session)` (full graph + staging) +
   `context.md`, builds the phase-aware prompt.
3. Decision invocation runs **with streaming** → `shaping:advance_stream` deltas.
4. Response parsed into node emissions **and** mutation ops.
5. Ops resolved against session state (fail closed on bad IDs); nodes/edges added,
   staging mutated, phases transitioned.
6. State persisted (`state.json`), `context.md` appended on relevant events.
7. WebSocket broadcasts node/edge/staging/phase events to all clients.

## Error Handling & Fail-Closed Rules

- Unknown or stale node/temp IDs in ops: drop the op, emit an OBSERVATION naming
  the reason. Never silently mutate the wrong target.
- `supersede`/`discard` against an already-accepted staged record: refuse and
  surface a TENSION (operator already committed intent to that doc).
- Serialized-graph size cap exceeded: digest dead/old subtrees first; never drop
  active nodes or staging entries silently — note the digest in the context peek.
- Streaming failure during decision: fall back to non-streamed result (current
  behavior) and show a progress indicator rather than erroring the advance.

## Testing Strategy

- **Backend unit:** `serialize_graph` shape/stability; parser accepts each new op;
  op resolution against good/bad/stale IDs (fail-closed); `supersede` discards
  targets and stages merged record; phase retune transitions.
- **Backend integration:** advance loop emits `advance_stream`; consolidation op
  produces one staged record from two; continue-from-observation appends children.
- **Frontend:** layered-tree layout produces non-overlapping positions for known
  fixtures; record card opens modal; staging discard/edit hit the right
  endpoints; thinking-stream region renders deltas; context peek shows
  `context.md`.
- **Manual / observation:** screenshots of a real shaping session showing
  branches, a TENSION continued, a tidy layout with elbow edges, a record modal,
  and a consolidation.

## Sequencing

1. **Phase 1 — Keystone (§1):** serialization, op vocabulary, parser, disposition.
   Everything else depends on it.
2. **Phase 2 — Vocabulary (§2)** and **Staging control (§5):** depend on §1's ops.
3. **Phase 3 — Transparency (§4):** thinking stream + context peek.
4. **Phase 3 (parallel) — Legibility (§3):** layout, edges, record modal —
   independent of the agent changes, can land alongside any phase.

## Open Questions / Residual Risk

- Serialized-graph token cost on long sessions — mitigated by digesting, but the
  exact cap/digest heuristic needs tuning against real sessions.
- Raw thinking-stream verbosity may need a summarization pass if it proves noisy.
- The op vocabulary may need iteration once exercised on real consolidations; it
  is intentionally the spec for a later filesystem-tools migration.
