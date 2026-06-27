Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Customer Import Amount Parser

## Purpose And Scope

Define parsing for customer import rows before they are persisted.

In scope:

- `src/imports/parseImportAmount.ts`
- Boundary validation for untrusted CSV/import input.
- Explicit rejection of invalid, missing, negative, or non-finite amounts.

Out of scope:

- CSV file loading.
- Database writes.
- Currency conversion.
- UI display formatting.

## Behavior

Given an import row amount, when the value is a string containing a non-negative
finite decimal number, then the parser returns the numeric amount.

Given an import row amount is missing, blank, negative, non-numeric, infinite,
or NaN, then the parser rejects it before persistence.

## Acceptance Criteria

- Valid non-negative finite decimal strings parse to numbers.
- Missing, blank, negative, non-numeric, infinite, and NaN-like values throw
  explicit errors before any caller can persist them.
- Simplification work may remove incidental helpers only if the trust-boundary
  validation remains equivalent or stronger.

## Constraints

- Import rows are an absolute trust boundary.
- Do not rely on upstream callers to validate the amount.
- Do not remove explicit corruption-prevention errors to reduce code size.
