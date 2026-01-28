---
name: team-prompt-contract-testing
description: Use when modifying src/agent_loom/team/prompts.py (or prompt-facing behavior in team runtime) to keep prompts deterministic and covered by tests/test_team_prompts.py.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-30T20:09:25.393Z"
  updated_at: "2026-01-30T20:09:25.393Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed prompt assembly, templates, or any code in `src/agent_loom/team/prompts.py`.
- You changed prompt-facing behavior in `src/agent_loom/team/core.py` or `src/agent_loom/team/cli.py`.
- You introduced/modified team runtime modules that influence prompt inputs (commonly `src/agent_loom/team/inbox.py`, `src/agent_loom/team/models.py`, `src/agent_loom/team/constants.py`).

## Goal

Keep prompt outputs stable, reviewable, and regression-tested.

## Steps

1. Identify the prompt contract you changed
   - Inputs: what variables/context are interpolated?
   - Outputs: what exact text format or invariants must hold?

2. Add/update tests
   - Prefer updating `tests/test_team_prompts.py`.
   - Assert on stable invariants (sections/headers/required phrases) instead of brittle full snapshots unless a full snapshot is the contract.
   - Add a regression test for any bug fix.

3. Run diagnostics and checks
   - Run LSP diagnostics on touched files via `lsp_diagnostics`.
   - Run `uv run ruff check .`.
   - Run `uv run pytest tests/test_team_prompts.py` (or the smallest relevant subset).

4. Review prompt diffs like API diffs
   - Read the final prompt text as if you are the model.
   - Confirm: no accidental leakage (paths, secrets), no contradictory instructions, no duplicated sections, and consistent terminology.

## Common failure modes

- Tests assert full prompt text but the prompt contains nondeterministic content (timestamps, paths, order-dependent dict iteration).
- Prompt changes land without corresponding test coverage, causing silent regressions.
- “Small” refactors subtly reorder or drop constraints (role, tool rules, JSON-only requirements).
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
