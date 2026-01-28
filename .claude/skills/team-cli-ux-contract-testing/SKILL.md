---
name: team-cli-ux-contract-testing
description: Use when changing src/agent_loom/team/cli.py output/flags to keep team CLI UX deterministic and regression-tested in tests/test_team_cli_ux.py.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-31T16:34:02.636Z"
  updated_at: "2026-01-31T16:34:02.636Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed user-visible output or flags in `src/agent_loom/team/cli.py`.
- You changed formatting, ordering, headers, or any printed text.

## Goal

Lock the team CLI output as a stable contract.

## Checklist

1. Identify the UX contract
   - What exact lines/sections must appear?
   - What ordering must be stable?
   - What should never appear (debug noise, nondeterministic IDs, paths)?

2. Make output deterministic
   - Use explicit ordering for lists/records.
   - Avoid relying on dict/set iteration.
   - Avoid embedding timestamps/random IDs unless explicitly required.

3. Add/update `tests/test_team_cli_ux.py`
   - Capture CLI output and assert on stable invariants.
   - Prefer asserting on required blocks/lines over asserting the entire output, unless the full output is the contract.
   - If ANSI/styling exists, normalize/strip so tests assert on semantic text.

4. Run correctness checks
   - Run `uv run basedpyright`.
   - Run `uv run ruff check .`.
   - Run `uv run pytest tests/test_team_cli_ux.py`.

## Common failure modes

- Output order changes across runs due to nondeterministic iteration.
- Tests assert full strings that include nondeterministic data.
- CLI behavior changes without updating the UX contract test, causing silent drift.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
