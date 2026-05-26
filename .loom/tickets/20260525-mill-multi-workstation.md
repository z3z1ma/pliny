# Multi-Workstation Engine

ID: ticket:20260525-mill-multi-workstation
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - core concurrency change to the workstation engine; asyncio subprocess management at scale needs careful design.

## Summary

Generalize the workstation engine from single-ticket to N concurrent workstations. Each workstation gets a stable ID, owns one worktree + harness subprocess + event stream. The WebSocket protocol gains workstation_id multiplexing. WIP limit enforcement blocks new starts when at capacity.

Closure claim: N workstations can run concurrently with independent worktrees, subprocesses, and multiplexed WebSocket events, with WIP limits enforced.

## Related Records

- `spec:mill-factory-floor` REQ-001, REQ-002, REQ-009, REQ-015, REQ-017, REQ-018 - behavior contract
- `plan:20260525-production-factory-floor` Unit 1 - parent plan
- `loom-mill/src/loom_mill/workstation/` - existing single-workstation engine to generalize
- `loom-mill/src/loom_mill/state/` - existing state model to extend
- `loom-mill/src/loom_mill/api/` - existing WebSocket API to update

## Scope

Read:
- All existing `loom-mill/src/loom_mill/` code (understand current architecture)
- `spec:mill-factory-floor` (behavior contract)

Write:
- `loom-mill/src/loom_mill/workstation/` - refactor to manage N concurrent workstations
- `loom-mill/src/loom_mill/state/` - extend state model for multiple workstations
- `loom-mill/src/loom_mill/api/` - update WebSocket protocol with workstation_id multiplexing, add REST endpoints for workstation CRUD
- `loom-mill/tests/` - new tests for concurrent workstations and WIP limits
- `.mill/` directory structure for per-workstation runtime state

Non-goals:
- Do not implement log streaming (Unit 2)
- Do not implement iteration history persistence (Unit 3)
- Do not implement scheduling logic (Unit 5)
- Do not change the frontend yet (Units 7-9)
- Do not implement merge/shipping (Unit 6)

Stop conditions:
- If asyncio subprocess management reveals fundamental issues with concurrent worktree operations, stop and report.
- If git worktree creation/cleanup races with concurrent operations, stop and report.

## Acceptance

- ACC-001: The engine supports starting N workstations concurrently, each with its own worktree and harness subprocess.
  - Evidence: pytest test starting 3 workstations with mock harness commands, verifying all 3 run independently.
  - Audit: code review of concurrency model (asyncio tasks, subprocess lifecycle, resource cleanup).

- ACC-002: Each workstation has a stable ID and is immutably associated with one ticket.
  - Evidence: pytest test verifying workstation ID persistence and ticket association.
  - Audit: verify ID generation and immutability in code.

- ACC-003: WebSocket messages are multiplexed by workstation_id. Clients can distinguish events from different workstations.
  - Evidence: pytest test with WebSocket client receiving events from 3 workstations and correctly demultiplexing.
  - Audit: message format matches spec interface contract.

- ACC-004: WIP limits are enforced. Starting a workstation when at capacity returns an error.
  - Evidence: pytest test setting WIP=2, starting 2 workstations, verifying 3rd start is rejected.
  - Audit: verify enforcement cannot be bypassed.

- ACC-005: Workstation lifecycle (start/pause/stop/resume) works independently per workstation.
  - Evidence: pytest test pausing one workstation while others continue running.
  - Audit: verify subprocess management is per-workstation, no shared state leaks.

## Current State

Ready to start. The existing single-workstation engine in `loom-mill/src/loom_mill/workstation/` provides the base to generalize from.

## Journal

- 2026-05-25: Created ticket. Source: `plan:20260525-production-factory-floor` Unit 1. First move: read existing workstation engine, design N-concurrent architecture, implement.
