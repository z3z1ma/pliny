# Workstation Lifecycle UX: Dismiss, States, Context Actions

ID: ticket:20260525-mill-workstation-lifecycle-ux
Type: Ticket
Status: review
Created: 2026-05-25
Updated: 2026-05-25
Risk: low - frontend-only behavioral improvements with minor backend endpoint addition.
Priority: medium - depends on layout overhaul being done first.
Depends On: ticket:20260525-mill-layout-overhaul

## Summary

Fix workstation lifecycle UX issues: (1) completed workstations pile up with no way to dismiss them, (2) inappropriate controls shown for current state (Start button on completed workstation), (3) "ticket not found" errors shown in-card, (4) no clear visual distinction between active/completed/errored states.

Closure claim: Workstation lifecycle states are visually distinct, completed workstations can be dismissed, and controls match the current state.

## Related Records

- `spec:mill-factory-floor` REQ-011, REQ-016 - workstation panels and operator controls
- `ticket:20260525-mill-layout-overhaul` - provides the new WorkstationRow component to build on
- `loom-mill/src/loom_mill/workstation/manager.py:87-97` - existing stop(remove=True) method

## Scope

Write:
- `loom-mill/frontend/src/lib/WorkstationRow.svelte` - state-aware actions, dismiss button
- `loom-mill/frontend/src/lib/WorkstationList.svelte` - "Clear all completed" action
- `loom-mill/frontend/src/lib/DetailPanel.svelte` - show state-appropriate content

Backend (minor):
- `loom-mill/src/loom_mill/api/workstation.py` - add `DELETE /workstations/{id}` if not already working for completed workstations (verify the existing endpoint works for dismiss without stopping first)

Non-goals:
- Do NOT implement keyboard shortcuts (separate ticket)
- Do NOT implement drag-to-reorder
- Do NOT implement auto-dismiss timer (manual only for now)

## Detailed Design

### State-Appropriate Actions per WorkstationRow

| State | Visible actions (on hover) | Row appearance |
|-------|---------------------------|----------------|
| running | Pause, Stop | Normal weight, green dot, live timer |
| paused | Resume, Stop | Normal weight, yellow dot, static timer |
| stopped | Resume, Dismiss | Dimmed, red dot |
| completed | View Summary, Dismiss | In "Completed" section, dimmed, gray dot |
| conflict | Resolve, Abort | Red dot, red left border (andon-like) |

### "Dismiss" Behavior

Dismiss calls `DELETE /workstations/{id}` which:
1. Removes the workstation from the manager's tracking
2. Cleans up the worktree (if still exists)
3. Removes from frontend state

The workstation disappears from the list. Its iteration history remains in `.mill/` for later review if needed.

### "Clear All Completed" Button

In the WorkstationList header, when completed workstations exist, show a small "Clear" link:

```svelte
<div class="flex items-center justify-between px-3 py-1.5 border-t border-border-subtle">
  <span class="text-[10px] text-text-tertiary">Completed ({completedCount})</span>
  <button class="text-[10px] text-text-tertiary hover:text-text-secondary underline">Clear all</button>
</div>
```

Clicking "Clear all" dismisses all completed workstations in one batch.

### Error States

When a workstation has `ticket not found` or similar errors:
- Show the error inline in the row as a subtle red text below the title
- Do NOT show Start/Pause/Stop buttons for errored workstations - only "Dismiss"
- The error should be truncated to one line with hover tooltip for full message

### Visual Distinction

Active workstations:
- Full opacity
- Green/yellow/red dot based on state
- Live timer counting up (update every second for running)

Completed workstations:
- 50% opacity or slightly dimmed text
- Gray dot
- Show total duration (static, not counting)
- In a separate collapsible section

Conflict/Andon workstations:
- Red left border (2px accent)
- Red dot pulsing (CSS animation)
- Reasoning text shown below title in muted red

## Acceptance

- ACC-001: Completed workstations show a "Dismiss" action (×) on hover that removes them from the list.
  - Evidence: Playwright test: create workstation, let it complete, hover to reveal dismiss, click, verify it disappears.
  - Audit: verify worktree cleanup happens on dismiss.

- ACC-002: "Clear all completed" button removes all completed workstations at once.
  - Evidence: Playwright test with 2 completed workstations, click clear, verify both gone.
  - Audit: verify batch operation.

- ACC-003: Controls shown match workstation state (no Start button on completed workstations).
  - Evidence: Playwright screenshot showing running workstation with Pause/Stop, completed with only Dismiss.
  - Audit: verify each state shows only appropriate actions.

- ACC-004: Duration in workstation rows is a live counter for running workstations, static for completed.
  - Evidence: Playwright test verifying running workstation duration increases over 3 seconds.
  - Audit: verify timer implementation.

- ACC-005: `npm --prefix loom-mill/frontend run build` passes.
  - Evidence: build output.

## Current State

Dependency `ticket:20260525-mill-layout-overhaul` is closed. Frontend lifecycle implementation has progressed in the current master-detail files: row actions are state-gated, missing-ticket rows are dismiss-only, completed/finished workstations are grouped with dismiss support, stopped workstations remain outside bulk clear and keep Resume/Dismiss controls, clear-all completed calls DELETE per completed/finished workstation, and the detail panel shows state-specific context. Existing backend `DELETE /workstations/{id}` is present and routes through `WorkstationManager.stop(remove=True)` for cleanup/removal; no backend edit was made. Audit `audit:20260525-mill-workstation-lifecycle-ux-audit` found blockers around bulk-clearing stopped workstations and unregistered row-action endpoints; both have been fixed in the frontend. Evidence `evidence:20260525-mill-workstation-lifecycle-ux-build` records a passing frontend build and scoped whitespace check after those fixes. Playwright/manual browser verification for ACC-001 through ACC-004 is still missing, so the ticket remains in review.

## Journal

- 2026-05-25: Created ticket. Source: operator feedback that completed workstations pile up and controls don't match state.
- 2026-05-25: Dependency `ticket:20260525-mill-layout-overhaul` is closed; unblocked lifecycle UX implementation.
- 2026-05-25: Ralph implementation run updated scoped frontend lifecycle UX files and verified `npm --prefix loom-mill/frontend run build` passes. Moved to review because Playwright/manual behavior evidence and audit are still pending.
- 2026-05-25: Recorded `audit:20260525-mill-workstation-lifecycle-ux-audit`; fixed FIND-001 by excluding stopped workstations from the completed bulk-clear group and fixed FIND-002 by routing Stop to the legacy stop endpoint and Resolve/Abort to shipping endpoints. Recorded `evidence:20260525-mill-workstation-lifecycle-ux-build` after `npm --prefix loom-mill/frontend run build` and scoped `git diff --check` passed.
- 2026-05-25: Recorded `audit:20260525-mill-workstation-lifecycle-ux-followup-audit`; original code blockers appear resolved, but restored `Status: review` because ACC-001 through ACC-004 still need behavioral evidence before closure.
