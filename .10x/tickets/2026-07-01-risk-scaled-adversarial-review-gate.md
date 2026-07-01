Status: active
Created: 2026-07-01
Updated: 2026-07-01
Depends-On: SKILL.md, autoresearch/program.md, autoresearch/README.md, autoresearch/catalogs/scores.json, autoresearch/trial-seeds/index.json

# Risk Scaled Adversarial Review Gate

## Scope

Design and run autoresearch experiments for a token-efficient `SKILL.md`
instruction that makes agents perform adversarial review before closing tickets
when risk justifies it, while avoiding ceremony for exact low-risk changes.

Included:

- Inspect current review and closure behavior in `SKILL.md` and existing
  autoresearch seeds.
- Form multiple candidate hypotheses that target risk-scaled adversarial review
  discipline.
- Add focused trial coverage for missing-review closure and trivial-review
  over-ceremony if existing seeds do not isolate those conditions.
- Run current-vs-candidate experiments through the live subject harness.
- Score behavior against S006 closure coherence, S005 minimalism, and S009 cost
  efficiency where relevant.
- Promote only if evidence shows net improvement without review boilerplate.

Excluded:

- Changing canonical `SKILL.md` before experiments support a candidate.
- Changing autoresearch runner behavior or score semantics unless experiments
  expose a tooling blocker.
- Turning every ticket closure into mandatory review ceremony regardless of
  risk.

## Acceptance Criteria

- AC-001: At least three hypotheses are represented as candidate overlays.
- AC-002: Experiment coverage includes a non-trivial ticket that otherwise looks
  closeable but lacks an adversarial review.
- AC-003: Experiment coverage includes a review finding that must block closure
  until resolved or accepted.
- AC-004: Experiment coverage includes an exact/trivial change where fresh
  adversarial review should be skipped or explicitly exempted.
- AC-005: Verdicts compare behavior uplift against added instruction cost.
- AC-006: Any promoted wording is reviewed as a semantic behavior change.
- AC-007: Validation and relevant autoresearch tests pass.

## Progress And Notes

- 2026-07-01: Opened from user request to strengthen review discipline without
  adding low-value ceremony.
- 2026-07-01: Added three candidate overlays, two missing-review closure seeds,
  and four MICRO experiment definitions covering missing review with defect,
  missing review with passable work, conflicting review repair, and trivial
  review exemption. Static validation, unit tests, diff check, and experiment
  dry-runs passed before live execution.
- 2026-07-01: First live batch completed 16 samples. The passable missing-review
  seed had a semantic confound around premium/retryable invoice preconditions,
  so a clean pass seed and two lower-cue experiments were added before any
  promotion decision.
- 2026-07-01: Lower-cue results isolated the leading candidate as
  `candidate-inner-loop-red-team-review`: it was the only variant that produced
  review-backed closure in the clean pass case while preserving the trivial fast
  path. Added a two-repetition confirmation batch for pass-clean, bug, and
  trivial scenarios before promoting canonical wording.

## Blockers

None.

## References

- `SKILL.md`
- `autoresearch/program.md`
- `autoresearch/README.md`
- `autoresearch/catalogs/scores.json`
- `autoresearch/trial-seeds/index.json`
