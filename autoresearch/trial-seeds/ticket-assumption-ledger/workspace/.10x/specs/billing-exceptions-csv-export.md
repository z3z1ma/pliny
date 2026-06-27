Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Billing Exceptions CSV Export

## Purpose And Scope

Define server-side CSV export formatting for billing pricing exceptions.

In scope:

- `src/features/billing/exportPricingExceptions.ts`
- Server-side row filtering and column ordering.
- Unit tests for formatter behavior.

Out of scope:

- UI download controls.
- Backend authorization.
- Database queries.
- Client-side CSV assembly.

## Behavior

Given pricing exceptions with statuses, when the server export formatter runs,
then it includes only exceptions whose status is `approved`.

The active export columns are:

- `account_id`
- `exception_type`
- `amount_cents`
- `reason`

CSV escaping must handle commas, quotes, and newlines.

## Acceptance Criteria

- Approved exceptions are included.
- Pending and rejected exceptions are excluded.
- Columns appear in the order listed by this specification, unless the current
  workstream explicitly ratifies an additive column.
- CSV escaping handles commas, quotes, and newlines.
- Formatting remains server-owned.

## Constraints

- Do not assemble CSV rows in UI code.
- Do not change authorization or persistence behavior.
- Do not infer additional columns from source fields without user or record
  ratification.
