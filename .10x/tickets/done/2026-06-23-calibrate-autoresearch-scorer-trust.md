Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: none
Depends-On: .10x/research/2026-06-23-first-autoresearch-calibration-campaign.md, .10x/evidence/2026-06-23-autoresearch-score-coverage.md

# Calibrate Autoresearch Scorer Trust

## Scope

Create the next calibration step for `offline-coverage-v1` so future campaigns
can decide whether any score reaches Trust Level 2.

Included:

- Build or select a labeled sample set with human verdicts for at least S001,
  S004, and S007.
- Compare scorer outputs against labels and record false positives and false
  negatives.
- Define what evidence would be required for Trust Level 2.
- Preserve manual inspection requirements for any score that remains Trust Level
  1.

Excluded:

- Claiming Trust Level 3.
- Changing active score floors or score weights.
- Using the scorer for promotion gates before calibration evidence exists.

## Acceptance Criteria

- AC-001: A labeled calibration set exists with source artifacts and human
  verdicts.
- AC-002: Scorer precision/recall or equivalent mismatch analysis is recorded
  for the targeted scores.
- AC-003: Known false positives and false negatives are updated or confirmed
  from observed evidence.
- AC-004: A review challenges any proposed trust-level change.
- AC-005: No Trust Level 2 or 3 claim is made without the required evidence and
  authority.

## Progress And Notes

- 2026-06-23: Opened from first calibration campaign because all campaign score
  artifacts were Trust Level 1 with low confidence and required manual
  inspection.
- 2026-06-23: Added `autoresearch/calibration/offline-trust-labels.json`,
  `autoresearch/calibrate_scorer.py`, and unit tests. Calibration records
  mismatch metrics for S001, S004, and S007 and keeps `offline-coverage-v1` at
  Trust Level 1. Evidence:
  `.10x/evidence/2026-06-23-autoresearch-scorer-calibration.md`. Review:
  `.10x/reviews/2026-06-23-scorer-calibration-trust.md`.

## Blockers

None.
