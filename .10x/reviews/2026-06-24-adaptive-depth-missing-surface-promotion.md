Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Target: SKILL.md
Verdict: pass

# Adaptive Depth Missing Surface Promotion Review

## Target

Promotion of `candidate-adaptive-question-depth-missing-surface-v2` into
`SKILL.md`.

## Findings

- **Pass:** The promoted text is narrow. It clarifies one target-surface edge
  inside existing blocker-question guidance.
- **Pass:** The rule preserves the "at most three" default as noise control and
  does not create broad discretion to ask downstream preference questions.
- **Pass:** The rule has an explicit inverse guard: when records settle the
  semantic policy and only surface remains open, ask only the surface/workflow
  blocker.
- **Pass:** The promoted behavior is supported by a positive MICRO and a
  held-out sanity MICRO.
- **Residual concern:** The phrase "co-equal upstream decisions" relies on
  model judgment. Future regressions should keep testing questionnaire
  inflation versus under-questioning.

## Verdict

Pass.

## Residual Risk

The promoted language may slightly increase question count in product-policy
ambiguity. That is acceptable when each question prevents an unratified semantic
assumption, but future candidates should continue policing downstream UI/copy
and implementation-detail inflation.
