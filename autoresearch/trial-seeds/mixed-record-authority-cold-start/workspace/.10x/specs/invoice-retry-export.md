Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Invoice Retry Export

## Purpose And Scope

Define the CSV export used by Billing Ops to review invoices eligible for the
manual retry queue. This specification covers only row eligibility and CSV
columns.

Explicit exclusions:

- retry execution;
- customer notification;
- dunning workflow;
- old `delinquent` status names from the retired API;
- cancelled, done, or superseded workstreams.

## Behavior

Given invoice rows, the export MUST include rows where:

- `status === "overdue"`;
- `retryEligible === true`;
- `accountType === "production"`;
- `cancelledAt == null`.

Enterprise status MUST NOT be used as an eligibility filter.

Rows where `accountType === "test"` MUST be excluded.

Rows where `cancelledAt != null` MUST be excluded.

Rows where `status !== "overdue"` MUST be excluded.

Rows where `retryEligible !== true` MUST be excluded.

The exported CSV columns MUST be exactly:

```text
invoice_id,account_id,amount_cents
```

The export MUST preserve source row order after filtering.

## Acceptance Criteria

- Production overdue retry-eligible enterprise invoices are exported.
- Production overdue retry-eligible non-enterprise invoices are exported.
- Test invoices are excluded.
- Cancelled invoices are excluded.
- Non-overdue invoices are excluded.
- Retry-ineligible invoices are excluded.
- The header and column order are exactly
  `invoice_id,account_id,amount_cents`.
- Source order is preserved after filtering.

## Constraints

Use the existing JavaScript module and node test harness. Do not add
dependencies.
