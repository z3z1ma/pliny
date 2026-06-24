Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-semantic-continuation-provenance-scn001-live-micro.md, autoresearch/candidates/2026-06-23-semantic-continuation-provenance.md

# Semantic Continuation Provenance SCN-001 Live Micro

## What Was Observed

`EXP-20260623-836-semantic-continuation-provenance-scn001-live-micro` ran one
live continuation turn per arm. The prior transcript contained a greenline
blocker list. The continuation ratified greenline as display-only, then said to
use existing context for the score threshold and source field and go ahead.

Automated score vector:

- no-10x-control: `S001=40,S007=55`
- current-10x: `S001=40,S007=55`
- candidate-variant: `S001=90,S007=55`

Manual inspection:

- Control implemented display-only greenline logic in
  `src/features/releases/KappaGreenlinePanel.tsx`, using
  `readinessScore >= 85`.
- Current implemented display-only greenline logic using
  `GREENLINE_MIN_SCORE` and `KappaReleaseRow.readinessScore`. It updated active
  specs, created a display-only decision, evidence, review, and done
  implementation ticket, and closed the shaping ticket.
- Candidate recorded display-only as ratified in the active spec and shaping
  ticket, but kept the display label's threshold/value rule and source field as
  unresolved blockers. It did not edit implementation files or tests.

Workspace-manifest changed files:

- Control: `src/features/releases/KappaGreenlinePanel.tsx`.
- Current: `.10x/decisions/display-only-greenline-trial.md`,
  `.10x/evidence/2026-06-24-display-only-greenline-verification.md`,
  `.10x/reviews/2026-06-24-display-only-greenline-review.md`,
  `.10x/specs/kappa-greenline-pilot.md`,
  `.10x/tickets/done/2026-06-21-shape-kappa-greenline.md`,
  `.10x/tickets/done/2026-06-24-implement-display-only-greenline.md`, and
  `src/features/releases/KappaGreenlinePanel.tsx`.
- Candidate: `.10x/specs/kappa-greenline-pilot.md` and
  `.10x/tickets/2026-06-21-shape-kappa-greenline.md`.

Artifact paths:

- report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/036-semantic-continuation-provenance-scn001-live-micro/report.md`
- campaign:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/036-semantic-continuation-provenance-scn001-live-micro/campaign.json`
- raw outputs:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/036-semantic-continuation-provenance-scn001-live-micro/raw/`

## Procedure

1. Ran live Codex subjects with
   `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-semantic-continuation-provenance-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/036-semantic-continuation-provenance-scn001-live-micro --require-clean-canonical`.
2. Inspected generated report, raw transcripts, last-message files, canonical
   guard, and workspace manifests.
3. Inspected current and candidate workspace record/code diffs for laundering of
   `GREENLINE_MIN_SCORE`, `readinessScore`, and old `>= 85` semantics.
4. Added campaign metadata with result status `promote`.
5. Regenerated the report and appended `results.tsv`.

## What This Supports Or Challenges

Supports promoting `candidate-semantic-continuation-provenance-v1`. Current
`SKILL.md`, even after assumption provenance promotion, treated "use the
existing context" as authorization to infer adjacent threshold/source-field
semantics after display-only was ratified. Candidate corrected that behavior.

Challenges the assumption that first-turn assumption provenance is enough for
continuations. Later turns need explicit protection against partial semantic
ratification becoming adjacent semantic invention.

## Limits

One live continuation sample per arm. The scenario is high-signal because the
current baseline directly failed, but future held-out continuations should test
other referential phrases, explicit threshold ratification, and active-record
authority where "existing context" is actually valid.
