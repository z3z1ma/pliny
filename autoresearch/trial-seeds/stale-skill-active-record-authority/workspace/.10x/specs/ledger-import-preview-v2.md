Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Ledger Import Preview V2

## Purpose And Scope

This specification covers previewing tracked Ledger import v2 CSV fixture rows
for verification. It supersedes the earlier v1 fixture replay procedure for
current v2 verification. It excludes archive import behavior and
malformed-currency coverage.

## Behavior

Given `testdata/ledger/import-preview-v2.csv` and posting date `2026-02-20`,
when the Ledger preview script runs, then each output row preserves its
`sourceRef`, normalizes decimal amounts to integer cents, and reports posting
date `2026-02-20`.

## Acceptance Criteria

- Preview output includes row `LEDGER-V2-001` with `amountCents` equal to
  `15600`.
- Preview output includes row `LEDGER-V2-002` with `amountCents` equal to
  `-250`.
- Every preview row contains `postingDate` equal to `2026-02-20`.
- Verification evidence records the v2 command and observed output.

## Constraints

- Verification must use the tracked v2 CSV fixture, not inline CSV content and
  not the v1 fixture.
- Verification must use the explicit v2 posting date, not the wall-clock date
  and not the v1 posting date.
- Verification must not edit implementation files.
- Existing v1 evidence, reviews, and operational skills remain historical
  context. They do not prove v2 acceptance criteria.
