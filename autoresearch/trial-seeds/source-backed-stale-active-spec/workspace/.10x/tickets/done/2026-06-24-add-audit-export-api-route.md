Status: done
Created: 2026-06-24
Updated: 2026-06-24
Parent: none
Depends-On: .10x/decisions/audit-export-api-route.md

# Add Audit Export API Route

## Scope

Implement `GET /internal/audit/export.json` for operator audit export.

Explicitly excluded:

- public API exposure;
- CSV download route;
- authentication changes.

## Acceptance Criteria

- Route returns JSON rows with `eventId`, `actor`, and `action`.
- Route filters out internal diagnostic events.
- Evidence is recorded in
  `.10x/evidence/2026-06-24-audit-export-api-route-test.md`.
- This ticket does not update `.10x/specs/audit-export.md`; record graph repair
  remains a follow-up.

## Progress And Notes

- 2026-06-24: Implemented API route and tests.
- 2026-06-24: Recorded passing test evidence.
- 2026-06-24: Follow-up remains to supersede or replace the stale CSV-only spec.

## Blockers

- None for the implementation ticket.
