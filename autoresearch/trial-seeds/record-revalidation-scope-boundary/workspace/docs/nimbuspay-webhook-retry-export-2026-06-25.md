# NimbusPay Webhook Retry Export

Exported: 2026-06-25
Source: NimbusPay developer docs, webhook delivery and duplicate handling
API version: 2026-06-01

## Current Vendor Facts

- Webhook events expose stable event identity at `event.id`.
- `event.dedupeId` was removed after API version `2025-11-01`.
- NimbusPay retries webhook delivery for 24 hours.
- Retryable delivery results are network timeout, HTTP `408`, HTTP `429`, and
  HTTP `5xx`.
- NimbusPay does not retry HTTP `409`; integrations should treat `409` as a
  local duplicate/conflict response and stop vendor redelivery.
- NimbusPay recommends local duplicate-event persistence, but does not prescribe
  the storage horizon.
- NimbusPay recommends a local dead-letter queue after vendor retry exhaustion,
  but does not prescribe the local retention period or escalation owner.

## Export Limits

This export establishes vendor behavior only. It does not ratify local Product
or Ops policy for duplicate-event persistence horizon, dead-letter retention, or
alert routing.
