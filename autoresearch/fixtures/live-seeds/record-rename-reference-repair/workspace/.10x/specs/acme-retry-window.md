Status: active
Created: 2026-06-24
Updated: 2026-06-24

# ACME Retry Window

## Purpose And Scope

Defines retry behavior for ACME ledger webhooks after receiver failures.

Included:

- Retryable receiver failure classes.
- Retry timing.
- Terminal duplicate-delivery handling.

Excluded:

- Customer notification behavior.
- Provider API migration.
- Backfill processing.

## Behavior

- Retry `5xx` receiver responses for up to 30 minutes.
- Treat `409` duplicate responses as terminal success.
- Do not retry `4xx` responses other than `409`.
- Persist `delivery_id` as the idempotency key.

## Acceptance Criteria

- `5xx` receiver responses enqueue retries until the 30-minute retry horizon is
  exhausted.
- `409` duplicate responses are recorded as delivered and do not enqueue
  retries.
- Other `4xx` responses are recorded as terminal failures and do not enqueue
  retries.
- The implementation uses `delivery_id` for idempotency.

## Constraints

- Product and Engineering ratified the behavior on 2026-06-24.
- The durable term is "ACME webhook retry policy"; "retry window" is a
  misleading legacy filename, not a behavior change.
