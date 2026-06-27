Status: open
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/2026-06-23-visible-rows-export-parent.md
Depends-On: .10x/specs/visible-rows-csv-export.md

# Add Visible Rows CSV Export

## Scope

Implement CSV export formatting for currently visible rows.

Included:

- Add `formatVisibleRowsCsv` in `src/formatVisibleRows.ts`.
- Export only rows whose `status` is `visible`.
- Preserve existing `formatVisibleRows` behavior.
- Extend `src/formatVisibleRows.test.ts`.

Excluded:

- Backend changes.
- Auth or permission changes.
- UI changes.
- Data model changes.

## Acceptance Criteria

- CSV columns are exactly `customer_id`, `account_name`, `status`.
- Hidden rows are excluded from CSV output.
- CSV escaping handles commas, quotes, and newlines.
- Existing `formatVisibleRows` test still passes.
- New tests cover column order, hidden-row exclusion, and escaping.

## Progress And Notes

- 2026-06-23: Child ticket opened and approved for execution by a child
  executor.

## Blockers

None.
