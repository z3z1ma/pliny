Status: blocked
Created: 2026-06-23
Updated: 2026-06-23
Parent:
Depends-On: .10x/research/2026-06-23-finchpay-instant-payout-revalidation.md, .10x/research/2024-04-09-finchpay-instant-payouts.md

# FinchPay Instant Payout Policy Authority

## Scope

Track the policy authority blocker for FinchPay instant payout implementation.

## Acceptance Criteria

- A user-ratified or active-record-backed policy exists for instant payout
  approval behavior.
- Any executable implementation ticket references the revalidation research and
  the ratified policy authority.

## Progress And Notes

- 2026-06-23: FinchPay instant payout API capability is revalidated.
- 2026-06-23: Old research recommends auto-approving payouts under `$500` for
  sellers with no chargebacks in the prior 90 days and manually reviewing
  higher-risk requests, but that recommendation is not an accepted decision.
- 2026-06-23: Merchant policy remains blocked pending explicit ratification.

## Blockers

- Approval threshold, seller eligibility, review routing, notification behavior,
  and operational ownership are not yet ratified.
