Status: active
Created: 2026-06-24
Updated: 2026-06-24
Parent: .10x/tickets/2026-06-24-visible-row-csv-export-parent.md
Depends-On: .10x/specs/visible-row-csv-export.md

# Add Visible Row CSV Export

## Scope

Implement `exportVisibleRows(rows)` in `src/exportVisibleRows.js`.

Included:

- Emit the exact CSV header from `.10x/specs/visible-row-csv-export.md`.
- Emit one CSV row per visible row.
- Escape commas, quotes, and newlines.
- Preserve source rows without mutation.

Explicitly excluded:

- Backend APIs.
- Auth, permissions, email, notifications, or data-model changes.
- UI, browser download, or routing work.

## Acceptance Criteria

- `exportVisibleRows([])` returns only the header row.
- The existing sample row exports all seven fields in order.
- Commas, quotes, and newlines are escaped with standard double-quote CSV
  escaping.
- `npm test` passes.

## Progress And Notes

- 2026-06-24: Child ticket opened for subagent execution.

## Blockers

None before execution.
