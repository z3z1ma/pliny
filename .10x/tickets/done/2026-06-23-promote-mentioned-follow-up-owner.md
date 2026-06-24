Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/research/2026-06-23-skill-autoresearch-run.md
Depends-On: .10x/evidence/2026-06-23-mentioned-follow-up-owner-scn009-live-micro.md

# Promote Mentioned Follow-Up Owner Into SKILL.md

## Scope

Promote `candidate-mentioned-follow-up-owner-v1` into canonical `SKILL.md`
after a live MICRO showed current 10x closing tickets while leaving an unowned
follow-up only in final prose.

Included:

- Add a closure-time follow-up ownership rule to `SKILL.md`.
- Mark the candidate artifact and manifest entry as promoted.
- Record live result evidence and promotion review.
- Update the experiment record and ongoing autoresearch run log.

Excluded:

- Changing scorer, scenario, harness, or runner behavior.
- Creating broad new process around every possible final-answer note.

## Acceptance Criteria

- AC-001: `SKILL.md` says closure-time follow-ups worth mentioning need a
  durable owner.
- AC-002: `SKILL.md` names acceptable owner forms: existing record, bounded
  follow-up ticket, or recorded no-action rationale.
- AC-003: `SKILL.md` prevents absorbing out-of-scope follow-ups into the current
  ticket.
- AC-004: `SKILL.md` blocks closure or asks permission when the user forbids
  durable tracking for an unresolved follow-up.
- AC-005: Candidate metadata records the promotion.
- AC-006: Evidence and review records exist for the live result and promotion.
- AC-007: `python3 autoresearch/validate.py`, autoresearch unit tests, and
  `git diff --check` pass after the change.

## Progress And Notes

- 2026-06-23: Opened after
  `EXP-20260623-848-mentioned-follow-up-owner-scn009-live-micro` showed a
  candidate improvement over current on final-answer-only follow-up leakage.
- 2026-06-23: Added closure-time follow-up ownership rule to `SKILL.md`.
- 2026-06-23: Updated candidate metadata, experiment result, and run log.
- 2026-06-23: Verified `python3 autoresearch/validate.py`, `python3 -m unittest
  discover autoresearch/tests`, JSON parsing for `autoresearch/candidates/candidates.json`,
  and `git diff --check`.

## Blockers

None.
