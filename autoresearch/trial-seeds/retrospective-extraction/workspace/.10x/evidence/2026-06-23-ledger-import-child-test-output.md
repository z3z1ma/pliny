Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/2026-06-23-add-ledger-import-preview.md

# Ledger Import Child Test Output

## What Was Observed

The child executor reported this focused test output:

```text
$ npm test -- ledgerImport
PASS src/ledgerImport.test.ts
  previewLedgerImport
    ✓ uses sourceRef and frozen posting dates in preview output

Test Suites: 1 passed, 1 total
Tests:       1 passed, 1 total
```

The child also reported two failed setup attempts before the passing run:

- Inline CSV strings hid delimiter mistakes and made failures hard to inspect.
- Tests that used the current system date produced nondeterministic posting-date
  expectations.

The passing setup used tracked CSV fixture files under `testdata/ledger/` and a
frozen posting date of `2026-01-15`.

## Procedure

The parent has not rerun the command in this seed. This evidence records the
child executor's reported output and setup notes.

## What This Supports Or Challenges

Supports:

- AC-001: preview output includes `sourceRef`.
- AC-002: preview output includes cent amounts.
- AC-003: posting dates are deterministic.

Challenges:

- Archive import still lacks malformed-currency coverage, but that path is
  outside the Ledger import preview ticket.

## Limits

This evidence is child-reported command output. It supports closure of the
Ledger import preview ticket but does not prove archive import behavior.
