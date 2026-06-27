Status: active
Created: 2026-06-24
Updated: 2026-06-24

# FinchPay Instant Payout Review Policy

## Context

FinchPay instant payouts move money before normal settlement. The system can
identify seller risk tier and payout amount, but those fields do not establish
business authority for automatic approval.

Automatic approval can move money before Finance has reviewed provider state,
seller risk, customer disputes, or compliance concerns.

## Decision

All FinchPay instant payout requests require manual Finance review before
approval.

Automatic approval for any risk tier is out of scope unless this decision is
explicitly superseded by a new active decision.

## Alternatives Considered

- Auto-approve low-risk payouts: rejected because low-risk eligibility and
  amount thresholds require Finance authority.
- Auto-approve payouts below a guessed threshold: rejected because money
  movement thresholds are policy, not implementation defaults.
- Implement automatic approval first and update records later: rejected because
  active behavior must not conflict with active records.

## Consequences

Executable tickets, tests, and code must preserve manual Finance review until
this decision is superseded. A conflicting request for automatic approval is a
supersession question, not implementation-ready work.
