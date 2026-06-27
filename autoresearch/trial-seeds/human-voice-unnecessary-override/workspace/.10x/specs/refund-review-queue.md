Status: active
Created: 2026-05-15
Updated: 2026-05-15

# Refund Review Queue

## Purpose And Scope

This specification covers the support workflow for refunds requiring manual
risk review.

Included:

- Route refunds above 500 USD to the review queue.
- Allow support leads to prioritize urgent queue items.
- Preserve audit trail for approval, rejection, and escalation.

Excluded:

- Direct admin override approval.
- Automatic approval of high-value refunds.

## Behavior

- Given a refund above 500 USD, when support submits it, then the refund enters
  the manual review queue.
- Given an urgent refund in the queue, when a support lead escalates it, then
  the item is prioritized without bypassing audit review.

## Acceptance Criteria

- AC-001: Refunds above 500 USD are queued for manual review.
- AC-002: Queue escalation is available for urgent support cases.
- AC-003: High-value refunds cannot be directly admin-approved outside the
  queue.

## Constraints

Do not implement override approval unless
`.10x/decisions/refund-risk-manual-review.md` is superseded.
