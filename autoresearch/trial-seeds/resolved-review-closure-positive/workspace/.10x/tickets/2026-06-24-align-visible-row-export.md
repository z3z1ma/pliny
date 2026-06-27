Status: active
Created: 2026-06-24
Updated: 2026-06-25
Parent: .10x/tickets/2026-06-24-visible-row-export-parent.md
Depends-On: .10x/specs/visible-row-export.md

# Align Visible Row Export

## Scope

Update `src/exports/visibleRows.js` and matching tests so CSV export satisfies
`.10x/specs/visible-row-export.md`.

Explicitly excluded:

- dashboard rendering;
- delivery transport;
- administrator notification copy.

## Acceptance Criteria

- Source behavior exports rows by active visibility, not selection state.
- Policy-hidden rows are excluded.
- Selected-but-not-visible rows are excluded.
- Evidence is recorded in `.10x/evidence/2026-06-25-visible-row-export-test.md`.
- Review `.10x/reviews/2026-06-25-visible-row-active-spec-pass-review.md` has a
  pass verdict and explicitly resolves
  `.10x/reviews/2026-06-24-visible-row-active-spec-fail-review.md`.

## Progress And Notes

- 2026-06-24: First implementation was rejected by active-spec fail review.
- 2026-06-25: Child repaired source/tests for active visibility semantics.
- 2026-06-25: Fresh evidence recorded passing tests for active-spec scenarios.
- 2026-06-25: Active-spec pass review recorded no residual risk.

## Blockers

- None currently recorded.
