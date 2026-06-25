Status: active
Created: 2026-06-25
Updated: 2026-06-25

# ACME Billing Event Import

## Purpose And Scope

This specification covers importing ACME billing vendor events into the local
billing ledger.

Included:

- Preserve each vendor event identifier as `vendorEventId`.
- Parse invoice-created and invoice-paid events from tracked JSON fixtures.
- Retry vendor reads according to `Retry-After` when ACME returns HTTP 429.

Excluded:

- Duplicate invoice event semantics.
- Discount amount validation.
- Live ACME API calls during tests.

## Behavior

- Given an ACME invoice event with `vendorEventId`, when the event is imported,
  then the ledger record preserves that value without renaming it to `eventId`
  or `externalId`.
- Given a tracked ACME 429 fixture with `Retry-After`, when the retry harness is
  exercised, then backoff is derived from the fixture header and not from a live
  ACME API call.
- Duplicate invoice events are not specified. Do not implement reject, merge,
  or quarantine behavior until product ratifies the durable semantics.

## Acceptance Criteria

- AC-001: Imported ledger records preserve `vendorEventId`.
- AC-002: Tests replay tracked ACME JSON fixtures and make no live API calls.
- AC-003: HTTP 429 retry behavior derives backoff from `Retry-After`.
- AC-004: Duplicate invoice event behavior is implemented only after the
  reject-row versus quarantine-file product decision is ratified.

## Constraints

- The fixture replay date for ACME billing import tests is 2026-03-31.
- Do not rename `vendorEventId` to `eventId` or `externalId`; ACME support and
  vendor reconciliation use the vendor term.
- Discount amount validation is outside this specification and must not be
  silently folded into the duplicate-event ticket.
