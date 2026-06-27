Status: active
Created: 2026-06-25
Updated: 2026-06-25
Parent: .10x/tickets/2026-06-25-acme-billing-import-parent.md
Depends-On: .10x/specs/acme-billing-event-import.md

# Implement ACME Billing Event Import

## Scope

Implement ACME billing event import behavior for vendor invoice events.

Included:

- Preserve imported event `vendorEventId`.
- Use tracked JSON fixtures for ACME 429 retry testing.
- Derive retry backoff from the fixture `Retry-After` header.

Excluded:

- Discount amount validation.
- Live ACME API calls.
- Duplicate invoice event behavior until product chooses reject-row or
  quarantine-file semantics.

## Acceptance Criteria

- AC-001: Imported ledger records include each event's `vendorEventId`.
- AC-002: Retry tests replay tracked ACME billing fixtures from
  `testdata/acme-billing/`.
- AC-003: Retry tests freeze the vendor clock at 2026-03-31 and assert backoff
  from `Retry-After`.
- AC-004: Duplicate invoice event behavior follows the product decision once
  the reject-row versus quarantine-file choice is ratified.
- AC-005: Durable learning discovered before closure is preserved even if the
  ticket remains blocked.

## Progress And Notes

- 2026-06-25: Child executor attempted to continue implementation but stopped
  before successful closure because duplicate invoice event behavior is not
  ratified.
- 2026-06-25: Durable execution learning: stable ACME 429 retry tests require
  tracked JSON fixtures under `testdata/acme-billing/`, a frozen vendor date of
  2026-03-31, replaying `rate-limit-429.json`, and asserting backoff from the
  fixture `Retry-After` header rather than making live ACME calls.
- 2026-06-25: Durable execution learning: imported ACME billing event identifiers
  are named `vendorEventId`, not `eventId` or `externalId`.
- 2026-06-25: Out-of-scope follow-up risk: malformed discount amount coverage is
  missing but belongs outside this duplicate-event blocker.
- 2026-06-25: Blocked semantic value: duplicate invoice event behavior needs
  product ratification between reject-row and quarantine-file.

## Blockers

- Duplicate invoice event behavior is unresolved. Do not implement, verify,
  review, or close until the reject-row versus quarantine-file product decision
  is ratified and recorded.
