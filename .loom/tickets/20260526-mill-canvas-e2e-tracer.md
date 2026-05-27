# End-to-End Canvas Integration (Vertical Tracer)

ID: ticket:20260526-mill-canvas-e2e-tracer
Type: Ticket
Status: closed
Created: 2026-05-26
Updated: 2026-05-26
Risk: high - integrates all contracts (model, protocol, components, WebSocket); first point where mismatches surface

Depends On: ticket:20260526-mill-canvas-graph-model
Depends On: ticket:20260526-mill-canvas-response-protocol
Depends On: ticket:20260526-mill-canvas-node-components

## Summary

Wire the full pipe from operator input through AI processing through WebSocket
through canvas rendering. This is the vertical tracer that proves the entire
architecture works end-to-end. When complete, an operator can type input, see a
root node appear on the canvas, watch AI processing produce child nodes that
appear connected by edges, and observe the graph growing reactively.

Single closure claim: Operator input produces AI-generated nodes on the canvas
end-to-end via the real pipe (backend engine → WebSocket → frontend canvas).

## Related Records

- `spec:mill-shaping-canvas` — REQ-001, REQ-006, REQ-007 govern the rendering
  and progressive growth behavior
- `plan:20260526-mill-shaping-canvas` — parent plan; this is Unit 5
- `ticket:20260526-mill-canvas-graph-model` — provides backend graph model and API
- `ticket:20260526-mill-canvas-response-protocol` — provides parser for multi-node
  output
- `ticket:20260526-mill-canvas-node-components` — provides renderable node
  components
- `loom-mill/frontend/src/lib/design/ShapingSession.svelte` — container to modify
- `loom-mill/frontend/src/lib/design/ShapingTimeline.svelte` — being replaced
- `loom-mill/frontend/src/lib/ws.svelte.ts` — WebSocket store to evolve
- `loom-mill/src/loom_mill/shaping/engine.py` — engine to evolve

## Scope

**What changes:**

Frontend:
- New `loom-mill/frontend/src/lib/design/ShapingCanvas.svelte`:
  - Mounts Svelvet canvas
  - Renders nodes from reactive store state using `{#each}` over nodes map
  - Renders edges from store state
  - Accepts new nodes via WebSocket events and renders them reactively
  - Handles seed input (same UX as current ShapingSession start screen)
  - Calls `/advance` after session creation and after operator input
  - Shows ProcessingNode while advance is in flight

- Modify `loom-mill/frontend/src/lib/design/ShapingSession.svelte`:
  - Replace `<ShapingTimeline>` with `<ShapingCanvas>`
  - Keep staging panel on the right
  - Remove chat-like input area at the bottom (input happens in the canvas nodes)

- Modify `loom-mill/frontend/src/lib/ws.svelte.ts`:
  - Change `shapingSession.blocks` → `shapingSession.nodes: Map<string, CanvasNode>`
    and `shapingSession.edges: CanvasEdge[]`
  - Handle `shaping:node_added` → add to nodes map
  - Handle `shaping:edge_added` → add to edges array
  - Handle `shaping:node_updated` → update node in map
  - Handle `shaping:node_invalidated` → mark nodes as stale
  - Remove `shaping:block_added` handler (deprecated)

- Update TypeScript types in `loom-mill/frontend/src/lib/types.ts`:
  - Add `CanvasNode`, `CanvasEdge`, `NodeStatus`, `CanvasNodeType` types
  - Remove `InteractionBlock` type entirely (replaced by `CanvasNode`)

Backend:
- Modify `loom-mill/src/loom_mill/shaping/engine.py`:
  - `advance()` uses `parse_canvas_response()` instead of `parse_decision()`
  - Creates `CanvasNode` objects (not `InteractionBlock`) from parsed output
  - Sets `parent_id` on new nodes (parent = the node that triggered advance,
    typically the last operator InputNode)
  - Creates edges between parent and children
  - Publishes `node_added` and `edge_added` events via store
  - Returns list of new nodes

- Modify `loom-mill/src/loom_mill/api/shaping.py`:
  - `create_shaping_session()`: creates session with root InputNode (not block)
  - `add_shaping_input()`: creates InputNode linked to appropriate parent
  - `advance_shaping_session()`: uses updated engine, returns nodes
  - `GET /sessions/{id}`: returns graph state (nodes + edges)

- Use echo harness for testing (since it returns whatever text we configure).
  Create a test harness wrapper that outputs valid multi-node XML so we can
  verify the full pipe without a real LLM.

**What must NOT change:**
- Staging/commit logic (still operates on staged_records)
- Factory Floor (completely separate)
- Harness subprocess mechanism (just changing what we parse from output)

**Stop condition:** If the echo harness cannot produce valid multi-node XML format,
create a simple mock script that does (e.g., a shell script that reads input and
outputs canned XML).

## Acceptance

- ACC-001: Operator can seed a session and see a root InputNode on the Svelvet
  canvas
  - Evidence: Playwright test: type text → click Begin → canvas shows InputNode
    with the typed text
  - Audit: Verify node ID matches backend, WebSocket event was the delivery
    mechanism

- ACC-002: Advancing produces AI nodes on the canvas connected to the root by edges
  - Evidence: Playwright test: after advance completes → 1+ new nodes appear →
    edges visually connect them to root → console has no errors
  - Audit: Verify edge source/target IDs are correct; nodes have correct types

- ACC-003: Multiple advance cycles produce a growing graph
  - Evidence: Playwright test: seed → advance → respond to question (via test
    interaction) → advance again → graph has 4+ nodes across 2+ levels
  - Audit: Verify parent-child relationships form a valid tree (no orphans, no
    cycles)

- ACC-004: WebSocket events drive rendering (not polling)
  - Evidence: Network tab shows WebSocket messages for node_added; no REST polling
    for state; frontend store updates reactively
  - Audit: Verify no `setInterval` or repeated fetch calls for canvas state

- ACC-005: ProcessingNode appears during advance and resolves when children arrive
  - Evidence: Playwright test captures the processing state (pulsing node visible)
    then verifies it's replaced by real nodes after advance completes
  - Audit: Verify no stale ProcessingNodes remain after advance resolves

- ACC-006: Backend tests pass with new engine flow
  - Evidence: `pytest` passes; tests verify advance produces CanvasNode objects
    with correct parent_ids and types
  - Audit: Review tests cover both echo harness path and error path

## Current State

Blocked on tickets 2, 3, and 4. Once those contracts are stable, this ticket wires
them together. First Ralph run: modify engine to use new parser, modify API to
serve graph, create ShapingCanvas.svelte, update WS store, verify with Playwright.

## Journal

- 2026-05-26: Created ticket with Status `open`. Vertical tracer: first end-to-end
  proof of the canvas architecture.
