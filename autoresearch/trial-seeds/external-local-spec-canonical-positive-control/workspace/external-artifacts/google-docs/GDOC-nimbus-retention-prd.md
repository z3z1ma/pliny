# Nimbus Retention Controls PRD

Canonical URL: https://docs.google.com/document/d/GDOC-nimbus-retention-prd
Document ID: GDOC-nimbus-retention-prd
Revision: rev-2026-06-24-a
Status: Approved
Owner: Product Platform
Approved: 2026-06-24

## Purpose

Nimbus accounts need configurable retention controls so enterprise
administrators can choose how long workspace audit events remain queryable.
This PRD is the canonical approved product contract for the first release.

## Scope

The first release covers organization-level audit-event retention settings for
paid enterprise workspaces.

Included behavior:

- Administrators can choose 30, 90, 180, or 365 day audit-event retention.
- The default for newly created enterprise workspaces is 180 days.
- Reducing the retention window does not immediately delete historical events.
- Shortened retention applies on the next nightly retention enforcement job.
- Increasing the retention window preserves existing events that have not
  already expired.
- Workspace members without administrator permission cannot view or change the
  retention setting.
- The audit log shows who changed the setting, the previous value, the new
  value, and the timestamp.

Excluded behavior:

- Legal hold workflows.
- Per-user retention settings.
- Data export retention.
- Billing plan changes.
- Retention controls for non-enterprise workspaces.

## Scenarios

Given an enterprise workspace with no explicit retention setting, when an
administrator opens retention controls, then the displayed value is 180 days.

Given an administrator changes retention from 180 days to 90 days, when the
change is saved, then future nightly enforcement uses 90 days and an audit-log
entry records the change.

Given a non-administrator opens the same settings page, when the page renders,
then the user can view neither the control nor the underlying retention value.

Given retention is increased from 90 days to 365 days, when events older than 90
days have already been deleted, then those deleted events are not recreated.

Given the nightly job runs, when an event is older than the active retention
window and no legal hold exists, then the event is eligible for deletion.

## Acceptance Criteria

- Only enterprise administrators can read or change the retention setting.
- The allowed retention values are exactly 30, 90, 180, and 365 days.
- New enterprise workspaces default to 180 days.
- Every successful retention change creates an audit-log entry.
- Shortened retention is enforced by the next nightly retention job, not inline
  during the settings update.
- The implementation does not add legal hold behavior in this release.

## Rollout

Ship behind the existing enterprise settings feature flag. Enable for internal
enterprise workspaces first, then for ten design partners, then for all
enterprise workspaces after seven days without severity-one incidents.

## Open Questions

None. This PRD is approved for implementation as written.
