Status: active
Created: 2026-05-15
Updated: 2026-05-15

# Refund Risk Manual Review

## Context

Support needs to process customer refunds quickly, but refunds above 500 USD
create chargeback, fraud, and audit risk. Three options were evaluated:
automatic approval, manager override, and mandatory manual review queue.

## Decision

Refunds above 500 USD must enter the refund review queue. Do not add direct
manager/admin override approval unless this decision is explicitly superseded
by a new active decision that defines eligibility, audit logging, limits,
rollback, and operational owner.

## Alternatives Considered

- Automatic approval: rejected because high-value refunds can move money without
  human risk review.
- Manager override button: rejected because it bypasses queue evidence and audit
  controls unless a separate override policy is defined.
- Manual review queue: accepted because it preserves delivery speed while
  retaining auditability and risk ownership.

## Consequences

The support path for urgent high-value refunds is to use the existing review
queue and escalate queue ownership, not to bypass the queue in product code.
