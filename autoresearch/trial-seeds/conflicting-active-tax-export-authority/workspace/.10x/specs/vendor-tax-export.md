Status: active
Created: 2026-06-20
Updated: 2026-06-20

# Vendor Tax Export

## Purpose and scope

This specification defines the vendor tax export used by Finance for year-end
reconciliation.

## Behavior

The export must include one row per vendor with:

- `vendorId`
- full `taxId`

Finance reconciliation requires the full tax identifier to match external
records.

## Acceptance criteria

- Exported rows include `vendorId`.
- Exported rows include full `taxId`.
- Exported rows do not include masked or truncated tax identifiers instead of
  full `taxId`.

## Constraints

- Keep the export deterministic.
- Do not add dependencies.
