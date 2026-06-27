Status: active
Created: 2026-06-24
Updated: 2026-06-24
Parent: .10x/tickets/2026-06-24-visible-row-export-integration-parent.md
Depends-On: .10x/specs/visible-row-csv-export.md

# Add Visible Row Export Button State

## Scope

Implement `isExportEnabled` in `src/exportToolbarState.js` according to
`.10x/specs/visible-row-csv-export.md`.

Included:

- Export-button enabled state.
- Focused tests in `src/exportToolbarState.test.js`.

Excluded:

- CSV serialization.
- Pagination.
- Permissions.
- Background jobs.

## Acceptance Criteria

- The export button is enabled when at least one row is visible according to
  `uiVisible === true` and `policyHidden !== true`.
- The export button is disabled when no rows are visible.
- Selected hidden rows do not enable export.
- Unselected visible rows enable export.
- Evidence is recorded in
  `.10x/evidence/2026-06-24-visible-row-export-button-child-test-output.md`.
- Review `.10x/reviews/2026-06-24-visible-row-export-button-child-review.md`
  has pass verdict only if evidence covers the active spec.

## Progress And Notes

- 2026-06-24: Child agent reported source and tests updated.
- 2026-06-24: Child agent reported `npm test` passed.
- 2026-06-24: Child review recorded pass and no residual risk.

## Blockers

None recorded by child.
