Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Privacy Audit Export

## Purpose And Scope

This specification covers a privacy audit export for account review. It excludes
customer-facing exports and regulatory retention beyond the audit export
surface.

## Behavior

User-ratified policy values:

- retention period is 90 days;
- closed accounts are excluded from the export;
- exported fields are exactly `accountId`, `createdAt`, `status`, and
  `balanceCents`;
- emails are redacted entirely by omission from export rows;
- Data Platform owns the audit export.

## Acceptance Criteria

- An export row MUST include only `accountId`, `createdAt`, `status`, and
  `balanceCents`.
- Accounts with `closedAt` set MUST NOT produce an export row.
- Exported audit data MUST be retained for 90 days.
- Export rows MUST NOT include `email`.
- Source fields such as `accountId`, `createdAt`, `status`, `balanceCents`,
  `email`, and `closedAt` are available inspection context only.

## Constraints

- Do not cross-apply refund ownership, retry cadence, or notification decisions
  to the audit export.
