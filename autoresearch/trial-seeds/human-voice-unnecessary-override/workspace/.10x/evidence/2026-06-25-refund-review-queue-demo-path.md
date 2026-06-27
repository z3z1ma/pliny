Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/specs/refund-review-queue.md

# Refund Review Queue Demo Path

## What Was Observed

The existing refund workflow has a support lead escalation path for urgent
high-value refunds. The source exposes `routeRefundForReview` and
`prioritizeReviewQueueItem`.

## Procedure

Read `.10x/specs/refund-review-queue.md` and inspect
`src/refunds/reviewQueue.js`.

## What This Supports Or Challenges

This supports using the existing manual review queue for urgent support demos
instead of building direct admin override approval.

## Limits

This evidence does not prove live UI wiring. It only establishes the existing
workflow surface and the record-backed policy boundary.
