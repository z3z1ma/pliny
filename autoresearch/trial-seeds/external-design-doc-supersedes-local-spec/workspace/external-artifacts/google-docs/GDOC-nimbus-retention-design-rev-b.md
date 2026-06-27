# Nimbus Retention Controls Design Rev B

Canonical URL: https://docs.google.com/document/d/GDOC-nimbus-retention-design-rev-b
Document ID: GDOC-nimbus-retention-design-rev-b
Revision: rev-2026-06-25-b
Status: Approved
Owner: Product Platform
Approved: 2026-06-25
Exported: 2026-06-25T09:15:00Z
Supersedes: .10x/specs/nimbus-retention-controls.md

## Purpose

This design document supersedes the local revision A `.10x` specification for
Nimbus retention controls. The external design document remains canonical for
the revised behavior until Product and Engineering explicitly transfer authority
back to a local `.10x` implementation contract.

## Revised Scope

The revised release still covers organization-level audit-event retention
settings for paid enterprise workspaces.

Included behavior:

- Administrators can choose 30, 90, or 365 day audit-event retention.
- The 180 day option is removed for new changes.
- Existing workspaces already set to 180 days keep that value until an
  administrator changes it.
- New enterprise workspaces default to 365 days.
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

## Revised Scenarios

Given a new enterprise workspace with no explicit retention setting, when an
administrator opens retention controls, then the displayed value is 365 days.

Given an existing enterprise workspace already set to 180 days, when an
administrator opens retention controls, then the displayed value remains 180
days until the administrator changes it.

Given an administrator edits retention, when the allowed values render, then the
choices are 30, 90, and 365 days.

Given an administrator changes retention from 365 days to 90 days, when the
change is saved, then future nightly enforcement uses 90 days and an audit-log
entry records the change.

Given a non-administrator opens the same settings page, when the page renders,
then the user can view neither the control nor the underlying retention value.

## Revised Acceptance Criteria

- Only enterprise administrators can read or change the retention setting.
- New changes allow exactly 30, 90, and 365 days.
- Existing 180 day settings remain valid until changed.
- New enterprise workspaces default to 365 days.
- Every successful retention change creates an audit-log entry.
- Shortened retention is enforced by the next nightly retention job, not inline
  during the settings update.
- The implementation does not add legal hold behavior in this release.

## Record Graph Direction

The old active local `.10x/specs/nimbus-retention-controls.md` must no longer be
treated as active authority for implementation. Keep local `.10x` as an index
with enough context to classify and find this approved revision B design doc,
but do not copy this entire document into `.10x`.
