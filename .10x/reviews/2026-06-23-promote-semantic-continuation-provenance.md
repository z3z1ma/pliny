Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Target: SKILL.md, autoresearch/candidates/2026-06-23-semantic-continuation-provenance.md
Verdict: pass

# Promote Semantic Continuation Provenance Review

## Target

Canonical promotion of `candidate-semantic-continuation-provenance-v1` into
`SKILL.md`.

## Findings

- **Pass:** The promoted rule targets a direct observed failure: current
  implemented from `GREENLINE_MIN_SCORE`/`readinessScore` after only
  display-only was ratified.
- **Pass:** The rule is narrow to continuation turns and does not weaken Outer
  Loop discipline.
- **Pass:** The rule preserves useful progress: it allows the answered branch to
  stay answered and asks only for remaining semantic values.
- **Pass:** The rule does not create a broad rejection of "existing context".
  It allows active current records or explicit user answers to authorize values.
- **Concern accepted:** This promotion is based on one high-signal run. The
  failure was severe: current crossed into implementation, active spec
  acceptance criteria, evidence, review, and ticket closure on unratified
  adjacent semantics.

## Verdict

Pass. Promote the semantic continuation provenance rule and continue with the
record-hardening MICRO to test durable-record laundering directly.

## Residual Risk

The main residual risk is overblocking when the user says "use existing context"
and an active record actually owns the threshold or field. Future tests should
include a positive-control continuation where active records do authorize the
referenced value.
