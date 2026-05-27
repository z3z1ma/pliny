# Design Room Shaping Canvas

ID: spec:mill-shaping-canvas
Type: Spec
Status: active
Created: 2026-05-26
Updated: 2026-05-26
Replaces: spec:mill-shaping-sessions

## Summary

The shaping experience is an **infinite canvas of branching nodes**. The operator's
initial input creates the root node. AI processing branches out from that node,
creating child nodes that represent questions, observations, options, and eventually
record proposals. The canvas IS the workspace — not a timeline that feeds a
separate staging area, but the spatial decision graph itself.

This supersedes the previous "vertical timeline" design which was fundamentally
still chat with styled blocks. The novel experience is spatial, branching, and
visual.

## Core Concept

The canvas contains **nodes** connected by **edges**. Each node is one atomic unit
of interaction:

- **Input node**: Operator's raw text (the root, or a response to a question)
- **Processing node**: AI is thinking/exploring (animated, transient)
- **Question node**: AI needs clarification (has a response affordance)
- **Observation node**: AI discovered something (informational)
- **Option node**: One of several directions the work could go (selectable)
- **Record node**: A proposed Loom record (ticket, spec, plan, etc.)

Edges represent causal flow. A node can have multiple children (branching). Option
nodes exist in groups — picking one marks the others as dead (red/dimmed). Record
nodes that get accepted become the staging subgraph.

The operator sees the full decision tree growing spatially. They can zoom, pan,
and click nodes to interact. The graph is the history, the reasoning, AND the
output all in one view.

## Requirements

### REQ-001: Canvas as primary interaction surface

The shaping experience renders as a zoomable, pannable infinite canvas. Nodes
are positioned spatially with edges showing causal flow. The canvas supports
hundreds of nodes without performance degradation.

### REQ-002: Node types and rendering

Each node type has distinct visual treatment:
- Input nodes: user-colored, compact text
- Processing nodes: animated/pulsing, transient (disappear when child nodes arrive)
- Question nodes: accent-colored, contain response input or buttons
- Observation nodes: muted, expandable detail
- Option nodes: appear in a group (fan-out from parent); selectable; unchosen
  siblings turn red/dimmed with no further children
- Record nodes: rich card with surface badge, title, expandable content preview,
  accept/reject actions

### REQ-003: Branching and option selection

When the AI presents options, they appear as sibling nodes branching from the same
parent. The operator clicks one to continue. The chosen option gets children; the
unchosen options are marked as dead paths (red/dimmed border, no further expansion).
Dead branches remain visible for context but are visually recessive.

### REQ-004: Record nodes feed the staging area

Record nodes that are "accepted" by the operator appear in the staging panel.
The staging panel shows the aggregate subgraph of accepted records with their
cross-references. Commit materializes this subgraph to `.loom/`.

### REQ-005: Auto-layout with manual adjustment

Nodes are auto-positioned using a tree/DAG layout (top-down or left-right).
The operator can manually drag nodes to adjust position. Layout should minimize
edge crossings and maintain readability as the graph grows.

### REQ-006: Root node from operator input

The session starts when the operator provides text input. This becomes the root
node. AI processing begins immediately, creating child nodes as it explores,
questions, and eventually proposes records.

### REQ-007: Progressive growth

New nodes animate into existence (subtle scale-up or fade-in). The canvas
auto-pans to keep the newest "active front" visible. The operator can zoom out to
see the full tree or zoom into specific branches.

### REQ-008: Node interaction

- Click a question node → expands response input inline
- Click an option node → selects it, marks siblings dead, triggers next processing
- Click a record node → expands full content preview with accept/reject
- Hover any node → shows brief tooltip
- Double-click any node → opens detail panel/popover

### REQ-009: Staging panel (right sidebar)

Persistent sidebar showing:
- Count of accepted records by surface type
- Mini-graph of accepted record relationships
- Commit button (enabled when ≥1 record accepted)
- List of accepted records (clickable → highlights in canvas)

### REQ-010: Session persistence and resume

Canvas state (node positions, selection state, active branch) persists to
`.mill/shaping-sessions/`. Sessions resume with full visual state on refresh.

### REQ-011: AI processing is bounded and parallel

Multiple processing nodes can be active simultaneously. Each represents a bounded
harness invocation. When processing completes, the processing node is replaced by
its output nodes (questions, observations, options, or records).

### REQ-012: Reactive downstream regeneration

When the operator changes an assumption in an earlier node (edits an input, changes
an answer to a question, or picks a different option), downstream nodes that
depended on that assumption are invalidated and regenerated. This is the key
reactive property: the graph is not just append-only, it's a live dependency tree.

Invalidated nodes are marked as stale (visually dimmed), then regenerated via new
AI processing. The operator sees the downstream consequences of changing their mind
propagate through the graph.

## Scenarios

### SCN-001: Operator shapes a feature

1. Operator clicks "+New", types raw thoughts about graph visualization
2. Root input node appears on canvas
3. Processing node appears (pulsing) — AI exploring codebase
4. Processing resolves into: 1 observation node + 1 question node
5. Operator answers the question (types in the question node's input)
6. New input node appears as child of question
7. Processing node → resolves into 2 option nodes: "Force-directed only" vs "Force + DAG"
8. Operator clicks "Force + DAG" — the other option turns red
9. Processing → 3 record nodes branch out (1 spec, 1 plan, 2 tickets)
10. Operator accepts all 4 record nodes
11. Staging panel shows 4 records, commit button glows
12. Operator commits → records materialize in `.loom/`

### SCN-002: Dead branch stays visible

After operator picks option A over option B, option B is dimmed with a red border.
If the operator zooms out, they can still see the unchosen path and understand why
it was rejected. But no further nodes grow from dead branches.

### SCN-003: Canvas with 30+ nodes

After extended shaping (20 minutes), the canvas has 30+ nodes across multiple
branches. The operator can zoom out to see the full tree structure, or zoom into
a specific branch. Auto-layout keeps the graph readable.

## Non-examples

- NOT a vertical scrolling timeline (that's chat)
- NOT a sidebar graph next to a text editor (that's annotation)
- NOT a form wizard (that's sequential)
- NOT a mind-map where the user builds the graph manually (the AI grows it)

## What this spec does NOT cover

- The AI reasoning/prompting strategy (uses existing shaping engine)
- The specific harness commands used
- The Markdown editor (separate mode)
- The Factory Floor

## Open Questions

All resolved.

## Resolved Decisions

- **Canvas rendering**: Svelvet (Svelte-native node graph library). Gives us
  reactive node connections — changing assumptions in a node can regenerate
  connected downstream nodes reactively. Provides zoom/pan, node dragging,
  edge routing, and Svelte component nodes out of the box.

- **Dead branch visibility**: Always visible by default. Add a "collapse dead
  branches" toggle. Full tree shows reasoning history; collapsed view focuses
  on the active path.

- **Chat panel**: Goes away in shaping mode. The canvas IS the interaction. For
  existing records, editor + chat remain as-is. "New" enters canvas mode;
  opening existing records enters editor mode.

## Evidence Expectations

- A canvas with 10+ nodes across 3+ branches, visually readable
- Option selection marking siblings as dead paths
- Record nodes accepted and visible in staging panel
- Commit producing correct records on disk
- Session resume with full canvas state preserved
