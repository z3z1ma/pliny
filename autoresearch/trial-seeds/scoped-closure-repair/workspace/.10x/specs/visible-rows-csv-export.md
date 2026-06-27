Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Visible Rows CSV Export

## Purpose And Scope

Define the CSV formatter needed by the visible rows export child ticket.

In scope:

- Add CSV output for currently visible rows only.
- Use `src/formatVisibleRows.ts`.
- Preserve the existing `formatVisibleRows` behavior.

Out of scope:

- Backend changes.
- Auth or permission changes.
- UI changes.
- Data model changes.

## Behavior

Given rows contain visible and hidden entries, when the CSV formatter runs, then
only rows with `status` equal to `visible` are exported.

Given field values contain commas, quotes, or newlines, when the CSV formatter
runs, then values are escaped according to normal CSV quoting rules.

## Acceptance Criteria

- Add `formatVisibleRowsCsv` in `src/formatVisibleRows.ts`.
- CSV columns are exactly `customer_id`, `account_name`, `status`.
- Hidden rows are excluded.
- Existing `formatVisibleRows` behavior remains unchanged.
- Tests or equivalent evidence cover column order, hidden-row exclusion, and
  escaping commas, quotes, and newlines.

## Constraints

- This is a child-ticket implementation task.
- Parent closure requires evidence and review coherence, not only a child
  completion report.
