---
name: ticket-runtime-simplification-checklist
description: Use when refactoring src/agent_loom/ticket/core.py or src/agent_loom/ticket/cli.py to simplify behavior while preserving deterministic ticket UX contracts.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-03T06:27:17.969Z"
  updated_at: "2026-02-03T06:27:17.969Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You are simplifying or refactoring ticket behavior in `src/agent_loom/ticket/core.py`.
- You are changing user-facing ticket output/flags in `src/agent_loom/ticket/cli.py`.

## Goal

Make ticket internals simpler without breaking the ticket UX contract.

## Checklist

1. Identify the contract surface
   - Decide what output/fields are guaranteed and what is incidental.
   - Write the invariants down as test assertions (not prose docs).

2. Keep output deterministic
   - Explicitly sort anything originating from dict/set iteration.
   - Avoid timestamps, random IDs, or machine-specific absolute paths in output.

3. Lock the behavior with a focused UX contract test
   - Prefer `tests/test_ticket_ux.py`.
   - Assert required sections/lines and ordering; avoid brittle full snapshots unless intentionally the contract.

4. Prune docs that duplicate contracts
   - If a large cookbook is removed or shrunk, ensure the equivalent invariants exist in tests.
   - Update any `.opencode/skills/` references that pointed at removed docs/paths.

5. Verification gate
   - `uv run basedpyright`
   - `uv run ruff check .`
   - `uv run pytest tests/test_ticket_ux.py`

## Common failure modes

- Removing “helpful” docs without replacing the safety net with tests.
- Output order drifting due to nondeterministic iteration.
- Tests asserting unstable strings (paths, environment-dependent values).
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
