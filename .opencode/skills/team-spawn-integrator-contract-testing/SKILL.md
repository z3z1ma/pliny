---
name: team-spawn-integrator-contract-testing
description: Use when changing team spawn/integrator behavior so startup and wiring are deterministic and regression-tested in tests/test_team_spawn_integrator.py.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-01T00:21:23.979Z"
  updated_at: "2026-02-01T00:21:23.979Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed team spawn/integrator wiring, usually in `src/agent_loom/team/core.py` or `src/agent_loom/team/cli.py`.
- You added/changed how an integrator process/module is selected, started, or configured.
- You changed what gets returned/persisted as a result of spawning (IDs, config, paths, status).

## Goal

Keep spawn/integrator behavior deterministic and locked by a focused contract test.

## Checklist

1. Define the contract
   - What exactly should be started (and what should not)?
   - What arguments/config must be passed?
   - What observable outputs must be stable (returned values, persisted state, printed summaries)?

2. Make behavior deterministic
   - Explicit ordering when building lists (agents, steps, commands).
   - Avoid relying on dict/set iteration.
   - Stub/mock nondeterminism (temp paths, timestamps, random IDs) in tests.

3. Add/update `tests/test_team_spawn_integrator.py`
   - Assert stable invariants (not incidental implementation detail).
   - Prefer direct unit-style tests over full snapshots unless the full output is the contract.

4. Verify
   - Run LSP diagnostics on touched files.
   - Run `uv run ruff check .`.
   - Run `uv run pytest tests/test_team_spawn_integrator.py`.

## Common failure modes

- Tests accidentally assert on nondeterministic content (paths, random IDs, timing).
- Spawn code changes without updating the contract test, letting wiring drift.
- Ordering-dependent behavior differs across machines/runs due to implicit iteration.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
