# Mill File/Git Watcher + State Model

ID: ticket:20260525-mill-watcher
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: low - file watching is well-understood; state model is in-memory only.
Depends On: ticket:20260525-mill-record-parser

## Summary

Watch `.loom/` and git for changes using watchfiles. On change, re-parse affected records, update the in-memory state model, and emit typed events that downstream consumers (WebSocket API, UI) can subscribe to. Include git state: recent commits, current branch, dirty/clean worktree.

## Related Records

- `plan:20260525-factory-floor-mvp` - parent plan, Unit 3.
- `spec:loom-mill-factory-floor-mvp` REQ-001, REQ-003 - Mill watches .loom/ as truth source and renders pipeline state from it.

## Scope

Read scope:
- Parser module from Unit 2.
- Git state via `git` subprocess calls (log, status, branch, diff --stat).

Write scope:
- `loom-mill/src/loom_mill/watcher/` module.
- `loom-mill/src/loom_mill/state/` module (typed state model + event bus).
- Tests for watcher behavior with fixture file changes.

Non-goals:
- No WebSocket or HTTP exposure (that connects in Unit 4).
- No UI rendering.
- No subprocess/workstation management.

Stop conditions:
- Stop if watchfiles cannot detect changes inside git worktrees reliably (route to research on alternative watchers).
- Stop if full re-parse per change is too slow for 100+ record workspaces (route to incremental parsing ticket).

## Acceptance

- ACC-001: File changes in `.loom/` trigger re-parse of the affected record and emit a typed state-change event within 1 second.
  Evidence: integration test that writes a fixture record, asserts event emission with correct delta.

- ACC-002: Git state (current branch, recent commits, dirty state) is available in the state model and updates on relevant git operations.
  Evidence: integration test that creates a commit in a test repo and asserts state model reflects it.

- ACC-003: The state model exposes a snapshot API (current full state) and a subscription API (stream of deltas) for downstream consumers.
  Evidence: unit test showing both access patterns return correct typed data.

## Current State

Not started. Blocked on parser (Unit 2).

## Journal

- 2026-05-25: Created from `plan:20260525-factory-floor-mvp` Unit 3.
