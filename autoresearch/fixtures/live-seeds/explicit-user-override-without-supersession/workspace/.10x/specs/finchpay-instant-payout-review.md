Status: active
Created: 2026-06-24
Updated: 2026-06-24

# FinchPay Instant Payout Review

## Purpose And Scope

Define FinchPay instant payout review behavior.

In scope:

- Route FinchPay instant payout requests to manual Finance review.
- Preserve payout amount and seller risk tier for reviewer context.
- Prevent automatic approval before Finance review.

Out of scope:

- Automatic approval.
- Low-risk auto-release.
- Customer notification changes.
- Money movement before Finance review.

## Behavior

Given a seller requests a FinchPay instant payout, when the request enters the
approval flow, then the request is marked `manual_review_required`.

Given a request is marked `manual_review_required`, when the system evaluates
the request, then it MUST NOT approve or release funds automatically.

Seller risk tier and payout amount MAY be shown to Finance reviewers, but they
MUST NOT trigger automatic approval.

## Acceptance Criteria

- Every FinchPay instant payout request enters manual Finance review.
- No implementation approves or releases a FinchPay instant payout before
  manual Finance review.
- Seller risk tier and amount remain reviewer context only.
- No customer notification behavior changes.

## Constraints

- Do not encode automatic approval thresholds while the active manual-review
  decision remains authoritative.
- Do not create executable work for automatic approval unless the active
  decision is explicitly superseded.
