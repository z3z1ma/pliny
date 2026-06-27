Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Ledger Import Terms

## Glossary Terms

- `sourceRef`: stable identifier from the source ledger file used to trace an
  imported row back to the external ledger record.

## Conventions And Preferences

Ledger import records use `sourceRef`; do not rename it to `externalId`.

The current verification target is Ledger import preview v2. V2 verification
uses `testdata/ledger/import-preview-v2.csv` and posting date `2026-02-20`.
Older v1 replay examples remain historical evidence only.

## Heuristics And Nuances

Reusable Ledger import procedures should use `sourceRef` consistently in
examples so future agents do not reintroduce the older `externalId` term.
