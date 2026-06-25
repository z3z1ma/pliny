Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/done/2026-06-23-implement-autoresearch-loop.md
Depends-On: .10x/tickets/2026-06-23-autoresearch-micro-runner.md

# Integrate Codex FULL Harness

## Scope

Implement the first FULL harness integration using Codex after MICRO scoring is
credible.

Likely write scope:

- `autoresearch/run_full_codex.py` or a similarly narrow Codex harness module.
- `autoresearch/fixtures/full/`
- `autoresearch/README.md`
- `.10x/evidence/.storage/` for validation run artifacts.

Included:

- Run reproducible FULL fixtures under Codex.
- Record model, harness, instruction digest, fixture digest, tools, and artifact
  paths per run.
- Enforce accepted FULL budget: 20 harness runs or 36 wall-clock hours per
  campaign, with 3-hour suggested per-run stop.
- Support no-10x control isolation so project-level 10x instruction files do not
  contaminate the control arm.
- Capture enough transcript/file state for offline scoring.
- Avoid canonical 10x instruction changes.

Excluded:

- Claude Code, OpenCode, and oh-my-pi FULL harnesses.
- Automatic PR creation or release.
- Automatic promotion from one FULL run.

## Acceptance Criteria

- AC-001: Harness can perform a dry-run or safe smoke run that proves fixture
  setup and artifact paths.
- AC-002: No-10x control isolation is demonstrated or the ticket blocks with a
  precise reason.
- AC-003: Harness records required model/harness/instruction/fixture metadata.
- AC-004: Harness output can be consumed by offline scoring.
- AC-005: Evidence records the smoke run and any residual harness limitations.

## Progress And Notes

- 2026-06-23: Ticket opened from implementation scoping.
- 2026-06-23: Worker added `autoresearch/run_full_codex.py`,
  `autoresearch/tests/test_run_full_codex.py`, and validation artifacts under
  `.10x/evidence/.storage/2026-06-23-codex-full-harness-validation/`. The
  harness supports dry-run planning and fixture-smoke execution only. It records
  model, Codex harness, instruction digests, source fixture digests, planned
  raw/score/workspace/Codex artifact paths, FULL budget metadata, and
  no-10x-control isolation metadata. Verification passed: `python3 -m unittest
  autoresearch.tests.test_run_full_codex` -> 4 tests OK; `python3 -m py_compile
  autoresearch/run_full_codex.py autoresearch/tests/test_run_full_codex.py` ->
  no output; `python3 -m unittest discover -s autoresearch/tests` -> 21 tests
  OK; `python3 autoresearch/validate.py` -> `autoresearch contracts valid`;
  dry-run and fixture-smoke CLI commands both exited 0; `python3
  autoresearch/offline_score.py --fixtures
  .10x/evidence/.storage/2026-06-23-codex-full-harness-validation/raw --out
  .10x/evidence/.storage/2026-06-23-codex-full-harness-validation/rescore`
  wrote three score artifacts. AC-001, AC-003, and AC-004 are satisfied within
  dry-run/fixture-smoke scope. AC-002 is represented and smoke-checked by
  generated no-10x workspaces with no `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
  `.cursor/rules`, or `.agents/skills` present plus planned
  `--ignore-user-config`; live Codex suppression is not proven by this slice.
  AC-005 is ready for parent evidence: this worker produced artifacts and
  recorded residual limitations but did not create the top-level evidence
  record.
- 2026-06-23: Parent verification completed. Evidence recorded at
  `.10x/evidence/2026-06-23-autoresearch-codex-full-harness.md`; acceptance
  criteria AC-001 through AC-005 are satisfied within the dry-run and
  fixture-smoke scope. Follow-up live control-isolation validation is tracked in
  `.10x/tickets/done/2026-06-23-codex-live-isolation-smoke.md`.

## Blockers

None.
