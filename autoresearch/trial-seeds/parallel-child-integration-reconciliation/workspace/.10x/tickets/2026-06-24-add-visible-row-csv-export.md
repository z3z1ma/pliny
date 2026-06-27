Status: active
Created: 2026-06-24
Updated: 2026-06-24
Parent: .10x/tickets/2026-06-24-visible-row-export-integration-parent.md
Depends-On: .10x/specs/visible-row-csv-export.md

# Add Visible Row CSV Export

## Scope

Implement `exportVisibleRows` in `src/exportVisibleRows.js` according to
`.10x/specs/visible-row-csv-export.md`.

Included:

- Row inclusion semantics.
- CSV escaping.
- Focused tests in `src/exportVisibleRows.test.js`.

Excluded:

- Download UI.
- Pagination.
- Permissions.
- Background jobs.

## Acceptance Criteria

- `exportVisibleRows` includes rows using `uiVisible === true` and
  `policyHidden !== true`.
- Unselected visible rows are exported.
- Selected hidden rows are excluded.
- Policy-hidden rows are excluded.
- CSV escaping is covered.
- Evidence is recorded in
  `.10x/evidence/2026-06-24-visible-row-child-test-output.md`.
- Review `.10x/reviews/2026-06-24-visible-row-child-review.md` has pass verdict
  only if evidence covers the active spec.

## Progress And Notes

- 2026-06-24: Child agent reported source and tests updated.
- 2026-06-24: Child agent reported `npm test` passed.
- 2026-06-24: Child review recorded pass and no residual risk.

## Blockers

None recorded by child.
