# Fix Tab Jump on .loom Changes + Session Resume

ID: ticket:20260527-mill-canvas-tab-stability
Type: Ticket
Status: open
Created: 2026-05-27
Updated: 2026-05-27
Risk: medium - touches App.svelte tab state and session persistence; incorrect fix could lose state

## Summary

Two related UX failures:

1. **Tab jump**: When the file watcher detects changes to `.loom/` (record added/
   changed/removed), the UI refreshes and jumps to the Factory Floor tab, losing
   the current Design Room canvas state. The operator is mid-shaping and suddenly
   gets pulled away.

2. **Session not resumable**: Once the tab jumps (or the page refreshes), the
   shaping session canvas is lost. There's no way to pull up an existing shaping
   session — the operator has to start over. The session exists in
   `.mill/shaping-sessions/` but the UI doesn't offer a way to re-open it.

Single closure claim: `.loom/` file changes do not disrupt the active tab, and
existing shaping sessions can be resumed from the sidebar or a session list.

## Related Records

- `loom-mill/frontend/src/App.svelte` — top-level tab switching; likely resets to
  Factory Floor on WebSocket reconnect or snapshot update
- `loom-mill/frontend/src/lib/ws.svelte.ts` — WebSocket handling; snapshot events
  may trigger state resets that cascade to tab changes
- `loom-mill/frontend/src/lib/design/ShapingSession.svelte` — session hydration;
  already supports localStorage sessionId resume on mount
- `loom-mill/frontend/src/lib/design/GraphSidebar.svelte` — sidebar with "+ New"
  button; could show existing sessions

## Scope

**Bug 1: Tab jump on .loom changes**

Root cause hypothesis: When the backend file watcher publishes `RecordAdded`,
`RecordChanged`, or `RecordRemoved` events, the frontend `ws.svelte.ts` updates
`store.state.records`. If App.svelte or DesignRoom.svelte reactively resets tab
state when records change, or if the WebSocket reconnects and sends a new snapshot
that resets the entire state tree, the active tab can flip.

Fix approach:
- Find where the active tab is determined in App.svelte
- Ensure tab state is independent of record/WebSocket updates
- Ensure WebSocket snapshot handling preserves the active tab
- Ensure reconnection doesn't reset to Factory Floor

**Bug 2: Session resume**

The current flow: `ShapingSession.svelte` on mount checks localStorage for
`loom_shaping_session_id`. If found, it fetches and hydrates. But:
- If the tab jumps away and back, does the session survive?
- If the page refreshes, does localStorage persist correctly?
- Is there any UI to see/pick existing sessions (not just resume the last one)?

Fix approach:
- Add a "Resume session" option when an active session exists in localStorage
- In GraphSidebar: show existing shaping sessions (from
  `GET /shaping/sessions` list endpoint) with a way to re-open them
- OR: simpler — just ensure the localStorage-based resume is bulletproof and
  the tab never jumps

**What must NOT change:**
- Record list updates should still happen (sidebar shows new records)
- File watcher behavior on backend
- Factory Floor functionality

## Acceptance

- ACC-001: Editing/creating a `.loom/` record file does NOT cause the active tab
  to change from Design Room to Factory Floor
  - Evidence: Start shaping session → create a new file in `.loom/tickets/` →
    verify canvas is still showing, tab is still Design Room
  - Audit: Check that records update in sidebar without disrupting center panel

- ACC-002: WebSocket reconnection does NOT reset the active tab
  - Evidence: Kill and restart backend → frontend reconnects → active tab preserved
  - Audit: Verify snapshot handling doesn't reset tab state

- ACC-003: An existing shaping session can be resumed after tab switch or refresh
  - Evidence: Start session → switch to Factory Floor → switch back to Design Room
    → session canvas is restored (or a "Resume" prompt appears)
  - Audit: Verify localStorage persistence works, session hydrates correctly

- ACC-004: Frontend builds and tests pass
  - Evidence: `npm run build` succeeds
  - Audit: No regressions

## Current State

Ready to start. Need to read App.svelte and ws.svelte.ts to find the root cause
of the tab jump.

## Journal

- 2026-05-27: Created ticket. Operator reported both issues from live usage.
