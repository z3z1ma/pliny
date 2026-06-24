Status: done
Created: 2024-04-09
Updated: 2024-04-09

# FinchPay Instant Payouts

## Question

Could FinchPay support instant payout initiation for marketplace sellers in
April 2024, and what rollout policy did the research recommend?

## Sources And Methods

- Read FinchPay payout API documentation for version `2024-03-15`.
- Tested `finchpay-node` `1.8.2` in the seller sandbox on 2024-04-09.
- Compared instant payout settlement against standard ACH payout timing.

## Findings

- FinchPay exposed `POST /v1/payouts/instant`.
- Requests accepted `seller_id`, `amount_cents`, `currency`, and
  `idempotency_key`.
- Sandbox instant payouts settled within five minutes.
- The API supported idempotent retries using the request `idempotency_key`.

## Conclusions

As of 2024-04-09, FinchPay technically supports instant payouts. The research
recommended auto-approving instant payouts under `$500` for sellers with no
chargebacks in the prior 90 days, then manually reviewing all higher-risk
requests.

The API capability is version-sensitive. The auto-approval recommendation is a
product policy recommendation, not an accepted decision.
