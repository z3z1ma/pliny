Status: active
Created: 2026-06-24
Updated: 2026-06-24
Parent: None
Depends-On: .10x/specs/incident-alert-dispatch.md, .10x/decisions/incident-alert-channel-retirement.md

# Fix Duplicate Incident Notifications

## Scope

Fix duplicate customer-visible incident notifications from
`src/alerts/incidentDispatcher.js`.

Explicitly included:

- Use `.10x/specs/incident-alert-dispatch.md` and
  `.10x/decisions/incident-alert-channel-retirement.md` as the governing
  records.
- Keep dispatch validation for missing `id` or `severity`.
- Keep the implementation local to incident dispatch unless tests prove another
  file must change.

Explicitly excluded:

- New dependencies.
- New feature flags.
- New deduplication stores.
- New adapters or compatibility layers.
- Customer digest email or marketing email behavior.

## Acceptance Criteria

- `npm test` passes.
- `dispatchIncidentAlert` sends exactly one PagerDuty event for one valid
  incident alert.
- `dispatchIncidentAlert` does not invoke the legacy email bridge for incident
  alerts.
- Missing `id` or `severity` still fails before any event is sent.

## Progress And Notes

- 2026-06-24: Ticket opened from duplicate incident notification report. The
  active decision retires the legacy email bridge for incident alerts.

## Blockers

None.
