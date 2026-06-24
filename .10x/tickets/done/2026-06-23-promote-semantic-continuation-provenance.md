Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/research/2026-06-23-skill-autoresearch-run.md
Depends-On: .10x/evidence/2026-06-23-semantic-continuation-provenance-scn001-live-micro.md

# Promote Semantic Continuation Provenance Into SKILL.md

## Scope

Promote `candidate-semantic-continuation-provenance-v1` into canonical
`SKILL.md` after a live continuation MICRO showed current 10x implementing from
unratified source-field and threshold semantics.

Included:

- Add continuation-specific semantic provenance guidance to `SKILL.md`.
- Mark the candidate artifact and manifest entry as promoted.
- Record promotion evidence and review.
- Update the ongoing autoresearch run log.

Excluded:

- Changing scorer, scenario, harness, or runner behavior.
- Promoting the record-hardening gate.
- Adding a broad rule against using existing context when active records own the
  answer.

## Acceptance Criteria

- AC-001: `SKILL.md` says partial semantic ratification does not ratify adjacent
  semantic values.
- AC-002: `SKILL.md` says "use existing context" authorizes only current active
  records or explicit user answers.
- AC-003: `SKILL.md` says source constants, source fields, stale tickets, and
  familiar patterns do not become product semantics on continuation turns.
- AC-004: `SKILL.md` directs the agent to ask only for remaining unratified
  semantic values and avoid code/tests that encode them.
- AC-005: Candidate metadata records the promotion.
- AC-006: Evidence and review records exist for the promotion.
- AC-007: `python3 autoresearch/validate.py`, autoresearch unit tests, and
  `git diff --check` pass after the change.

## Progress and Notes

- 2026-06-23: Opened after
  `EXP-20260623-836-semantic-continuation-provenance-scn001-live-micro` showed
  candidate `S001=90,S007=55` versus current `S001=40,S007=55`.
- 2026-06-23: Added the semantic continuation provenance rule to `SKILL.md`.
- 2026-06-23: Recorded evidence and review for the promotion.
- 2026-06-23: Verified `python3 autoresearch/validate.py`,
  `python3 -m unittest discover autoresearch/tests`, and `git diff --check`.

## Blockers

None.
