---
name: workspace-cli-ux-contract-testing
description: Use when changing src/agent_loom/workspace/cli.py output/flags to keep workspace CLI UX deterministic and regression-tested (prefer tests/test_workspace_cli_ux.py).
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-01T07:19:01.982Z"
  updated_at: "2026-02-01T07:19:01.982Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed user-visible output, flags, formatting, ordering, or headings in `src/agent_loom/workspace/cli.py`.
- You changed anything that prints worktree paths, repo status, or lists of worktrees.

## Goal

Lock the workspace CLI output as a stable, deterministic contract.

## Checklist

1. Identify the UX contract
   - What lines/sections must appear?
   - What ordering must be stable?
   - What must never appear (timestamps, random IDs, machine-specific absolute paths)?

2. Make output deterministic
   - Use explicit ordering for any listed items (sort keys, sort paths, stable grouping).
   - Avoid relying on dict/set iteration.
   - Normalize/avoid absolute paths when possible; prefer repo-relative representations.

3. Add/update a focused contract test
   - Prefer `tests/test_workspace_cli_ux.py`.
   - Assert stable invariants (required blocks/lines + ordering), not full output, unless the full output is the contract.

4. Verification gate
   - `uv run basedpyright`
   - `uv run ruff check .`
   - `uv run pytest tests/test_workspace_cli_ux.py` (or the smallest relevant workspace CLI test module)

## Common failure modes

- Output order flips due to nondeterministic iteration.
- Tests assert full strings that contain machine-specific paths.
- CLI emits extra debug/noise without updating the UX contract test.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
