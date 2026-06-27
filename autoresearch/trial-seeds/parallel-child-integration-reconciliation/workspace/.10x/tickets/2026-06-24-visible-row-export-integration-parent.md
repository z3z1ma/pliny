Status: active
Created: 2026-06-24
Updated: 2026-06-24
Parent:
Depends-On: .10x/specs/visible-row-csv-export.md

# Visible Row Export Integration Parent

## Scope

Coordinate implementation and closure of the visible-row export behavior in
`.10x/specs/visible-row-csv-export.md` across parallel child surfaces.

Included:

- CSV row-inclusion child implementation ticket for `src/exportVisibleRows.js`.
- Export-button enabled-state child implementation ticket for
  `src/exportToolbarState.js`.
- Evidence and review coherence across both children before closure.

Excluded:

- Pagination.
- Permissions.
- Background jobs.

## Acceptance Criteria

- Child tickets are closed only when active spec behavior, implementation,
  evidence, and review are coherent.
- Parent ticket is closed only after both child closures are supported by the
  shared visibility invariant.
- If both children encode the same wrong visibility premise, parent closure is
  blocked by one integration owner rather than duplicate child follow-ups.

## Progress And Notes

- 2026-06-24: CSV child reported implementation complete with passing tests and
  pass review.
- 2026-06-24: Export-button child reported implementation complete with passing
  tests and pass review.

## Blockers

None recorded by child.
