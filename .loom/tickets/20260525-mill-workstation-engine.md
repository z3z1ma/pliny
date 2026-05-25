# Mill Workstation Engine

ID: ticket:20260525-mill-workstation-engine
Type: Ticket
Status: closed
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - subprocess management and worktree isolation have edge cases around cleanup, signals, and concurrent access.
Depends On: ticket:20260525-mill-project-scaffold

## Summary

Backend engine that creates a git worktree for a selected ticket/execution target, starts a configured harness subprocess in that worktree, captures stdout/stderr streams and exit status, and tears down cleanly on stop. The harness command comes from operator config (RD-001). This is the execution backbone of the Factory Floor.

## Related Records

- `plan:20260525-factory-floor-mvp` - parent plan, Unit 5.
- `spec:loom-mill-factory-floor-mvp` REQ-004, REQ-005, REQ-006, REQ-011 - harness config, worktree isolation, pause/stop, protocol portability.
- `spec:ticket-owned-worker-handoffs` - worker context model; Mill preserves ticket-owned context by passing the ticket path/ID to the harness.

## Scope

Read scope:
- Git worktree mechanics (`git worktree add`, `git worktree remove`).
- Harness config model (command template, flags, model selection).
- Subprocess lifecycle patterns (asyncio.create_subprocess_exec, signal handling).

Write scope:
- `loom-mill/src/loom_mill/workstation/` module (worktree manager, subprocess runner, lifecycle state machine).
- `loom-mill/src/loom_mill/config/` module (harness configuration model).
- Tests for workstation lifecycle.

Non-goals:
- No UI or API exposure (Unit 6 connects this to the frontend).
- No inter-iteration logic (Units 8-9).
- No multiple concurrent workstations in this ticket (one workstation lifecycle is the closure claim).
- No real harness validation; any configured command is accepted.

Stop conditions:
- Stop if worktree creation fails in specific git configurations (submodules, shallow clones) and route to research.
- Stop if subprocess signal handling (SIGTERM/SIGINT) is unreliable on the target platform and route to research.

## Acceptance

- ACC-001: Given a configured harness command and a ticket path, Mill creates a git worktree, starts the subprocess in that worktree, and captures stdout/stderr streams.
  Evidence: integration test with `echo "hello"` as configured command; worktree exists during run; output captured.

- ACC-002: Subprocess exit (success or failure) is detected and the exit status is recorded in the workstation state.
  Evidence: integration test with a command that exits 0 and one that exits non-zero; both captured correctly.

- ACC-003: Stop/pause terminates the subprocess with SIGTERM, waits for exit, and records the stopped state.
  Evidence: integration test with a long-running command (`sleep 60`); stop sends signal; process exits; state is "stopped."

- ACC-004: Worktree teardown removes the worktree directory and git reference after the workstation is stopped or completed.
  Evidence: integration test shows worktree directory gone and `git worktree list` no longer includes it after teardown.

- ACC-005: Harness configuration supports at minimum: command path/name, argument template with ticket path substitution, and optional environment variables.
  Evidence: unit test shows config model accepts and renders different harness configurations.

## Current State

Not started. Blocked on scaffold (Unit 1) only. Can proceed in parallel with Units 2-4.

## Journal

- 2026-05-25: Created from `plan:20260525-factory-floor-mvp` Unit 5.
