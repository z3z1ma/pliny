Status: open
Created: 2026-06-24
Updated: 2026-06-24
Parent: none
Depends-On: .10x/specs/audit-export.md, .10x/specs/superseded/audit-export-csv-only.md, .10x/decisions/audit-export-api-route.md, .10x/tickets/done/2026-06-24-repair-audit-export-spec.md, .10x/evidence/2026-06-24-audit-export-spec-repair-verification.md

# Audit Export Post Repair Hygiene

## Scope

Inspect the audit export record graph after the prior spec repair and fix any
remaining active-record contradiction.

Included:

- inspect the active audit export spec and superseded CSV-only spec;
- inspect the prior repair ticket, repair evidence, pass review, active
  decision, implementation ticket, and source/tests as needed to establish
  authority;
- remove stale active specification language only if the active record still
  contradicts the API route authority;
- record bounded verification evidence;
- close this ticket if the record graph is coherent after repair.

Explicitly excluded:

- source changes;
- test changes;
- running tests;
- changing the superseded CSV-only history except for reference repair if
  strictly necessary.

## Acceptance Criteria

- No active audit export specification says no HTTP API route exists.
- The active audit export specification remains aligned to
  `.10x/decisions/audit-export-api-route.md`.
- The superseded CSV-only contract remains preserved as historical context.
- Verification evidence records the active-spec hygiene check and its limits.
- This ticket is moved to `tickets/done/` only after the active record set is
  coherent.

## Progress And Notes

- 2026-06-24: Opened after a post-repair scan suggested the active
  `.10x/specs/audit-export.md` may still contain one stale no-route acceptance
  criterion despite otherwise describing the API route contract.

## Blockers

- None known. Authority should be derived from active decision, active spec
  body, done implementation ticket, evidence, and source/tests.
