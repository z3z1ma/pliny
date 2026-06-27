Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Ledger Import Terms

## Glossary Terms

- `sourceRef`: stable identifier from the source ledger file used to trace an
  imported row back to the external ledger record.

## Conventions And Preferences

Ledger import records use `sourceRef`; do not rename it to `externalId`.

## Heuristics And Nuances

Reusable Ledger import procedures should use `sourceRef` consistently in
examples so future agents do not reintroduce the older `externalId` term.
