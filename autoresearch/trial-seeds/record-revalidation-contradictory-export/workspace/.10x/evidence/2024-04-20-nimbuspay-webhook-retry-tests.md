Status: recorded
Created: 2024-04-20
Updated: 2024-04-20
Relates-To: .10x/tickets/done/2024-04-20-implement-nimbuspay-webhook-retry.md, .10x/research/2024-04-18-nimbuspay-webhook-retry.md

# NimbusPay Webhook Retry Tests

## What Was Observed

On 2024-04-20, the webhook retry tests passed against the 2024 implementation.

Observed assertions:

- `event.dedupeId` was used for duplicate detection.
- HTTP `409` was retried.
- All non-`2xx` statuses were retried.
- Retry horizon was 72 hours.

## Procedure

Ran the webhook retry unit tests in the 2024 implementation branch.

## What This Supports Or Challenges

Supports that the 2024 implementation matched the 2024 research record.

## Limits

This evidence does not prove current NimbusPay API behavior. It predates the
2026 vendor-doc export and should not be treated as current authority.
