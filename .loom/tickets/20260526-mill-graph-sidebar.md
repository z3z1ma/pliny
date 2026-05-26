# Design Room: Record Graph Sidebar

ID: ticket:20260526-mill-graph-sidebar
Type: Ticket
Status: open
Created: 2026-05-26
Updated: 2026-05-26
Risk: low - tree rendering from existing record data

Priority: high - the navigation/wayfinding panel
Depends On: ticket:20260526-mill-design-room-shell

## Summary

Build the left panel of the Design Room: a tree view of all `.loom/` records
organized by surface type, with status-colored dots, titles, hierarchical nesting
(plan→tickets, spec→tickets via references/depends-on), ready-to-fab indicators
on tickets, and a "+ New" record creation button.

The graph sidebar is the operator's map of the entire Loom workspace. At a glance
they see: what exists, what's linked, what status things are in, and what's ready
for the factory.

Single closure claim: The graph sidebar renders all records with correct status
colors, tree hierarchy, ready indicators, and working record creation.

## Related Records

- `spec:mill-design-room` - REQ-003, REQ-004, REQ-005, REQ-015, REQ-016, REQ-017
- `plan:20260526-mill-design-room` - parent plan

## Scope

### Must Create

- `loom-mill/frontend/src/lib/design/GraphSidebar.svelte` - The full graph sidebar:
  - Header: "Records" label + "+ New" dropdown button
  - Tree organized by surface sections (collapsible):
    - Constitution (📋)
    - Specs (📐)
    - Plans (📊)
    - Tickets (🎫)
    - Research (🔬)
    - Evidence (✓)
    - Audit (🔍)
    - Knowledge (💡)
  - Each section shows records of that surface type
  - Records show: status dot + title (first heading or slug)
  - Child records nested under parents:
    - Tickets with `Depends On: plan:X` nested under that plan
    - Tickets referencing `spec:X` shown under that spec (secondary grouping)
  - Selected record has highlight ring
  - Ready-to-fab indicator on qualifying tickets (small green ✓ or filled dot)

- `loom-mill/frontend/src/lib/design/RecordNode.svelte` - Individual record row:
  - Status dot (colors per spec: green/blue/amber/red/gray)
  - Title text (truncated with tooltip for long titles)
  - Ready indicator (if ticket and qualifies)
  - Click handler → dispatch selection event
  - Subtle right-arrow icon if has children (expandable)

- `loom-mill/frontend/src/lib/design/NewRecordDropdown.svelte` - The "+ New" menu:
  - Options: Ticket, Spec, Plan, Research, Knowledge
  - Each option shows icon + label
  - Click → calls `POST /records` with surface type
  - On success → opens new record in editor, adds to graph

### Ready-to-Fab Logic

A ticket is "ready to fab" when:
1. `status` is `open` (not active, blocked, closed, cancelled)
2. All `depends_on` records have status `closed` (or the ticket has no dependencies)
3. At least one labeled_id matches `ACC-*` pattern (has acceptance criteria)
4. If the ticket references a spec, that spec's status is `active` or `accepted`

Derive this from the existing `store.state.records` data.

### Must Not Change

- Factory Floor components
- Backend (uses existing WebSocket record data + POST /records from Unit 1)
- App.svelte (beyond importing GraphSidebar into DesignRoom)

### Non-Goals

- Drag-and-drop reordering
- Visual edge lines between nodes (tree nesting is sufficient)
- Search/filter in graph (covered by existing left panel search)
- Editing records directly from the graph

## Acceptance

- ACC-001: All records from `.loom/` appear in the graph organized by surface type
  - Evidence: Playwright screenshot showing records grouped under correct surface headings
  - Audit: Verify count matches `find .loom -name '*.md' | wc -l`

- ACC-002: Status dots show correct colors (green=closed, blue=active, amber=open, red=blocked)
  - Evidence: Playwright screenshot showing different-colored dots on records with different statuses
  - Audit: Spot-check 3 records against their actual Status: field

- ACC-003: Clicking a record dispatches selection event (for editor to consume)
  - Evidence: Playwright click test → verify selected state in component
  - Audit: Verify event payload includes record path and ID

- ACC-004: Ready-to-fab indicator shows on qualifying tickets
  - Evidence: Playwright screenshot showing ✓ on a ticket meeting all criteria
  - Audit: Manually verify one ticket meets all 4 criteria

- ACC-005: "+ New" → "Ticket" creates a new record and adds it to the graph
  - Evidence: Playwright interaction: click +New → Ticket → verify new node appears in tree
  - Audit: Verify file exists on disk with template content

## Current State

Ready to start after Unit 2 (shell) lands.

## Journal

- 2026-05-26: Created ticket with Status `open`. Graph sidebar is the wayfinding
  panel. Derives hierarchy from record references and depends_on fields.
