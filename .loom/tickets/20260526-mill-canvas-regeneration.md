# Reactive Downstream Regeneration

ID: ticket:20260526-mill-canvas-regeneration
Type: Ticket
Status: review
Created: 2026-05-26
Updated: 2026-05-26
Risk: high - most novel and complex feature; dependency tracking, invalidation cascades, re-invocation loops, and concurrent state management all intersect

Depends On: ticket:20260526-mill-canvas-e2e-tracer
Depends On: ticket:20260526-mill-canvas-interaction

## Summary

When the operator edits an earlier node (changes their answer to a question, or
retroactively picks a different option), all downstream dependent nodes are
invalidated and regenerated. The graph is not append-only — it's a live dependency
tree where changing an assumption propagates consequences downstream.

This is the key differentiating feature per spec REQ-012: changing assumptions in
a node reactively regenerates connected downstream nodes.

Single closure claim: Editing an earlier node invalidates all downstream dependents
(marked stale visually) and triggers re-invocation that produces new replacement
nodes.

## Related Records

- `spec:mill-shaping-canvas` — REQ-012 defines reactive regeneration behavior
- `plan:20260526-mill-shaping-canvas` — parent plan; this is Unit 7
- `ticket:20260526-mill-canvas-interaction` — provides option selection and dead
  branch mechanics; regeneration builds on similar graph-mutation patterns
- `ticket:20260526-mill-canvas-graph-model` — node model must support `stale` status
- `loom-mill/src/loom_mill/shaping/engine.py` — engine must support re-advance
  from arbitrary nodes

## Scope

**What changes:**

Backend — New endpoint `POST /sessions/{id}/nodes/{node_id}/edit`:
- Validates the node is editable (only `input` type nodes are editable; AI-
  generated nodes like observation/question/record are outputs, not editable inputs)
- Accepts `{content: "new text"}` body
- Updates the node's content
- Finds all descendants (direct children, their children, recursively)
- Marks all descendants as `stale` (not `dead` — stale means "will be replaced")
- Persists state
- Publishes `node_invalidated` event with list of stale node_ids
- Triggers regeneration: calls engine.advance() with the edited node as the new
  "parent context" — the engine re-processes from that point
- As new nodes are created by the engine, they replace the stale subtree:
  - New nodes get the same parent_id as the edited node's original children
  - Stale nodes are eventually removed (after new nodes arrive) or remain as
    ghost overlay briefly

Backend — New endpoint `POST /sessions/{id}/nodes/{node_id}/reselect`:
- For changing option selection retroactively
- Validates node is an option type
- If the option was previously dead (operator is changing their mind):
  - Marks the OLD selected sibling as dead (+ its descendants)
  - Marks THIS option as active
  - If this option already has children: mark them as active (un-stale)
  - If this option has NO children: trigger advance from this option
- Publishes appropriate `node_updated` and `node_invalidated` events

Backend — Regeneration engine logic:
- `engine.regenerate(session, from_node_id)`:
  - Builds context from the path root → from_node (the "conversation so far"
    up to the edited point)
  - Invokes harness with this trimmed context (not the full session history)
  - Parses response, creates new child nodes under from_node
  - Old stale nodes can be cleaned up (removed from graph) or kept as a "previous
    generation" layer (design choice: remove for simplicity)
- Must handle: regeneration producing different number of nodes than before
- Must handle: regeneration producing different types (was question, now observation)
- Must terminate: if regeneration triggers another advance that triggers another,
  set a max depth (e.g., 3 levels max auto-regeneration; deeper levels stay stale
  until operator clicks "regenerate")

Frontend:
- `InputNode.svelte`: Add edit affordance (pencil icon → inline textarea → save)
  - On save: call `POST /sessions/{id}/nodes/{node_id}/edit`
- `OptionNode.svelte`: Dead options get a "Re-select" action (subtle, not prominent)
  - On click: call `POST /sessions/{id}/nodes/{node_id}/reselect`
- `ws.svelte.ts`:
  - Handle `shaping:node_invalidated` → mark listed nodes as stale in store
  - Handle subsequent `node_added` events → new nodes appear
  - Handle `shaping:nodes_removed` → remove stale nodes from store after
    replacement arrives
- Visual treatment:
  - Stale nodes: dashed border, 60% opacity, subtle pulsing animation
  - Stale nodes show "Regenerating..." text overlay
  - New replacement nodes animate in (scale-up from 0) as stale nodes fade out

**What must NOT change:**
- Forward-only advance (existing advance flow still works for new nodes)
- Option selection for the FIRST time (that's ticket 6's dead branch logic)
- Layout algorithm (ticket 8)
- Staging/commit (ticket 9)

**Stop conditions:**
- If regeneration loops (new nodes trigger more regeneration infinitely): cap at
  3 auto-regeneration levels, leave deeper subtrees stale with manual trigger
- If regeneration is too slow (multiple sequential harness calls): implement
  "regenerate on demand" — stale nodes show a "Regenerate" button instead of
  automatic re-invocation
- If concurrent edits cause state corruption: serialize edit operations per session
  (queue)

## Acceptance

- ACC-001: Editing an InputNode's text marks all its descendants as stale
  - Evidence: Playwright test: session with 3 levels → edit root answer → all
    children and grandchildren show stale styling (dashed border, dimmed)
  - Audit: Backend state shows `stale` status on all descendants; verify list
    is complete

- ACC-002: After edit, regeneration produces new child nodes that replace the stale
  subtree
  - Evidence: Playwright test: edit → stale nodes visible → after delay → new nodes
    appear → stale nodes removed/replaced → graph is valid again
  - Audit: Verify new nodes have correct parent_id (the edited node); verify no
    orphan stale nodes remain permanently

- ACC-003: Re-selecting a dead option marks the old selection as dead and activates
  the new branch
  - Evidence: Playwright test: option A selected → later re-select option B →
    option A and its descendants become dead → option B activates → advance
    produces children for B
  - Audit: Verify state transitions are correct; no node is simultaneously dead
    and stale

- ACC-004: Regeneration terminates (no infinite loops)
  - Evidence: Backend test: force a scenario where regeneration could theoretically
    loop → verify it stops at max depth (3) → deeper nodes stay stale
  - Audit: Verify max-depth enforcement exists and is tested

- ACC-005: Concurrent edits don't corrupt state
  - Evidence: Backend test: two rapid edit calls on the same node → state is
    consistent after both complete → no duplicate nodes, no missing edges
  - Audit: Verify serialization mechanism (queue or lock) exists

## Current State

Implementation and requested verification are complete for the current run. The
backend now supports edit/reselect endpoints, stale invalidation, bounded
regeneration, stale subtree removal events, and per-session mutation locks. The
frontend now has InputNode edit and dead-option reselect affordances, plus WebSocket
handling for invalidation, removal, and both `node_updated` payload shapes.

Evidence: `evidence:20260526-mill-canvas-regeneration-validation`

Remaining review posture: no Playwright visual/browser verification or audit has
been performed yet, so the ticket is in `review` rather than `closed`.

## Journal

- 2026-05-26: Created ticket with Status `open`. The novel differentiator. High
  risk but high reward. Multiple stop conditions defined for scope control.
- 2026-05-26: Status set to `active` for ticket-owned Ralph implementation run.
  Live code confirms the dependency surfaces named in the operator prompt exist;
  scope remains limited to regeneration, reselect, stale/removal events, frontend
  affordances, and requested verification.
- 2026-05-26: Implemented backend edit/reselect regeneration, session stale/active
  helpers, bounded engine regeneration, frontend edit/reselect affordances, stale
  removal handling, backend tests, and frontend build verification. Evidence
  recorded in `evidence:20260526-mill-canvas-regeneration-validation`. Status set
  to `review` because Playwright visual evidence and audit remain unperformed.
