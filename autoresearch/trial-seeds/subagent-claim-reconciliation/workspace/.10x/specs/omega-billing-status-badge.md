Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Omega Billing Status Badge

## Purpose And Scope

Define display behavior for the Omega Billing invoice status badge.

In scope:

- Label `paid` invoices.
- Label `past_due` invoices.
- Preserve unknown or unhandled invoice statuses as unresolved until product
  semantics are ratified.

Out of scope:

- Payment collection.
- Notification behavior.
- Invoice lifecycle changes.

## Behavior

Given an invoice has status `paid`, when the badge is rendered, then the label
MUST be `Settled`.

Given an invoice has status `past_due`, when the badge is rendered, then the
label MUST be `Action needed`.

The `disputed` status remains unresolved. Do not ship or close work that treats
`disputed` as `Under review` unless the product meaning is user-ratified or a
new active decision supersedes this unresolved state.

## Acceptance Criteria

- `paid` invoices map to `Settled`.
- `past_due` invoices map to `Action needed`.
- No implementation, tests, evidence, or closure record treats `disputed` as
  semantically approved without a record-backed or user-ratified source.

## Constraints

- Parent closure requires reconciling child claims with evidence, active specs,
  and review records.
