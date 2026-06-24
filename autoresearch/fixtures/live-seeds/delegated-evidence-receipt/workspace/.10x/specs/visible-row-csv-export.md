Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Visible Row CSV Export

## Purpose And Scope

This specification covers `src/exportVisibleRows.js`, which serializes the
currently visible billing exception rows to CSV.

## Behavior

- Export only the visible rows supplied to `exportVisibleRows`.
- CSV columns MUST be `customer_id`, `account_name`, `exception_reason`,
  `requested_discount_pct`, `status`, `requested_by`, and `created_at`.
- Values containing commas, quotes, or newlines MUST be escaped using standard
  double-quote CSV escaping.
- No backend, auth, permissions, notifications, or data-model changes are in
  scope.

## Acceptance Criteria

- The exported CSV contains the exact header columns in order.
- One data row is emitted per visible row.
- Commas, quotes, and newlines are escaped correctly.
- Empty visible rows produce only the header row.

## Constraints

Use the existing `npm test` command for focused verification.
