# Scheduling Agent

ID: ticket:20260525-mill-scheduling-agent
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - dependency resolution from semi-structured records requires robust parsing; LLM heijunka advisory adds external dependency.
Depends On: ticket:20260525-mill-multi-workstation

## Summary

Implement the pull-based scheduling agent. When a workstation finishes and WIP capacity exists: scan `.loom/tickets/` for ready tickets, resolve dependencies, apply priority ordering, consult LLM advisory for heijunka (load leveling), pull the top candidate into a free workstation. Support enable/disable toggle and operator overrides (pin/exclude/reorder).

Closure claim: The factory autonomously pulls the next ready ticket when capacity exists, respecting dependencies, priority, WIP limits, and heijunka.

## Related Records

- `spec:mill-scheduling-agent` REQ-001 through REQ-009 - full behavior contract
- `plan:20260525-production-factory-floor` Unit 5 - parent plan
- `ticket:20260525-mill-multi-workstation` - prerequisite (provides workstation lifecycle events)
- `loom-mill/src/loom_mill/parser/` - existing record parser for reading ticket topology

## Scope

Write:
- `loom-mill/src/loom_mill/scheduling/` (new module) - scheduler engine: graph scan, dependency resolution, priority ranking, LLM advisory, decision logging
- `loom-mill/src/loom_mill/api/` - endpoints: GET queue, PUT overrides, PUT enable/disable, GET scheduling log
- `loom-mill/tests/` - scheduling tests with fixture ticket graphs

Non-goals:
- Do not implement the shipping dock (Unit 6) - scheduler reacts to "workstation finished" events regardless of how finish is defined
- Do not build frontend scheduling UI (Unit 9)
- Do not modify `.loom/` records (scheduler is read-only against the graph)

## Acceptance

- ACC-001: Scheduler triggers automatically when a workstation finishes and WIP capacity exists.
  - Evidence: pytest test where workstation finish event triggers scheduling pass.
  - Audit: verify trigger mechanism.

- ACC-002: Only tickets with status in configured ready set (default: `open`) are candidates.
  - Evidence: pytest test with mixed-status tickets showing correct filtering.
  - Audit: verify status check.

- ACC-003: Dependency resolution: tickets referencing unfinished tickets in Related Records are excluded.
  - Evidence: pytest test with dependency chain (A→B→C) showing correct blocking.
  - Audit: verify parsing of Related Records references.

- ACC-004: Priority ordering respects: explicit Priority field > plan ordering > creation date.
  - Evidence: pytest test with tickets having different priority sources.
  - Audit: verify precedence order.

- ACC-005: LLM heijunka advisory is consulted and its recommendation followed when available. Fallback to deterministic priority when model unavailable.
  - Evidence: pytest test with mock LLM showing advisory input format and scheduler using response. Timeout test showing fallback.
  - Audit: verify advisory is best-effort, not blocking.

- ACC-006: Operator overrides (pin, exclude, reorder) are respected over computed ordering.
  - Evidence: pytest test with pinned ticket being selected over higher-priority candidates.
  - Audit: verify override persistence.

- ACC-007: Scheduler can be disabled. When disabled, no automatic pulls occur.
  - Evidence: pytest test with disabled scheduler showing no auto-pull on workstation finish.
  - Audit: verify disable toggle.

## Current State

Blocked on Unit 1 (multi-workstation). Ready once workstation lifecycle events exist.

## Journal

- 2026-05-25: Created ticket. Source: `plan:20260525-production-factory-floor` Unit 5.
