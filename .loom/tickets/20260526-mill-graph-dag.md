# DAG Hierarchy Graph View

ID: ticket:20260526-mill-graph-dag
Type: Ticket
Status: review
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - needs different layout algorithm from the connected graph; must handle cyclic references gracefully
Depends On: ticket:20260526-mill-graph-connected

## Summary

Add a directed acyclic graph view that shows the Loom ontology's structural
hierarchy. Unlike the connected-record graph (which shows any reference), this
view enforces directional structure: plans decompose into tickets, specs define
behavior for tickets, evidence supports tickets, etc.

This is most useful for:
- Understanding how a plan decomposes into work
- Seeing dependency chains between tickets
- Visualizing which specs govern which tickets
- Understanding the full lifecycle of a piece of work

Closure claim: Operators can see the structural hierarchy of their Loom workspace
as a navigable DAG, with clear parent-child and dependency relationships.

## Related Records

- `plan:20260526-mill-next-gen` - parent plan
- `ticket:20260526-mill-graph-connected` - connected graph (shares rendering infra)
- `loom-mill/frontend/src/lib/types.ts` - RecordMetadata.depends_on field

## Scope

Write:
- `loom-mill/frontend/src/lib/design/DagView.svelte` (new) - DAG layout and rendering
- `loom-mill/frontend/src/lib/design/GraphView.svelte` - add mode toggle (connected vs DAG)
- `loom-mill/frontend/src/lib/design/DesignRoom.svelte` - wire DAG mode

Read:
- Existing GraphView infrastructure from ticket:20260526-mill-graph-connected

Non-goals:
- Do NOT add graph editing (creating dependencies by dragging)
- Do NOT add cycle detection warnings (just render what exists)
- Do NOT make this the default view (it's an opt-in visualization)

### Detailed Design

**Hierarchy rules for edge direction** (parent → child):
- plan → its child tickets (tickets whose references include the plan)
- spec → tickets that reference the spec
- ticket → evidence that references the ticket
- ticket → audit that references the ticket
- plan → plan (nested plans, rare)

**Dependency edges** (uses `metadata.depends_on`):
- ticket → ticket it depends on (drawn as dashed line)

**Layout**: Top-down layered layout (Sugiyama or similar):
- Plans at the top
- Specs slightly below plans
- Tickets in the middle
- Evidence/audit at the bottom
- Dependency edges drawn as horizontal/diagonal lines

Can use d3-dag or a simple layered layout algorithm since the graph is typically
small (< 50 nodes).

**Rendering**:
- Same node/edge style as connected graph (reuse components)
- Different layout algorithm (layered vs force-directed)
- Mode toggle in the graph toolbar: "Connected" | "Hierarchy"
- Hierarchy view shows the full workspace by default (not just current record)
- Can optionally scope to "descendants of current plan" or similar

**Scope toggle**:
- "Full workspace": all records
- "Current plan": only records within the selected plan's subtree
- "Current record": the current record and its direct dependencies/dependents

## Acceptance

- ACC-001: DAG view shows plans at the top with tickets below them, connected by
  directional edges.
  - Evidence: Open DAG with a plan that has child tickets; verify layout hierarchy.
  - Audit: Verify edge direction is correct (plan → ticket, not reverse).

- ACC-002: Dependency edges (from `depends_on`) are visually distinct from hierarchy
  edges.
  - Evidence: Create two tickets where one depends on the other; verify dashed edge.
  - Audit: Verify dependency doesn't create a hierarchy relationship.

- ACC-003: Clicking a node navigates to that record.
  - Evidence: Click a node; verify editor opens that record.

- ACC-004: Mode toggle switches between connected and DAG views without losing context.
  - Evidence: Toggle between modes; verify current record stays highlighted.

- ACC-005: `npm --prefix loom-mill/frontend run build` passes.
  - Evidence: Build output.

## Current State

Implementation is complete inside the operator's narrowed write scope. Added
connected/hierarchy mode selection, full-workspace/current-subtree hierarchy scope,
layered DAG positioning, hierarchy and dependency edge differentiation, layer
labels, and current-record highlighting in `GraphView.svelte`. Build evidence
exists; manual visual UI acceptance and audit remain before closure.

## Evidence

- `evidence:20260526-mill-graph-dag-build` - `npm --prefix loom-mill/frontend run build` passed; supports ACC-005.

## Journal

- 2026-05-26: Created ticket. Source: operator wants a structured DAG view using
  Loom's ontology hierarchy for plan decomposition visualization.
- 2026-05-26: Started implementation. Current session is acting as the bounded
  Ralph implementation run; write scope narrowed to `GraphView.svelte` by the
  operator's latest instructions.
- 2026-05-26: Added hierarchy mode inside `GraphView.svelte` and verified the
  frontend production build. Moved to review because manual browser acceptance and
  audit expectations remain.
