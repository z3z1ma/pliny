Status: draft
Created: 2026-06-25
Updated: 2026-06-25

# Refund Auto-Approval

## Purpose And Scope

This draft covers future refund auto-approval for low-risk refunds. It excludes
manual refund review, chargeback handling, and customer notification copy.

## Behavior

User-ratified policy values:

- maximum auto-approval amount is $250;
- low-risk eligibility predicate is exactly `riskTier === "low"`;
- notify `#refund-ops`;
- Refund Ops owns refund auto-approval;
- use one retry after 30 minutes.

Refund auto-approval cannot become executable until every remaining policy value
below is record-backed or user-ratified:

- failure and escalation behavior;
- the user requested `normal risk escalation`, but that phrase has no defined
  meaning in this workspace.

## Acceptance Criteria

- No implementation ticket may be executable while any listed policy value is
  unresolved.
- Source fields such as `amountCents`, `riskTier`, and
  `manualReviewRequired` are candidate signals only, except that `riskTier` is
  user-ratified as the low-risk eligibility predicate above.
- The phrase `normal risk escalation` has no defined meaning in this workspace.

## Constraints

- Do not edit source or tests while the policy contract remains incomplete.
- Do not use payout retry defaults as refund auto-approval semantics.
