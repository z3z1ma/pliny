Status: open
Created: 2026-06-23
Updated: 2026-06-23
Parent:
Depends-On: autoresearch/fixtures/live-seeds/records-first-checkout/workspace/.10x/specs/checkout-retry-policy.md, autoresearch/fixtures/live-seeds/records-first-checkout/workspace/.10x/decisions/checkout-payment-provider.md

# Add Checkout Retry Banner

## Scope

Add a billing-portal retry banner for failed checkout payments.

Included:

- Render failed checkout timestamp and retry call to action.
- Route retry through the existing Stripe checkout session flow.
- Show pending state while webhook confirmation is outstanding.
- Disable duplicate retry submissions while pending.
- Add tests for failed, pending, and successful retry states.

Excluded:

- New payment providers.
- Provider abstraction.
- Email templates.
- Subscription cancellation rules.

## Acceptance Criteria

- Failed checkout state shows a retry banner.
- Retry action uses the existing Stripe checkout session flow.
- Pending retry state disables duplicate submissions.
- Successful webhook-backed retry clears the banner.
- Tests cover failed, pending, and successful states.

## Progress And Notes

- 2026-06-23: Seed ticket for records-first retrieval evaluation.

## Blockers

None in this seed record.
