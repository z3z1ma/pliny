Status: done
Created: 2026-06-27
Updated: 2026-06-27
Depends-On:

# Harden Autoresearch Scientific Environment

## Scope

Make the active autoresearch environment easier for a fresh scientist to use
without weakening the live-trial, scientist-inspection model.

Included:

- Add a first-class trial seed index that covers every `autoresearch/trial-seeds/`
  seed and explains the conditions each seed creates.
- Enrich seed metadata enough to support seed selection, prompt design,
  scientific contract registration, and rubric selection.
- Validate that the index stays synchronized with the seed directory, scenario
  catalog, and score catalog.
- Strengthen rubric guidance for manual scientist judgment without pretending
  scoring is automated.
- Add only lightweight report support that reduces missed artifact-inspection
  risk.
- Record evidence, review, and residual limits.

Excluded:

- Reintroducing static pass/fail grading or calibration-only paths.
- Reorganizing experiment definitions and run output directories unless the
  current layout proves unsafe.
- Mutating canonical `SKILL.md`.

## Acceptance Criteria

- AC-001: A fresh scientist can inspect one seed index to discover all trial
  seeds, target scenarios, target rubrics, conditions, traps, and prompt
  families.
- AC-002: `python3 autoresearch/validate.py` fails if the seed index drifts from
  existing seed directories or references unknown scenario/score IDs.
- AC-003: Manual scoring guidance is robust, evidence-grounded, and explicitly
  preserves scientist judgment.
- AC-004: Reports include a lightweight artifact-inspection checklist when
  artifacts are present.
- AC-005: Autoresearch validation and tests pass.

## Progress and Notes

- 2026-06-27: Opened after complex current-skill trials showed seed selection
  still required manual archaeology.
- 2026-06-27: Added generated trial seed index, seed index validation, manual
  scoring policy checks, report artifact checklist, README/program/template/spec
  guidance, and trial-seed README. Evidence:
  `.10x/evidence/2026-06-27-autoresearch-scientific-environment-hardening.md`.
  Review:
  `.10x/reviews/2026-06-27-autoresearch-scientific-environment-hardening-review.md`.

## Blockers

None.

## Closure

All acceptance criteria met.
