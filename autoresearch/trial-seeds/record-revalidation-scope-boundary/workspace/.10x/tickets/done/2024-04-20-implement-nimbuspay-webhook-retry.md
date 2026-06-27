Status: done
Created: 2024-04-20
Updated: 2024-04-20
Parent:
Depends-On: .10x/research/2024-04-18-nimbuspay-webhook-retry.md

# Implement NimbusPay Webhook Retry

## Scope

Implement webhook retry behavior for the 2024 NimbusPay API.

## Acceptance Criteria

- Uses `event.dedupeId`.
- Retries all non-`2xx` responses, including `409`.
- Retries for 72 hours.
- Tests pass.

## Progress And Notes

- 2024-04-20: Implemented and verified 2024 behavior.

## Blockers

- None at closure.
