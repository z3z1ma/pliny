# Shipping Dock

ID: ticket:20260525-mill-shipping-dock
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - parallel worktree merging can produce conflicts; git operations need careful sequencing.
Depends On: ticket:20260525-mill-multi-workstation

## Summary

Implement the merge workflow for finished workstations. Two modes: auto-merge (after ticket reaches ready-to-ship status) and operator-approved (queues for manual trigger). Configurable target branch per-factory (default) and per-ticket (override). Merge with `--no-ff`. Conflict detection triggers jidoka (workstation enters conflict state, andon fires). Worktree cleanup after successful merge. Notify scheduler of freed capacity.

Closure claim: Completed tickets merge to configurable target branch via auto or manual mode, with jidoka on conflicts and clean worktree teardown.

## Related Records

- `spec:mill-shipping-dock` REQ-001 through REQ-011 - full behavior contract
- `plan:20260525-production-factory-floor` Unit 6 - parent plan
- `ticket:20260525-mill-multi-workstation` - prerequisite (provides workstation lifecycle)

## Scope

Write:
- `loom-mill/src/loom_mill/shipping/` (new module) - merge engine: mode selection, target branch resolution, merge execution, conflict detection, cleanup
- `loom-mill/src/loom_mill/api/` - endpoints: POST ship, POST skip, POST abort, POST resolve-conflict, GET queue
- `loom-mill/tests/` - shipping tests with mock git repos

Non-goals:
- Do not push to remote (local merge only)
- Do not implement PR creation
- Do not implement squash merge (--no-ff only for now)
- Do not build frontend shipping UI (Unit 9)

## Acceptance

- ACC-001: Auto-merge mode: ticket reaching ready-to-ship status triggers automatic merge to target branch.
  - Evidence: pytest test with mock git repo showing merge commit created on target branch.
  - Audit: verify trigger mechanism and merge commit format.

- ACC-002: Operator-approved mode: ticket queues at shipping dock, merge only on explicit trigger.
  - Evidence: pytest test showing ticket queues and only merges on API call.
  - Audit: verify no auto-merge in this mode.

- ACC-003: Target branch is configurable per-factory (default) with per-ticket override.
  - Evidence: pytest test with factory default `dev` and ticket override `feature/x`, verifying correct targets.
  - Audit: verify override lookup mechanism.

- ACC-004: Merge conflicts trigger jidoka: workstation enters `conflict` state, conflict files are reported.
  - Evidence: pytest test with conflicting changes showing conflict detection and state transition.
  - Audit: verify no data loss on conflict.

- ACC-005: Successful merge cleans up worktree and notifies scheduler of freed capacity.
  - Evidence: pytest test verifying worktree deletion and scheduler notification event.
  - Audit: verify cleanup is safe (no uncommitted work lost).

- ACC-006: Sequential merges: when A and B both target `dev`, B's merge includes A's changes.
  - Evidence: pytest test showing sequential merge correctness.
  - Audit: verify rebase/merge-from-target logic.

## Current State

Blocked on Unit 1. Ready once multi-workstation lifecycle exists.

## Journal

- 2026-05-25: Created ticket. Source: `plan:20260525-production-factory-floor` Unit 6.
