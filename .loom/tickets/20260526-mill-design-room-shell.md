# Design Room: Tab Navigation + Layout Shell

ID: ticket:20260526-mill-design-room-shell
Type: Ticket
Status: open
Created: 2026-05-26
Updated: 2026-05-26
Risk: low - structural layout change with clear boundaries

Priority: high - the frame all Design Room panels fill
Depends On: ticket:20260526-mill-design-room-backend

## Summary

Add top-level mode switching between "Design Room" and "Factory Floor" and create
the three-panel layout shell for the Design Room. This is the structural frame
that all subsequent panels fill.

The mode switch should be in the header (left of the title). State is preserved
across switches - returning to Factory Floor shows the same workstation selection;
returning to Design Room shows the same document open.

Single closure claim: Tab navigation works between both modes, Design Room shows
a three-panel layout shell with correct proportions, and mode state persists.

## Related Records

- `spec:mill-design-room` - REQ-001, REQ-002
- `plan:20260526-mill-design-room` - parent plan

## Scope

### Must Change

- `loom-mill/frontend/src/App.svelte` - Add `activeMode: 'design' | 'factory'`
  state. Render mode switcher in header. Conditionally render DesignRoom or
  FactoryFloor based on mode. Preserve state of each mode.

- Create `loom-mill/frontend/src/lib/DesignRoom.svelte` - The top-level Design
  Room component with three-panel layout:
  - Left: graph sidebar placeholder (240px, collapsible)
  - Center: document editor placeholder (flex)
  - Right: chat panel placeholder (360px, collapsible)
  - Collapse toggles on panel dividers

- Create `loom-mill/frontend/src/lib/FactoryFloor.svelte` - Extract the existing
  Factory Floor UI (WorkstationList + DetailPanel + StatusBar + ConnectionBanner)
  into its own component so App.svelte can switch between modes.

- Create `loom-mill/frontend/src/lib/ModeSwitch.svelte` - The tab/switch UI in the
  header. Two options: "Design Room" (pencil icon) and "Factory Floor" (factory
  icon). Active mode is visually distinct (underline or background).

### Visual Direction

The mode switch should be subtle and Linear-like:
- Two text buttons in the header, left-aligned next to "Loom Mill" title
- Active mode: text-text-primary, border-b-2 border-accent-primary
- Inactive mode: text-text-tertiary, hover:text-text-secondary
- Icons: pencil/edit for Design, factory/cog for Floor

The three-panel layout:
- Dividers: 1px border-border-default, draggable (stretch goal) or fixed
- Collapse: double-click divider or small toggle icon
- Panel headers: compact, 32px, bg-bg-surface, border-b

### Must Not Change

- Factory Floor functionality (just move it into its own component)
- WebSocket connection (shared across both modes)
- Theme, header, footer (shared chrome)

### Non-Goals

- Panel content (graph, editor, chat come in subsequent tickets)
- Responsive behavior for Design Room (handled in Unit 7)
- Animations on mode switch (handled in Unit 7)

## Acceptance

- ACC-001: Header shows mode switcher with "Design Room" and "Factory Floor" options
  - Evidence: Playwright screenshot showing both mode options in header
  - Audit: Verify active state visual distinction

- ACC-002: Clicking "Design Room" shows three-panel layout; clicking "Factory Floor" shows existing execution UI
  - Evidence: Playwright screenshots of both modes
  - Audit: Verify no content flash or reload

- ACC-003: State persists across mode switches (select a workstation in Factory Floor, switch to Design Room, switch back → same workstation selected)
  - Evidence: Playwright interaction test
  - Audit: Verify no state reset on switch

- ACC-004: Three-panel layout has correct proportions (240px + flex + 360px)
  - Evidence: Playwright screenshot with DOM measurement
  - Audit: Verify panels respect min-widths

- ACC-005: Frontend builds clean
  - Evidence: `npm --prefix loom-mill/frontend run build` output
  - Audit: No errors or warnings

## Current State

Ready to start after backend ticket lands.

## Journal

- 2026-05-26: Created ticket with Status `open`. The shell is structural work
  that enables all subsequent Design Room panels.
