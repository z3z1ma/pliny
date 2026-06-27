Status: active
Created: 2026-06-23
Updated: 2026-06-23
Parent:
Depends-On: .10x/tickets/2026-06-23-add-ledger-import-preview.md

# Ledger Import Parent

## Scope

Coordinate Ledger import preview execution while preserving durable learning
even if the child blocks before closure.

Included:

- Keep the child active or blocked until acceptance criteria, evidence, review,
  and retrospective obligations are coherent.
- Preserve reusable learning in the correct durable record type.
- Preserve the unresolved archive malformed-currency product decision as a
  blocker rather than guessed implementation behavior.

Excluded:

- Direct parent implementation.
- Direct implementation or archive import code changes.

## Acceptance Criteria

- Child ticket remains blocked while archive malformed-currency behavior is
  unresolved.
- Durable learning discovered during the blocked execution captures the fixture
  procedure and `sourceRef` naming convention in durable records.
- No child or parent closure is claimed before evidence, review, and blockers
  are coherent.
- No implementation files are edited while the blocker remains unresolved.

## Progress And Notes

- 2026-06-23: Child executor stopped before successful closure due unresolved
  archive malformed-currency behavior.
- 2026-06-23: Durable learning remains to be extracted for the Ledger fixture
  procedure and `sourceRef` naming convention.

## Blockers

- Archive malformed-currency behavior requires product ratification before
  child execution can continue.
