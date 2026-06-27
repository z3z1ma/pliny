# FinchPay Payout API

Version: 2026-06-01

FinchPay currently supports instant payout initiation through:

```text
POST /v1/payouts/instant
```

Required request fields:

- `seller_id`
- `amount_cents`
- `currency`
- `idempotency_key`

The endpoint returns `202 Accepted` for an accepted payout request and includes
`payout_id`, `status`, and `created_at`.

Clients should send an idempotency key for retry safety. FinchPay treats
requests with the same idempotency key as the same payout request.

This API document does not define merchant auto-approval threshold, chargeback
policy, seller eligibility rules, manual review workflow, notification behavior,
or operational ownership.
