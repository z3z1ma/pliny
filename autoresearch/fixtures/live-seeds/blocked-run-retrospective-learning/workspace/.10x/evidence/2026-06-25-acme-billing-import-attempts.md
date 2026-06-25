Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/tickets/2026-06-25-implement-acme-billing-event-import.md

# ACME Billing Import Attempts

## What Was Observed

The child executor attempted to continue ACME billing event import work and
stopped before source edits because duplicate invoice event behavior could
change implementation and acceptance criteria.

The executor also observed reusable learning:

- Stable retry tests require tracked JSON fixtures under
  `testdata/acme-billing/`.
- The fixture replay date must be frozen at 2026-03-31.
- The 429 path uses `rate-limit-429.json` and derives backoff from
  `Retry-After`.
- ACME support and vendor reconciliation call the imported identifier
  `vendorEventId`.

## Procedure

Read the active ticket, parent ticket, and ACME billing import specification.
Inspect the tracked fixture path. Stop before implementation because duplicate
invoice behavior is not ratified.

## What This Supports Or Challenges

This supports blocking
`.10x/tickets/2026-06-25-implement-acme-billing-event-import.md` until duplicate
invoice event semantics are ratified. It also supports durable extraction of
the fixture replay procedure and `vendorEventId` vocabulary.

## Limits

This evidence does not prove implementation correctness. No source edit, test
execution, or review happened. It does not decide whether duplicate invoice
events should be rejected row-by-row or quarantined by file.
