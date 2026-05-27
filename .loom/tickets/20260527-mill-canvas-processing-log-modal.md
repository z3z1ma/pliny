# Processing Node Log View Modal

ID: ticket:20260527-mill-canvas-processing-log-modal
Type: Ticket
Status: closed
Created: 2026-05-27
Updated: 2026-05-27
Risk: low - UI-only change; backend already streams harness output via WebSocket

## Summary

Add a log view modal to the ProcessingNode on the shaping canvas. When the operator
clicks the ProcessingNode (or a "View logs" button on it), a modal opens showing
the live harness subprocess output — same pattern as workstation log views on the
Factory Floor. This gives complete transparency into what the harness is doing,
whether it's actually running, and what output it's producing.

Single closure claim: Clicking a ProcessingNode opens a modal showing live-streaming
harness output for the active exploration, using the same visual pattern as
workstation logs.

## Related Records

- `spec:mill-shaping-canvas` — governs canvas UX
- `loom-mill/frontend/src/lib/design/canvas/ProcessingNode.svelte` — current
  processing node showing elapsed time and cancel button
- `loom-mill/src/loom_mill/shaping/orchestrator.py` — manages harness invocations,
  streams output via `exploration_stream` events
- `loom-mill/src/loom_mill/shaping/events.py` — ShapingEvent types including
  `exploration_stream`
- `loom-mill/frontend/src/lib/ws.svelte.ts` — WebSocket store; needs to capture
  streaming output for display
- Factory Floor log rendering pattern — reference for visual design

## Scope

**What changes:**

Frontend:
- New `loom-mill/frontend/src/lib/design/canvas/ProcessingLogModal.svelte`:
  - Renders as a fixed/absolute overlay (modal) over the canvas
  - Dark terminal-style background (monospace font, dark bg)
  - Shows log lines streaming in real-time (auto-scroll to bottom)
  - Close button (X) in top-right corner
  - Shows: harness command, elapsed time, line count
  - Lines accumulate from WebSocket `exploration_stream` events
  - If harness finishes: shows exit code, final state
  - If no output yet: shows "Waiting for output..."

- Modify `ProcessingNode.svelte`:
  - Add clickable "View logs" link or make the entire node clickable
  - On click: open the log modal
  - Pass the exploration/invocation ID so the modal can filter events

- Modify `ws.svelte.ts`:
  - Handle `shaping:exploration_stream` events: accumulate log lines per
    exploration/invocation ID
  - Store shape: `explorationLogs: Record<string, string[]>` on the shaping session
  - Handle `shaping:exploration_complete` → mark log as finished

- Modify `ShapingCanvas.svelte`:
  - Manage modal open/close state
  - Pass log data to ProcessingLogModal when open

Backend:
- Verify `orchestrator.py` actually publishes `exploration_stream` events with
  line-level output. If it only publishes `exploration_start`/`exploration_complete`,
  add streaming: read harness stdout/stderr line-by-line and publish each line as
  a `ShapingEvent(event="exploration_stream", data={...line...})`.
- Ensure the event payload includes: `session_id`, `invocation_id`, `line` (the
  text), `stream` ("stdout" or "stderr")

**What must NOT change:**
- ProcessingNode timer and cancel button (keep those)
- Canvas layout or other node types
- Backend advance logic

**Stop condition:** If the orchestrator doesn't stream lines currently and the
refactor is large, stream only the final output (not line-by-line) as a simpler
first pass.

## Acceptance

- ACC-001: Clicking the ProcessingNode opens a log modal showing harness output
  - Evidence: Playwright test: start session → advance → ProcessingNode appears →
    click it → modal opens showing log lines or "Waiting for output..."
  - Audit: Verify modal renders correctly, is dismissible, doesn't block canvas

- ACC-002: Log modal shows live-streaming output as the harness runs
  - Evidence: If harness produces output, lines appear in the modal in real-time
    (via WebSocket events). Auto-scrolls to bottom.
  - Audit: Verify no duplicate lines, correct ordering, auto-scroll behavior

- ACC-003: Log modal shows terminal state when harness finishes
  - Evidence: After harness completes, modal shows "Completed (exit 0)" or
    "Failed (exit 1)" with the full output preserved
  - Audit: Verify exit code is displayed, log remains viewable after completion

- ACC-004: Modal is closable and doesn't interfere with canvas interaction
  - Evidence: Close button (X) or clicking outside closes modal. After closing,
    canvas nodes are still interactive (no event capture leaks)
  - Audit: Verify no z-index issues, no event propagation bugs

- ACC-005: Frontend builds and backend tests pass
  - Evidence: `npm run build` succeeds, `pytest` passes
  - Audit: No regressions

## Current State

Ready to start. The backend orchestrator already has exploration event publishing;
need to verify it streams line-level output. The frontend needs a new modal
component and WebSocket event handling.

## Journal

- 2026-05-27: Created ticket with Status `open`. Operator identified that
  ProcessingNode at "368s" gives no transparency into what's actually happening.
  Log modal gives full visibility into harness subprocess.
