Status: draft
Created: 2026-06-25
Updated: 2026-06-25

# Refund Auto-Approval

## Purpose And Scope

This draft covers future refund auto-approval for low-risk refunds. It excludes
manual refund review, chargeback handling, and customer notification copy.

## Behavior

Refund auto-approval cannot become executable until every policy value below is
record-backed or user-ratified:

- maximum auto-approval amount;
- low-risk eligibility predicate;
- retry count and cadence;
- notification destination;
- failure and escalation behavior;
- operational owner.

## Acceptance Criteria

- No implementation ticket may be executable while any listed policy value is
  unresolved.
- Source fields such as `amountCents`, `riskTier`, and
  `manualReviewRequired` are candidate signals only.
- The phrase `normal risk escalation` has no defined meaning in this workspace.

## Constraints

- Do not edit source or tests while the policy contract remains incomplete.
- Do not use payout retry defaults as refund auto-approval semantics.
