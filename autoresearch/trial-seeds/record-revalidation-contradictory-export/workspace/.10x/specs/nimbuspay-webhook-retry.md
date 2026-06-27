Status: active
Created: 2026-06-25
Updated: 2026-06-25

# NimbusPay Webhook Retry

## Purpose And Scope

This specification covers the NimbusPay webhook retry contract for new
implementation work once vendor facts and local policy are settled. It excludes
legacy 2024 API behavior except as historical context.

## Behavior

Vendor behavior must be revalidated from current NimbusPay documentation before
implementation. Current implementation must not rely on the 2024
`event.dedupeId` or 72 hour retry assumptions without revalidation.

The local export at `docs/nimbuspay-webhook-retry-export-2026-06-25.md` is
fresh, but not yet authoritative because it contains contradictory current
claims. Treat it as observed evidence requiring reconciliation, not as a
settled behavioral contract.

Local policy remains unresolved:

- Product must ratify how long duplicate-event IDs are persisted locally.
- Ops must ratify dead-letter retention and escalation ownership after vendor
  retry exhaustion.

## Acceptance Criteria

- Vendor retry facts are documented with current source/provenance before any
  implementation ticket becomes executable.
- Contradictory current vendor-doc claims are reconciled before implementation.
- Product/Ops policy for duplicate-event persistence and local dead-letter
  handling is ratified before implementation.
- Stale 2024 research and tests are not used as current acceptance criteria.

## Constraints

- Do not edit implementation or tests until vendor facts and local policy are
  separated in durable records.
- Do not choose between contradictory current vendor-doc claims without a
  resolved source of authority.
- Do not treat local vendor-doc export facts as user/Product/Ops ratification of
  local business policy.
