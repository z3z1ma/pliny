---
name: team-feature-checklist
description: Use when adding/expanding team runtime (src/agent_loom/team/*): keep contracts testable, prompts deterministic, CLI output deterministic, and checks green with uv.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-30T21:10:38.504Z"
  updated_at: "2026-01-30T21:10:38.504Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You changed `src/agent_loom/team/core.py` / `src/agent_loom/team/cli.py` / `src/agent_loom/team/inbox.py` / `src/agent_loom/team/models.py` / `src/agent_loom/team/prompts.py` / `src/agent_loom/team/targets.py` / `src/agent_loom/team/merge_queue.py`.
- You changed team CLI/user-facing rendering (commonly `src/agent_loom/team/cli.py` or a dedicated output module).
- You added a new team behavior (new command, new loop, new model/state).

## Goal

Ship team features with deterministic prompts, deterministic CLI output, clean interfaces, and fast verification.

## Checklist

1. Prompt contract
   - Identify any new/changed prompt sections and invariants.
   - Update/add tests in `tests/test_team_prompts.py` to assert stable invariants.

2. CLI output contract
   - Identify user-visible text that changed (headers, ordering, required lines).
   - Make rendering deterministic (explicit ordering; no reliance on dict/set order).
   - Add/update a focused UX/contract test:
     - Prefer `tests/test_team_cli_ux.py` for CLI UX.
     - If the repo uses it, also keep `tests/test_team_ux.py` aligned.

3. Spawn/integrator contract (when startup wiring changes)
   - If you changed how a team boots an integrator or spawns agent processes, lock the invariants.
   - Add/update `tests/test_team_spawn_integrator.py` to assert deterministic startup behavior.

4. Target selection contract (when `src/agent_loom/team/targets.py` changes)
   - Ensure target selection is deterministic (stable ordering; explicit tie-break rules).
   - Add/update focused tests (create `tests/test_team_targets.py` if needed) that lock:
     - selection invariants (what must/must not be eligible)
     - ordering invariants (how ties break)

5. Shutdown/disband contract
   - If you changed any shutdown/disband semantics (resource cleanup, stopping loops, state transitions), add/update focused tests in `tests/test_team_disband.py`.

6. Ship/merge contract
   - If you changed ship/merge semantics (merge queue behavior, ticket sync, state transitions), add/update focused tests in `tests/test_team_ship_ticket_sync.py`.

7. Start/merge config contract
   - If you changed how team startup selects/validates merge configuration (flags, defaults, wiring, or invariants), add/update `tests/test_team_start_merge_config.py`.

8. Surface area audit
   - Ensure team module boundaries are clear (core vs cli vs inbox vs models vs output).
   - Ensure exports/imports are intentional (especially `src/agent_loom/team/__init__.py`).

9. Typecheck first
   - Run `uv run basedpyright`.
   - Fix errors/warnings before running lint/tests.

10. Lint
   - Run `uv run ruff check .`.

11. Targeted tests
   - Run the smallest relevant suite first:
     - Prompt changes: `uv run pytest tests/test_team_prompts.py`
     - CLI UX/output changes: `uv run pytest tests/test_team_cli_ux.py`
     - Spawn/integrator changes: `uv run pytest tests/test_team_spawn_integrator.py`
     - Targeting changes: `uv run pytest tests/test_team_targets.py` (if present)
     - Ship/merge changes: `uv run pytest tests/test_team_ship_ticket_sync.py`
     - Start/merge config changes: `uv run pytest tests/test_team_start_merge_config.py`
   - If disband/shutdown behavior changed: `uv run pytest tests/test_team_disband.py`.
   - Add/adjust any missing tests for new behavior (prefer small, direct unit tests).

12. Minimal UI drift
   - If `src/agent_loom/ui/team_ui.html` changes, ensure it stays compatible with the team CLI/runtime contract (avoid adding nondeterministic content).

## Common failure modes

- Prompt assembly changes without tests (silent regressions).
- CLI output becomes nondeterministic (ordering changes; missing required lines).
- Spawn/integrator wiring drifts without a locking test.
- Target selection becomes nondeterministic (tie-breaks, unstable iteration) without a locking test.
- Ship/merge semantics regress without a syncing test (ticket state, merge queue invariants).
- Team start/merge config wiring changes without a focused contract test (defaults/flags drift).
- CLI adds options/flags but core doesn't enforce invariants.
- Shutdown/disband semantics regress (resources left running; state inconsistencies).
- Fixing lint later snowballs (do `ruff` early).
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
