# Canvas Node Components

ID: ticket:20260526-mill-canvas-node-components
Type: Ticket
Status: closed
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - Svelvet custom node API constraints unknown until proof completes; interaction affordances inside nodes may be limited

Depends On: ticket:20260526-mill-canvas-svelvet-proof

## Summary

Create Svelte 5 components for each canvas node type, rendered as custom Svelvet
nodes. Each component has distinct visual treatment, interactive affordances, and
status-driven styling (active/dead/stale). These components are the visual
building blocks of the shaping canvas.

Single closure claim: All six node types render correctly as Svelvet custom nodes
with appropriate styling for each status state.

## Related Records

- `spec:mill-shaping-canvas` — REQ-002 defines node types and visual treatment;
  REQ-003 defines dead branch styling; REQ-008 defines interaction affordances
- `plan:20260526-mill-shaping-canvas` — parent plan; this is Unit 4
- `ticket:20260526-mill-canvas-svelvet-proof` — provides the Svelvet integration
  pattern that node components must follow
- `loom-mill/frontend/src/lib/design/ShapingBlock.svelte` — existing block
  rendering; visual patterns to adapt (not reuse directly)
- `loom-mill/frontend/src/lib/design/ProposalCard.svelte` — existing record card;
  interaction patterns to adapt

## Scope

**What changes:**

Create new components under `loom-mill/frontend/src/lib/design/canvas/`:

- `InputNode.svelte`: Operator's text input. Compact card with user-colored left
  border. Shows the text content. When in `stale` status: dashed border + dimmed.
  When in `dead` status: red-tinted border + 40% opacity.

- `ProcessingNode.svelte`: Transient indicator while AI is working. Pulsing
  animation, themed accent color. Shows brief context ("Exploring...",
  "Reasoning..."). Disappears (unmounts) when child nodes arrive.

- `QuestionNode.svelte`: AI question. Accent-colored left border, question text
  prominently displayed. When options exist: render clickable option buttons below
  the question. When open-ended: render a small inline textarea with submit button.
  Response affordance triggers a callback.

- `ObservationNode.svelte`: AI discovery. Muted/subtle styling. Expandable detail
  (click to show full text if long). Optional evidence section (collapsible).

- `OptionNode.svelte`: One option in a group. Contains label text. Visual states:
  - default: outlined card, neutral
  - selected: solid accent background, checkmark
  - dead: red-tinted border, greyed, strikethrough label, 40% opacity
  Click handler for selection.

- `RecordNode.svelte`: Proposed Loom record. Rich card with:
  - Surface badge (tickets/specs/plans/research) with icon and color
  - Title (bold)
  - Content preview (first 6 lines, expandable)
  - Action buttons: Accept (green), Reject (red), Edit (neutral)
  - Status indicator when accepted/rejected

- `CanvasEdge.svelte` (or edge config): Style configuration for edges:
  - Causal edges: subtle gray, slightly curved
  - Option-group edges: dashed, branch out from parent to option siblings

All components:
- Accept a `status` prop (`active` | `dead` | `stale`) and render accordingly
- Use the existing Tailwind design tokens (bg-bg-surface, text-text-primary, etc.)
- Are accessible (ARIA labels, keyboard focusable where interactive)
- Use Svelte 5 runes syntax (`$props`, `$state`, `$derived`)

**What must NOT change:**
- Existing ShapingBlock.svelte, ProposalCard.svelte (keep for now; replaced later
  in integration ticket)
- Backend code
- WebSocket store (that's the integration ticket)

**Stop condition:** If Svelvet's custom node API cannot support interactive
elements (textarea, buttons) inside nodes, document the limitation. Options:
(a) use a popover/panel that opens on node click instead of inline, or
(b) use Svelvet's `let:selected` binding to trigger an external panel.

## Acceptance

- ACC-001: All six node type components exist and render with correct visual
  treatment matching spec REQ-002
  - Evidence: A test page (or Playwright route) that renders each node type in
    isolation with sample data; screenshots captured
  - Audit: Visual comparison against spec descriptions; verify no missing elements

- ACC-002: Each component renders correctly in all three status states
  (active/dead/stale)
  - Evidence: Test page shows each node type × each status (18 combinations);
    screenshots show distinct visual differences
  - Audit: Verify dead = red/dimmed, stale = dashed/pulsing, active = normal

- ACC-003: Interactive nodes (Question, Option, Record) respond to user interaction
  - Evidence: Playwright test: click option button in QuestionNode → callback
    fires. Click OptionNode → callback fires. Click Accept in RecordNode →
    callback fires.
  - Audit: Verify callbacks receive correct data; no event propagation issues

- ACC-004: Components use Svelte 5 runes and existing design tokens
  - Evidence: Code review shows `$props()`, `$state()`, `$derived()` usage; no
    legacy Svelte 4 syntax; Tailwind classes use project tokens
  - Audit: Generalist reviews for code quality and consistency with existing
    component patterns

- ACC-005: Components integrate with Svelvet's node system (render inside Svelvet
  canvas without errors)
  - Evidence: Mount all 6 node types as Svelvet nodes on a test canvas; Playwright
    screenshot shows correct rendering within the canvas context
  - Audit: Verify nodes are draggable, connectable by edges, and respect canvas
    zoom/pan

## Current State

Ready to start after Svelvet proof passes (needs to know the custom node pattern).
First Ralph run: create component files, implement visual treatment, create test
page, capture screenshots.

## Journal

- 2026-05-26: Created ticket with Status `open`. Frontend components; depends on
  Svelvet proof for custom node API pattern.
