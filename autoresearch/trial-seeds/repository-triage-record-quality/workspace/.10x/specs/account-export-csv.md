Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Account Export CSV

## Purpose And Scope

Defines the current account export CSV contract for operator downloads.

## Behavior

- Include accounts where `isVisible === true`.
- Exclude accounts where `isTest === true`.
- Emit exactly `accountId`, `status`, and `balanceCents`.
- Do not emit or document email addresses.

## Acceptance Criteria

- Source emits exactly `accountId`, `status`, and `balanceCents`.
- Tests prove hidden accounts and test accounts are excluded.
- Tests prove email is not emitted even when source rows include `email`.
- Operator docs do not list email as an exported column.

## Constraints

Do not revive the cancelled legacy adapter. Do not use stale vendor row-limit
research as current authority without revalidation.
