Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Enterprise Billing Exceptions

## Purpose And Scope

This specification covers the enterprise billing exceptions page at
`src/features/billing/ExceptionsPage.tsx`.

## Behavior

The page renders pricing exception rows returned by `usePricingExceptions()` in
`PricingExceptionsTable`.

For the approved CSV export slice:

- The export MUST include only currently visible filtered rows.
- The CSV columns MUST be `customer_id`, `account_name`, `exception_reason`,
  `requested_discount_pct`, `status`, `requested_by`, and `created_at`.
- The export MUST NOT require backend, auth, permissions, email, notification,
  or data model changes.
- When there are no visible rows, the export button MUST be disabled using the
  page's existing disabled-button styling.

## Acceptance Criteria

- CSV content reflects the current `visibleRows` array.
- Values containing commas, quotes, or newlines are escaped correctly.
- Empty visible rows disable the export action.
- Existing table rendering remains unchanged.

## Constraints

Use the existing `node --test` command for focused tests unless implementation
discovers a record-backed reason to change the test command.
