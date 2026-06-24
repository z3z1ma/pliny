Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Target: SKILL.md, autoresearch/candidates/2026-06-23-fish-before-opening-pressure.md
Verdict: pass

# Promote Fish Before Opening Pressure Review

## Target

Canonical promotion of `candidate-fish-before-opening-pressure-v1` into
`SKILL.md`.

## Findings

- **Pass:** The promoted rule targets the observed gap: current 10x avoided a
  duplicate ticket but left the explicit follow-up request only in final prose.
- **Pass:** The rule preserves the existing fish-before-opening invariant and
  does not permit duplicate durable owners.
- **Pass:** The rule limits existing-ticket updates to new durable context from
  the current turn, reducing the risk of mechanical ticket churn.
- **Pass:** The terminal-ticket branch requires reading done or cancelled owners
  before deciding whether to reopen, create distinct follow-up work, or treat the
  issue as already handled.
- **Concern accepted:** The promotion is based on one high-signal MICRO run and
  needs future held-out coverage for materially distinct follow-ups that only
  look textually similar.

## Verdict

Pass. Promote the narrow fish-before-opening pressure rule.

## Residual Risk

The main residual risk is over-deduplicating distinct work into an existing
active ticket because the issue wording overlaps. Future scenarios should test
near-duplicate requests where separate tickets are correct.
