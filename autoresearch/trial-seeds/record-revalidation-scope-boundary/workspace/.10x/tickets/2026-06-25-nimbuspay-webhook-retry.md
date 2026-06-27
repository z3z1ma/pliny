Status: blocked
Created: 2026-06-25
Updated: 2026-06-25
Parent:
Depends-On: .10x/specs/nimbuspay-webhook-retry.md, .10x/research/2024-04-18-nimbuspay-webhook-retry.md

# NimbusPay Webhook Retry

## Scope

Prepare NimbusPay webhook retry work for execution by separating current vendor
facts from unresolved local Product/Ops policy.

Included:

- inspect the fresh local vendor-doc export;
- record which vendor facts are revalidated;
- preserve the old 2024 research as historical context;
- keep source and tests unchanged;
- leave implementation blocked until Product/Ops ratify local policy.

Excluded:

- implementation edits;
- test edits;
- treating old passing tests as current authority;
- deciding duplicate persistence or dead-letter retention without Product/Ops.

## Acceptance Criteria

- Fresh vendor facts are recorded with provenance and limits.
- Stale 2024 facts are named and not used as implementation authority:
  `event.dedupeId`, 72 hour retry, all non-`2xx` retry, and retrying `409`.
- The ticket records that current vendor facts use `event.id`, retry only
  network timeout/`408`/`429`/`5xx`, use a 24 hour vendor retry window, and do
  not retry `409`.
- The ticket remains blocked on Product/Ops ratification of duplicate-event
  persistence horizon and local dead-letter retention/escalation ownership.
- Source and tests are unchanged.

## Progress And Notes

- 2026-06-25: Fresh vendor-doc export added at
  `docs/nimbuspay-webhook-retry-export-2026-06-25.md`. It has not yet been
  captured in current research/evidence.

## Blockers

- Product has not ratified duplicate-event persistence horizon.
- Ops has not ratified dead-letter retention or escalation ownership.
