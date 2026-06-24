Status: open
Created: 2026-06-21
Updated: 2026-06-22
Parent:
Depends-On: .10x/specs/kappa-greenline-pilot.md, .10x/decisions/no-automatic-greenline-release.md

# Shape Kappa Greenline

## Scope

Shape the Kappa greenline pilot before implementation.

Included:

- Inspect existing preview code.
- Identify which greenline semantics remain unratified.

Excluded:

- Implementing auto-release.
- Encoding a greenline threshold.
- Adding tests for release eligibility.

## Acceptance Criteria

- Product ratifies whether greenline is display-only, review-ready,
  release-eligible, auto-release, or some other state before implementation.
- No executable ticket treats old threshold notes as current acceptance criteria.

## Progress And Notes

- 2026-06-21: Old whiteboard note suggested "greenline = score >= 85 and
  auto-release after operator view." This was not ratified and is now stale.
- 2026-06-22: Active spec and decision require semantic ratification first.

## Blockers

- Meaning of greenline.
- Whether greenline changes release eligibility or only display.
- Required permission, audit, and notification behavior if greenline changes
  release state.
