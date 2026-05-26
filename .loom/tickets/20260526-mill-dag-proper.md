# Proper DAG Graph View

ID: ticket:20260526-mill-dag-proper
Type: Ticket
Status: open
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - needs proper DAG layout algorithm with correct ontology ordering and connected-nodes-only scope

## Summary

The current "Hierarchy" mode in the graph view is a naive layered layout that shows
all workspace records and uses incorrect layer ordering. It needs to be rebuilt as
a proper DAG view:

1. **Only show connected nodes** - like the connected graph mode, start from the
   current record and expand to connected records. Not a full-workspace dump.
2. **Correct ontology ordering**: research precedes anything (it informs all other
   surfaces), specs precede plans (specs define behavior that plans decompose into
   work), audits are children of tickets (like evidence).
3. **True DAG layout** - not a simple "group by layer" grid. Use actual DAG layout
   algorithms (Sugiyama/layered or force-directed with layer constraints) that
   respect edge direction and minimize crossings. Can be top-down or left-right.

### Correct ontology hierarchy:
- Research → can inform any surface (specs, plans, tickets, constitution)
- Constitution/Knowledge → foundational, referenced by others
- Specs → define behavior that plans and tickets implement
- Plans → decompose into tickets
- Tickets → executable work
- Evidence → supports/proves ticket claims (child of ticket)
- Audit → reviews ticket claims (child of ticket)

### Key behaviors:
- Start from current record, expand to all connected records via references
- Show directional edges (parent → child based on which surface is higher)
- Dashed edges for `depends_on` relationships between same-level nodes
- Proper edge routing that minimizes crossings
- Click-to-navigate on any node
- Current record highlighted

## Related Records

- `plan:20260526-mill-next-gen` - parent plan
- `ticket:20260526-mill-graph-dag` - previous naive implementation to replace
- `loom-mill/frontend/src/lib/design/GraphView.svelte` - existing implementation to fix

## Scope

Write:
- `loom-mill/frontend/src/lib/design/GraphView.svelte` - replace hierarchy mode with proper DAG

Non-goals:
- Do NOT change the connected (force-directed) mode
- Do NOT add new dependencies if avoidable (the existing d3-force may be sufficient with layer constraints, or use a simple Sugiyama implementation)

## Acceptance

- ACC-001: Hierarchy mode only shows nodes connected to the current record (not all workspace records).
  - Evidence: Open a plan, verify only its connected records appear.
  - Audit: Verify disconnected records are excluded.

- ACC-002: DAG respects correct ontology ordering (research at top, evidence/audit at bottom, specs above plans).
  - Evidence: Open a record that connects to multiple surfaces, verify layout order.

- ACC-003: Edge routing minimizes crossings and the graph is visually readable.
  - Evidence: Screenshot with 5-15 connected records showing clean DAG layout.

- ACC-004: `npm --prefix loom-mill/frontend run build` passes.

## Current State

Ready to start. Assigned to frontend-expert for proper DAG algorithm and visual quality.

## Journal

- 2026-05-26: Created ticket. Replaces naive hierarchy from ticket:20260526-mill-graph-dag.
