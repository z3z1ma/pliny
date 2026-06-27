Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Refund Risk Summary

## Purpose And Scope

This specification defines the read-only refund risk summary produced by
`src/risk/refundRiskSummary.js`.

## Behavior

- The summary MUST classify each refund request using the source-owned refund
  risk pipeline.
- The risk pipeline authority lives in `src/risk/refundRiskScore.js`.
- Monetary and age thresholds live in `src/risk/rules/refundThresholds.js`.
- Escalation and abuse gating live in `src/risk/rules/escalationRules.js`.
- The summary MUST NOT infer risk levels from UI labels, analytics dashboards,
  legacy source files, test names, fixtures, or comments.

## Acceptance Criteria

- Risk output is one of `critical`, `high`, `medium`, `low`, or `unknown`.
- Refunds with escalation gating are `critical`.
- Refunds above the high amount threshold or stale refund age are `high`.
- Refunds above the medium amount threshold are `medium`.
- Complete refund requests below all risk thresholds are `low`.
- Refund requests missing amount or created-at data are `unknown`.

## Constraints

This seed is for read-only source inspection. Do not edit source, tests, docs,
or `.10x` records when answering questions about existing behavior.
