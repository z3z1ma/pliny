Status: done
Created: 2026-06-23
Updated: 2026-06-23

# FinchPay Instant Payout Revalidation

## Question

Does the current local FinchPay vendor documentation support instant payout API
capability?

## Sources And Methods

- Read `vendor-docs/finchpay-payouts-2026-06.md`, version `2026-06-01`.
- Compared the current local vendor documentation to the old FinchPay
  instant-payout recommendation captured in prior work.

## Findings

- The current local vendor documentation supports `POST /v1/payouts/instant`.
- Required fields are `seller_id`, `amount_cents`, `currency`, and
  `idempotency_key`.
- Accepted requests return `202 Accepted` with `payout_id`, `status`, and
  `created_at`.
- Idempotency keys are supported for retry safety.
- The vendor documentation does not define merchant policy such as thresholds,
  seller eligibility, manual review workflow, notification behavior, or
  operational ownership.

## Conclusions

The FinchPay instant payout API capability is record-backed by current local
vendor documentation. Merchant approval policy remains separate and requires
active-record authority or explicit user ratification before implementation.
