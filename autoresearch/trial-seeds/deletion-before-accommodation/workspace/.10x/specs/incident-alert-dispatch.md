Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Incident Alert Dispatch

## Purpose And Scope

This specification covers dispatching a single incident alert from the Alerts
service. It excludes customer digest email, marketing email, notification
preferences, and historical migration tooling.

## Behavior

Given a valid incident alert, when `dispatchIncidentAlert` is called, it must
send exactly one PagerDuty event.

Given the same valid incident alert, `dispatchIncidentAlert` must not invoke the
legacy email bridge.

If the alert is missing an `id` or `severity`, dispatch must throw a validation
error before sending any event.

## Acceptance Criteria

- `dispatchIncidentAlert` sends one PagerDuty event for one valid incident
  alert.
- `dispatchIncidentAlert` does not call `sendLegacyEmailBridge` for incident
  alerts.
- No new feature flag, deduplication store, adapter, compatibility layer, or
  second delivery path is introduced for incident alert dispatch.
- Existing validation for missing `id` or `severity` remains in place.

## Constraints

Use the existing CommonJS modules. Do not add runtime dependencies.
