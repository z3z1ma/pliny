Status: active
Created: 2026-07-01
Updated: 2026-07-01

# Risk Scaled Adversarial Review Gate

## Question

What is the most token-efficient `SKILL.md` instruction that makes agents run
adversarial review before closing tickets when review would materially reduce
risk, while preserving the trivial-work fast path?

## Sources And Methods

Inspected:

- `SKILL.md`, especially Inner Loop Execution, Evidence/Review/Closure, and
  Retrospective Protocol.
- `autoresearch/program.md`.
- `autoresearch/catalogs/scores.json`, especially S006 Closure Coherence, S005
  Scope Minimalism, and S009 Cost Efficiency Index.
- `autoresearch/trial-seeds/index.json`, focusing closure and trivial-edit
  seeds.
- Existing review/closure candidates and records, including conflicting-review
  and closure-positive seeds.

Initial finding: current `SKILL.md` requires existing review findings to be
resolved before closure, but does not clearly require deciding whether a fresh
adversarial review is needed when no review exists.

Candidate hypotheses:

- `candidate-risk-scaled-review-gate-v1`: compact risk-based closure gate.
- `candidate-review-state-closure-gate-v1`: explicit review-state closure model.
- `candidate-inner-loop-red-team-review-v1`: broader Inner Loop red-team loop.

Seed coverage:

- `risk-review-missing-bug`: non-trivial closure with evidence and no review;
  source/tests miss cancellation suppression.
- `risk-review-missing-pass`: non-trivial closure with evidence and no review;
  source/tests satisfy the active spec.
- `risk-review-missing-pass-clean`: non-trivial closure with evidence and no
  review; source/tests satisfy a clean active spec whose behavior is exactly the
  modeled invoice-state surface.
- `conflicting-reviewers-closure`: existing fail/pass review conflict must block
  closure until active-spec findings are handled.
- `exact-trivial-edit`: exact low-risk typo fix should not trigger review
  ceremony.

## Findings

- First live batch exposed a confound in `risk-review-missing-pass`: the spec
  mentioned premium/retryable preconditions that the source model did not
  represent. Current 10x blocked on that; candidates closed. This is useful
  evidence about semantic strictness, but not clean evidence for review-gate
  promotion.
- Added `risk-review-missing-pass-clean` and lower-cue closure prompts before
  drawing promotion conclusions.
- Lower-cue results selected `candidate-inner-loop-red-team-review` as the
  leading hypothesis. The current skill was safe on the bug case but left the
  clean pass parent blocked because it did not generate its own review state.
  The other two candidates tended to block on missing review instead of
  conducting one. A confirmation batch repeats pass-clean, bug, and trivial
  conditions against current vs the leading candidate.

## Conclusions

Pending.
