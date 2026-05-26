# Connected-Record Graph View

ID: ticket:20260526-mill-graph-connected
Type: Ticket
Status: review
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - needs graph rendering library integration; visual quality matters for UX

## Summary

Add an Obsidian-style force-directed graph view to the Design Room. When a record
is open in the editor, the operator can open a graph showing that record and all
records connected to it (references in either direction). Clicking a node navigates
to that record in the editor.

The relationship data already exists: every `LoomRecord` in `store.state.records`
has `references` (outgoing) and can be cross-referenced to find incoming links.
No backend changes needed.

Closure claim: Operators can visualize and navigate record relationships from any
open record in the Design Room via a force-directed graph.

## Related Records

- `plan:20260526-mill-next-gen` - parent plan
- `loom-mill/frontend/src/lib/types.ts:48-69` - LoomRecord with references field
- `loom-mill/frontend/src/lib/ws.svelte.ts` - store has all records
- `loom-mill/frontend/src/lib/design/DesignRoom.svelte` - container for Design Room
- `loom-mill/frontend/src/lib/design/editor-extensions.ts` - existing reference parsing for links

## Scope

Write:
- `loom-mill/frontend/src/lib/design/GraphView.svelte` (new) - force-directed graph component
- `loom-mill/frontend/src/lib/design/DesignRoom.svelte` - add button to open graph, graph panel
- `loom-mill/frontend/package.json` - add d3-force (or similar minimal graph layout library)

Read:
- `loom-mill/frontend/src/lib/design/GraphSidebar.svelte` - existing tree view (complementary)
- `loom-mill/frontend/src/lib/ws.svelte.ts` - store access pattern

Non-goals:
- Do NOT replace the GraphSidebar tree view (they complement each other)
- Do NOT add graph editing (drag to create links, etc.)
- Do NOT add graph persistence (it's a live computed view)
- Do NOT add filtering/search in the graph (future work)
- Do NOT show the full workspace graph by default (too dense; start from current record)

### Detailed Design

**Data model (computed from store)**:

```typescript
interface GraphNode {
  id: string;          // record metadata.id or path
  label: string;       // first heading or ID
  surface: string;     // 'tickets', 'specs', 'plans', etc.
  isCurrent: boolean;  // the currently-open record
}

interface GraphEdge {
  source: string;      // from node id
  target: string;      // to node id
  type: 'references' | 'depends_on';
}
```

Computation:
1. Start from the current record
2. Find all records it references (outgoing edges from `record.references`)
3. Find all records that reference it (incoming edges: scan all records for ones
   whose `references` include the current record's ID)
4. Optionally expand 1 more hop (references of references) for richer context

**Rendering**: Use d3-force (lightweight, well-understood):
- Nodes as circles with labels
- Color-coded by surface type (tickets=purple, specs=blue, plans=green, etc.)
- Current record highlighted (larger, different border)
- Edges as lines with arrow direction
- Force simulation for organic layout
- Drag to reposition nodes
- Click to navigate
- Hover to preview (title + status)

**Panel integration**: The graph opens as a panel alongside or replacing the editor:
- Button in the editor toolbar: "Graph" icon
- Opens a split view (editor left, graph right) or full-panel graph
- Toggle back to editor-only with the same button
- Graph auto-updates when the open record changes

**Styling**: Dark, calm, matches the existing Design Room aesthetic:
- Node fill: surface-specific muted color
- Edge stroke: border-subtle
- Label text: text-secondary, small (10px)
- Background: bg-primary
- Current node: accent-primary ring

## Acceptance

- ACC-001: Opening the graph from a record with references shows nodes for all
  connected records with correct edges.
  - Evidence: Open a plan that references tickets; verify all tickets appear as nodes.
  - Audit: Verify bidirectional edges (references AND referenced-by) both appear.

- ACC-002: Clicking a node in the graph navigates to that record in the editor.
  - Evidence: Click a ticket node; verify editor shows that ticket's content.
  - Audit: Verify sidebar selection syncs after navigation.

- ACC-003: Graph is visually readable for 5-20 nodes (typical record graph size).
  - Evidence: Screenshot of graph with ~10 connected records.
  - Audit: Verify labels are readable, nodes don't overlap excessively.

- ACC-004: `npm --prefix loom-mill/frontend run build` passes.
  - Evidence: Build output.

## Current State

Implementation complete inside the ticket write scope. Added the SVG d3-force
connected graph component, Design Room editor/graph toggle, click navigation, drag
repositioning, hover preview, and resize handling. Build evidence exists; manual
UI acceptance for navigation/readability remains for review.

## Evidence

- `evidence:20260526-mill-connected-graph-build` - `npm --prefix loom-mill/frontend run build` passed; supports ACC-004.

## Journal

- 2026-05-26: Created ticket. Source: operator wants Obsidian-style graph view for
  navigating record relationships.
- 2026-05-26: Started implementation from ticket scope; current session is acting
  as the bounded Ralph implementation run.
- 2026-05-26: Added `GraphView.svelte`, wired the Design Room graph toggle, and
  installed `d3-force` with TypeScript types. Build passed and evidence was
  recorded. Moved to review because manual UI checks and audit expectations remain.
