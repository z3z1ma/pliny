Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/research/2026-06-23-skill-autoresearch-run.md
Depends-On: .10x/evidence/2026-06-23-assumption-provenance-gate-scn001-live-micro.md, .10x/evidence/2026-06-23-assumption-provenance-greenline-scn001-live-micro.md

# Promote Assumption Provenance Gate Into SKILL.md

## Scope

Promote the proven assumption-provenance spine of
`candidate-assumption-provenance-gate-v1` into canonical `SKILL.md` after a
payment-retry MICRO showed manual cleanliness and a held-out greenline MICRO
showed candidate-over-current improvement.

Included:

- Add assumption provenance guidance to `SKILL.md`.
- Mark the candidate artifact and manifest entry as promoted.
- Record promotion evidence and review.
- Update the ongoing autoresearch run log.

Excluded:

- Promoting every sentence from the candidate overlay.
- Changing scorer, scenario, harness, or runner behavior.
- Adding a broad escape hatch around Outer Loop discipline.

## Acceptance Criteria

- AC-001: `SKILL.md` says correct implementation on an unratified premise is a
  failure.
- AC-002: `SKILL.md` classifies execution-relevant assumptions as
  record-backed, user-ratified, or blocked before Inner Loop entry.
- AC-003: `SKILL.md` says source names, stale tickets, examples, and familiar
  patterns do not authorize unratified product semantics.
- AC-004: `SKILL.md` forbids invented semantic defaults while allowing narrow
  mechanical defaults.
- AC-005: `SKILL.md` says tests can encode unratified assumptions and are not
  neutral evidence.
- AC-006: Candidate metadata records the promotion.
- AC-007: Evidence and review records exist for the promotion.
- AC-008: `python3 autoresearch/validate.py`, autoresearch unit tests, and
  `git diff --check` pass after the change.

## Progress and Notes

- 2026-06-23: Opened after
  `EXP-20260623-835-assumption-provenance-greenline-scn001-live-micro` showed
  candidate `S001=100,S007=75` versus current `S001=90,S007=65`.
- 2026-06-23: Added the assumption-provenance section to `SKILL.md`.
- 2026-06-23: Recorded evidence and review for the promotion.
- 2026-06-23: Verified `python3 autoresearch/validate.py`,
  `python3 -m unittest discover autoresearch/tests`, and `git diff --check`.

## Blockers

None.
