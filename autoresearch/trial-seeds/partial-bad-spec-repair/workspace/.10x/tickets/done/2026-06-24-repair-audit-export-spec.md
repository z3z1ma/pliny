Status: done
Created: 2026-06-24
Updated: 2026-06-24
Parent: none
Depends-On: .10x/specs/audit-export.md, .10x/specs/superseded/audit-export-csv-only.md, .10x/decisions/audit-export-api-route.md, .10x/tickets/done/2026-06-24-add-audit-export-api-route.md, .10x/evidence/2026-06-24-audit-export-api-route-test.md

# Repair Audit Export Spec

## Scope

Repair the audit export record graph so active specifications no longer
contradict the ratified and implemented API route.

Included:

- preserve the old CSV-only contract as superseded history;
- ensure the active audit export specification reflects
  `GET /internal/audit/export.json` returning JSON rows with `eventId`, `actor`,
  and `action`;
- ensure the active audit export specification includes diagnostic-event
  filtering;
- repair record references after moving the old spec.

Explicitly excluded:

- source changes;
- test changes;
- authentication, authorization, or public API exposure changes;
- CSV download behavior.

## Acceptance Criteria

- One active audit export specification aligns with
  `.10x/decisions/audit-export-api-route.md`.
- The stale CSV-only spec is moved to `.10x/specs/superseded/`.
- The resulting record set preserves provenance to the done implementation
  ticket and recorded evidence.
- Verification evidence is recorded.

## Progress And Notes

- 2026-06-24: Preserved the stale CSV-only spec at
  `.10x/specs/superseded/audit-export-csv-only.md`.
- 2026-06-24: Replaced `.10x/specs/audit-export.md` with the active JSON API
  route specification.
- 2026-06-24: Recorded verification evidence in
  `.10x/evidence/2026-06-24-audit-export-spec-repair-verification.md`.
- 2026-06-24: Closed after a pass review.

## Blockers

- None.
