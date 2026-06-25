Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Nimbus Retention Controls

## External Provenance

- Canonical source at creation: Google Docs PRD
- Canonical URL: https://docs.google.com/document/d/GDOC-nimbus-retention-prd
- Document ID: GDOC-nimbus-retention-prd
- Revision: rev-2026-06-24-a
- Status: Approved
- Local export path: `external-artifacts/google-docs/GDOC-nimbus-retention-prd.md`

Product and Engineering ratified this local `.10x` specification as the
canonical implementation contract for revision A.

## Purpose and Scope

Nimbus accounts need configurable organization-level audit-event retention for
paid enterprise workspaces.

Included:

- Enterprise administrators can choose 30, 90, 180, or 365 day audit-event
  retention.
- New enterprise workspaces default to 180 days.
- Shortened retention applies on the next nightly retention enforcement job.
- Increasing retention preserves existing events that have not already expired.
- Only enterprise administrators can view or change the setting.
- The audit log records the actor, previous value, new value, and timestamp.

Excluded:

- Legal hold workflows.
- Per-user retention settings.
- Data export retention.
- Billing plan changes.
- Retention controls for non-enterprise workspaces.

## Behavior

Given an enterprise workspace with no explicit retention setting, when an
administrator opens retention controls, then the displayed value is 180 days.

Given an administrator changes retention from 180 days to 90 days, when the
change is saved, then future nightly enforcement uses 90 days and an audit-log
entry records the change.

Given a non-administrator opens the same settings page, when the page renders,
then the user can view neither the control nor the underlying retention value.

## Acceptance Criteria

- Only enterprise administrators can read or change retention settings.
- Allowed retention values are exactly 30, 90, 180, and 365 days.
- New enterprise workspaces default to 180 days.
- Every successful retention change creates an audit-log entry.
- Shortened retention is enforced by the next nightly retention job, not inline
  during settings update.
- The implementation does not add legal hold behavior in revision A.

## Constraints

Ship behind the existing enterprise settings feature flag.
