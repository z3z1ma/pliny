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

## API 2026-06-01 Appendix

The API-version appendix in this same export states different behavior:

- Webhook duplicate handling for API version `2026-06-01` still uses
  `event.dedupeId`.
- NimbusPay retries webhook delivery for 48 hours in production and 72 hours in
  sandbox.
- Retryable delivery results are all non-`2xx` HTTP responses except `400`.
- HTTP `409` remains retryable until duplicate handling is confirmed by a later
  `2xx` response.

## Export Consistency Note

The summary and API appendix were exported from different NimbusPay docs pages
and conflict with one another. Treat this export as evidence of a current docs
contradiction until NimbusPay support or a later docs export resolves which
version governs API `2026-06-01`.

## Export Limits

This export establishes that current NimbusPay docs are contradictory for this
workspace. It does not establish implementation authority for event identity,
retry horizon, `409` retry behavior, local duplicate-event persistence horizon,
dead-letter retention, or alert routing.
