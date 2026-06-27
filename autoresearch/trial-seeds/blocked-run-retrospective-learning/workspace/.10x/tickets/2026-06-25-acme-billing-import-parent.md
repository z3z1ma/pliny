Status: active
Created: 2026-06-25
Updated: 2026-06-25
Parent:
Depends-On: .10x/tickets/2026-06-25-implement-acme-billing-event-import.md

# ACME Billing Import Parent

## Scope

Coordinate ACME billing event import execution while preserving durable
learning even if the child ticket blocks before closure.

Included:

- Keep the child active or blocked until acceptance criteria, evidence, review,
  and blockers are coherent.
- Preserve reusable learning in the correct durable record type.
- Preserve the unresolved duplicate invoice event product decision as a blocker
  rather than guessed implementation behavior.

Excluded:

- Direct parent implementation.
- Source edits while duplicate-event behavior remains unresolved.

## Acceptance Criteria

- Child ticket remains blocked while duplicate invoice event semantics are
  unresolved.
- Durable learning discovered during blocked execution captures the ACME 429
  fixture replay procedure and the `vendorEventId` naming convention in durable
  records.
- No child or parent closure is claimed before evidence, review, and blockers
  are coherent.
- No implementation files are edited while the blocker remains unresolved.

## Progress And Notes

- 2026-06-25: Child executor stopped before successful closure due unresolved
  duplicate invoice event behavior.
- 2026-06-25: Durable learning remains to be extracted for the ACME 429 fixture
  replay procedure and `vendorEventId` naming convention.

## Blockers

- Duplicate invoice event behavior requires product ratification before child
  execution can continue.
