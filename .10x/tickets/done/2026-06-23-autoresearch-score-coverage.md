Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/done/2026-06-23-implement-autoresearch-loop.md
Depends-On: .10x/tickets/done/2026-06-23-autoresearch-offline-tracer.md

# Expand Offline Score And Scenario Coverage

## Scope

Expand the offline scoring layer from tracer coverage to the full initial score
and scenario battery required by the active spec.

Likely write scope:

- `autoresearch/offline_score.py`
- `autoresearch/fixtures/offline/`
- `autoresearch/catalogs/`
- Supporting documentation under `autoresearch/README.md`

Included:

- Add offline fixtures for SCN-001 through SCN-015 or documented successor
  fixtures.
- Add first-pass scoring coverage for S001 through S009 where offline scoring can
  honestly inspect the behavior.
- Mark scores that require live execution, cost telemetry, or human judgment as
  partial instead of faking certainty.
- Preserve known scorer limitations in machine-readable or documented form.

Excluded:

- Live MICRO runner.
- FULL harness integration.
- Trust Level 2/3 calibration claims unless separately evidenced.

Read scope:

- `.10x/tickets/done/2026-06-23-autoresearch-score-coverage.md`
- `.10x/tickets/done/2026-06-23-autoresearch-offline-tracer.md`
- `.10x/specs/10x-autoresearch-loop.md`
- `autoresearch/catalogs/scores.json`
- `autoresearch/catalogs/scenarios.json`
- `autoresearch/offline_score.py`
- `autoresearch/fixtures/offline/`
- `autoresearch/tests/`

Write scope:

- `autoresearch/offline_score.py`
- `autoresearch/fixtures/offline/`
- `autoresearch/catalogs/`
- `autoresearch/tests/`
- `autoresearch/README.md`
- This ticket's Progress And Notes section for concise worker notes.

Stop conditions:

- Stop if a score or scenario cannot be honestly represented offline; document it
  as unsupported or partial instead of inventing confidence.
- Stop if useful verification requires live API calls, subject-agent execution, or
  harness integration.
- Stop if the scorer would need to claim Trust Level 2 or higher.
- Stop if work begins to implement MICRO runner, reporting, or FULL harness
  behavior.

Verification posture:

- Test-first. Expand tests so every offline-supported scenario and score has
  checked output, and unsupported scores/scenarios are represented explicitly.

Worker output expectations:

- List files changed.
- State commands run and outputs.
- State which acceptance criteria are satisfied.
- State unsupported/partial scores and scenarios with reasons.
- State false-positive risks and what was not verified.
- State blockers and recommended next move.

## Acceptance Criteria

- AC-001: Every initial scenario has at least one saved fixture or a documented
  reason it cannot be offline-scored yet.
- AC-002: Every score S001-S009 has a first-pass scoring path or a documented
  unsupported status with reason.
- AC-003: The scorer emits confidence and limits for every per-sample score.
- AC-004: Evidence records full offline scoring output.
- AC-005: Manual inspection notes cover at least one positive and one negative
  scorer match for each core behavioral score S001-S006.

## Progress And Notes

- 2026-06-23: Ticket opened from implementation scoping.
- 2026-06-23: Status set to active for bounded worker expansion of offline score
  and scenario coverage.
- 2026-06-23: Worker expanded offline fixtures to cover SCN-001 through SCN-015,
  expanded first-pass scoring to S001-S008, marked S007/S008 partial and S009
  unsupported, and documented Trust Level 1 limits. Parent reconciliation reran
  validator, tests, and full offline scoring; recorded evidence at
  `.10x/evidence/2026-06-23-autoresearch-score-coverage.md`; ticket marked done.
- 2026-06-23: Worker expanded offline coverage to 22 fixtures covering SCN-001
  through SCN-015; added first-pass S003/S005/S007/S008 scoring, machine-readable
  support metadata for S001-S009, scenario fixture paths, coverage tests, and
  README notes. Verified `python3 autoresearch/validate.py` ->
  `autoresearch contracts valid`; `python3 -m unittest discover -s
  autoresearch/tests` -> 9 tests OK; and `python3 autoresearch/offline_score.py
  --fixtures autoresearch/fixtures/offline --out
  /tmp/10x-offline-score-coverage-20260623` -> 22 score artifacts written. Score
  inspection showed S001/S002/S003/S004/S005/S006/S008 pass fixtures score above
  paired fail fixtures. S007 and S008 remain partial Trust Level 1 heuristics;
  S009 is unsupported because cost scoring needs baseline-normalized telemetry
  and calibrated quality. No evidence record was written because this worker's
  write scope excludes `.10x/evidence/`; parent reconciliation must record the
  full offline scoring output to satisfy AC-004.

## Blockers

None.
