# Log Streaming

ID: ticket:20260525-mill-log-streaming
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: low - straightforward async IO piping; main concern is memory management for long-running subprocesses.
Depends On: ticket:20260525-mill-multi-workstation

## Summary

Pipe full stdout and stderr from each harness subprocess to the WebSocket in real-time, tagged by workstation ID. Stream without buffering entire output in memory. Persist full logs in `.mill/` per workstation.

Closure claim: Full subprocess output streams to the frontend per-workstation in real-time without unbounded memory growth.

## Related Records

- `spec:mill-factory-floor` REQ-003, REQ-015 - behavior contract
- `plan:20260525-production-factory-floor` Unit 2 - parent plan
- `ticket:20260525-mill-multi-workstation` - prerequisite (provides multi-workstation engine)

## Scope

Write:
- `loom-mill/src/loom_mill/workstation/` - add stdout/stderr streaming from subprocess
- `loom-mill/src/loom_mill/api/` - add log event type to WebSocket protocol
- `.mill/workstations/{id}/logs/` - persist log files
- `loom-mill/tests/` - streaming tests

Non-goals:
- Do not build frontend log panel (Unit 7)
- Do not implement log search/filtering
- Do not implement log rotation (simple truncation is fine for now)

## Acceptance

- ACC-001: Full stdout and stderr from each harness subprocess arrives at WebSocket clients in real-time (< 1 second latency), tagged by workstation ID.
  - Evidence: pytest test with subprocess writing to stdout/stderr, verifying WebSocket client receives within latency bound.
  - Audit: verify no cross-workstation contamination.

- ACC-002: Log streaming does not buffer entire subprocess output in memory. Uses async line-by-line or chunk streaming.
  - Evidence: code inspection showing streaming pattern (asyncio.StreamReader or equivalent).
  - Audit: memory profile argument in code review.

- ACC-003: Full logs persist in `.mill/workstations/{id}/logs/` for later retrieval via API.
  - Evidence: pytest test verifying log files are written and retrievable after subprocess exits.
  - Audit: verify `.mill/` location (not in `.loom/`).

## Current State

Blocked on Unit 1 (multi-workstation engine). Ready to start once that ships.

## Journal

- 2026-05-25: Created ticket. Source: `plan:20260525-production-factory-floor` Unit 2.
