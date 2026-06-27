Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Ledger Import Terms

## Glossary Terms

- `sourceRef`: stable identifier from the source ledger file used to trace an
  imported row back to the external ledger record.

## Conventions And Preferences

Ledger import records use `sourceRef`; do not rename it to `externalId`.

## Heuristics And Nuances

When writing reusable Ledger import procedures, use `sourceRef` consistently in
examples so future agents do not reintroduce the older `externalId` term.
