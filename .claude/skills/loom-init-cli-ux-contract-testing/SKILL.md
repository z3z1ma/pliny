---
name: loom-init-cli-ux-contract-testing
description: Use when reintroducing or refactoring a loom init-style flow so the CLI UX stays deterministic and regression-tested (deprecated while src/agent_loom/init/ is absent).
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-01T16:37:50.515Z"
  updated_at: "2026-02-01T16:37:50.515Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You are (re)introducing an init/bootstrap flow (for example restoring `src/agent_loom/init/cli.py`).
- You changed user-visible output or flags in an init/bootstrap command.

## Status

This checklist is **deprecated while `src/agent_loom/init/` does not exist**.
If init is removed, use `cli-command-removal-contract-checklist` instead.

## Goal

Keep `loom init` (or equivalent) output stable, minimal, and deterministic.

## Checklist

1. Identify the init UX contract
   - Required lines/sections (what the user must learn from the output).
   - Stable ordering for any listed items.
   - Prohibited output: secrets, nondeterministic values, machine-specific absolute paths.

2. Keep output deterministic
   - Explicit ordering for lists/records.
   - Avoid timestamps/random IDs unless required.

3. Add/update `tests/test_loom_init_cli_ux.py`
   - Assert required blocks/lines and ordering.
   - Prefer invariant assertions over full-output snapshots unless the snapshot is the contract.

4. Verification gate
   - `uv run basedpyright`
   - `uv run ruff check .`
   - `uv run pytest tests/test_loom_init_cli_ux.py`

## Common failure modes

- Printing absolute paths from the local machine.
- Output drift without updating the contract test.
- Overly verbose init output that obscures the next action.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
