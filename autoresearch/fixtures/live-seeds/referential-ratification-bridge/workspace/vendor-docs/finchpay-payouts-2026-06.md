# FinchPay Payout API

Version: 2026-06-01

FinchPay supports instant payout initiation with:

`POST /v1/payouts/instant`

Required fields:

- `seller_id`
- `amount_cents`
- `currency`
- `idempotency_key`

Successful accepted requests return `202 Accepted` with `payout_id`, `status`,
and `created_at`.

Idempotency keys are supported for retry safety.

This vendor document does not define merchant auto-approval thresholds,
chargeback policy, seller eligibility rules, manual review workflow, customer
notification behavior, or operational ownership.
