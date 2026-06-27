# GitHub PR 482: ACME Webhook Retry Follow-Up

Canonical URL: https://github.example/acme/payments/pull/482#discussion_r918273645
Exported: 2026-06-24T15:10:00Z
PR Status: merged
Repository: acme/payments
Thread: discussion_r918273645

## Summary

The PR implemented ACME webhook retry scheduling. During review, Engineering
and Security settled the idempotency key decision for ACME webhooks.

## Discussion Excerpt

Reviewer A:

> The patch currently uses `event_id` as the idempotency key. ACME support says
> `event_id` can be reused across replay attempts after a regional failover.
> Their delivery contract documents `provider_delivery_id` as stable per
> delivery attempt and unique across replay.

Author:

> Switching to `provider_delivery_id` means replayed duplicate deliveries won't
> collapse into the same dedupe bucket as the original event. That seems safer
> for retry scheduling, but it is a different key than our first draft.

Security:

> Decision: use `provider_delivery_id` for ACME webhook idempotency. Do not use
> `event_id`. The tradeoff is that replayed deliveries are distinct delivery
> records, but the receiver can still link them through `event_id` for audit.
> This avoids failover collisions and matches ACME's delivery contract.

Maintainer:

> Accepted. PR 482 is merged with `provider_delivery_id`. Please make sure the
> local engineering record graph can find this decision later; the PR discussion
> remains the canonical review artifact.

## Follow-Up

No implementation change is requested in this export. The code merged in PR 482
already uses `provider_delivery_id`.
