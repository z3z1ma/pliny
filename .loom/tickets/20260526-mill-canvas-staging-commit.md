# Staging, Commit, and Session Resume

ID: ticket:20260526-mill-canvas-staging-commit
Type: Ticket
Status: review
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - session resume must preserve full canvas state (node positions, selections, dead branches); data loss on refresh would break trust

Depends On: ticket:20260526-mill-canvas-e2e-tracer
Depends On: ticket:20260526-mill-canvas-interaction

## Summary

Close the production loop: Record nodes accepted by the operator feed the staging
panel, commit materializes them to `.loom/`, and session state (including canvas
positions, dead branches, and accepted records) persists and resumes correctly on
page refresh.

Single closure claim: Record nodes flow to staging, commit produces correct files
on disk, and the full canvas session resumes with preserved visual state.

## Related Records

- `spec:mill-shaping-canvas` — REQ-004 (record nodes feed staging), REQ-009
  (staging panel), REQ-010 (session persistence and resume)
- `plan:20260526-mill-shaping-canvas` — parent plan; this is Unit 9
- `ticket:20260526-mill-canvas-interaction` — provides record node accept/reject
  actions
- `loom-mill/frontend/src/lib/design/StagingPanel.svelte` — existing staging UI;
  adapt to work with canvas state
- `loom-mill/src/loom_mill/shaping/commit.py` — existing commit flow; should work
  with new model since it operates on `staged_records`
- `loom-mill/src/loom_mill/shaping/staging.py` — existing staging CRUD

## Scope

**What changes:**

Record node → Staging integration:
- `RecordNode.svelte` accept action: calls existing `POST /sessions/{id}/staged/{temp_id}/accept`
- `RecordNode.svelte` reject action: calls existing `DELETE /sessions/{id}/staged/{temp_id}`
- `RecordNode.svelte` edit action: opens inline content editor, calls existing `PUT /sessions/{id}/staged/{temp_id}`
- When a record node is accepted: its visual state changes (green border, checkmark)
  AND it appears in the StagingPanel
- When a record node is rejected: its visual state changes (red, strikethrough)
  AND it's removed from StagingPanel

Staging panel integration:
- `StagingPanel.svelte`: adapts to read from `store.shapingSession.stagedRecords`
  (same data source, but now driven by canvas record node actions)
- Clicking a record in the staging panel: pans the canvas to the corresponding
  RecordNode and highlights it (ring animation)
- Staging panel shows surface badges, mini-graph, commit button (existing behavior)

Commit flow:
- Commit button calls existing `POST /sessions/{id}/commit`
- Existing `CommitFlow` materializes accepted staged records to `.loom/`
- After successful commit: session ends, operator returns to Design Room
- Verify: commit produces correctly formatted Markdown files in the right `.loom/`
  subdirectories

Session resume:
- Canvas state persisted to `.mill/shaping-sessions/{id}/canvas-state.json`:
  - Node positions (x, y for each node, including manual pins)
  - Dead branch collapse toggle state
  - Zoom level and pan position
  - Which nodes are expanded (for observation/record content)
- On page refresh or session re-open:
  - Frontend calls `GET /sessions/{id}` → gets full graph state (nodes, edges,
    staged records)
  - Frontend loads canvas-state.json (via new API endpoint or embedded in session
    response)
  - Canvas hydrates with saved positions, zoom, pan, collapse state
  - All visual states (dead/stale/active) restore correctly
- New backend: include `canvas_state` in session persistence and API response:
  - `GET /sessions/{id}` response adds `canvas_state: {positions: {...}, zoom: ..., pan: {...}, collapsed: bool}`
  - `PUT /sessions/{id}/canvas-state` saves frontend canvas state periodically
    (debounced, every 5s of changes)

Frontend state management:
- `ws.svelte.ts` shapingSession: ensure nodes Map + edges array is the single
  source of truth
- Periodic save: debounced `PUT` of canvas state (positions, zoom, pan) to prevent
  data loss
- localStorage fallback: save session ID so refresh reconnects to the right session

**What must NOT change:**
- CommitFlow internals (operates on staged_records, model-agnostic)
- Staging record model (temp_id, surface, title, content, status)
- Factory Floor functionality

**Stop condition:** If canvas state serialization becomes too large (>1MB for big
sessions), strip observation content from the state and re-fetch on hydration.

## Acceptance

- ACC-001: Accepting a record node in the canvas adds it to the staging panel
  - Evidence: Playwright test: canvas shows RecordNode → click Accept → staging
    panel shows the record with correct surface/title → RecordNode shows green
    accepted state
  - Audit: Verify backend staged_records list includes the accepted record

- ACC-002: Rejecting a record node removes it from staging
  - Evidence: Playwright test: accept → then reject → staging panel no longer
    shows it → RecordNode shows red rejected state
  - Audit: Verify backend staged_records reflects removal

- ACC-003: Commit produces correct files on disk
  - Evidence: Playwright + filesystem test: accept 2 records (1 ticket, 1 spec) →
    commit → verify `.loom/tickets/` and `.loom/specs/` contain new files with
    correct content
  - Audit: Verify file content matches what was in the RecordNode; verify no extra
    files created

- ACC-004: Session resumes with full canvas state on page refresh
  - Evidence: Playwright test: create session with 5+ nodes → arrange canvas
    (zoom, pan, collapse dead branches) → refresh page → canvas shows same nodes
    in same positions with same zoom/pan/collapse state
  - Audit: Verify no data loss; compare pre-refresh and post-refresh screenshots

- ACC-005: Clicking a record in staging pans canvas to that node
  - Evidence: Playwright test: zoom out → click record in staging panel → canvas
    smoothly pans to the RecordNode and highlights it
  - Audit: Verify highlight is temporary (fades after 2s)

- ACC-006: Canvas state saves periodically without blocking interaction
  - Evidence: Network tab shows debounced PUT requests (not every frame); no UI
    jank during save
  - Audit: Verify save frequency is reasonable (every 5s max); verify save failure
    doesn't crash the UI

## Current State

Frontend implementation is complete for the user-requested slice: RecordNode accept,
reject, and edit actions call the existing staging API and refetch session state;
StagingPanel clicks trigger a temporary RecordNode highlight; commit clears the
shaping session state, removes the persisted localStorage session ID, and exits
back to editor mode. Session resume remains the existing GET/hydration path per
the user-scoped instruction to skip real-time Svelvet position persistence for now.

Evidence: `evidence:20260526-mill-canvas-staging-commit-build`.

Not yet verified: browser/Playwright behavior against a running backend, actual
commit files written under `.loom/`, pan-to-node behavior beyond the temporary
highlight fallback, full refresh preservation of manual Svelvet positions, and
audit.

## Journal

- 2026-05-26: Created ticket with Status `open`. Closes the production loop:
  shape → accept → commit → records on disk. Session resume prevents data loss.
- 2026-05-26: Status set to `active` for frontend implementation of RecordNode
  staging API actions, staging-panel canvas highlighting, commit flow wiring, and
  requested frontend build verification.
- 2026-05-26: Implemented the requested frontend integration slice and recorded
  build evidence. Status moved to `review`; remaining work is browser/e2e
  verification of the running staging/commit flow and audit.
