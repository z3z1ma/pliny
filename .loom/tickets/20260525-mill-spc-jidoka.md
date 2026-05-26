# SPC + Jidoka

ID: ticket:20260525-mill-spc-jidoka
Type: Ticket
Status: closed
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - LLM integration for pattern detection adds external dependency; mitigated by deterministic fallback rules.
Depends On: ticket:20260525-mill-iteration-history

## Summary

Implement the inter-iteration Statistical Process Control (SPC) pass. After each iteration boundary: collect structured summary from iteration history, send to configured SPC model, receive continue/alert/stop signal. On `stop`: halt workstation automatically (jidoka). Implement deterministic fallback rules for when the model is unavailable or slow. Configurable thresholds and model per-factory.

Closure claim: SPC runs after every iteration, detects configured failure patterns via LLM + fallback rules, and jidoka halts workstations on `stop` signals.

## Related Records

- `spec:mill-process-control` REQ-001 through REQ-011 - full behavior contract
- `plan:20260525-production-factory-floor` Unit 4 - parent plan
- `ticket:20260525-mill-iteration-history` - prerequisite (provides iteration data)

## Scope

Write:
- `loom-mill/src/loom_mill/processes/spc.py` (or similar) - SPC engine: data collection, LLM prompt, signal parsing, fallback rules
- `loom-mill/src/loom_mill/processes/jidoka.py` (or similar) - jidoka wiring: stop signal → workstation halt
- `loom-mill/src/loom_mill/api/` - config endpoints for SPC model, thresholds
- `loom-mill/tests/` - SPC tests with fixture iteration histories, jidoka halt tests, timeout/fallback tests

Non-goals:
- Do not build the andon board UI (Unit 9)
- Do not implement scheduling responses to jidoka stops (Unit 5)
- Do not create evidence records (SPC signals are `.mill/` runtime observations)

## Acceptance

- ACC-001: SPC runs automatically after every iteration boundary on every active workstation.
  - Evidence: pytest test showing SPC invoked after each iteration, with correct input data.
  - Audit: verify SPC is not skippable and runs for all workstations.

- ACC-002: SPC model receives structured input (not raw logs) and returns continue/alert/stop with reasoning.
  - Evidence: pytest test with mock LLM verifying prompt format and response parsing.
  - Audit: verify input is token-efficient (structured summary, not full diffs).

- ACC-003: On `stop` signal, workstation halts automatically (jidoka). No further iterations run.
  - Evidence: pytest test where mock SPC returns `stop` and workstation subprocess is terminated.
  - Audit: verify halt is immediate and clean.

- ACC-004: Deterministic fallback rules detect: same test failing 3+ iterations, same files modified 3+ iterations, monotonically increasing duration, empty diffs, scope drift.
  - Evidence: pytest tests for each pattern type with fixture iteration data.
  - Audit: verify fallback triggers when model is unavailable.

- ACC-005: SPC model and thresholds are configurable per-factory.
  - Evidence: pytest test showing different model/threshold configs produce different behavior.
  - Audit: verify config persists in `.mill/`.

## Current State

Blocked on Unit 3 (iteration history). Ready once iteration data is available.

## Journal

- 2026-05-25: Created ticket. Source: `plan:20260525-production-factory-floor` Unit 4.
