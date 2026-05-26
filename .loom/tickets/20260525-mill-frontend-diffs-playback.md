# Frontend: Diff Viewer + Playback

ID: ticket:20260525-mill-frontend-diffs-playback
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: low - UI rendering of diffs and timeline navigation; main concern is large diff performance.
Depends On: ticket:20260525-mill-iteration-history

## Summary

Add diff viewer component: per-iteration diff (syntax highlighted) and aggregate diff (total change for ticket). Add playback: step through completed iterations of any workstation, viewing diff + duration + SPC signals at each step. Timeline/scrubber UI for navigation.

Closure claim: The operator can view diffs per-iteration and in aggregate, and can step through iteration history like scrubbing a timeline.

## Related Records

- `spec:mill-factory-floor` REQ-006, REQ-007 - behavior contract
- `plan:20260525-production-factory-floor` Unit 8 - parent plan
- `ticket:20260525-mill-iteration-history` - provides iteration history API

## Scope

Write:
- `loom-mill/frontend/src/lib/DiffViewer.svelte` (new) - syntax-highlighted diff rendering
- `loom-mill/frontend/src/lib/Playback.svelte` (new) - iteration timeline, step controls, scrubber
- `loom-mill/frontend/src/lib/types.ts` - types for iteration/diff data
- `loom-mill/frontend/src/App.svelte` - integrate diff/playback panels

Non-goals:
- Do not change the backend iteration API
- Do not implement full code editor (read-only diff display)
- Do not implement video-style playback (step-by-step is sufficient)

## Acceptance

- ACC-001: Per-iteration diff is displayed with syntax highlighting and clear file/hunk structure.
  - Evidence: Playwright screenshot showing a diff with colored additions/deletions and file headers.
  - Audit: visual quality and readability.

- ACC-002: Aggregate diff shows total change across all iterations for a workstation.
  - Evidence: Playwright screenshot showing aggregate view.
  - Audit: verify it represents cumulative change, not just last iteration.

- ACC-003: Playback allows stepping through iterations 1-N. At each step, shows: diff, duration, SPC signal if any.
  - Evidence: Playwright test stepping through iterations and verifying content changes at each step.
  - Audit: verify timeline navigation is intuitive.

- ACC-004: Playback works for both completed and active workstations (showing iterations completed so far).
  - Evidence: Playwright test on active workstation showing partial history.
  - Audit: verify no crash on active workstation playback.

## Current State

Blocked on Unit 3 (iteration history API). Ready once iteration data is retrievable.

## Journal

- 2026-05-25: Created ticket. Source: `plan:20260525-production-factory-floor` Unit 8.
