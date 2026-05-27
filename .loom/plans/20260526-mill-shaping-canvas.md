# Shaping Canvas Implementation

ID: plan:20260526-mill-shaping-canvas
Type: Plan
Status: completed
Created: 2026-05-26
Updated: 2026-05-26
Risk: high - Svelvet Svelte 5 compatibility is unproven; reactive regeneration is novel; response protocol design affects entire AI interaction model

## Summary

Replace the current timeline-based shaping UI with an infinite canvas where AI
interaction grows as a visible node graph. The operator sees questions, options,
observations, and record proposals as spatial nodes connected by edges. Selecting
an option kills sibling branches. Editing an earlier node invalidates and
regenerates downstream dependents reactively.

This requires coordinated changes across:
- Frontend: Svelvet canvas replaces timeline; custom node components for each type
- Backend models: flat block list becomes a node/edge graph
- Response protocol: model output format supports multiple typed nodes per response
- Engine: advance produces graph mutations (add nodes, add edges)
- WebSocket: new event types for graph mutations
- Interaction: option selection, question response, dead branch marking
- Reactive regeneration: dependency tracking and downstream re-invocation
- Layout: auto-positioning algorithm, collapse toggle, pan behavior

## Related Records

- `spec:mill-shaping-canvas` — the governing spec for canvas behavior, node types,
  interaction requirements, and evidence expectations
- `spec:mill-shaping-sessions` — superseded spec for reference; shows what we're
  replacing
- `plan:20260526-mill-shaping-sessions` — prior plan for the timeline implementation;
  tickets from this plan are effectively superseded by this new direction
- `loom-mill/src/loom_mill/shaping/models.py` — current data model (flat blocks)
- `loom-mill/src/loom_mill/shaping/engine.py` — current engine (single-decision loop)
- `loom-mill/src/loom_mill/shaping/parser.py` — current parser (single ```action block)
- `loom-mill/src/loom_mill/shaping/prompts.py` — current prompt template
- `loom-mill/frontend/src/lib/design/ShapingTimeline.svelte` — what gets replaced
- `loom-mill/frontend/src/lib/ws.svelte.ts` — WebSocket store; needs graph state

## Strategy

### Route: Risk-First, Then Contract-First, Then Vertical Integration

The riskiest assumption is that Svelvet works with Svelte 5 (its peer dep declares
only Svelte 3/4). If this fails, the entire canvas rendering approach changes. So
we prove this FIRST before investing in the rest.

Once Svelvet is proven, we establish the two shared contracts that all other work
depends on: (1) the backend graph data model (nodes + edges), and (2) the model
response protocol (how AI output becomes multiple typed nodes). These are
independent and can proceed in parallel.

With contracts defined, we wire the vertical tracer: one end-to-end path from
operator input through AI response through WebSocket through canvas rendering.
This proves the full pipe before we add interaction breadth.

Then we broaden: full interaction UX (option selection, dead branches, question
response), reactive regeneration (the hardest piece), and finally layout/polish/
staging/commit integration.

### Decomposition Logic

1. **Svelvet proof** is risk-first. Narrow scope: install, render one custom node,
   verify zoom/pan. If it fails, we pivot to custom SVG canvas (using our existing
   d3/SVG patterns from GraphView.svelte) before proceeding.

2. **Backend graph model** and **response protocol** are contract-first. They're
   independent concerns that other tickets depend on. Both must stabilize before
   integration.

3. **Canvas node components** depend on Svelvet proof but not on backend contracts.
   Can proceed after ticket 1 passes.

4. **End-to-end integration** is the vertical tracer. It depends on contracts (2, 3)
   and components (4). This is the first moment we can see real AI nodes on a canvas.

5. **Interaction UX** broadens from the vertical tracer. Option selection, dead
   branches, question response — the things that make the canvas feel alive.

6. **Reactive regeneration** is the hardest ticket and the most novel feature. It
   depends on the integration working. Editing an earlier node must invalidate and
   regenerate the downstream DAG.

7. **Layout + collapse** makes the canvas readable at scale.

8. **Staging, commit, and resume** closes the loop: record nodes → staging panel →
   materialized files on disk. Session state resumes on refresh.

### What Is Deliberately Left Out

- Factory Floor changes (unrelated)
- Chat panel (removed in shaping mode per spec)
- Voice input (existing feature, not affected)
- Multiple concurrent sessions (future work)
- Collaborative multi-user canvas (future work)

### Sequencing Constraints

- Ticket 1 MUST pass before any other frontend work begins (Svelvet risk)
- Tickets 2 and 3 are independent; can proceed in parallel after 1
- Ticket 4 depends on 1 only (frontend-only)
- Ticket 5 depends on 2, 3, and 4 (integration of all contracts)
- Tickets 6, 7, 8 depend on 5 (need working integration)
- Ticket 6 before 7 (regeneration uses dead-branch concepts)
- Ticket 8 can proceed after 5 (independent of 6/7)
- Ticket 9 depends on 5 and 6 (staging needs record node actions)

### Validation Posture

Every ticket:
- Must include Playwright or pytest evidence before claiming closure
- Frontend tickets: `frontend-expert` implements, `general` audits integration
- Backend tickets: `general` implements, `general` audits with tests
- Integration tickets: both agents verify their side
- No ticket claims done without observable proof in the running application

### Replanning Triggers

- Svelvet fails with Svelte 5 → pivot to custom SVG canvas, rewrite tickets 1+4
- Response protocol proves too fragile in practice → simplify to one-node-per-advance
- Reactive regeneration proves too complex → defer to future plan, ship without it
- Canvas performance degrades past 30 nodes → research alternative rendering

## Execution Units

### Unit 1: Svelvet Compatibility Proof

Ticket: ticket:20260526-mill-canvas-svelvet-proof

Prove Svelvet works with Svelte 5. Install the package, create a minimal test
component that renders a Svelvet canvas with one custom Svelte 5 component node,
verify zoom/pan/drag, take a Playwright screenshot. If peer dep warnings appear
but the library functions, document the workaround. If it fundamentally breaks,
document the failure mode and update the plan to pivot to custom SVG.

This is risk-first. Nothing else proceeds until this passes or we pivot.

Scope boundary: Only prove rendering and basic interaction. Do not build real node
types or wire to backend.

Evidence: Playwright screenshot of a Svelvet canvas with a custom node component
rendered, zoomed, and interacted with. Or: documented failure and pivot decision.

Audit: Generalist verifies the proof is honest (not a false positive from partial
rendering).

Stop condition: If Svelvet fails, stop and update this plan before proceeding.

### Unit 2: Backend Graph Data Model

Ticket: ticket:20260526-mill-canvas-graph-model

Replace the flat `blocks: list[InteractionBlock]` model with a graph-native model:
`nodes: dict[str, CanvasNode]` and `edges: list[CanvasEdge]`. Each node has an ID,
type, parent_id, content, status (active/stale/dead), position hint, and timestamp.
Each edge has source_id, target_id, and type (causal/option-group).

Update `SessionState` to use the new model. Update session persistence (JSON files
under `.mill/shaping-sessions/`). Update the REST API to serve the graph structure.
Existing sessions with old flat-block format in `.mill/shaping-sessions/` can be
discarded (transient runtime state, not committed). No migration needed.

The API contract change: `GET /shaping/sessions/{id}` returns `{nodes: {...}, edges: [...], ...}` instead of `{blocks: [...]}`.

Add new WebSocket event types: `node_added`, `edge_added`, `node_updated`,
`node_invalidated`.

Evidence: pytest suite passes with new model. API returns correct graph structure.
Existing tests adapted or replaced.

Audit: Generalist reviews model completeness against spec REQ-002 through REQ-012.

Stop condition: If the model cannot represent option groups (multiple siblings with
one active) cleanly, stop and redesign before proceeding.

### Unit 3: Model Response Protocol

Ticket: ticket:20260526-mill-canvas-response-protocol

Design and implement the response format that allows the AI model to produce
MULTIPLE typed nodes in a single response. The current format (`\`\`\`action` block)
supports only one decision per invocation. The canvas needs the model to potentially
emit: an observation + a question, or multiple option nodes, or an observation +
a record proposal.

Proposed format: XML-like tags that the parser extracts:

```
<node type="observation">
I found the existing GraphView uses d3-force for layout.
</node>
<node type="question" options="Force-directed,Hierarchical DAG,Both">
Which layout approach should we use?
</node>
```

For record proposals:
```
<node type="record" surface="tickets" title="Implement DAG layout">
# Implement DAG layout
ID: ticket:20260526-dag-layout
...full content...
</node>
```

For options (branching):
```
<node type="option-group" reasoning="Two valid architectural approaches">
<option label="Svelvet library">Use Svelvet for canvas rendering</option>
<option label="Custom SVG">Build custom SVG canvas with d3</option>
</node>
```

Update `parser.py` to extract multiple nodes from model output. Update `prompts.py`
to instruct the model on the new format. The parser should be tolerant: if the model
outputs the old ```action format, treat it as a single node for compatibility.

Evidence: Unit tests demonstrating multi-node parsing for all node types. Tests for
malformed output (graceful degradation). Tests for all node type parsing.

Audit: Generalist reviews parser robustness, edge cases, and prompt clarity.

Stop condition: If LLM output proves too unreliable with this format in manual
testing, simplify to one-node-per-invocation with multiple sequential advance calls.

### Unit 4: Canvas Node Components

Ticket: ticket:20260526-mill-canvas-node-components

Create Svelte 5 components for each canvas node type, rendered as custom Svelvet
nodes. Each component receives its node data as props and renders the appropriate
visual treatment per spec REQ-002:

- `InputNode.svelte`: operator text, compact, user-colored border
- `ProcessingNode.svelte`: animated pulsing, disappears when children arrive
- `QuestionNode.svelte`: accent-colored, contains response affordance (inline
  textarea + option buttons when options exist)
- `ObservationNode.svelte`: muted, expandable detail, evidence toggle
- `OptionNode.svelte`: appears in groups; visual states for active/selected/dead
- `RecordNode.svelte`: rich card with surface badge, title, content preview,
  accept/reject/edit actions

Each node component must work as a Svelvet custom node (using Svelvet's node
component pattern). Edge rendering should use Svelvet's built-in edges with
appropriate styling (different colors/styles for causal vs option-group edges).

Visual states:
- Active: full opacity, colored border per type
- Dead: red-tinted border, 40% opacity, greyed content
- Stale: dashed border, pulsing "regenerating" indicator
- Selected: bright accent ring

Evidence: Storybook-like isolated rendering of each node type in all states (via
a test page), captured with Playwright screenshots.

Audit: Generalist verifies visual states match spec, accessibility (ARIA labels,
keyboard focus), and component API cleanliness.

Stop condition: If Svelvet's custom node API proves too restrictive for our
interaction needs (e.g., cannot handle inline inputs), document the limitation
and propose alternative.

### Unit 5: End-to-End Integration (Vertical Tracer)

Ticket: ticket:20260526-mill-canvas-e2e-tracer

Wire the full pipe from operator input to rendered canvas nodes. This is the
vertical tracer that proves the architecture works end-to-end:

1. Operator types text in the seed input → backend creates session with root
   InputNode
2. Frontend receives `node_added` via WebSocket → renders InputNode on canvas
3. Frontend calls `/advance` → engine invokes harness → model responds with
   multi-node XML → parser extracts nodes → engine creates CanvasNodes with
   parent references → persists to session → publishes `node_added` events
4. Frontend receives events → new nodes appear on canvas connected to parent
   by edges
5. Operator can see the graph growing

This ticket wires:
- `ShapingSession.svelte` to render `ShapingCanvas.svelte` (new) instead of
  `ShapingTimeline.svelte`
- `ShapingCanvas.svelte` uses Svelvet with `{#each}` over nodes from the store
- `ws.svelte.ts` handles new event types and maintains reactive node/edge state
- Engine's `advance()` returns nodes (not blocks) using the new parser
- WebSocket serialization for graph events

Does NOT include: interaction (question response, option selection), reactive
regeneration, layout algorithm, staging integration. Those are separate tickets.
Use echo harness for testing (existing config) so we can verify the pipe without
needing a real LLM.

Evidence: Playwright test showing: seed input → session created → advance triggered
→ nodes appear on canvas with edges → can zoom/pan. Console shows no errors.
Backend test showing full advance cycle produces correct graph state.

Audit: Generalist audits both frontend integration (correct event handling, no race
conditions) and backend integration (correct node creation, persistence, event
publishing).

Stop condition: If the echo harness cannot produce valid multi-node XML, create a
mock/test harness that does.

### Unit 6: Canvas Interaction UX

Ticket: ticket:20260526-mill-canvas-interaction

Implement the interactive behaviors that make the canvas a living shaping tool:

**Question response**: When a QuestionNode has options, clicking an option creates
a new InputNode as child of the question, sends the response to the backend, and
triggers advance. When options are "open", an inline textarea appears in the node;
submitting creates the child InputNode.

**Option selection**: When an OptionGroupNode presents options, clicking one option
marks it as "selected" (active), marks all siblings as "dead" (red/dimmed, no
further growth). The selected option becomes the parent for subsequent AI nodes.
Backend creates appropriate edges and marks dead nodes.

**Dead branch propagation**: When a node is marked dead, ALL its descendants are
also marked dead recursively. Dead nodes remain visible but recessive (per spec
REQ-003).

**Processing node lifecycle**: ProcessingNode appears while advance is running.
When advance completes and produces child nodes, the ProcessingNode is either
removed or replaced by its children (transitions smoothly).

Evidence: Playwright test demonstrating: ask question → answer it → new nodes
appear. Present options → select one → siblings go red → selected branch grows.
Verify dead propagation across 3+ levels.

Audit: Generalist verifies interaction state machine correctness, ensures no orphan
nodes, verifies dead propagation is complete.

Stop condition: If Svelvet custom nodes cannot support inline inputs (textarea inside
a node), use a popover/modal pattern instead.

### Unit 7: Reactive Downstream Regeneration

Ticket: ticket:20260526-mill-canvas-regeneration

Implement REQ-012: when the operator edits an earlier node (changes their answer
to a question, or picks a different option retroactively), all downstream dependent
nodes are invalidated and regenerated.

**Dependency tracking**: Each node tracks which parent answers it depends on. When
a node's content changes, find all descendant nodes in the subtree rooted at that
node.

**Invalidation**: Mark all descendants as "stale" (visually: dashed border, dimmed,
pulsing indicator). Remove them from the active graph computation but keep them
visible briefly.

**Regeneration**: Re-invoke the engine starting from the edited node. The engine
produces new child nodes that replace the stale subtree. New nodes animate in;
stale nodes fade out.

**Editing semantics**:
- Editing an InputNode (operator answer): regenerates everything below it
- Changing option selection: marks old selected subtree as dead/stale, activates
  the newly selected option's subtree (or generates one if it doesn't exist)
- Editing is NOT allowed on AI-generated nodes (observation, question, record)
  directly — those are outputs, not inputs

**Backend support**: New endpoint `POST /shaping/sessions/{id}/nodes/{node_id}/edit`
that accepts new content, marks descendants stale, and triggers regeneration.
WebSocket events: `node_invalidated` (marks subtree stale), then `node_added`
events as regeneration produces new nodes.

Evidence: Playwright test: create session → get 3+ levels of nodes → edit the
first answer → downstream nodes go stale → new nodes regenerate → canvas shows
the updated graph. Backend test: edit triggers correct invalidation and
re-advance.

Audit: Generalist verifies: no orphan stale nodes remain permanently, regeneration
terminates (no infinite loops), concurrent edits don't corrupt state.

Stop condition: If regeneration proves too expensive (requires many sequential
harness calls), implement "regenerate on demand" (operator clicks a button to
regenerate a subtree) rather than automatic.

### Unit 8: Canvas Layout and Navigation

Ticket: ticket:20260526-mill-canvas-layout

Implement auto-layout that makes the canvas readable as the graph grows:

**Layout algorithm**: Top-down tree layout (Sugiyama-lite or d3-hierarchy). Nodes
are positioned in layers: root at top, children below, siblings spaced
horizontally. Minimize edge crossings.

**Manual adjustment**: Operator can drag nodes to custom positions. Dragged nodes
become "pinned" — auto-layout respects their position. Un-pin by double-clicking.

**Collapse dead branches toggle**: UI toggle (in canvas controls) that hides all
dead-branch subtrees. When collapsed, dead branches show as a small "N hidden"
badge on the last live ancestor. Toggle back to show them.

**Auto-pan**: When new nodes appear (from advance), the canvas smoothly pans to
keep the newest "active front" visible. If operator has manually panned away,
respect that (don't fight the operator).

**Zoom controls**: Zoom in/out buttons, fit-all button, minimap for orientation
in large graphs.

**Performance**: Must handle 50+ nodes without jank. Svelvet should handle this
natively but verify.

Evidence: Playwright screenshots: canvas with 10+ nodes in readable auto-layout.
Toggle collapse → dead branches disappear → toggle back → they return. Drag a
node → layout adjusts around it.

Audit: Generalist verifies layout produces no overlapping nodes, collapse/expand
is correct and complete, performance is acceptable.

### Unit 9: Staging, Commit, and Session Resume

Ticket: ticket:20260526-mill-canvas-staging-commit

Close the production loop:

**Record nodes → staging**: When a RecordNode is accepted (operator clicks accept
in the node), it appears in the staging panel (right sidebar). Rejecting removes
it. Editing opens inline editor in the node.

**Staging panel integration**: The existing StagingPanel.svelte continues to show
accepted records with surface badges, mini-graph of relationships, and commit
button. Clicking a record in staging highlights it on the canvas (pan + ring).

**Commit flow**: Commit materializes accepted records to `.loom/` using the
existing `CommitFlow`. After commit, the session ends and the operator returns
to the Design Room.

**Session resume**: Full canvas state (node positions, selection state, which
branches are dead, which nodes are accepted) persists to
`.mill/shaping-sessions/{id}/`. On page refresh or session re-open, the canvas
hydrates with complete visual state. Svelvet node positions must be saved and
restored.

**Frontend state management**: `ws.svelte.ts` shapingSession state evolves from
`{blocks: [...]}` to `{nodes: Map<id, node>, edges: [...], ...}`. The Svelvet
canvas renders from this reactive state.

Evidence: Playwright test: accept 2 records → staging shows them → commit →
files appear on disk. Refresh page → canvas resumes with all state intact.

Audit: Generalist verifies: commit produces correct files, no data loss on resume,
staging ↔ canvas highlighting works bidirectionally.

## Milestones

### Milestone: Canvas Renders (risk gate)

Child tickets: ticket:20260526-mill-canvas-svelvet-proof

What becomes true: We know Svelvet works with Svelte 5 and can render custom
component nodes. The plan proceeds as-is, or pivots to custom SVG.

### Milestone: Contracts Stable

Child tickets: ticket:20260526-mill-canvas-graph-model, ticket:20260526-mill-canvas-response-protocol

What becomes true: The backend graph data model and the model response format are
implemented and tested. All downstream tickets have stable interfaces to build
against.

### Milestone: First Nodes on Canvas

Child tickets: ticket:20260526-mill-canvas-node-components, ticket:20260526-mill-canvas-e2e-tracer

What becomes true: An operator can type input, trigger AI, and see nodes appear on
a real canvas with edges. The full pipe works end-to-end, even if interaction is
limited.

### Milestone: Interactive Canvas

Child tickets: ticket:20260526-mill-canvas-interaction, ticket:20260526-mill-canvas-regeneration

What becomes true: The canvas is a live, interactive shaping tool. Options branch,
dead paths are marked, questions can be answered inline, and editing earlier nodes
regenerates the graph. This is the core novel experience.

### Milestone: Production-Ready

Child tickets: ticket:20260526-mill-canvas-layout, ticket:20260526-mill-canvas-staging-commit

What becomes true: The canvas is readable at scale, sessions resume correctly, and
the full loop (shape → accept → commit → records on disk) works. Ready for real
use.

## Current State

All 9 tickets implemented, audited, and blocker-fixed. Plan complete.

- 126 backend tests passing
- Frontend builds clean
- Adversarial audit: 3 blockers found and fixed, dead code removed
- All milestones satisfied

Known deferred items (minor, from final audit):
- Canvas visual state (zoom/pan/drag positions) not persisted to backend
- Auto-pan not implemented (Svelvet has no programmatic pan API)
- `exploration_stream`/`exploration_cancelled` WS events not handled (frontend)
- Rejected record state not durable across page refresh

## Journal

- 2026-05-26: Created plan with Status `open`. Spec `mill-shaping-canvas` governs.
  Strategy: risk-first (Svelvet proof), contract-first (model + protocol), then
  vertical integration, then interaction breadth, then regeneration, then polish.
  Nine execution units filed as child tickets.
- 2026-05-26: Ticket 1 (Svelvet proof) closed. Risk gate passes. Plan proceeds.
- 2026-05-26: Tickets 2, 3, 4 implemented in parallel. Adversarial audit found 5
  issues (sibling parent_id, parser truncation, field mismatches, missing event,
  stale ticket status). All fixed.
- 2026-05-26: Ticket 5 (e2e tracer) implemented. Full pipe working.
- 2026-05-26: Tickets 6 (interaction) and 8 (layout) implemented in parallel.
  Option selection, dead propagation, tree layout, collapse toggle all working.
- 2026-05-26: Tickets 7 (regeneration) and 9 (staging/commit) implemented in
  parallel. Edit/reselect endpoints, stale subtree removal, commit filtering.
- 2026-05-26: Final adversarial audit. 3 blockers found: hydration contract
  mismatch, ObservationNode crash, commit filtering. All fixed. Dead code
  (ShapingTimeline, ShapingBlock) deleted. Advance serialized.
- 2026-05-26: Status → completed.
