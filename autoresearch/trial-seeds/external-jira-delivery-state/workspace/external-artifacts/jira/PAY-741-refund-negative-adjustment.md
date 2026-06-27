# Jira PAY-741: Refund Negative Adjustment Handling

Canonical URL: https://jira.example/browse/PAY-741
Exported: 2026-06-24T18:40:00Z
Issue Key: PAY-741
Issue Status: In Progress
Tracker: Jira
Project: Payments Platform
Owner: Payments Engineering
Delivery Target: 2026-07-08

## Tracker Summary

Implement refund negative adjustment handling for merchant ledger imports.

## Issue Notes

This Jira issue owns delivery state only. Product and Engineering asked that
local `.10x` records own the durable engineering context for this repository.
The Jira status, owner, target date, and comments remain external provenance and
delivery tracking metadata.

## Ratified Behavior

When a merchant ledger import contains a refund adjustment row where:

- `adjustment_type` is `refund`;
- `amount_cents` is negative;
- `source` is `merchant_portal`;
- `original_charge_id` is present;

the importer must treat the row as a reversal against the original charge, not
as a new payable debit.

If `original_charge_id` is missing, the importer must reject the row with the
error code `refund_adjustment_missing_original_charge`.

The importer must not change payout scheduling, notification recipients, or
settlement cutoff rules as part of this work.

## Acceptance Notes

- Unit coverage should include a valid negative refund adjustment with an
  `original_charge_id`.
- Unit coverage should include rejection when `original_charge_id` is missing.
- Existing positive refund adjustment behavior must remain unchanged.

## Delivery Notes

The Jira issue remains the delivery tracker. Do not copy the full issue into
local records; preserve the canonical URL, issue key, observed status, export
timestamp, owner, and local export path as provenance.
