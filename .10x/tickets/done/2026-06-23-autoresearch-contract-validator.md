Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/done/2026-06-23-implement-autoresearch-loop.md
Depends-On: .10x/tickets/done/2026-06-23-autoresearch-static-contracts.md

# Implement Autoresearch Contract Validator

## Scope

Implement standard-library validation for the static autoresearch contracts.

Likely write scope:

- `autoresearch/validate.py`
- `autoresearch/tests/` or a minimal fixture directory if the repo has no test
  convention yet.
- Small updates to `autoresearch/README.md` documenting validation commands.

Included:

- Validate score catalog shape and ID coverage.
- Validate scenario catalog shape and ID coverage.
- Validate experiment template required fields.
- Validate score artifact schema sanity.
- Validate cross-references between requirements, scores, and scenarios where the
  static files expose those relationships.
- Return non-zero exit status on validation failure.

Excluded:

- Running subject-agent experiments.
- Scoring transcripts.
- JSON Schema dependency installation.
- Full CI integration unless it can be done with existing project conventions.

Read scope:

- `.10x/tickets/done/2026-06-23-autoresearch-contract-validator.md`
- `.10x/tickets/done/2026-06-23-autoresearch-static-contracts.md`
- `.10x/specs/10x-autoresearch-loop.md`
- `.10x/decisions/superseded/autoresearch-initial-implementation-defaults.md`
- `autoresearch/README.md`
- `autoresearch/catalogs/scores.json`
- `autoresearch/catalogs/scenarios.json`
- `autoresearch/templates/experiment.md`
- `autoresearch/templates/manual-inspection.md`
- `autoresearch/schemas/score-artifact.schema.json`

Write scope:

- `autoresearch/validate.py`
- `autoresearch/tests/` or another small local fixture directory under
  `autoresearch/`
- `autoresearch/README.md`
- This ticket's Progress And Notes section for concise worker notes.

Stop conditions:

- Stop if validation requires a dependency outside the standard library.
- Stop if a static contract appears semantically inconsistent with the active spec
  and cannot be validated without changing the prior ticket's artifacts.
- Stop if the work starts becoming scoring, running, reporting, or harness
  execution.

Verification posture:

- Test-first. The worker should include at least one invalid fixture or local test
  path that fails validation, then show the checked-in static contracts pass.

Worker output expectations:

- List files changed.
- State validation commands run and outputs.
- State which acceptance criteria are satisfied.
- State what was not verified.
- State risks, blockers, and recommended next move.

## Acceptance Criteria

- AC-001: A documented command validates all static contracts and exits zero on
  the checked-in valid state.
- AC-002: At least one intentionally invalid fixture or local test path proves the
  validator catches a missing score/scenario ID.
- AC-003: The validator uses only Python standard library or another existing
  runtime already present in the repo.
- AC-004: Evidence records the validation command and output.

## Progress And Notes

- 2026-06-23: Ticket opened from implementation scoping.
- 2026-06-23: Status set to active for bounded worker implementation of
  standard-library contract validation only.
- 2026-06-23: Worker added standard-library validator, focused unittest coverage
  for checked-in contracts plus missing S009/SCN-015 copied-contract failures,
  and README validation commands. Verified `python3 autoresearch/validate.py`
  and `python3 -m unittest discover -s autoresearch/tests` both pass.
- 2026-06-23: Parent reconciliation read validator code/tests, reran validation
  and focused tests, recorded evidence at
  `.10x/evidence/2026-06-23-autoresearch-contract-validator.md`, and marked the
  ticket done. Separate audit is deferred until scorer behavior can be challenged
  against real fixtures.

## Blockers

None.
