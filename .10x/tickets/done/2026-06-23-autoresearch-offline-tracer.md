Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/done/2026-06-23-implement-autoresearch-loop.md
Depends-On: .10x/tickets/done/2026-06-23-autoresearch-contract-validator.md

# Build Offline Scoring Tracer

## Scope

Create the first offline scorer path against saved transcript/file-output
fixtures. This is the tracer bullet before broad scenario coverage or live model
execution.

Likely write scope:

- `autoresearch/offline_score.py`
- `autoresearch/fixtures/offline/`
- `autoresearch/tests/`
- `autoresearch/README.md`

Included:

- Define a minimal fixture format for saved transcript and produced-file state.
- Add representative passing and failing fixtures for SCN-001, SCN-004, SCN-008,
  and SCN-009.
- Produce a score artifact compatible with `score-artifact.schema.json`.
- Implement first-pass scoring for at least S001, S002, S004, and S006 on those
  fixtures.
- Mark all scorer outputs as Trust Level 1 unless calibration evidence justifies
  otherwise.

Excluded:

- Live API or harness calls.
- Complete coverage for every score/scenario.
- Promotion claims.

Read scope:

- `.10x/tickets/done/2026-06-23-autoresearch-offline-tracer.md`
- `.10x/tickets/done/2026-06-23-autoresearch-contract-validator.md`
- `.10x/specs/10x-autoresearch-loop.md`
- `autoresearch/catalogs/scores.json`
- `autoresearch/catalogs/scenarios.json`
- `autoresearch/schemas/score-artifact.schema.json`
- `autoresearch/validate.py`
- `autoresearch/tests/test_validate.py`

Write scope:

- `autoresearch/offline_score.py`
- `autoresearch/fixtures/offline/`
- `autoresearch/tests/`
- `autoresearch/README.md`
- This ticket's Progress And Notes section for concise worker notes.

Stop conditions:

- Stop if useful fixture scoring requires live API calls or harness execution.
- Stop if score artifact validation would require a third-party JSON Schema
  dependency; document an equivalent structural check instead.
- Stop if scoring expands beyond tracer coverage for S001, S002, S004, S006 and
  SCN-001, SCN-004, SCN-008, SCN-009.
- Stop if the scorer would need to claim Trust Level 2 or higher.

Verification posture:

- Test-first. Add fixture/test coverage showing passing and failing fixtures
  produce different numeric scores and valid score-artifact structure.

Worker output expectations:

- List files changed.
- State commands run and outputs.
- State which acceptance criteria are satisfied.
- State score limitations, false-positive risks, and what was not verified.
- State blockers and recommended next move.

## Acceptance Criteria

- AC-001: Offline scoring command reads saved fixtures and writes score artifacts.
- AC-002: Passing and failing fixtures produce different numeric scores for the
  targeted scores.
- AC-003: The generated score artifacts validate with the contract validator or a
  documented equivalent.
- AC-004: Evidence records command output and at least one inspected score
  rationale.
- AC-005: The ticket records scorer limitations and false-positive risks.

## Progress And Notes

- 2026-06-23: Ticket opened from implementation scoping.
- 2026-06-23: Status set to active for bounded worker implementation of offline
  tracer scoring only.
- 2026-06-23: Worker added stdlib offline scorer, eight pass/fail fixtures for
  SCN-001/004/008/009, focused tests, and README usage notes. Verified
  `python3 autoresearch/validate.py` -> `autoresearch contracts valid`,
  `python3 -m unittest discover -s autoresearch/tests` -> 6 tests OK, and
  `python3 autoresearch/offline_score.py --fixtures autoresearch/fixtures/offline
  --out /tmp/10x-offline-scores` -> 8 score artifacts written. Inspected
  `/tmp/10x-offline-scores/scn001-pass.score.json`: S001 value 100.0,
  rationale names ambiguity detection, inspect-before-ask, no file output,
  focused question, concrete recommendation, and record routing. Limitation:
  Trust Level 1 keyword/path heuristics can reward superficial wording or miss
  terse equivalent behavior; no live harness, API, or third-party JSON Schema
  validation was run.
- 2026-06-23: Parent reconciliation read scorer/tests/fixtures, reran validator,
  full autoresearch tests, and offline scorer into a fresh temp directory,
  inspected generated score values and one S001 rationale, recorded evidence at
  `.10x/evidence/2026-06-23-autoresearch-offline-tracer.md`, and marked the
  ticket done. Noted that SCN-009 pass S004 scores 75.0, which is pass/fail
  separation but not calibrated floor evidence.

## Blockers

None.
