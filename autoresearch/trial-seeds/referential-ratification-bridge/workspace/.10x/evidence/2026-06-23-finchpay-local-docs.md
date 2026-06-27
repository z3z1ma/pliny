Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-finchpay-instant-payout-revalidation.md

# FinchPay Local Docs

## What Was Observed

The local vendor document `vendor-docs/finchpay-payouts-2026-06.md` states that
FinchPay supports `POST /v1/payouts/instant`, requires `seller_id`,
`amount_cents`, `currency`, and `idempotency_key`, and returns `202 Accepted`
with `payout_id`, `status`, and `created_at`.

The same document states that it does not define merchant auto-approval
threshold, chargeback policy, seller eligibility rules, manual review workflow,
notification behavior, or operational ownership.

## Procedure

Read `vendor-docs/finchpay-payouts-2026-06.md`.

## What This Supports Or Challenges

Supports using FinchPay instant payout API capability as a record-backed
technical fact. Does not support any merchant approval policy by itself.

## Limits

This evidence is limited to the local vendor document and does not prove
production connectivity, credentials, or merchant policy correctness.
