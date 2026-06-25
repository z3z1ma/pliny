Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/done/2026-06-23-implement-autoresearch-loop.md
Depends-On: .10x/tickets/done/2026-06-23-autoresearch-codex-full-harness.md

# Validate Live Codex No-10x Isolation Smoke

## Scope

Run one tightly bounded live Codex smoke sample to validate actual control-arm
instruction isolation behavior beyond the fixture-smoke representation.

Included:

- Use `autoresearch/run_full_codex.py` artifacts or a follow-up runner slice as
  the basis for a single safe live Codex smoke sample.
- Run in an isolated temporary fixture workspace.
- Exercise the no-10x control arm only unless the implementation needs a matched
  current-10x smoke for comparison.
- Use `codex exec --ephemeral --json --output-last-message` and the planned
  no-10x isolation arguments, including `--ignore-user-config`.
- Capture Codex stdout/JSONL, final message, workspace manifest, raw artifact,
  score artifact, command exit code, and limits.
- Record whether `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules`, and
  `.agents/skills` were absent from the live workspace.
- Keep within the accepted FULL budget and stop after one smoke sample unless a
  precise failure requires a second diagnostic attempt.

Excluded:

- Claude Code, OpenCode, or oh-my-pi live runs.
- Promotion decisions.
- Canonical instruction changes.
- Long-running Codex tasks or campaign-scale FULL runs.

## Acceptance Criteria

- AC-001: A live Codex smoke command executes with captured exit code, JSONL or
  stdout/stderr, final-message path, and workspace manifest.
- AC-002: Evidence records whether the no-10x workspace lacked the suppressed
  instruction files and whether `--ignore-user-config` was present in the actual
  command.
- AC-003: The live smoke output is converted into an offline-score-compatible raw
  artifact and scored, or the ticket blocks with a precise format mismatch.
- AC-004: Evidence states exactly what the smoke proves and does not prove about
  Codex instruction isolation.
- AC-005: Any required runner changes are captured in this ticket or in a
  narrower child ticket before implementation.

## Progress And Notes

- 2026-06-23: Ticket opened during parent reconciliation of
  `.10x/tickets/done/2026-06-23-autoresearch-codex-full-harness.md`. The first Codex
  FULL harness slice represented and smoke-checked no-10x isolation but did not
  invoke live Codex, so actual `--ignore-user-config` behavior remains unproven.
- 2026-06-23: Worker ran one live no-10x Codex smoke in generated workspace
  `.10x/evidence/.storage/2026-06-23-codex-live-isolation-smoke/workspace/`.
  The workspace was initialized as its own empty git repo and had no
  `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules`, or `.agents/skills`
  before or after the run. Actual argv was recorded in
  `.10x/evidence/.storage/2026-06-23-codex-live-isolation-smoke/command.json`;
  it used `codex --ask-for-approval never exec --cd <workspace> --ephemeral
  --json --output-last-message <last-message> --ignore-user-config --sandbox
  read-only <prompt>`. Command started at `2026-06-23T07:53:38.158350+00:00`,
  ended at `2026-06-23T07:53:42.798358+00:00`, exited 0, and wrote
  `LIVE_CODEX_SMOKE_OK` to `last-message.txt`. JSONL captured four events
  (`thread.started`, `turn.started`, `item.completed`, `turn.completed`) with
  no subject-agent tool events. The live output was converted to raw fixture
  `.10x/evidence/.storage/2026-06-23-codex-live-isolation-smoke/raw/live-codex-isolation-smoke.json`
  and scored by `python3 autoresearch/offline_score.py --fixtures
  .10x/evidence/.storage/2026-06-23-codex-live-isolation-smoke/raw/live-codex-isolation-smoke.json
  --out .10x/evidence/.storage/2026-06-23-codex-live-isolation-smoke/scores`,
  which exited 0 and wrote
  `.10x/evidence/.storage/2026-06-23-codex-live-isolation-smoke/scores/live-codex-isolation-smoke.score.json`
  with S004 value 100.0 at Trust Level 1. This supports only the narrow claim
  that one live Codex exec in the generated workspace returned the requested
  tiny final answer without JSONL tool events or non-git workspace file writes.
  It does not prove complete instruction isolation, suppression of every
  user/project/plugin instruction source, or behavior on longer tasks; stderr
  included CODEX_HOME plugin and skill loader warnings despite
  `--ignore-user-config`. No runner change was required.
- 2026-06-23: Parent verification completed. Evidence recorded at
  `.10x/evidence/2026-06-23-codex-live-isolation-smoke.md`; AC-001 through
  AC-005 are satisfied for the one-sample smoke scope. Follow-up
  `.10x/tickets/done/2026-06-23-codex-home-isolation.md` tracks stronger CODEX_HOME
  plugin/skill isolation.

## Blockers

None.
