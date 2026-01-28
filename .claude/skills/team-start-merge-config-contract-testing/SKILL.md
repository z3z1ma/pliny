---
name: team-start-merge-config-contract-testing
description: Use when changing team start/merge configuration wiring so defaults and rendered config stay deterministic and regression-tested in tests/test_team_start_merge_config.py.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-01T06:00:43.219Z"
  updated_at: "2026-02-01T06:00:43.219Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed how team start parameters map into merge behavior.
- You changed merge configuration defaults or validation in team startup paths.
- You edited code that affects the start-time merge config shape.

## Goal

Keep team start/merge configuration deterministic and covered by a focused contract test.

## Checklist

1. Identify the contract
   - What are the supported config inputs?
   - What are the defaults when values are omitted?
   - What is the final resolved config (shape + values) the team uses?

2. Make resolution deterministic
   - Avoid nondeterministic ordering in any serialized/rendered config.
   - Ensure defaulting is explicit and consistent.

3. Update/add contract coverage
   - Edit `tests/test_team_start_merge_config.py` to assert:
     - default config values
     - override precedence rules
     - deterministic ordering for any lists/sections

4. Verification gate
   - `uv run basedpyright`
   - `uv run ruff check .`
   - `uv run pytest tests/test_team_start_merge_config.py`

## Common failure modes

- Defaults change silently without test updates.
- Order-dependent string rendering produces flaky assertions.
- Multiple call sites resolve config differently (split-brain defaults).
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
