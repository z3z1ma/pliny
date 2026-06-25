Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/done/2026-06-23-implement-autoresearch-loop.md
Depends-On: .10x/tickets/done/2026-06-23-autoresearch-score-coverage.md

# Generate Autoresearch Reports

## Scope

Generate secondary reports from score artifacts and `.10x/` records. Reports are
views, not canonical truth.

Likely write scope:

- `autoresearch/report.py`
- `autoresearch/reports/` or documented output paths.
- `autoresearch/README.md`

Included:

- Summarize per-score vectors.
- Compare baseline/current/candidate arms.
- Show quality floors and floor failures.
- Show scenario-level breakdown.
- Show manual inspection status.
- Show negative, null, confounded, and backfire results.
- Show costs when available.

Excluded:

- Acting as source of truth for verdicts.
- UI polish beyond readable Markdown or simple HTML.
- Live run execution.

## Acceptance Criteria

- AC-001: Report generation consumes saved score artifacts and emits a readable
  report.
- AC-002: Report preserves component failures and does not hide them behind an
  aggregate.
- AC-003: Report includes negative/null/backfire statuses when present.
- AC-004: Evidence records report generation command and an example report path.

## Progress And Notes

- 2026-06-23: Ticket opened from implementation scoping.
- 2026-06-23: Implemented `autoresearch/report.py` Markdown report generation
  from saved `*.score.json` artifacts, added focused tests in
  `autoresearch/tests/test_report.py`, and documented the CLI in
  `autoresearch/README.md`.
- 2026-06-23: Validation commands run: `python3 -m unittest
  autoresearch.tests.test_report` (3 tests OK), `python3
  autoresearch/validate.py` (`autoresearch contracts valid`), `python3 -m
  unittest discover -s autoresearch/tests` (17 tests OK), `python3
  autoresearch/offline_score.py --fixtures autoresearch/fixtures/offline --out
  .10x/evidence/.storage/2026-06-23-reporting-validation/scores`, and `python3
  autoresearch/report.py --scores
  .10x/evidence/.storage/2026-06-23-reporting-validation/scores --out
  .10x/evidence/.storage/2026-06-23-reporting-validation/report.md`.
- 2026-06-23: Validation report path:
  `.10x/evidence/.storage/2026-06-23-reporting-validation/report.md`. Not
  verified: live or FULL harness execution, promotion decisions, calibrated
  verdicts, or human inspection of scorer matches.
- 2026-06-23: Parent verification completed. Evidence recorded at
  `.10x/evidence/2026-06-23-autoresearch-reporting.md`; acceptance criteria
  AC-001 through AC-004 are satisfied within the ticket's reporting scope.

## Blockers

None.
