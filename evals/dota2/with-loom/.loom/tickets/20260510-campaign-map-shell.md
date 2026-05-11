# Campaign Map Shell

ID: ticket:20260510-campaign-map-shell
Type: Ticket
Status: closed
Created: 2026-05-10
Updated: 2026-05-10
Risk: medium - owns the main product feel, responsive structure, and accessible map navigation.
Depends On: ticket:20260510-campaign-summary-data-foundation

## Summary

Build the production-feel Campaign Map shell: the navigable territory map, top command bar, hero scouting panel, territory panel frame, responsive layout, focus states, and original RTS-inspired visual language. This slice owns structure and feel, not deep analytics internals.

## Related Records

- `plan:20260510-rts-meta-explorer` - sequences this after data foundation.
- `spec:opendota-rts-meta-explorer` - defines Campaign Map behavior and quality bar.

## Scope

May change:

- `src/main.jsx` shell/layout components
- `src/styles.css` shell/map/responsive styles
- minimal analytics helpers needed for visible hero summary

Must not change:

- deep hero endpoint behavior beyond placeholder states
- match detail endpoint behavior beyond placeholder states
- backend services or credentials

## Acceptance

- ACC-001: The primary UI is a navigable Campaign Map with named territory controls, not a dashboard/table layout.
  - Evidence: source inspection and browser observation if available.
  - Audit: challenge spec fit and visual originality.

- ACC-002: Territory controls are keyboard-focusable buttons with visible focus and active state.
  - Evidence: source/CSS inspection.
  - Audit: challenge accessible navigation shape.

- ACC-003: Layout adapts for desktop and mobile without horizontal-scroll-prone structural choices.
  - Evidence: CSS inspection; browser viewport evidence preferred if available.
  - Audit: challenge responsive risk honestly if not browser-observed.

## Current State

Closed. Campaign Map shell structure, territory navigation, responsive source rules, and focus-state source hardening are in place. Build output and focused review results are recorded in `evidence:20260510-campaign-map-shell-checks`.

Acceptance state:

- ACC-001 satisfied by source review: primary UI is a named Campaign Map with territory controls, not a dashboard/table shell.
- ACC-002 satisfied after fix: territory controls are keyboard-focusable buttons with active state and protected source-level focus inset at narrow widths.
- ACC-003 satisfied after fix: mobile flex header rows stack correctly, and major layout grids collapse in source.

This ticket does not claim real browser visual verification; that remains for `ticket:20260510-campaign-production-verification` if browser tooling is available.

## Journal

- 2026-05-10: Created from the split of cancelled `ticket:20260510-campaign-map-deep-analytics`.
- 2026-05-10: Set active after `ticket:20260510-campaign-summary-data-foundation` closed.
- 2026-05-10: Focused shell review found mobile stacking and possible focus clipping issues; fixed both in `src/styles.css`.
- 2026-05-10: Reran `npm run build` and `git diff --check`; follow-up review passed the focus clipping fix. Evidence recorded in `evidence:20260510-campaign-map-shell-checks`.
- 2026-05-10: Closed ticket; next plan move is `ticket:20260510-hero-deep-territories`.
