# Canvas Layout and Navigation

ID: ticket:20260526-mill-canvas-layout
Type: Ticket
Status: closed
Created: 2026-05-26
Updated: 2026-05-26
Risk: low - layout is visual polish; core functionality works without it (Svelvet provides basic positioning)

Depends On: ticket:20260526-mill-canvas-e2e-tracer

## Summary

Implement auto-layout that positions nodes in a readable tree/DAG arrangement,
manual drag adjustment, dead branch collapse toggle, auto-pan to active front,
and zoom controls. This makes the canvas usable at scale (30+ nodes across
multiple branches).

Single closure claim: The canvas auto-positions nodes in a readable tree layout,
supports manual adjustment, and provides collapse/zoom/pan controls for navigation.

## Related Records

- `spec:mill-shaping-canvas` — REQ-005 (auto-layout with manual adjustment),
  REQ-007 (progressive growth / auto-pan)
- `plan:20260526-mill-shaping-canvas` — parent plan; this is Unit 8
- `ticket:20260526-mill-canvas-e2e-tracer` — provides working canvas with nodes
  and edges to layout
- `loom-mill/frontend/src/lib/design/GraphView.svelte` — existing layout patterns
  (d3-force, layered); reference for algorithms

## Scope

**What changes:**

Layout algorithm (`loom-mill/frontend/src/lib/design/canvas/layout.ts` or similar):
- Tree layout: top-down (root at top, children below)
- Algorithm: adapted Sugiyama-lite or d3-hierarchy treemap
  - Assign layers (depth from root)
  - Within each layer, space siblings horizontally
  - Minimize edge crossings between layers
  - Handle variable node widths/heights
- Output: `{nodeId: {x, y}}` position map
- Recompute on node add/remove; animate position transitions

Manual adjustment:
- Nodes are draggable (Svelvet provides this natively)
- When operator drags a node, mark it as "pinned" (position locked)
- Auto-layout skips pinned nodes (respects their position, flows around them)
- Double-click a pinned node to un-pin (returns to auto-layout)

Collapse dead branches:
- UI toggle button in canvas controls area: "Show dead branches" on/off
- When collapsed: all dead subtrees are hidden (nodes/edges removed from render)
- A small badge appears on the last live ancestor: "N hidden"
- When expanded: dead subtrees reappear in their positions
- State persists in session (saved with canvas state)

Auto-pan:
- When new nodes appear (from advance), smoothly pan the viewport to keep the
  newest active node visible
- Respect operator intent: if operator has manually panned within the last 2s,
  don't auto-pan (anti-fight behavior)
- "Follow mode" indicator: subtle badge showing auto-pan is active

Zoom controls:
- Svelvet provides zoom/pan natively; ensure controls are visible:
  - Zoom in / Zoom out buttons
  - Fit all button (zoom to show entire graph)
  - Minimap for orientation (Svelvet has minimap support)
- Keyboard shortcuts: Ctrl+= zoom in, Ctrl+- zoom out, Ctrl+0 fit all

**What must NOT change:**
- Node component visual design (ticket 4)
- Interaction handlers (ticket 6)
- Regeneration logic (ticket 7)
- Backend graph model (positions stored as hints, not authoritative)

**Stop condition:** If layout computation becomes slow (>100ms for 50 nodes),
simplify to a basic tree layout without crossing minimization.

## Acceptance

- ACC-001: Nodes are auto-positioned in a readable top-down tree layout
  - Evidence: Playwright screenshot of canvas with 10+ nodes across 3+ branches;
    no overlapping nodes; clear parent-child visual hierarchy
  - Audit: Verify layout handles asymmetric trees (one deep branch, one shallow)

- ACC-002: Dragging a node pins it; double-click un-pins
  - Evidence: Playwright test: drag node → add new sibling → verify dragged node
    stays put while sibling is auto-positioned → double-click → node returns to
    auto-layout position
  - Audit: Verify pin state persists across re-layouts

- ACC-003: Dead branch collapse toggle works
  - Evidence: Playwright test: create dead branches → toggle collapse → dead nodes
    disappear → badge shows "N hidden" → toggle back → nodes reappear
  - Audit: Verify badge count is correct; verify expand restores exact positions

- ACC-004: Auto-pan keeps active front visible
  - Evidence: Playwright test: zoom into a corner → trigger advance → viewport
    smoothly pans to show new nodes
  - Audit: Verify anti-fight: manual pan → immediate advance → no auto-pan for 2s

- ACC-005: Zoom controls and minimap function correctly
  - Evidence: Playwright test: zoom buttons work, fit-all shows entire graph,
    minimap renders (if Svelvet supports)
  - Audit: Verify keyboard shortcuts work

## Current State

Blocked on end-to-end integration. First Ralph run: implement layout algorithm,
wire to canvas, add controls, test with Playwright.

## Journal

- 2026-05-26: Created ticket with Status `open`. Visual polish that makes the
  canvas usable at scale. Lower risk than interaction/regeneration tickets.
