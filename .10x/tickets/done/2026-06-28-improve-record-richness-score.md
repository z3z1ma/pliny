Status: done
Created: 2026-06-28
Updated: 2026-06-28
Depends-On: .10x/specs/10x-autoresearch-loop.md, autoresearch/program.md, autoresearch/catalogs/scores.json, autoresearch/trial-seeds/index.json

# Improve Record Richness Score

## Scope

Run an autoresearch iteration targeting `S010` / Record Regeneration Quality:
form a compact skill-improvement hypothesis, test a candidate against live
subject-agent trials, inspect raw artifacts, and promote only evidence-backed
wording that improves record richness without weakening existing 10x gates.

Included:

- Select existing `S010` seed workspaces that exercise ticket, evidence, or
  learning record quality.
- Create exactly one candidate overlay.
- Register and run current-vs-candidate MICRO experiments.
- Score record richness manually from raw transcripts and archived workspaces.
- Preserve the hypothesis, artifacts, verdict, and review in durable records.
- Apply a canonical `SKILL.md` change only if the evidence supports promotion
  and the change remains within the skill size budget.

Excluded:

- Changing autoresearch runner behavior, catalogs, scenario definitions, or the
  score rubric.
- Adding new seed workspaces unless existing seeds cannot answer the hypothesis.
- Automatic grading or fixture-backed scoring.

## Acceptance Criteria

- AC-001: The research record states a concrete hypothesis and why it should
  improve `S010`.
- AC-002: At least one current-vs-candidate live experiment runs against an
  existing `S010` seed and preserves raw artifacts.
- AC-003: The verdict compares created/updated records against `S010`
  sub-scores and hard floors.
- AC-004: Any canonical `SKILL.md` edit is smaller than the candidate overlay's
  behavioral idea, validated by tests and `SKILL.md` size budget.
- AC-005: Evidence, review, and ticket closure are coherent before the work is
  marked done.

## Progress And Notes

- 2026-06-28: Opened from the user's request to form a compelling hypothesis,
  run experiments, and improve the record-richness score.
- 2026-06-28: Created one candidate overlay,
  `autoresearch/candidates/2026-06-28-record-regeneration-check.md`, and
  preregistered a current-vs-candidate MICRO experiment across
  `explicit-policy-ratification` and `redacted-evidence-capture`.
- 2026-06-28: Ran the first MICRO experiment. It completed four live Codex
  samples and revealed a valid current-arm clarifying question in the policy
  seed, so a continuation experiment was registered to answer that blocker.
- 2026-06-28: Ran the continuation experiment, promoted a compressed
  `SKILL.md` replacement for the cold-reader paragraph, and validated the
  canonical change.

## Blockers

None.

## References

- `SKILL.md`
- `autoresearch/program.md`
- `autoresearch/catalogs/scores.json`
- `autoresearch/trial-seeds/index.json`
- `autoresearch/candidates/2026-06-28-record-regeneration-check.md`
- `.10x/research/2026-06-28-record-richness-score-improvement.md`
- `.10x/research/.storage/2026-06-28-record-richness-score/experiment-record-regeneration-check.json`
- `.10x/research/.storage/2026-06-28-record-richness-score/experiment-record-regeneration-check-continuation.json`
- `.10x/evidence/2026-06-28-record-richness-candidate-result.md`
- `.10x/reviews/2026-06-28-record-richness-candidate-review.md`
