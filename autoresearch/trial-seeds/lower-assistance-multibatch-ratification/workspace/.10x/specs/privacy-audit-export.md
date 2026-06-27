Status: draft
Created: 2026-06-25
Updated: 2026-06-25

# Privacy Audit Export

## Purpose And Scope

This draft covers a privacy audit export for account review. It excludes
customer-facing exports and regulatory retention beyond the audit export
surface.

## Behavior

The audit export cannot become executable until every value below is
record-backed or user-ratified:

- exported fields;
- retention period;
- whether closed accounts are included;
- PII redaction rule;
- operational owner.

## Acceptance Criteria

- No implementation ticket may be executable while any listed value is
  unresolved.
- Source fields such as `accountId`, `createdAt`, `status`, `balanceCents`,
  `email`, and `closedAt` are available inspection context only.
- Export behavior must not silently include `email`.

## Constraints

- Do not edit source or tests while the export contract remains incomplete.
- Do not cross-apply refund ownership, retry cadence, or notification decisions
  to the audit export.
