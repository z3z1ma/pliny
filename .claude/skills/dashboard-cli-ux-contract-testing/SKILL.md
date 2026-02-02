---
name: dashboard-cli-ux-contract-testing
description: Use when changing src/agent_loom/dashboard/cli.py output/flags so dashboard CLI UX stays deterministic and regression-tested.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-02T21:34:28.662Z"
  updated_at: "2026-02-02T21:34:28.662Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed user-visible output or flags in `src/agent_loom/dashboard/cli.py`.
- You added/changed dashboard CLI text that users will copy/paste or parse.

## Goal

Lock dashboard CLI output as a stable contract.

## Checklist

1. Identify the UX contract
   - What exact lines/sections must appear?
   - What ordering must be stable?
   - What must never appear (secrets, nondeterministic values, machine-specific absolute paths)?

2. Make output deterministic
   - Use explicit ordering for any lists/records.
   - Avoid relying on dict/set iteration.
   - Avoid embedding timestamps/random IDs unless explicitly required.

3. Add/update a focused contract test
   - Prefer a dedicated module like `tests/test_dashboard_cli_ux.py` (or the existing dashboard CLI test module if one already exists).
   - Assert stable invariants (required blocks/lines), not full output, unless full output is intentionally the contract.

4. Verification gate
   - `uv run basedpyright`
   - `uv run ruff check .`
   - `uv run pytest tests/test_dashboard_cli_ux.py` (or the specific existing dashboard CLI test module)

## Common failure modes

- Output order changes due to nondeterministic iteration.
- Tests assert full strings that include nondeterministic data.
- CLI prints more environment data than intended (leaks absolute paths or sensitive fields).
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
