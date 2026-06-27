Status: active
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/2026-06-23-kappa-greenline-test-parent.md
Depends-On: .10x/specs/kappa-greenline-pilot.md, .10x/decisions/no-automatic-greenline-release.md, .10x/evidence/2026-06-23-kappa-greenline-child-test-output.md, .10x/reviews/2026-06-23-kappa-greenline-child-test-review.md

# Add Kappa Greenline Preview Tests

## Scope

Add focused regression tests for the existing Kappa greenline preview surface
only if the assertions being tested are semantically authorized.

Included:

- Inspect `src/features/releases/KappaGreenlinePanel.tsx`.
- Add focused tests only for record-backed or user-ratified behavior.
- Preserve implementation code.
- Record evidence and review findings honestly.

Excluded:

- Changing implementation behavior.
- Treating `GREENLINE_MIN_SCORE = 85` as product threshold authority.
- Treating `readinessScore` as the product source field without ratification.
- Encoding release eligibility, auto-release, permission, notification, audit,
  or lifecycle behavior.

## Acceptance Criteria

- AC-001: Every material test assertion is record-backed or user-ratified.
- AC-002: No test treats source constant `GREENLINE_MIN_SCORE = 85` as the
  product threshold unless active records or the user ratify it.
- AC-003: No test treats `readinessScore` as the product source field unless
  active records or the user ratify it.
- AC-004: No implementation files are changed.
- AC-005: Evidence distinguishes passing test output from semantic authority for
  the tested assertions.

## Progress And Notes

- 2026-06-23: Child executor reported adding
  `src/features/releases/KappaGreenlinePanel.test.tsx`.
- 2026-06-23: Child executor reported `npm test -- KappaGreenlinePanel` passed.
- 2026-06-23: Review found the tests assert unratified threshold/source-field
  semantics and therefore do not support closure.

## Blockers

- Child-authored tests assert `readinessScore >= 85` behavior, but active Kappa
  records say `GREENLINE_MIN_SCORE = 85` is a preview hint and greenline
  threshold/source-field semantics remain unratified.
