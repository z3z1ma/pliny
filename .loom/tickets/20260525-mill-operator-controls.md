# Mill Operator Controls + Harness Config

ID: ticket:20260525-mill-operator-controls
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - convergence point connecting visibility and execution; integration complexity.
Depends On: ticket:20260525-mill-pipeline-ui, ticket:20260525-mill-workstation-engine

## Summary

Connect the pipeline UI (visibility) to the workstation engine (execution). Add a harness configuration surface where the operator selects command, model, and flags. Add start/pause/stop controls per ticket in the dashboard. Show workstation state (idle, running, paused, stopped, exit code) in the pipeline view.

## Related Records

- `plan:20260525-factory-floor-mvp` - parent plan, Unit 6 (convergence point).
- `spec:loom-mill-factory-floor-mvp` REQ-004, REQ-006 - harness config is operator-selectable; pause/stop controls exist.

## Scope

Read scope:
- Workstation engine API from Unit 5.
- Pipeline UI components from Unit 4.
- State model from Unit 3.

Write scope:
- `loom-mill/frontend/src/` components for harness config panel, start/pause/stop buttons, workstation status indicators.
- `loom-mill/src/loom_mill/api/` REST endpoints for workstation commands (start, pause, stop) and harness config CRUD.
- `loom-mill/src/loom_mill/config/` harness config persistence (file-based in `.mill/`).

Non-goals:
- No steering (edit record + resume) in this ticket; that's Unit 7.
- No inter-iteration summary or backpressure display.
- No multiple concurrent workstations (one at a time for MVP).
- No automatic scheduling or queue management.

Stop conditions:
- Stop if the API contract between frontend and backend workstation control needs more state than the current model provides (route to state model extension).

## Acceptance

- ACC-001: Harness configuration UI allows selecting/editing command, model flag, and additional arguments, and persists the config.
  Evidence: screenshot showing config panel; file written to `.mill/config` or similar.

- ACC-002: "Start" button on an open ticket creates a workstation and begins execution with the configured harness.
  Evidence: integration test or manual evidence showing button click → workstation starts → state updates in UI.

- ACC-003: "Pause" / "Stop" buttons terminate the running subprocess and update workstation state in the UI.
  Evidence: integration test or manual evidence showing pause → process stops → UI shows paused state.

- ACC-004: Workstation state (idle, running, paused, stopped, exit status) is visible per-ticket in the pipeline view.
  Evidence: screenshot showing status indicators on tickets in different workstation states.

## Current State

Not started. Blocked on Units 4 (pipeline UI) and 5 (workstation engine).

## Journal

- 2026-05-25: Created from `plan:20260525-factory-floor-mvp` Unit 6.
