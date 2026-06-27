Status: recorded
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Relates-To: .10x/research/EXP-YYYYMMDD-NNN-short-slug.md

# Manual Inspection: EXP-YYYYMMDD-NNN-short-slug

## Scope

Experiment, scenario, arm, sample, rubric criteria, and raw artifacts inspected.

## Required Checks

- The rubric judgment matches subject behavior, not quoted instructions or templates.
- The scenario included the inputs it claimed to include.
- The control actually elicited the target failure when required.
- The candidate did not improve by silently narrowing scope.
- The judgment rationale points to real output.
- No high-severity failure is hidden behind a passing aggregate judgment.

## Recording Triggers

Record this inspection when any applies:

- A result supports promotion.
- A rubric or tooling mismatch is found.
- A run is surprising or contradicts prediction.
- A control fails to fail.
- A candidate backfires.
- A full-run component fails despite a passing final verdict.

## Observations

Raw observations with artifact references, transcript lines, files, diffs, and
command or workspace artifact paths.

## Findings

Rubric judgments confirmed, rubric judgments rejected, false positives, false
negatives, hidden high-severity failures, scope shrinkage, seed-state problems,
and control validity.

## Conclusion And Limits

What the inspection supports or challenges, what remains unverified, and whether
the result is preliminary, promotion-supporting, rejected, inconclusive, or
requires follow-up.
