Status: open
Created: 2026-06-25
Updated: 2026-06-25
Parent:
Depends-On: .10x/specs/ledger-import-preview.md

# Verify Ledger Import Fixture Replay

## Scope

Run the Ledger import fixture replay verification using the tracked fixture and
record evidence. Do not edit implementation files, fixture files, or skill
files.

## Acceptance Criteria

- The verification uses `testdata/ledger/import-preview.csv`.
- The verification uses posting date `2026-01-15`.
- The observed output preserves `sourceRef` values `LEDGER-001` and
  `LEDGER-002`.
- The observed output reports `amountCents` values `12345` and `-678`.
- A `.10x/evidence/` record captures the command, output, validation, and
  limits.
- No implementation files are edited.

## Progress And Notes

- 2026-06-25: Ticket opened after the fixture replay procedure was distilled
  into an active project skill.

## Blockers

- None known.
