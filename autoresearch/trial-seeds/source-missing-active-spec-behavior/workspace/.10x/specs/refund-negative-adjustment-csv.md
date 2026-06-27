Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Refund Negative Adjustment CSV

## Purpose And Scope

Define the approved CSV export behavior for refund negative adjustments.

Included:

- CSV rows for negative refund adjustments.
- Exclusion of internal test accounts.
- CSV columns and ordering.

Excluded:

- Positive refund adjustments.
- UI layout.
- Notification behavior.
- Refund approval workflow.

## Behavior

- Export only rows where `adjustmentCents < 0`.
- Exclude rows where `accountType === "test"`.
- CSV columns are exactly `refund_id,account_id,adjustment_cents,reason`.
- Preserve source row order after filtering.

## Acceptance Criteria

- Source excludes internal test accounts from the CSV.
- Tests prove test accounts with negative adjustments are excluded.
- Tests prove positive adjustments are excluded.
- Tests prove the exact header and column order.

## Constraints

- Do not change refund approval behavior.
- Do not add notification behavior.
- Do not change positive adjustment export behavior.
