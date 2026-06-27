Status: open
Created: 2026-06-25
Updated: 2026-06-25
Parent:
Depends-On: .10x/specs/ledger-import-preview-v2.md

# Verify Ledger Import V2 Fixture Replay

## Scope

Run the Ledger import v2 fixture replay verification using the tracked v2
fixture and record evidence. Do not edit implementation files, fixture files,
or skill files.

## Acceptance Criteria

- The verification uses `testdata/ledger/import-preview-v2.csv`.
- The verification uses posting date `2026-02-20`.
- The observed output preserves `sourceRef` values `LEDGER-V2-001` and
  `LEDGER-V2-002`.
- The observed output reports `amountCents` values `15600` and `-250`.
- A `.10x/evidence/` record captures the command, output, validation, and
  limits.
- No implementation files are edited.
- Existing v1 skill, evidence, and review records are not treated as v2 proof.

## Progress And Notes

- 2026-06-25: Ticket opened after active Ledger import preview requirements
  moved from v1 fixture replay to v2 fixture replay. The old replay skill still
  exists for historical v1 procedure memory and must not be used as v2 proof.

## Blockers

- None known.
