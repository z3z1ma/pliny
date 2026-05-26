# Frontend: Multi-Workstation Panels + Log Streaming

ID: ticket:20260525-mill-frontend-workstations
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: low - primarily UI rendering work; main concern is performance with N concurrent log streams.
Depends On: ticket:20260525-mill-multi-workstation, ticket:20260525-mill-log-streaming

## Summary

Update the frontend to render N workstation panels simultaneously. Each panel shows: ticket ID, current iteration number, status (running/paused/stopped/finished/conflict), takt indicator, last commit time, and controls (pause/stop/view-logs/view-diff). Add a log panel per workstation showing streamed output. Handle WebSocket multiplexing on the client side.

Closure claim: The frontend renders N concurrent workstations with live state and log streaming without performance degradation.

## Related Records

- `spec:mill-factory-floor` REQ-011, REQ-016 - behavior contract
- `plan:20260525-production-factory-floor` Unit 7 - parent plan
- `ticket:20260525-mill-multi-workstation` - provides backend multi-workstation
- `ticket:20260525-mill-log-streaming` - provides backend log streaming

## Scope

Write:
- `loom-mill/frontend/src/lib/WorkstationPanel.svelte` (new) - individual workstation card
- `loom-mill/frontend/src/lib/LogViewer.svelte` (new) - scrollable log panel per workstation
- `loom-mill/frontend/src/lib/WorkstationGrid.svelte` (new or refactor) - grid/list of N panels
- `loom-mill/frontend/src/lib/ws.svelte.ts` - update WebSocket store for multiplexed events
- `loom-mill/frontend/src/lib/types.ts` - extend types for multi-workstation state
- `loom-mill/frontend/src/App.svelte` - integrate new layout

Non-goals:
- Do not implement diff viewer (Unit 8)
- Do not implement playback (Unit 8)
- Do not implement andon board or metrics (Unit 9)
- Do not change the backend

## Acceptance

- ACC-001: Frontend renders N workstation panels (tested with at least 3) showing correct per-workstation state.
  - Evidence: Playwright screenshot showing 3 workstation panels with distinct states.
  - Audit: visual quality matches Linear-inspired theme.

- ACC-002: Each workstation panel shows: ticket ID, iteration number, status badge, takt indicator, last commit time.
  - Evidence: Playwright screenshot with labeled elements.
  - Audit: information density is appropriate.

- ACC-003: Log viewer shows real-time streamed output per workstation without cross-contamination.
  - Evidence: Playwright test with backend running, verifying logs appear in correct panels.
  - Audit: verify log scrolling doesn't block UI.

- ACC-004: Controls (pause/stop) work per-workstation via API calls.
  - Evidence: Playwright test clicking pause on one workstation, verifying others continue.
  - Audit: verify API integration.

## Current State

Blocked on Units 1 + 2. Ready once backend multi-workstation and log streaming are available.

## Journal

- 2026-05-25: Created ticket. Source: `plan:20260525-production-factory-floor` Unit 7.
