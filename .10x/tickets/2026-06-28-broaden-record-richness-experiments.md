Status: active
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/specs/10x-autoresearch-loop.md, autoresearch/program.md, autoresearch/catalogs/scores.json, autoresearch/trial-seeds/index.json

# Broaden Record Richness Experiments

## Scope

Rollback the under-evidenced canonical `SKILL.md` record-regeneration edit,
retain it as a candidate, and run a broader comparative search for the best
`S010` / Record Regeneration Quality uplift per added skill token.

Included:

- Restore canonical `SKILL.md` to the pre-promotion cold-reader wording.
- Keep the record-regeneration-check idea as an experimental candidate.
- Inspect `SKILL.md` holistically for alternative ways to improve record
  richness without adding ceremony or record spam.
- Form multiple compact hypotheses that target different mechanisms, not only
  cold-start regeneration framing.
- Run parallel or batched current-vs-candidate live experiments across existing
  `S010` seed workspaces.
- Score uplift, regressions, and character/token cost before considering any
  canonical promotion.

Excluded:

- Changing autoresearch runner behavior, rubric definitions, or seed catalogs.
- Promoting a new canonical `SKILL.md` change from fewer than a meaningfully
  diverse set of trials.
- Treating a single harness, single seed, or single stochastic win as promotion
  authority.

## Acceptance Criteria

- AC-001: Canonical `SKILL.md` no longer contains the under-evidenced promoted
  record-regeneration sentence.
- AC-002: At least three distinct hypotheses are represented as candidate
  overlays with estimated character cost.
- AC-003: Experiments cover multiple `S010` scenario families, including at
  least ticket/spec handoff, evidence/research capture, and record-minimalism or
  learning-preservation pressure.
- AC-004: Verdicts compare uplift against added tokens/characters and identify
  regression risks.
- AC-005: No candidate is promoted until evidence supports net score uplift
  across the diverse scenario set.

## Progress And Notes

- 2026-06-28: Opened after the user correctly noted that
  `f37bfab` promoted from insufficient evidence. The canonical skill change is
  being rolled back while the idea remains available as a candidate.
- 2026-06-28: Added four new candidate overlays and retained the original
  regeneration-check candidate. Registered a five-scenario first batch covering
  external index, record economy, ticket handoff, evidence audit, and
  retrospective learning.

## Blockers

None.

## References

- `SKILL.md`
- `autoresearch/candidates/2026-06-28-record-regeneration-check.md`
- `autoresearch/candidates/2026-06-28-source-material-delta-audit.md`
- `autoresearch/candidates/2026-06-28-executor-handoff-contract.md`
- `autoresearch/candidates/2026-06-28-record-economy-density.md`
- `autoresearch/candidates/2026-06-28-audit-limits-redaction.md`
- `.10x/evidence/2026-06-28-record-richness-candidate-result.md`
- `.10x/research/2026-06-28-record-richness-score-improvement.md`
- `.10x/research/2026-06-28-record-richness-hypothesis-search.md`
