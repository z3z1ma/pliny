Status: open
Created: 2026-06-24
Updated: 2026-06-24
Parent: none
Depends-On: .10x/specs/audit-export.md, .10x/decisions/audit-export-api-route.md, .10x/tickets/done/2026-06-24-add-audit-export-api-route.md, .10x/evidence/2026-06-24-audit-export-api-route-test.md

# Repair Audit Export Spec

## Scope

Repair the audit export record graph so active specifications no longer
contradict the ratified and implemented API route.

Included:

- supersede or replace `.10x/specs/audit-export.md`;
- ensure the active audit export specification reflects
  `GET /internal/audit/export.json` returning JSON rows with `eventId`, `actor`,
  and `action`;
- ensure the active audit export specification includes diagnostic-event
  filtering, matching the done ticket and recorded test evidence;
- repair record references if any record is moved or renamed.

Explicitly excluded:

- source changes;
- test changes;
- authentication, authorization, or public API exposure changes;
- CSV download behavior.

## Acceptance Criteria

- No active specification says audit export MUST NOT expose an HTTP API route.
- One active audit export specification aligns with
  `.10x/decisions/audit-export-api-route.md`.
- The stale CSV-only spec is moved to `.10x/specs/superseded/` or replaced in
  place with a coherent active specification.
- The resulting record set preserves provenance to the done implementation
  ticket and recorded evidence.
- Verification evidence is recorded showing the active spec set no longer
  contains the stale no-HTTP-route requirement.

## Progress And Notes

- 2026-06-24: Opened after inspection showed `.10x/specs/audit-export.md`
  conflicts with `.10x/decisions/audit-export-api-route.md`,
  `.10x/tickets/done/2026-06-24-add-audit-export-api-route.md`, recorded
  evidence, and current `src/audit/exportRoute.js` /
  `src/audit/exportRoute.test.js`.

## Blockers

- None. The active decision resolves authority: the API route is intended
  behavior, and the active spec is stale.
