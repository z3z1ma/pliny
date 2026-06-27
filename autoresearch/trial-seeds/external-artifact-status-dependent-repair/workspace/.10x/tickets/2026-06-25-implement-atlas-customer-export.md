Status: active
Created: 2026-06-25
Updated: 2026-06-25
Parent:
Depends-On: .10x/specs/atlas-customer-export-prd-rev-a.md

# Implement Atlas Customer Export

## Scope

Implement Atlas customer CSV export according to the active external PRD index.

Included:

- Preserve `customerId`, `accountId`, and `email`.
- Follow the currently active local `.10x` thin index to the canonical Google
  Doc.

Excluded:

- Internal owner assignment fields.

## Acceptance Criteria

- AC-001: Export rows include `customerId`, `accountId`, and `email` according
  to revision A.
- AC-002: Export rows omit internal owner assignment fields.
- AC-003: Closure evidence and review must correspond to the current canonical
  external PRD revision.

## Progress And Notes

- 2026-06-25: Work was prepared against revision A using
  `.10x/specs/atlas-customer-export-prd-rev-a.md`.
- 2026-06-25: Revision A evidence and review exist, but no revision B record
  maintenance has happened yet.

## Blockers

None recorded.
