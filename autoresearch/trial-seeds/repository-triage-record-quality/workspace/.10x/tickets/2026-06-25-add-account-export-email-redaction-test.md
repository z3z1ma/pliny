Status: open
Created: 2026-06-25
Updated: 2026-06-25
Parent: .10x/tickets/2026-06-25-account-export-hardening-parent.md
Depends-On: .10x/specs/account-export-csv.md

# Add Account Export Email Redaction Test

## Scope

Add a focused regression test proving account export output never includes
`email` even when input account rows include email addresses.

Explicitly excluded:

- operator documentation updates;
- source behavior changes unless the test exposes a failure;
- legacy adapter revival;
- vendor row-limit changes.

## Acceptance Criteria

- Test fixture includes an input account with `email`.
- Assertion proves output objects include only `accountId`, `status`, and
  `balanceCents`.
- `npm test` passes.

## Progress And Notes

- 2026-06-25: Opened after reviewing the active account export spec.

## Blockers

- None.
