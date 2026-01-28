---
name: ticket-ux-contract-testing
description: Use when modifying ticket CLI UX/output (or ticket core changes that alter UX) to keep formatting deterministic and regression-tested in tests/test_ticket_ux.py.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-31T03:33:28.930Z"
  updated_at: "2026-01-31T03:33:28.930Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed ticket CLI output/formatting (commonly `src/agent_loom/ticket/cli.py`).
- You changed ticket core semantics that affect displayed UX (commonly `src/agent_loom/ticket/core.py`).
- You added/changed ticket UX tests.

## Goal

Keep ticket UX deterministic and regression-tested.

## Steps

1. Define the contract
   - Decide what must remain stable (headers, ordering, required fields, wording invariants).
   - Avoid asserting on irrelevant whitespace unless whitespace is the contract.

2. Make output deterministic
   - Use explicit ordering for lists/fields.
   - Avoid dict/set iteration order as an implicit contract.

3. Add/update focused tests
   - Prefer `tests/test_ticket_ux.py` for UX/output contracts.
   - Assert on stable invariants (or snapshot only if the full text is the contract).

4. Verification
   - Run `lsp_diagnostics` on touched files.
   - Run `uv run ruff check .`.
   - Run `uv run pytest tests/test_ticket_ux.py` (then expand if needed).

## Common failure modes

- Output changes without tests (silent UX regressions).
- Order-dependent output breaks under minor refactors.
- Tests snapshot too much nondeterministic content.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
