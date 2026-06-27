Status: draft
Created: 2026-06-24
Updated: 2026-06-24

# Zeus Webhook Retry

## Purpose And Scope

Draft retry behavior for Zeus ledger webhooks. This draft was created before
Security reviewed provider replay semantics.

## Behavior

- Retry every non-`2xx` response for one hour.
- Treat `409` responses as terminal duplicate delivery.
- Persist `event.id` as the idempotency key.

## Acceptance Criteria

- Receiver failures produce retry jobs for non-`2xx` responses.
- `409` responses do not retry.
- The receiver stores `event.id` for dedupe.

## Constraints

- This draft is not approved for implementation.
- Security review is required before any executable ticket uses this behavior.
