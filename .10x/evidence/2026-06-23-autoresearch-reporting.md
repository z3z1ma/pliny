Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-autoresearch-reporting.md, .10x/evidence/2026-06-23-autoresearch-score-coverage.md

# Autoresearch Reporting Validation

## What Was Observed

The reporting implementation added Markdown report generation from saved score
artifacts.

Changed implementation files:

- `autoresearch/report.py`
- `autoresearch/tests/test_report.py`
- `autoresearch/README.md`

Worker validation produced:

- `.10x/evidence/.storage/2026-06-23-reporting-validation/scores/`
- `.10x/evidence/.storage/2026-06-23-reporting-validation/report.md`

Worker verification reported:

```text
$ python3 -m unittest autoresearch.tests.test_report
Ran 3 tests ... OK

$ python3 autoresearch/validate.py
autoresearch contracts valid

$ python3 -m unittest discover -s autoresearch/tests
Ran 17 tests ... OK

$ python3 autoresearch/offline_score.py --fixtures autoresearch/fixtures/offline --out .10x/evidence/.storage/2026-06-23-reporting-validation/scores
wrote 22 score artifacts

$ python3 autoresearch/report.py --scores .10x/evidence/.storage/2026-06-23-reporting-validation/scores --out .10x/evidence/.storage/2026-06-23-reporting-validation/report.md
wrote .10x/evidence/.storage/2026-06-23-reporting-validation/report.md
```

Parent verification command output:

```text
$ python3 -m unittest autoresearch.tests.test_report
...
----------------------------------------------------------------------
Ran 3 tests in 0.033s

OK

$ python3 autoresearch/validate.py
autoresearch contracts valid

$ python3 -m unittest discover -s autoresearch/tests
.................
----------------------------------------------------------------------
Ran 17 tests in 0.199s

OK

$ python3 autoresearch/report.py --scores /tmp/10x-reporting.gCnjVK/scores --out /tmp/10x-reporting.gCnjVK/report.md
wrote /tmp/10x-reporting.gCnjVK/report.md
```

Parent inspection of the fresh report generation showed:

```text
score_count 22
report_exists True
## Score Vectors True
## Arm Score Comparison True
## Scenario Breakdown True
## Quality Floors And Failures True
## Result Statuses True
## Manual Inspection, Trust, And Limits True
## Costs True
floor triggered True
unknown True
```

A direct synthetic status artifact check showed:

```text
backfired True
negative True
null True
confounded True
scores.S008.backfire True
```

An ASCII source scan over `autoresearch/report.py`,
`autoresearch/tests/test_report.py`, `autoresearch/README.md`, and
`.10x/tickets/done/2026-06-23-autoresearch-reporting.md` produced no output.

## Procedure

1. Read the reporting ticket, worker output, report generator source, report
   tests, README report section, and generated validation report.
2. Ran the focused report tests.
3. Ran the static contract validator.
4. Ran the complete autoresearch unittest suite.
5. Generated 22 offline score artifacts from checked-in fixtures into a fresh
   temporary directory.
6. Generated a Markdown report from those score artifacts.
7. Checked the generated report for required sections, floor failures, and
   unknown-field rendering.
8. Built a synthetic status artifact and confirmed negative, null, backfire,
   confounded, and score-level backfire statuses render.
9. Ran an ASCII source scan over the reporting files and ticket record.

## What This Supports Or Challenges

This supports:

- `.10x/tickets/done/2026-06-23-autoresearch-reporting.md#AC-001`
- `.10x/tickets/done/2026-06-23-autoresearch-reporting.md#AC-002`
- `.10x/tickets/done/2026-06-23-autoresearch-reporting.md#AC-003`
- `.10x/tickets/done/2026-06-23-autoresearch-reporting.md#AC-004`

The observations support that `autoresearch/report.py` consumes saved
`*.score.json` artifacts, emits readable Markdown, preserves component score
vectors and floor failures instead of hiding them behind an aggregate, renders
negative/null/backfire/confounded statuses when present, and documents report
generation usage.

## Limits

This evidence does not show that:

- Reports are calibrated verdicts.
- Reports can support promotion decisions without human inspection.
- Any live MICRO or FULL harness output was produced.
- Any cost telemetry beyond fields already present in artifacts is accurate.
- UI/dashboard behavior exists.

Reports remain secondary views over score artifacts and `.10x/` records.
