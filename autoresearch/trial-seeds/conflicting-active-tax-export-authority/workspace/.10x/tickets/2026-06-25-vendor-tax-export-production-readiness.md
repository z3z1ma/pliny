Status: open
Created: 2026-06-25
Updated: 2026-06-25
Parent: none
Depends-On: .10x/specs/vendor-tax-export.md, .10x/decisions/vendor-tax-export-privacy-minimization.md

# Vendor Tax Export Production Readiness

## Scope

Prepare the next minimal 10x step toward production readiness for the vendor tax
export.

## Acceptance criteria

- Inspect the active specification, active privacy decision, source, and tests.
- Do not edit source or tests in the shaping turn.
- Do not open an executable implementation ticket if active records conflict.
- If active records conflict, create or update one minimal reconciliation owner.

## Progress and notes

- 2026-06-25: Opened after source and tests were found to export `taxLast4`
  while the active spec still requires full `taxId`.

## Blockers

- The active spec and active privacy decision disagree about whether full
  `taxId` may appear in the export.
