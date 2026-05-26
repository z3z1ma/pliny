# Design Room Next Generation & Factory Floor Polish

ID: plan:20260526-mill-next-gen
Type: Plan
Status: open
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - graph views need a new rendering library; shaping sessions are architecturally novel

## Summary

The next leg of Loom Mill development adds three capabilities:

1. **Factory Floor review UX**: When tickets reach review status, operators need
   convenient action buttons (Accept/Escalate/Request change) with a notes field.
   Currently there's no way to close a ticket from the Factory Floor UI.

2. **Graph views**: Two complementary visualizations in the Design Room:
   - Connected-record graph (Obsidian-style): shows the current record and all
     records it references, with click-to-navigate
   - DAG hierarchy graph: uses the ontology's native structure (plans → tickets →
     evidence, specs → tickets) for a structured directed view

3. **Shaping sessions**: A fundamentally new interaction paradigm for the Design
   Room. See `spec:mill-shaping-sessions` for the full behavioral contract. This
   is the highest-leverage feature and needs phased implementation starting with
   the staging area concept.

## Related Records

- `spec:mill-shaping-sessions` - behavioral contract for the shaping experience
- `spec:mill-design-room` - Design Room current behavior
- `spec:mill-factory-floor` - Factory Floor current behavior
- `plan:20260526-mill-factory-data-integrity` - just completed, fixes data pipeline

## Strategy

Execute in three tracks:

**Track A (quick wins)**: Review UX ticket is independent, small, and immediately
useful. Execute first.

**Track B (visualization)**: Graph views are a medium-sized frontend feature. The
relationship data already exists in the frontend store (records have `references`,
`metadata.depends_on`, and `labeled_ids`). No backend work needed. Needs a graph
rendering library (d3-force or equivalent). Execute after Track A.

**Track C (shaping sessions)**: This is architecturally novel and needs phased
implementation. The spec covers the full vision; the first executable slice is the
staging area (records in memory, not yet on disk) with basic agent-driven
questioning. Uses existing chat harness as the AI backend initially. Execute after
the spec's open questions are resolved enough to ticket.

Recovery: Tracks A and B are independently valuable. Track C can ship incrementally
—even just the staging area concept without sophisticated agent behavior would be
useful.

## Execution Units

### Unit: Factory Floor Review UX

Ticket: ticket:20260526-mill-review-ux

Add Accept/Escalate/Request-change action buttons and a notes text field when
viewing a ticket in review status in the Factory Floor detail panel. Generalist
implements the backend endpoint and basic UI; frontend-expert polishes.

Closure claim: Operators can close, escalate, or request changes on review tickets
directly from the Factory Floor UI without editing Markdown.

### Unit: Connected-Record Graph View

Ticket: ticket:20260526-mill-graph-connected

Add an Obsidian-style force-directed graph view to the Design Room showing the
currently-open record and all records it references (and that reference it).
Clicking a node navigates to that record. Uses the existing `references` and
`depends_on` data from the store.

Closure claim: Operators can visualize and navigate record relationships from any
open record in the Design Room.

### Unit: DAG Hierarchy Graph View

Ticket: ticket:20260526-mill-graph-dag

Add a directed acyclic graph view that uses the Loom ontology hierarchy: plans
contain tickets, specs are referenced by tickets, evidence supports tickets, etc.
Useful for understanding plan decomposition and dependency chains. Separate view
mode from the connected-record graph.

Closure claim: Operators can see the structural hierarchy of their Loom workspace
as a navigable DAG.

### Unit: Shaping Sessions MVP

Ticket: (not yet created - depends on spec refinement)

First implementation slice of `spec:mill-shaping-sessions`. The MVP likely includes:
- Session state management (staged records in `.mill/shaping-sessions/`)
- Basic staging area UI showing proposed records
- Agent interaction using the existing chat harness with structured prompting
- Commit flow to materialize staged records to `.loom/`

This ticket will be created after the spec's open questions (OQ-001 through OQ-006)
are resolved enough to bound the first slice.

## Milestones

### Milestone: Factory Floor Complete

Child tickets: ticket:20260526-mill-review-ux

True when: Operators can act on review tickets from the Factory Floor without
touching Markdown files.

### Milestone: Visualization Available

Child tickets: ticket:20260526-mill-graph-connected, ticket:20260526-mill-graph-dag

True when: Both graph views are functional and navigable from the Design Room.

### Milestone: Shaping Sessions MVP

Child tickets: (shaping sessions ticket, to be created)

True when: An operator can start a shaping session, have the agent propose records
into a staging area, and commit the staged records to disk.

## Current State

Plan created. Spec for shaping sessions filed as draft. Notification bug already
fixed. Review UX and graph view tickets ready to be created and executed.

## Journal

- 2026-05-26: Created plan with Status `open`. Factory data integrity plan just
  completed. Moving to next capabilities: review UX, graph views, shaping sessions.
  Spec filed for shaping sessions since it's architecturally novel.
