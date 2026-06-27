Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Checkout Retry Policy

## Purpose And Scope

Define the checkout retry behavior for failed card payments in the customer
billing portal.

In scope:

- Show customers that the last checkout attempt failed.
- Let customers retry payment after updating card details.
- Show pending retry state while Stripe webhook confirmation is outstanding.

Out of scope:

- New payment providers.
- Manual finance approval.
- Email notification templates.
- Subscription cancellation policy.

## Behavior

Given a checkout payment fails, when the customer returns to billing, then the
portal should show a retry banner with the failed timestamp and a button to
update payment details.

Given a retry is submitted, when Stripe confirmation is pending, then the portal
should show a pending state and prevent duplicate retry submissions.

Given Stripe confirms success, when the portal refreshes, then the retry banner
should disappear and the invoice should show paid state.

## Acceptance Criteria

- Failed checkout state shows a retry banner in the billing portal.
- Retry action routes through the existing Stripe checkout session flow.
- Pending retry state disables duplicate retry submission.
- Successful retry clears the banner after webhook-backed confirmation.
- Tests cover failed, pending, and successful retry states.

## Constraints

- Stripe remains the source of truth for retry status.
- Do not add a provider abstraction.
- Do not change subscription cancellation rules.
