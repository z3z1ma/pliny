Status: done
Created: 2026-06-27
Updated: 2026-06-27
Depends-On:

# Tighten Autoresearch Happy Path Ergonomics

## Scope

Make the live-trial autoresearch happy path self-explanatory for a fresh
scientist running one current-skill or candidate trial.

Included:

- Document or formalize one-arm current-skill regression/smoke runs so they do
  not require discovering `evaluation_only` in code.
- Align the active autoresearch spec with the live-trial scientist-inspection
  decision, especially around removed scorer, score-vector, trust-level, and
  top-line-index requirements.
- Enrich the experiment definition/template enough to pre-register hypothesis,
  expected behavior, rubric or inspection checks, quality floor, verdict
  destination, and seed provenance without adding a controller.
- Improve the report or raw metadata so subject messages that cite temporary
  workspaces are paired with durable archived workspace paths.
- Preserve the current simple `run_once.py` flow: one registered trial in, one
  artifact bundle out.

Excluded:

- Reintroducing static offline scoring, calibration fixtures, score artifacts,
  result ledgers, or fixture-backed MICRO execution.
- Adding a daemon, queue, scheduler, database, or autonomous loop controller.
- Automating grading or promotion.
- Changing canonical `SKILL.md`.

## Acceptance Criteria

- AC-001: A current-skill one-sample smoke/regression run can be registered from
  documented fields alone; no code inspection is needed to discover arm-set
  behavior.
- AC-002: Active docs/spec/templates no longer contradict
  `.10x/decisions/autoresearch-live-trial-scientist-inspection.md` by requiring
  removed scorer artifacts or numeric scorer output from live trial runs.
- AC-003: Experiment registration captures hypothesis, expected pass behavior,
  inspection criteria, seed provenance, budget, and verdict destination in a
  durable field or record section.
- AC-004: The report or adjacent metadata points reviewers to durable archived
  workspace paths when subject output mentions temporary execution paths.
- AC-005: Existing validation and unit tests pass, and at least one smoke trial
  or dry-run demonstrates the revised happy path.

## Progress and Notes

- 2026-06-27: Opened after
  `.10x/reviews/2026-06-27-current-skill-smoke-tooling-review.md` found the
  live smoke run passed but exposed cold-start ergonomics gaps.
- 2026-06-27: Implemented exact arm semantics, required scientific contracts,
  scenario provenance validation, report scientific-contract and archived
  workspace surfacing, active spec/template/program/README alignment, and
  catalog wording cleanup. Evidence:
  `.10x/evidence/2026-06-27-autoresearch-ergonomics-result.md`. Review:
  `.10x/reviews/2026-06-27-autoresearch-ergonomics-review.md`.

## Blockers

None.

## Closure

All acceptance criteria met.
