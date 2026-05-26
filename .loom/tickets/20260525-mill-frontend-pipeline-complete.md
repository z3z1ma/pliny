# Frontend: Pipeline + Andon + Metrics + Changelog

ID: ticket:20260525-mill-frontend-pipeline-complete
Type: Ticket
Status: closed
Created: 2026-05-25
Updated: 2026-05-25
Risk: low - UI rendering work integrating signals from multiple backend systems.
Depends On: ticket:20260525-mill-spc-jidoka, ticket:20260525-mill-scheduling-agent, ticket:20260525-mill-shipping-dock

## Summary

Update the pipeline to show all lifecycle stages (shaped → executing → evidence → audit → shipping → closed). Add andon board aggregating SPC stops/alerts across workstations with links to source. Add quality metrics panel (iterations/ticket, average duration, SPC stops, rework count, completion rate). Add changelog view (tickets shipped this session with summary diffs and evidence state).

Closure claim: The control room shows complete pipeline state, aggregated alerts, quality metrics, and session changelog.

## Related Records

- `spec:mill-factory-floor` REQ-010, REQ-012, REQ-013, REQ-014 - behavior contract
- `plan:20260525-production-factory-floor` Unit 9 - parent plan
- `ticket:20260525-mill-spc-jidoka` - provides SPC signals for andon board
- `ticket:20260525-mill-scheduling-agent` - provides queue state for pipeline
- `ticket:20260525-mill-shipping-dock` - provides shipping events for changelog

## Scope

Write:
- `loom-mill/frontend/src/lib/Pipeline.svelte` - update for all lifecycle stages
- `loom-mill/frontend/src/lib/AndonBoard.svelte` (new) - aggregated alert/stop view
- `loom-mill/frontend/src/lib/Metrics.svelte` (new) - quality metrics panel
- `loom-mill/frontend/src/lib/Changelog.svelte` (new) - session changelog view
- `loom-mill/frontend/src/lib/types.ts` - types for metrics, changelog, andon entries
- `loom-mill/frontend/src/App.svelte` - integrate new panels into layout

Non-goals:
- Do not change any backend logic
- Do not implement historical metrics (cross-session tracking is future work)
- Do not implement metric export

## Acceptance

- ACC-001: Pipeline shows all lifecycle stages with tickets correctly placed by their `.loom/` status.
  - Evidence: Playwright screenshot showing tickets in shaped/executing/evidence/audit/shipping/closed columns.
  - Audit: verify stage assignment logic.

- ACC-002: Andon board aggregates all SPC stops and alerts with: workstation ID, ticket, reasoning, timestamp, link to workstation.
  - Evidence: Playwright screenshot showing andon board with multiple entries.
  - Audit: verify entries link to correct workstations.

- ACC-003: Quality metrics panel shows: iterations per ticket (avg), average iteration duration, SPC stop count, rework count, completion rate.
  - Evidence: Playwright screenshot showing metrics panel with values.
  - Audit: verify calculations are correct.

- ACC-004: Changelog shows tickets shipped this session with their summary diff stats and evidence state.
  - Evidence: Playwright screenshot showing changelog entries.
  - Audit: verify changelog reflects actual shipped tickets.

## Current State

Blocked on Units 4, 5, 6 (needs SPC signals, scheduling state, shipping events). Ready once backend intelligence and shipping are available.

## Journal

- 2026-05-25: Created ticket. Source: `plan:20260525-production-factory-floor` Unit 9.
