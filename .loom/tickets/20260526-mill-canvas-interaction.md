# Canvas Interaction UX

ID: ticket:20260526-mill-canvas-interaction
Type: Ticket
Status: closed
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - interaction state machine complexity; dead branch propagation must be complete and correct

Depends On: ticket:20260526-mill-canvas-e2e-tracer

## Summary

Implement the interactive behaviors that make the canvas a living shaping tool:
answering questions inline, selecting options (which kills sibling branches),
and propagating dead status through the graph. After this ticket, the canvas
supports the full interaction loop that produces a branching, living decision tree.

Single closure claim: Canvas nodes support operator interaction that correctly
mutates the graph (question answers produce children, option selection marks
siblings dead, dead status propagates to all descendants).

## Related Records

- `spec:mill-shaping-canvas` — REQ-003 (branching/selection), REQ-008 (node
  interaction), REQ-002 (visual states)
- `plan:20260526-mill-shaping-canvas` — parent plan; this is Unit 6
- `ticket:20260526-mill-canvas-e2e-tracer` — provides working canvas with nodes
  and edges; this ticket adds interaction on top
- `ticket:20260526-mill-canvas-node-components` — components already have
  interaction affordances (buttons, textarea); this ticket wires them to backend

## Scope

**What changes:**

Frontend interaction wiring:
- `QuestionNode.svelte`: When operator clicks an option button or submits text in
  the inline textarea:
  1. Create a new InputNode as child of the question (optimistic or after API)
  2. Call `POST /sessions/{id}/input` with the response text and `parent_node_id`
  3. Call `POST /sessions/{id}/advance` to trigger next AI processing
  4. Show ProcessingNode while waiting

- `OptionNode.svelte` / Option selection flow:
  1. Operator clicks an option node
  2. Frontend calls `POST /sessions/{id}/nodes/{option_id}/select`
  3. Backend marks selected option as `active`, marks all siblings in the same
     option_group as `dead`
  4. Backend propagates dead status to ALL descendants of dead siblings
  5. Backend publishes `node_updated` events for all affected nodes
  6. Frontend receives events → dead nodes render with red/dimmed styling
  7. Selected option becomes parent for subsequent advance calls

Backend:
- New endpoint: `POST /sessions/{id}/nodes/{node_id}/select`
  - Validates node is an option type
  - Finds all siblings in same `option_group_id`
  - Marks this node as selected (keeps `active`)
  - Marks siblings as `dead`
  - Recursively marks all descendants of dead siblings as `dead`
  - Persists state
  - Publishes `node_updated` events for all changed nodes
  - Triggers advance from selected option (optional: configurable)

- Update `POST /sessions/{id}/input` to accept `parent_node_id` parameter:
  - Creates InputNode with specified parent
  - Creates edge from parent to new node
  - This allows the frontend to specify which question the response answers

- Dead propagation logic (in models or session):
  - `mark_dead(node_id)`: sets node status to `dead`, recursively marks all
    children (nodes whose parent_id == this node), their children, etc.
  - Returns list of all affected node_ids for event publishing

Frontend state handling:
- `ws.svelte.ts`: When receiving `node_updated` events with `status: "dead"`,
  update the node in the reactive map → Svelvet re-renders with dead styling
- The canvas should NOT remove dead nodes (they stay visible per spec REQ-003)
- Dead nodes are non-interactive (buttons disabled, no input affordances)

**What must NOT change:**
- Canvas layout (that's ticket 8)
- Reactive regeneration (that's ticket 7)
- Staging/commit (that's ticket 9)
- Node component visual design (already done in ticket 4; only wiring changes here)

**Stop condition:** If dead propagation causes performance issues on large graphs
(100+ nodes becoming dead simultaneously), batch the WebSocket updates into a
single `nodes_batch_updated` event.

## Acceptance

- ACC-001: Answering a question produces a child InputNode connected by an edge,
  triggers advance, and new AI nodes appear
  - Evidence: Playwright test: canvas shows question with options → click option →
    InputNode appears as child → ProcessingNode → AI nodes appear as grandchildren
  - Audit: Verify parent-child relationship is correct in backend state

- ACC-002: Selecting an option marks all siblings as dead with correct visual
  treatment
  - Evidence: Playwright test: option group with 3 options → select middle one →
    other 2 turn red/dimmed → verify all 3 still visible on canvas
  - Audit: Backend state shows correct `dead` status on siblings; verify
    `option_group_id` linkage

- ACC-003: Dead status propagates to all descendants recursively
  - Evidence: Playwright test: create a graph with option → children → grandchildren
    → select different option → ALL descendants of the unchosen sibling are dead
  - Audit: Backend test with 4+ levels of depth; verify no orphan active nodes
    under a dead parent

- ACC-004: Dead nodes are non-interactive (buttons disabled, no text input)
  - Evidence: Playwright test: after marking dead → click buttons on dead nodes →
    nothing happens; textarea is disabled/hidden
  - Audit: Verify no API calls are made when interacting with dead nodes

- ACC-005: Frontend handles rapid state updates without race conditions
  - Evidence: Test selecting an option while advance is in progress → no crashes,
    no inconsistent state, no duplicate nodes
  - Audit: Review frontend event handling for potential race conditions between
    `node_updated` and `node_added` events arriving out of order

## Current State

Implementation is complete for the backend select endpoint, recursive dead
propagation, `parent_node_id` question-response input wiring, frontend option
selection wiring, and backend test/build verification. The ticket is in `review`
because Playwright/browser evidence and audit have not been performed.

Evidence: `evidence:20260526-mill-canvas-interaction-validation`

## Journal

- 2026-05-26: Created ticket with Status `open`. Interaction broadening: makes the
  canvas a living tool instead of a static graph.
- 2026-05-26: Status set to `active` for implementation of backend option
  selection/dead propagation, question response parent wiring, frontend selection
  wiring, and requested backend/frontend verification.
- 2026-05-26: Implemented option selection and dead propagation, added backend
  tests, wired frontend option selection, and recorded validation evidence. Status
  moved to `review`; remaining work is browser/Playwright evidence and audit.
