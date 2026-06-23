Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/2026-06-23-calibrate-autoresearch-scorer-trust.md

# Autoresearch Scorer Calibration Evidence

## What Was Observed

A labeled calibration set exists at:

- `autoresearch/calibration/offline-trust-labels.json`

Calibration tooling exists at:

- `autoresearch/calibrate_scorer.py`

Calibration output was written to:

- `.10x/evidence/.storage/2026-06-23-scorer-calibration/scorer-calibration.json`
- `.10x/evidence/.storage/2026-06-23-scorer-calibration/scorer-calibration.md`

Command result:

```text
$ python3 autoresearch/calibrate_scorer.py --out .10x/evidence/.storage/2026-06-23-scorer-calibration
exit_code 0
recommended_trust_level 1
scores S001 S004 S007
```

Observed metrics:

```text
S001 samples=3 tp=2 fp=0 tn=1 fn=0 precision=1.0 recall=1.0 specificity=1.0 accuracy=1.0
S004 samples=3 tp=2 fp=0 tn=1 fn=0 precision=1.0 recall=1.0 specificity=1.0 accuracy=1.0
S007 samples=3 tp=2 fp=0 tn=1 fn=0 precision=1.0 recall=1.0 specificity=1.0 accuracy=1.0
```

The generated recommendation says to keep `offline-coverage-v1` at Trust Level
1 because the labeled set is useful for mismatch diagnostics but too small and
fixture-bound for Trust Level 2.

Unit tests passed:

```text
$ python3 -m unittest autoresearch.tests.test_calibrate_scorer
Ran 3 tests in 0.013s
OK
```

## Procedure

1. Created human-authored labels for S001, S004, and S007 using existing offline
   fixtures.
2. Scored the labeled fixtures through `offline_score.score_fixture`.
3. Compared expected pass/fail labels against score-threshold pass/fail results.
4. Wrote JSON and Markdown calibration summaries.
5. Added unit tests for default metrics, output writing, and missing-threshold
   rejection.

## What This Supports Or Challenges

This supports:

- `.10x/tickets/2026-06-23-calibrate-autoresearch-scorer-trust.md#AC-001`
- `.10x/tickets/2026-06-23-calibrate-autoresearch-scorer-trust.md#AC-002`
- `.10x/tickets/2026-06-23-calibrate-autoresearch-scorer-trust.md#AC-003`
- `.10x/tickets/2026-06-23-calibrate-autoresearch-scorer-trust.md#AC-005`

This challenges any move to Trust Level 2 or 3 based only on the current small
fixture-bound label set.

## Limits

The apparent perfect metrics are not promotion-grade. They cover only nine
score-label checks across existing fixtures. They do not establish robustness on
live agent outputs, adversarial outputs, new scenario families, or cross-harness
transcripts.
