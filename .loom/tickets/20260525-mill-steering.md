# Mill Steering Flow

ID: ticket:20260525-mill-steering
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: low - builds on existing pause/resume mechanics; main complexity is ensuring fresh state on resume.
Depends On: ticket:20260525-mill-operator-controls

## Summary

After pause, the operator can inspect and edit the relevant Loom record (open in configured editor or minimal inline view), then resume. Resume launches a fresh harness subprocess from the updated graph state rather than relying on stale in-memory or conversation state. This completes the pause→steer→resume cycle that makes the factory line correctable.

## Related Records

- `plan:20260525-factory-floor-mvp` - parent plan, Unit 7.
- `spec:loom-mill-factory-floor-mvp` REQ-007, SCN-003 - steering behavior contract.

## Scope

Read scope:
- Workstation engine pause/resume from Unit 5.
- File watcher from Unit 3 (detects record edits during pause).
- Operator controls from Unit 6.

Write scope:
- `loom-mill/frontend/src/` steering UI (open-in-editor button, optional inline record view, resume button).
- `loom-mill/src/loom_mill/workstation/` resume logic (fresh subprocess from current worktree state).
- Integration between watcher and steering (detect that records changed during pause).

Non-goals:
- No full Design Office inline editor. A button that opens `$EDITOR` or system default is sufficient for MVP.
- No automatic conflict resolution if the record changed while the worker was running.

Stop conditions:
- Stop if opening an external editor from a web UI requires platform-specific handling that exceeds this ticket scope (route to Tauri-specific ticket later).

## Acceptance

- ACC-001: While paused, the operator can open the relevant ticket record in an editor (system default or configured).
  Evidence: manual evidence showing "Edit" button opens the record file in an editor.

- ACC-002: If the operator edits a `.loom/` record during pause, the watcher detects the change and the state model updates.
  Evidence: integration test showing record edit → state model event → UI reflects new status or content change indicator.

- ACC-003: Resume after edit launches a fresh subprocess that reads the updated record and worktree state.
  Evidence: integration test where a constraint is added to a ticket during pause; the resumed subprocess's working directory contains the updated file.

## Current State

Not started. Blocked on operator controls (Unit 6).

## Journal

- 2026-05-25: Created from `plan:20260525-factory-floor-mvp` Unit 7.
