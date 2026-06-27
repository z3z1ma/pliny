Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Refund Negative Adjustment CSV

## Purpose And Scope

Define the refund negative adjustment CSV exported for operational refund review.
This spec covers only the CSV rows and columns for negative adjustments.

Explicit exclusions:

- refund approval workflow;
- notification behavior;
- CSV escaping beyond the fields listed here;
- historical completed-ticket behavior before this policy supersession.

## Behavior

Given refund adjustment rows, the export MUST include only rows where
`adjustmentCents < 0`.

Rows where `accountType === "test"` MUST be excluded, even when
`adjustmentCents < 0`.

The exported CSV columns MUST be exactly:

```text
refund_id,account_id,adjustment_cents,reason
```

The export MUST preserve source row order after filtering.

## Acceptance Criteria

- Negative adjustments for production accounts are exported.
- Negative adjustments for test accounts are excluded.
- Positive adjustments are excluded.
- The header and column order are exactly
  `refund_id,account_id,adjustment_cents,reason`.
- Source order is preserved after filtering.

## Constraints

Do not add dependencies. Use the existing JavaScript module and node test
harness.
