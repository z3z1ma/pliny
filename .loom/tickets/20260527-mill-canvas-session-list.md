# Shaping Session List and Resume

ID: ticket:20260527-mill-canvas-session-list
Type: Ticket
Status: review
Created: 2026-05-27
Updated: 2026-05-27
Risk: low - additive UI feature; backend list endpoint likely already exists
Priority: high - first class concern per operator; without this, sessions are effectively disposable

## Summary

The shaping canvas has no way to browse or resume prior sessions. If the operator
leaves mid-shaping, refreshes the page, or starts a new session, the old session's
decision tree is effectively lost to the UI (even though it still exists on disk
under `.mill/shaping-sessions/`). Sessions are first-class artifacts — the
operator should be able to list them, see their seed input / node count / timestamp,
click one to resume or simply review the decision tree they already built.

Single closure claim: The operator can see a list of all shaping sessions (with
seed text, date, node count), click one to open it on the canvas for resume or
review, and start new sessions without losing access to prior ones.

## Related Records

- `spec:mill-shaping-canvas` — governs canvas UX
- `loom-mill/src/loom_mill/api/shaping.py` — has `list_shaping_sessions()` endpoint
  (GET /shaping/sessions) that returns session metadata
- `loom-mill/src/loom_mill/shaping/session.py` — `ShapingSession.list_sessions()`
  returns basic session info
- `loom-mill/frontend/src/lib/design/DesignRoom.svelte` — container; shaping mode
  currently entered via "+ New" only
- `loom-mill/frontend/src/lib/design/ShapingSession.svelte` — manages session
  lifecycle, hydration
- `loom-mill/frontend/src/lib/design/GraphSidebar.svelte` — left sidebar with
  records tree and "+ New" button

## Scope

**What changes:**

Backend:
- Verify `GET /shaping/sessions` returns useful metadata (session_id, created_at,
  seed text/first input node content, node count, status). If it only returns IDs,
  enrich it to include: `{id, created_at, seed_text, node_count, has_staged}`.
- Add `ended_at` or status field to distinguish active vs committed/abandoned
  sessions.

Frontend — Session list UI:
- New `loom-mill/frontend/src/lib/design/canvas/SessionList.svelte`:
  - Fetches `GET /shaping/sessions` on mount
  - Renders a list of sessions, each showing:
    - Seed text (first operator input, truncated to ~60 chars)
    - Date/time (relative: "2 hours ago", "yesterday")
    - Node count badge
    - Status indicator (active / committed / abandoned)
  - Click a session → opens it on the canvas (sets sessionId, hydrates)
  - "New session" button at top

- Integration into Design Room flow:
  - When operator clicks "+ New" in sidebar AND there are existing sessions:
    show the SessionList first (not immediately create a new session)
  - SessionList has a prominent "Start new session" button/card at the top
  - Selecting an existing session enters shaping mode with that session
  - Starting new session enters shaping mode with no sessionId (current behavior)

- When entering shaping mode with no active session (centerMode === 'shaping' but
  no sessionId): show SessionList instead of the seed input. The seed input is
  only shown when "Start new session" is clicked from SessionList.

**What must NOT change:**
- Shaping canvas rendering (once a session is loaded)
- Backend session persistence format
- Commit/staging flow

**Stop condition:** If the backend `list_sessions` is missing critical metadata
(no seed text, no node count), add it. If the endpoint doesn't exist at all,
create it.

## Acceptance

- ACC-001: A list of existing shaping sessions is shown when entering shaping mode
  - Evidence: Playwright: click "+ New" → SessionList renders showing 1+ prior
    sessions with seed text, date, node count
  - Audit: Verify list fetches from backend, not just localStorage

- ACC-002: Clicking a session in the list opens it on the canvas with full state
  - Evidence: Playwright: click a session → canvas renders with that session's
    nodes and edges, session ID matches
  - Audit: Verify hydration fetches from backend, nodes render correctly

- ACC-003: "Start new session" creates a fresh session (existing behavior)
  - Evidence: Playwright: click "Start new session" → seed input appears → type
    text → Begin → new session created
  - Audit: Verify new session has different ID from existing ones

- ACC-004: Session list shows meaningful metadata (seed, date, node count, status)
  - Evidence: Playwright screenshot showing list with human-readable entries
  - Audit: Verify data matches actual session state on disk

- ACC-005: Frontend builds clean
  - Evidence: `npm run build` succeeds
  - Audit: No regressions

## Current State

Implementation complete and ready for review. Backend list endpoint now returns all
sessions with seed text, node count, status, and created timestamp; frontend list,
new-session, resume, and canvas back-to-sessions flows are wired. Build and backend
test suite passed; Playwright acceptance screenshots/manual browser checks were not
run in this slice per operator instruction not to start dev servers.

## Journal

- 2026-05-27: Created ticket. Operator emphasized this is a first-class concern —
  sessions are decision trees worth revisiting, not disposable chat threads.
- 2026-05-27: Started implementation. Verified `GET /shaping/sessions` and
  `ShapingSession.list_sessions()` before editing; backend needs seed text/status
  and must include ended sessions for all-session browsing.
- 2026-05-27: Implemented backend metadata and frontend session list flow. Evidence:
  `npm run build 2>&1 | grep "✓ built"` in `loom-mill/frontend` returned
  `✓ built in 2.63s`; `uv run pytest tests/ -q 2>&1 | tail -3` in `loom-mill`
  returned `126 passed in 43.88s`. Remaining verification gap: Playwright/browser
  UX acceptance and audit were not run.
