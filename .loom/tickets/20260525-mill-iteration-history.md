# Iteration History + Persistence

ID: ticket:20260525-mill-iteration-history
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: low - straightforward git diff capture and JSON persistence; main concern is race conditions between commit detection and subprocess activity.
Depends On: ticket:20260525-mill-multi-workstation

## Summary

Detect iteration boundaries per workstation (git commit on worktree branch, subprocess exit). Record per-iteration metadata: start/end time, duration, git diff stat, files changed, exit code, commit SHA. Persist in `.mill/workstations/{id}/iterations/{n}.json`. Provide REST API for random-access retrieval. Track takt time.

Closure claim: Every iteration is detected, recorded with full metadata, persisted in `.mill/`, and retrievable via API.

## Related Records

- `spec:mill-factory-floor` REQ-004, REQ-005, REQ-008, REQ-017 - behavior contract
- `plan:20260525-production-factory-floor` Unit 3 - parent plan
- `ticket:20260525-mill-multi-workstation` - prerequisite

## Scope

Write:
- `loom-mill/src/loom_mill/workstation/` - iteration boundary detection (git commit watcher per worktree)
- `loom-mill/src/loom_mill/state/` or new `iterations/` module - iteration data model and persistence
- `loom-mill/src/loom_mill/api/` - REST endpoints: GET iterations list, GET specific iteration, GET aggregate diff
- `.mill/workstations/{id}/iterations/` - JSON persistence
- `loom-mill/tests/` - iteration detection and persistence tests

Non-goals:
- Do not build the frontend diff viewer (Unit 8)
- Do not implement SPC analysis (Unit 4)
- Do not implement playback UI (Unit 8)

## Acceptance

- ACC-001: Git commits on a workstation's worktree branch are detected as iteration boundaries.
  - Evidence: pytest test with mock git commits triggering iteration boundary events.
  - Audit: verify detection mechanism (polling vs inotify vs git hook).

- ACC-002: Each iteration records: start time, end time, duration, git diff (stat + full diff), files changed, lines added/removed, exit code, commit SHA.
  - Evidence: pytest test verifying all metadata fields are populated correctly.
  - Audit: verify diff capture is accurate.

- ACC-003: Iteration data persists in `.mill/workstations/{id}/iterations/{n}.json` and survives process restart.
  - Evidence: pytest test writing iteration, restarting, reading back.
  - Audit: verify JSON schema matches spec interface contract.

- ACC-004: REST API supports random-access retrieval: list iterations, get specific iteration, get aggregate diff.
  - Evidence: pytest test exercising all three endpoints.
  - Audit: verify response format.

- ACC-005: Takt time (iteration duration) is tracked and emitted as a WebSocket event when iteration completes.
  - Evidence: pytest test verifying takt event contains duration and iteration number.
  - Audit: verify takt threshold comparison logic.

## Current State

Blocked on Unit 1. Ready to start once multi-workstation ships.

## Journal

- 2026-05-25: Created ticket. Source: `plan:20260525-production-factory-floor` Unit 3.
