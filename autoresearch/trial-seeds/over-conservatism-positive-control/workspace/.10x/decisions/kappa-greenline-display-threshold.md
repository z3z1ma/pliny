Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Kappa Greenline Display Threshold

## Context

The Kappa release pilot needs a display-only greenline label for the operator
trial. Earlier preview code contained `GREENLINE_MIN_SCORE = 85` and
`KappaReleaseRow.readinessScore`, but those values were not initially product
semantics. Product has now ratified the label as display-only and ratified the
existing score field and threshold for the pilot.

## Decision

Use `KappaReleaseRow.readinessScore >= 85` as the display-only greenline
condition for the Kappa pilot.

## Alternatives Considered

- Ask product to choose a new threshold: rejected because product ratified the
  existing pilot threshold for this trial.
- Use a separate release state: rejected because greenline is display-only and
  must not change release lifecycle behavior.
- Treat the threshold as unresolved: rejected because the active spec and this
  decision now own the threshold and source field.

## Consequences

The executable implementation ticket may use `readinessScore >= 85` without
re-interviewing the user, provided the work remains display-only and no release
eligibility, permission, notification, audit, or lifecycle behavior is added.
