---
name: team-mounts-contract-testing
description: Use when changing team mount behavior (typically in src/agent_loom/team/core.py) to keep mount semantics deterministic and regression-tested in tests/test_team_mounts.py.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-01T04:37:31.626Z"
  updated_at: "2026-02-01T04:37:31.626Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed mount logic in `src/agent_loom/team/core.py`.
- You changed mount data structures in `src/agent_loom/team/models.py` that affect mount behavior.
- You changed anything that alters what gets mounted, where it mounts, or how mounts are validated.

## Goal

Keep mounts deterministic, safe, and locked as a stable contract.

## Checklist

1. Define the contract
   - What mount sources are allowed?
   - What destination paths are allowed/forbidden?
   - What is the stable ordering for multiple mounts?

2. Make behavior deterministic
   - Explicitly sort mounts (stable tie-breaks).
   - Avoid dict/set iteration when producing mount lists.
   - Avoid machine-specific absolute paths in user-facing output.

3. Add/update contract tests
   - Update `tests/test_team_mounts.py` to assert stable invariants:
     - validation rules
     - ordering rules
     - error messages contain actionable context

4. Verification gate
   - `uv run basedpyright`
   - `uv run ruff check .`
   - `uv run pytest tests/test_team_mounts.py`

## Gotchas

- If mounts are rendered in CLI output, also update `tests/test_team_cli_ux.py` to keep the UX deterministic.
- Avoid embedding timestamps or random IDs in any persisted mount state or printed output.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
