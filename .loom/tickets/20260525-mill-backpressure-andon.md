# Mill Backpressure + Andon

ID: ticket:20260525-mill-backpressure-andon
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - pattern detection thresholds affect false-positive/negative tradeoff; getting this wrong either annoys or misleads the operator.
Depends On: ticket:20260525-mill-workstation-engine, ticket:20260525-mill-pipeline-ui

## Summary

Detect mechanical failure patterns across iterations: repeated identical failures, long iteration duration, no record change after a run, subprocess crash loops, repeated modification of the same files without progress. When a configured threshold is reached, raise an andon alert in the UI and hold further automatic continuation for that workstation. The operator decides what happens next.

## Related Records

- `plan:20260525-factory-floor-mvp` - parent plan, Unit 9.
- `spec:loom-mill-factory-floor-mvp` REQ-009, REQ-010, SCN-005 - backpressure and andon behavior.
- `research:20260524-loom-mill-software-factory` Finding 8 - jidoka/autonomation, andon cord, statistical process control.

## Scope

Read scope:
- Iteration history from workstation engine (exit codes, durations, output patterns).
- State model deltas from watcher (what records changed or didn't change between iterations).
- Git diff between iterations.

Write scope:
- `loom-mill/src/loom_mill/processes/backpressure.py` - pattern detector.
- `loom-mill/src/loom_mill/workstation/` - andon state integration (hold continuation).
- `loom-mill/frontend/src/` - andon alert component, backpressure indicators.
- `.mill/patterns/` - ephemeral pattern history (not in `.loom/`).

Non-goals:
- No semantic analysis of failure causes. Patterns are mechanical: same exit code, same test name in output, same files modified, no record delta, duration exceeds threshold.
- No automatic remediation. Andon stops and shows; operator or model decides next.
- No configurable threshold UI in this ticket (hardcoded reasonable defaults; config surface is future work).

Stop conditions:
- Stop if determining "same failure" requires output parsing beyond simple string/exit-code matching (route to research on output normalization).

## Acceptance

- ACC-001: Repeated subprocess failure (same non-zero exit code N times in a row, default N=3) triggers an andon alert.
  Evidence: integration test with a command that fails 3 times; andon state asserted.

- ACC-002: Iteration duration exceeding a configured threshold (default: 2x median of previous iterations or absolute cap) triggers a backpressure warning.
  Evidence: integration test with a slow command; warning raised after threshold.

- ACC-003: No record change after a completed iteration (subprocess exited 0 but `.loom/` unchanged) triggers a backpressure warning.
  Evidence: integration test with a no-op command; warning raised.

- ACC-004: Andon state holds further automatic continuation for the affected workstation until operator acknowledges or resumes.
  Evidence: integration test showing andon → no new subprocess starts → operator resume → execution continues.

- ACC-005: Andon alert in the UI points to the relevant ticket, iteration history, and output that triggered the alert.
  Evidence: screenshot showing andon alert with context links.

## Current State

Not started. Blocked on workstation engine (Unit 5) and pipeline UI (Unit 4).

## Journal

- 2026-05-25: Created from `plan:20260525-factory-floor-mvp` Unit 9.
