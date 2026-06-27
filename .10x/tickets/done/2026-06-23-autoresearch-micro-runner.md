Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/done/2026-06-23-implement-autoresearch-loop.md
Depends-On: .10x/tickets/done/2026-06-23-autoresearch-score-coverage.md

# Implement MICRO Runner

## Scope

Implement the first live MICRO experiment runner for controlled, repeated
subject-agent samples.

Likely write scope:

- `autoresearch/run_micro.py`
- `autoresearch/templates/`
- `autoresearch/README.md`
- `.10x/research/.storage/` or `.10x/evidence/.storage/` only for run artifacts
  produced during validation.

Included:

- Read a registered experiment record or equivalent local experiment definition.
- Run no-10x, current-10x, and candidate arms when configured.
- Enforce the accepted MICRO budget: 300 subject-agent samples or 10 wall-clock
  hours per campaign.
- Cache per scenario, variant, repetition, model, and instruction digest.
- Write raw outputs and score artifacts.
- Preserve no-10x control isolation requirements in runner design.
- Support dry-run mode that resolves planned calls without invoking a live model.

Excluded:

- Codex FULL harness integration.
- Claude/OpenCode/oh-my-pi integration.
- Live provider/API calls in this first runner slice; the first implementation
  proves dry-run and fixture-backed execution only.
- Automatic promotion decisions.
- Trust Level 3 scorer approval.

Read scope:

- `.10x/tickets/2026-06-23-autoresearch-micro-runner.md`
- `.10x/tickets/done/2026-06-23-autoresearch-score-coverage.md`
- `.10x/specs/10x-autoresearch-loop.md`
- `.10x/decisions/superseded/autoresearch-initial-implementation-defaults.md`
- `autoresearch/offline_score.py`
- `autoresearch/fixtures/offline/`
- `autoresearch/templates/experiment.md`
- `autoresearch/catalogs/`

Write scope:

- `autoresearch/run_micro.py`
- `autoresearch/templates/`
- `autoresearch/tests/`
- `autoresearch/README.md`
- `.10x/research/.storage/` or `.10x/evidence/.storage/` only for validation
  run artifacts produced during this ticket.
- This ticket's Progress And Notes section for concise worker notes.

Stop conditions:

- Stop if satisfying the ticket requires live API calls or harness execution.
- Stop if no-10x control isolation cannot be represented in the dry-run plan.
- Stop if budget enforcement cannot be tested without sleeping or long-running
  work.
- Stop if the runner starts making promotion decisions.

Verification posture:

- Test-first. Add tests for dry-run planning, missing experiment refusal, budget
  limit enforcement, cache-key determinism, and fixture-backed artifact writes.

Worker output expectations:

- List files changed.
- State commands run and outputs.
- State which acceptance criteria are satisfied.
- State what is not verified, especially live execution.
- State risks, blockers, and recommended next move.

## Acceptance Criteria

- AC-001: Dry-run mode shows planned arms, scenarios, repetitions, cache keys,
  and budget limits without live calls.
- AC-002: Runner refuses a non-exploratory MICRO run without a registered
  experiment definition.
- AC-003: Runner writes raw outputs and score artifacts to documented locations.
- AC-004: Runner enforces sample and wall-clock limits.
- AC-005: Evidence records a small safe MICRO run or dry-run plus offline-scored
  sample artifacts.

## Progress And Notes

- 2026-06-23: Ticket opened from implementation scoping.
- 2026-06-23: Status set to active for bounded implementation of dry-run and
  fixture-backed MICRO runner only.
- 2026-06-23: Worker added `autoresearch/run_micro.py`, runner tests, README
  docs, and a `micro-runner-definition` template block. The runner plans only
  dry-run or fixture-backed MICRO samples, requires registered definitions for
  non-exploratory runs, enforces 300-sample and 10-hour caps, generates
  deterministic cache keys, preserves no-10x isolation metadata, writes
  fixture-backed raw and score artifacts, and makes no live calls or promotion
  decisions. Verification passed: `python3 -m unittest
  autoresearch.tests.test_run_micro` -> 5 tests OK; `python3 -m unittest
  discover -s autoresearch/tests` -> 14 tests OK; `python3
  autoresearch/validate.py` -> `autoresearch contracts valid`; dry-run and
  fixture-backed validation artifacts written under
  `.10x/evidence/.storage/2026-06-23-micro-runner-validation/`.
- 2026-06-23: Parent verification completed. Evidence recorded at
  `.10x/evidence/2026-06-23-autoresearch-micro-runner.md`; acceptance criteria
  AC-001 through AC-005 are satisfied within the ticket's dry-run and
  fixture-backed scope.

## Blockers

Unblocked by completed `.10x/tickets/done/2026-06-23-autoresearch-score-coverage.md`.
