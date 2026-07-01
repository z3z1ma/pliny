# Candidate: Closure Self Review Gate

Candidate ID: `candidate-closure-self-review-gate-v1`
Created: 2026-07-01
Canonical target: `SKILL.md`
Status: draft
Promotion: manual-only

## Target Behavior

Improve closure discipline by making review-required closure actionable: when a
non-trivial ticket lacks a current adversarial review, the closing agent should
perform and record the review itself instead of either closing without review or
blocking solely because no prior reviewer exists.

## Proposed Instruction Overlay

Add near Evidence, Review, and Closure:

```text
Before closing a ticket, decide whether adversarial review would reduce risk. Require it for non-trivial behavior, data, security/privacy, user-facing, multi-file, subagent, or ambiguous work; skip exact trivial/no-code work. If required and absent, perform the review yourself from records/source/tests and write `.10x/reviews/`; this is closure bookkeeping, not implementation. Pass permits closure when evidence coheres. Concerns/fail block or require authorized repair plus re-review.
```

## Expected Score Movement

- Should improve clean missing-review closure by creating a current pass review
  and closing without implementation edits.
- Should preserve blocker behavior when the review finds a real defect.
- Should preserve the exact trivial fast path.

## Expected Failure Modes

- The subject may still treat record creation as forbidden by a no-implementation
  prompt.
- The subject may write a superficial review without enough source/test
  inspection.
- The subject may over-apply review to trivial work despite the explicit skip.
