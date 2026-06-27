Status: done
Created: 2026-06-27
Updated: 2026-06-27
Parent: user-request
Depends-On: .10x/decisions/autoresearch-live-trial-scientist-inspection.md, .10x/specs/10x-autoresearch-loop.md

# Retire Fixture-Backed Autoresearch

## Scope

Remove the unused and confusing static offline fixture-backed autoresearch path
while preserving the live clean-room subject-agent flow.

In scope:

- Remove offline fixture scoring, calibration labels, and fixture-backed MICRO
  runner code.
- Make `run_codex_subject.py` and `run_once.py` emit live trial artifacts only.
- Replace score-artifact reporting with a concise trial-artifact report.
- Update active docs, templates, catalogs, validator expectations, and focused
  tests to describe scientist inspection over raw trial artifacts.
- Keep live seed workspaces and `prior_raw_paths` support for clean-room trials.
- Rename the live seed directory so no active path contains the old fixture
  terminology.

Out of scope:

- Building a Python-owned autonomous loop.
- Promoting or changing canonical `SKILL.md`.
- Rewriting historical research/evidence/ticket records that accurately describe
  past fixture-backed work.

## Acceptance Criteria

- AC-001: `run_micro.py`, `offline_score.py`, `calibrate_scorer.py`, static
  offline fixtures, calibration labels, and score-artifact schema are removed.
- AC-002: Live runner outputs do not include `scores/`, `score_artifact_dir`,
  `score_artifact_path`, offline scorer imports, or Trust Level 1 scorer claims.
- AC-003: `run_once.py` still runs one registered Codex subject experiment and
  writes `summary.json`, `plan.json`, raw artifacts, command artifacts,
  workspaces, prompts, `canonical_guard.json`, and `report.md`.
- AC-004: Active program/docs/templates frame verdicts as researcher inspection
  over raw trial artifacts and durable `.10x/` records.
- AC-005: Validator and focused unit tests pass after the removal.
- AC-006: Evidence and review records capture the commands run and final diff
  review.
- AC-007: Live seed workspaces live under `autoresearch/trial-seeds/`, and no
  active path references the old seed directory name.

## Progress And Notes

- 2026-06-27: Opened from user request to remove fixture-backed machinery and
  simplify autoresearch around live trials plus scientist inspection.
- 2026-06-27: Completed. Evidence:
  `.10x/evidence/2026-06-27-retire-fixture-backed-autoresearch.md`. Review:
  `.10x/reviews/2026-06-27-retire-fixture-backed-autoresearch.md`.
- 2026-06-27: Follow-up cleanup renamed the live seed directory to
  `autoresearch/trial-seeds/` and updated path references repo-wide.

## Blockers

None.
