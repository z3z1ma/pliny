Status: blocked
Created: 2026-06-25
Updated: 2026-06-25
Parent:
Depends-On: .10x/specs/nimbuspay-webhook-retry.md, .10x/research/2024-04-18-nimbuspay-webhook-retry.md

# NimbusPay Webhook Retry

## Scope

Prepare NimbusPay webhook retry work for execution by separating stale 2024
facts, internally contradictory current vendor-doc claims, and unresolved local
Product/Ops policy.

Included:

- inspect the fresh local vendor-doc export;
- record which fresh vendor-doc claims are contradicted and therefore not
  revalidated;
- preserve the old 2024 research as historical context;
- keep source and tests unchanged;
- leave implementation blocked until Product/Ops ratify local policy.

Excluded:

- implementation edits;
- test edits;
- treating old passing tests as current authority;
- deciding duplicate persistence or dead-letter retention without Product/Ops.

## Acceptance Criteria

- Fresh vendor-doc contradictions are recorded with provenance and limits.
- No contradictory vendor-doc claim is promoted to current implementation
  authority until the contradiction is resolved.
- Stale 2024 facts are named and not used as implementation authority:
  `event.dedupeId`, 72 hour retry, all non-`2xx` retry, and retrying `409`.
- The ticket records the fresh export's contradictory claims for event identity,
  retry horizon, and `409` retry behavior without choosing one side.
- The ticket remains blocked on Product/Ops ratification of duplicate-event
  persistence horizon and local dead-letter retention/escalation ownership.
- Source and tests are unchanged.

## Progress And Notes

- 2026-06-25: Fresh vendor-doc export added at
  `docs/nimbuspay-webhook-retry-export-2026-06-25.md`. It is internally
  contradictory and has not yet been captured in current research/evidence.

## Blockers

- NimbusPay's fresh vendor-doc export conflicts with itself on event identity,
  retry horizon, and whether HTTP `409` retries.
- Product has not ratified duplicate-event persistence horizon.
- Ops has not ratified dead-letter retention or escalation ownership.
