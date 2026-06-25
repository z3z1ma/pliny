Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Customer Credit Export

## Purpose And Scope

Define the CSV export used by Finance to review approved customer credit
adjustments. This specification covers only row eligibility and CSV columns.

Explicit exclusions:

- credit creation workflow;
- notifications;
- payout or refund behavior;
- historical enterprise-only prototype behavior from cancelled work.

## Behavior

Given customer credit rows, the export MUST include approved production
customers in the US region.

Rows where `accountType === "test"` MUST be excluded.

Rows where `status !== "approved"` MUST be excluded.

Rows where `region !== "us"` MUST be excluded.

Enterprise status MUST NOT be used as an eligibility filter.

The exported CSV columns MUST be exactly:

```text
customer_id,credit_cents,reason
```

The export MUST preserve source row order after filtering.

## Acceptance Criteria

- Approved production US enterprise customers are exported.
- Approved production US non-enterprise customers are exported.
- Test accounts are excluded.
- Non-US rows are excluded.
- Pending rows are excluded.
- The header and column order are exactly
  `customer_id,credit_cents,reason`.
- Source order is preserved after filtering.

## Constraints

Use the existing JavaScript module and node test harness. Do not add
dependencies.
