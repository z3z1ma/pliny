Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Ledger Import Preview

## Purpose And Scope

This specification covers previewing tracked Ledger import CSV fixture rows for
verification. It excludes archive import behavior and malformed-currency
coverage.

## Behavior

Given `testdata/ledger/import-preview.csv` and posting date `2026-01-15`, when
the Ledger preview script runs, then each output row preserves its `sourceRef`,
normalizes decimal amounts to integer cents, and reports posting date
`2026-01-15`.

## Acceptance Criteria

- Preview output includes row `LEDGER-001` with `amountCents` equal to `12345`.
- Preview output includes row `LEDGER-002` with `amountCents` equal to `-678`.
- Every preview row contains `postingDate` equal to `2026-01-15`.
- Verification evidence records the command and observed output.

## Constraints

- Verification must use the tracked CSV fixture, not inline CSV content.
- Verification must use the explicit posting date, not the wall-clock date.
- Verification must not edit implementation files.
