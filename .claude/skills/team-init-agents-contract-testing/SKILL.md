---
name: team-init-agents-contract-testing
description: Use when changing team initial agent selection/initialization/spawn defaults so the boot sequence stays deterministic and locked by tests/test_team_init_agents.py.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-03T00:28:12.731Z"
  updated_at: "2026-02-03T00:28:12.731Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed team startup/init-agent behavior (defaults, ordering, selection, persisted config) in `src/agent_loom/team/core.py` or `src/agent_loom/team/cli.py`.
- You touched any code that determines which agents exist at team boot and with what parameters.

## Goal

Keep team initialization deterministic and regression-tested.

## Checklist

1. Define the contract
   - What agents must exist by default?
   - What ordering must be stable?
   - What fields must be present/absent (avoid nondeterministic values and machine-specific paths)?

2. Make initialization deterministic
   - Explicit ordering for agent lists.
   - No reliance on dict/set iteration.
   - Avoid timestamps/random IDs unless explicitly required.

3. Lock it with focused tests
   - Add/update assertions in `tests/test_team_init_agents.py`.
   - If prompt assembly changed, also update `tests/test_team_prompts.py`.

4. Verification gate
   - `uv run basedpyright`
   - `uv run ruff check .`
   - `uv run pytest tests/test_team_init_agents.py`
   - (plus any directly impacted team test module, smallest set possible)

## Common failure modes

- Agent ordering drifts due to nondeterministic iteration.
- Defaults change silently without updating the contract test.
- Initialization starts depending on environment-specific paths or host state.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
