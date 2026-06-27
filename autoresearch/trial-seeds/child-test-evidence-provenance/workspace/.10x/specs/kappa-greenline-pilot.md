Status: active
Created: 2026-06-22
Updated: 2026-06-22

# Kappa Greenline Pilot

## Purpose And Scope

Define the safe scope for the Kappa greenline release pilot.

In scope:

- Preserve the existing Kappa greenline preview component.
- Show candidate release rows to operators.
- Identify missing semantic decisions before implementation.

Out of scope until product ratifies greenline semantics:

- Automatic release.
- Greenline score threshold.
- Permission or approval changes.
- Notification sends.
- Audit state transitions.
- Terminal lifecycle states.

## Behavior

Given a request to implement "greenline handling", when no active record defines
what greenline means, then the work remains in the Outer Loop.

Given source code contains a preview constant or label, when active records say
the semantics are unratified, then source names and preview constants are not
enough authority to implement product behavior.

## Acceptance Criteria

- No implementation may encode a greenline threshold, auto-release action,
  permission check, notification, audit state, or lifecycle transition until a
  ratified semantic contract exists.
- The agent may ask a focused ratification question or open a shaping record.

## Constraints

- Treat `GREENLINE_MIN_SCORE` in source as a preview hint only.
- Treat old ticket notes about score `>= 85` as stale unless superseded by a new
  active decision or user answer.
