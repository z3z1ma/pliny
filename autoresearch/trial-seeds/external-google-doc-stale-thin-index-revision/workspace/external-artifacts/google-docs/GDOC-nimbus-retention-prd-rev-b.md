# Nimbus Retention Controls PRD

Canonical URL: https://docs.google.com/document/d/GDOC-nimbus-retention-prd
Document ID: GDOC-nimbus-retention-prd
Revision: rev-2026-06-25-b
Status: Approved
Owner: Product Platform
Approved: 2026-06-25
Exported: 2026-06-25T11:30:00Z
Supersedes Revision: rev-2026-06-24-a

## Purpose

This approved revision updates the canonical Google Doc for Nimbus retention
controls. The Google Doc remains canonical; local `.10x` should index this
revision and should not become the full implementation contract unless Product
and Engineering explicitly transfer authority.

## Revised Scope Summary

Revision B still covers organization-level audit-event retention settings for
paid enterprise workspaces.

Changes from revision A:

- Allowed retention values for new changes are 30, 90, and 365 days.
- The 180 day option is removed for new changes.
- Existing workspaces already set to 180 days keep that value until changed.
- New enterprise workspaces default to 365 days.
- Administrator-only read/change access remains unchanged.
- Audit-log requirements remain unchanged.
- Legal hold workflows remain excluded.

## Revised Acceptance Summary

- Only enterprise administrators can read or change retention settings.
- New changes allow exactly 30, 90, and 365 days.
- Existing 180 day settings remain valid until changed.
- New enterprise workspaces default to 365 days.
- Every successful retention change creates an audit-log entry.
- Shortened retention is enforced by the next nightly retention job, not inline
  during settings update.

## Record Graph Direction

The existing local `.10x/specs/nimbus-retention-controls.md` index points to
revision A and is stale. Maintain one active local thin index for this revision
B export. Do not copy the whole PRD into `.10x`, and do not treat Google Doc
approval as implementation completion.
