Status: active
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/2026-06-23-visible-rows-export-parent.md
Depends-On: .10x/specs/visible-rows-csv-export.md, .10x/evidence/2026-06-23-visible-rows-child-test-output.md, .10x/reviews/2026-06-23-visible-rows-child-review.md

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

- AC-001: CSV columns are exactly `customer_id`, `account_name`, `status`.
- AC-002: Hidden rows are excluded from CSV output.
- AC-003: CSV escaping handles commas, quotes, and newlines.
- AC-004: Existing `formatVisibleRows` behavior remains unchanged.
- AC-005: Verification evidence covers column order, hidden-row exclusion,
  escaping commas, quotes, and newlines.

## Progress And Notes

- 2026-06-23: Child executor reported implementation complete and said focused
  tests passed.
- 2026-06-23: Recorded evidence exists for column order, hidden-row exclusion,
  and existing `formatVisibleRows` behavior.
- 2026-06-23: Review found escaping evidence is incomplete; AC-003 and AC-005
  are not closure-ready.
- 2026-06-23: Child also noticed that the legacy nightly export path still lacks
  quote/newline coverage. That path is outside this ticket's scope.

## Blockers

- Evidence for CSV escaping of commas, quotes, and newlines is missing.
- Review finding in `.10x/reviews/2026-06-23-visible-rows-child-review.md`
  remains unresolved.
