Status: open
Created: 2026-06-25
Updated: 2026-06-25
Parent: .10x/tickets/2026-06-25-shape-refund-and-audit-rollout.md
Depends-On: .10x/specs/privacy-audit-export.md

# Implement Privacy Audit Export

## Scope

Implement the privacy audit export behavior in `src/audit/exportRows.js`
according to `.10x/specs/privacy-audit-export.md`.

Included:

- export only `accountId`, `createdAt`, `status`, and `balanceCents`;
- exclude closed accounts;
- represent export readiness as policy-ready for the ratified audit export
  contract.

Excluded:

- customer-facing exports;
- refund auto-approval behavior;
- regulatory retention beyond the 90-day audit export policy;
- adding new dependencies or unrelated infrastructure.

## Acceptance Criteria

- `auditExportContext(account)` returns only `accountId`, `createdAt`,
  `status`, and `balanceCents` for an open account.
- Export behavior omits `email` entirely.
- `auditExportContext(account)` returns `null` for a closed account, identified
  by a set `closedAt`, so the row builder produces no export row.
- `classifyAuditExportReadiness()` no longer reports
  `audit_export_policy_unratified`.
- Verification records evidence for the implemented behavior and its limits.

## Progress And Notes

- 2026-06-25: Ticket opened after audit export policy blockers were ratified.
  Source inspection found the target surface in `src/audit/exportRows.js`.

## Blockers

None.
