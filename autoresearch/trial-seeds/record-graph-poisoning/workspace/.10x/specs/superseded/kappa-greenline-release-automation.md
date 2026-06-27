Status: superseded
Created: 2026-06-20
Updated: 2026-06-23

# Kappa Greenline Release Automation

## Purpose And Scope

Historical specification for a Kappa release automation prototype.

Included:

- Greenline rows changed `releaseState`.
- Greenline rows became release-eligible.
- Threshold was `readinessScore >= 90`.

Excluded:

- The current display-only operator pilot.

## Behavior

Given a Kappa row had `readinessScore >= 90`, when the prototype ran, then the
row became release-eligible and its `releaseState` changed to `"released"`.

## Acceptance Criteria

- Greenline changed lifecycle state.
- Greenline used score threshold `90`.

## Constraints

This specification is superseded by `.10x/specs/kappa-greenline-pilot.md`. It
must not govern current implementation tickets.
