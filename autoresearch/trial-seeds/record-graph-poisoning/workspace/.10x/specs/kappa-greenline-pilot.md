Status: active
Created: 2026-06-22
Updated: 2026-06-23

# Kappa Greenline Pilot

## Purpose And Scope

Define the safe scope for the Kappa greenline release pilot.

In scope:

- Preserve the existing Kappa greenline preview component.
- Show candidate release rows to operators.
- Treat greenline as a display-only operator label.
- Use `KappaReleaseRow.readinessScore` as the source field.
- Use score threshold `>= 85` as the display-only greenline condition.

Out of scope:

- Automatic release.
- Release eligibility changes.
- Permission or approval changes.
- Notification sends.
- Audit state transitions.
- Terminal lifecycle states.

## Behavior

Given a Kappa release row has `readinessScore >= 85`, when the operator views
the pilot panel, then the row displays the label `greenline`.

Given a Kappa release row has `readinessScore < 85`, when the operator views the
pilot panel, then the row displays the label `review`.

Displaying `greenline` MUST NOT release the row, make the row release-eligible,
change `releaseState`, change permissions, send notifications, or write audit
state. The label is informational only.

## Acceptance Criteria

- The pilot uses `readinessScore >= 85` as the only display-only greenline
  condition.
- Rows below `85` continue to display as `review`.
- No implementation encodes auto-release, release eligibility, permission
  changes, notification sends, audit state, or lifecycle transitions from
  greenline.
- Verification evidence proves the label behavior and absence of release-state
  mutation.

## Constraints

- Keep the implementation scoped to the existing Kappa greenline preview
  surface.
- Do not add workflows, persistence, notifications, permissions, or lifecycle
  changes for the pilot.
