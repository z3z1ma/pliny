# Mill UI Design System: Linear-Inspired Theme

ID: ticket:20260525-mill-linear-theme
Type: Ticket
Status: closed
Created: 2026-05-25
Updated: 2026-05-25
Risk: low - purely visual/CSS changes with no backend or behavioral impact.

## Summary

Restyle the Loom Mill Factory Floor frontend to match Linear's design language: clean, minimal, refined typography, subtle depth, muted color palette, tight spacing, and both light and dark modes. The UX layout and interaction model stay the same; this is a visual quality pass.

## Related Records

- `plan:20260525-factory-floor-mvp` - parent plan for the Factory Floor MVP.
- `spec:loom-mill-factory-floor-mvp` REQ-012, Quality Bar - control room aesthetic, execution situational awareness.

## Scope

Read scope:
- `loom-mill/frontend/src/` (all existing Svelte components and CSS)
- Linear's public interface for visual reference (https://linear.app)

Write scope:
- `loom-mill/frontend/src/app.css` (global styles, CSS variables, Tailwind config)
- `loom-mill/frontend/src/lib/*.svelte` (all existing components - restyle)
- `loom-mill/frontend/src/App.svelte` (layout refinement)
- `loom-mill/frontend/tailwind.config.*` or Tailwind v4 theme if applicable
- New utility components if needed (e.g., Badge.svelte, Icon set)

Non-goals:
- Do not change the information architecture, component hierarchy, or interaction behavior.
- Do not add new features or functional components.
- Do not change the backend, API, or WebSocket protocol.
- Do not add external UI framework dependencies (shadcn, skeleton, etc.). Tailwind + custom components only.

Stop conditions:
- Stop if Tailwind v4 theme system creates blockers (fall back to CSS variables + v3 config).
- Stop if a specific Linear pattern requires JS animation libraries not yet in deps (note it, don't add).

## Acceptance

- ACC-001: Dark mode as default with a toggle for light mode. Both modes should be cohesive, not an afterthought.
  Evidence: Playwright screenshots in both modes showing consistent visual quality.

- ACC-002: Color palette matches Linear's feel: neutral grays for backgrounds, muted accent colors (violet/indigo range for primary), subtle borders, no harsh neon or saturated colors.
  Evidence: Side-by-side visual comparison showing refined palette.

- ACC-003: Typography uses Inter or system font stack with Linear-style sizing: tight line heights, medium weight for headings, small/muted for secondary text, monospace for IDs/codes.
  Evidence: Screenshot showing type hierarchy.

- ACC-004: Card/panel styling uses subtle depth (very light shadows or borders, not heavy drop shadows), consistent rounded corners (small radius like 6-8px), and clean spacing.
  Evidence: Screenshot showing ticket cards and panels with refined surfaces.

- ACC-005: Status badges, indicators, and buttons match Linear's understated style: pill badges with muted fills, small/refined buttons, no garish colors.
  Evidence: Screenshot showing status indicators and controls.

- ACC-006: The overall layout feels dense but not cramped, professional, and calm. No visual noise.
  Evidence: Full-page screenshot that looks like it could ship as a product.

## Design Direction

Reference Linear's visual characteristics:
- Background: very dark navy/slate in dark mode, near-white in light mode
- Surfaces: slightly elevated cards with 1px borders, not shadows
- Text: high contrast primary, low contrast secondary, very small/muted tertiary
- Accent: violet/indigo for interactive elements, not blue/cyan
- Status colors: muted versions (not saturated green/red/yellow)
- Spacing: 4px grid, tight but breathable
- Borders: 1px, very subtle (opacity 10-15% in dark mode)
- Transitions: 150ms ease for hover states, nothing flashy
- Icons: lucide or similar thin line icons if needed (optional)

## Current State

Not started.

## Journal

- 2026-05-25: Created. Operator wants Linear-inspired visual refinement plus light/dark mode toggle.
