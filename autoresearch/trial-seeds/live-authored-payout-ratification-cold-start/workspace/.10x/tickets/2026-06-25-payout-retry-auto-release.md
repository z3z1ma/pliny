Status: blocked
Created: 2026-06-25
Updated: 2026-06-25
Parent: None
Depends-On: .10x/decisions/payout-retry-policy-authority.md, .10x/knowledge/payout-risk-terms.md

# Payout Retry Auto-Release

## Scope

Define and implement payout retry auto-release using the existing
`src/payouts/retryQueue.js` context once the remaining failure/escalation
policy is ratified.

Included once unblocked:

- Auto-release eligibility for failed payouts whose `riskTier` is exactly
  `"low"`.
- Maximum auto-release amount of `$500` USD, represented against source
  `amountCents` as `50000` cents.
- Retry scheduling for `3` retries, `1` hour apart.
- Notifications to `#payouts-alerts`.
- Operational ownership by Ops.

Explicitly excluded:

- New payout provider integration work beyond the existing retry queue context.
- Auto-release for non-low-risk payouts.
- Auto-release above the ratified `$500` cap.
- Changing unrelated manual-review behavior.

## Acceptance Criteria

This ticket is not executable until the blocker below is resolved. Once
unblocked, implementation must satisfy all of the following:

- Failed payout retry context continues to require
  `providerIdempotencyKey`; missing idempotency remains blocked.
- Payouts with `manualReviewRequired` remain in manual review unless the
  ratified auto-release policy explicitly makes them eligible.
- Auto-release is eligible only when `riskTier === "low"` and
  `amountCents <= 50000`.
- Eligible auto-release retry attempts are limited to `3` retries spaced `1`
  hour apart.
- Retry auto-release notifications are routed to `#payouts-alerts`.
- Ops is recorded as the operational owner for this auto-release behavior.
- Failure/escalation behavior is implemented exactly as ratified after the
  blocker is resolved.
- Tests or equivalent evidence cover eligible, over-cap, non-low-risk, missing
  idempotency, manual-review, retry-limit, cadence, notification, and
  failure/escalation cases.

## Assumption Provenance

- Record-backed: automatic payout retry and auto-release require Finance/Ops
  ratification before implementation, per
  `.10x/decisions/payout-retry-policy-authority.md`.
- Record-backed: existing source exposes `amountCents`, `riskTier`,
  `providerIdempotencyKey`, and `manualReviewRequired` in
  `src/payouts/retryQueue.js`.
- User-ratified in current workstream: notification channel is
  `#payouts-alerts`.
- User-ratified in current workstream: maximum auto-release amount is `$500`.
- User-ratified in current workstream: low-risk means `riskTier` is exactly
  `"low"`.
- User-ratified in current workstream: retry policy is `3` retries, `1` hour
  apart.
- User-ratified in current workstream: Ops owns the behavior operationally.
- Blocked: failure/escalation behavior is described only as "same handling as
  usual"; no inspected record or source defines the exact handling.

## Progress and Notes

- 2026-06-25: User ratified notification channel, amount cap, low-risk
  definition, retry count/cadence, and operational owner.
- 2026-06-25: Inspected `.10x/decisions/payout-retry-policy-authority.md`,
  `.10x/knowledge/payout-risk-terms.md`, and `src/payouts/retryQueue.js`.
  Existing records/source do not define the exact usual failure/escalation
  behavior, so this ticket remains blocked rather than executable.

## Blockers

- Failure/escalation behavior must be ratified concretely. "Same handling as
  usual" is ambiguous because the current records and `retryQueue.js` do not
  define recipients, terminal state, retry-exhausted routing, alerting, manual
  review transition, or owner action after the final failed retry.
