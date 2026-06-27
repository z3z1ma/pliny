Status: open
Created: 2026-06-23
Updated: 2026-06-23
Parent:
Depends-On:

# Add CSV Export Quote And Newline Coverage

## Scope

Add test coverage for CSV export fields that contain quotes and embedded
newlines.

Included:

- Visible rows CSV export.
- Quoted field values.
- Embedded newline field values.

Excluded:

- Archive export behavior.
- Source code changes until coverage expectations are confirmed.
- UI rendering.

## Acceptance Criteria

- AC-001: A test case covers quote escaping in visible rows CSV export.
- AC-002: A test case covers embedded newline escaping in visible rows CSV
  export.
- AC-003: The test expectations follow the existing CSV export contract.

## Progress And Notes

- 2026-06-23: Opened from prior closure review. The legacy quote/newline gap
  needs a durable owner before implementation.

## Blockers

- None for tracking. Implementation has not started.
