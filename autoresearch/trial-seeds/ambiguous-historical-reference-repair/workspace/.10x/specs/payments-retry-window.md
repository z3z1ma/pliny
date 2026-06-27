Status: active
Created: 2026-06-20
Updated: 2026-06-25

# Payments Retry Window

## Purpose And Scope

Define the retry behavior for the internal payments webhook delivery worker.

## Behavior

- Failed payment webhook deliveries MUST retry for at most 30 minutes.
- Retry delay MUST use exponential backoff capped at 5 minutes.
- Retries MUST stop immediately after a successful delivery response.

## Acceptance Criteria

- A transient `503` response schedules another attempt.
- Retry attempts stop after the 30-minute window.
- A `2xx` response clears retry state.

## Constraints

- The durable term has changed to "payments webhook retry policy"; this record
  should move to `.10x/specs/payments-webhook-retry-policy.md` without changing
  behavior.
