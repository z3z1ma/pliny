Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: none
Depends-On: .10x/research/2026-06-23-first-autoresearch-calibration-campaign.md

# Design A Real Autoresearch Candidate Variant

## Scope

Define a real candidate 10x/autoresearch instruction or workflow variant for a
future comparison campaign.

Included:

- Identify one concrete behavioral weakness or friction point from existing
  autoresearch records.
- Propose the smallest candidate change that could plausibly improve that
  behavior.
- Define the candidate artifact path, instruction digest procedure, and scenarios
  it should affect.
- State expected tradeoffs and failure modes.

Excluded:

- Editing canonical `SKILL.md`, AGENTS instructions, specs, or decisions.
- Running promotion-grade evaluations.
- Treating placeholder/null fixtures as candidate evidence.

## Acceptance Criteria

- AC-001: A candidate artifact or precise candidate design exists and is distinct
  from current `SKILL.md`.
- AC-002: The design names the target behavior, expected score movement, and
  likely backfire modes.
- AC-003: The design includes fixture or scenario coverage sufficient for a
  future MICRO comparison.
- AC-004: The design explicitly states that promotion still requires separate
  evidence, review, and human authority.

## Progress And Notes

- 2026-06-23: Opened from first calibration campaign because
  `candidate-variant` was a placeholder/null candidate using current `SKILL.md`
  and identical fixtures.
- 2026-06-23: Added two real experimental candidate artifacts and registered
  them in `autoresearch/candidates/candidates.json`: campaign status metadata
  discipline and retrospective follow-up capture discipline. Evidence:
  `.10x/evidence/2026-06-23-real-autoresearch-candidates.md`.

## Blockers

None.
