# Mill Design Room

ID: spec:mill-design-room
Type: Spec
Status: active
Created: 2026-05-26
Updated: 2026-05-26

## Summary

The Design Room is one of two primary modes in Loom Mill (alongside the Factory
Floor). It is where the human operator shapes work: authoring records, building
context, refining specs, scoping tickets, and directing AI through conversation.
The output of the Design Room is shaped, executable work that the Factory Floor
picks up automatically through the scheduling mechanism.

This spec defines the behavior of the Design Room's three-panel layout, the
CodeMirror-based Markdown editor, the record graph sidebar, the chat panel with
harness integration, voice input, editor-to-chat context linking, and the
"ready to fab" readiness indicators.

## Product Slice

The Design Room UI and its supporting backend endpoints. This includes:
- The three-panel layout (graph + document + chat)
- Tab navigation between Design Room and Factory Floor
- The Markdown editor with live file sync
- The record graph sidebar with status indicators
- The chat panel with harness subprocess management
- Voice transcription input
- Editor highlight-to-chat context flow
- Record creation and file write-back
- "Ready to fab" derivation from record graph state

This spec does NOT cover the Factory Floor (spec:mill-factory-floor), the
scheduling agent behavior (spec:mill-scheduling-agent), or the process control
system (spec:mill-process-control). Those are separate product surfaces.

## Spec Set Coverage

The existing spec set covers the Factory Floor execution mode. This spec adds
the shaping mode, completing the two-tab Mill application. Together with
spec:mill-factory-floor, they define the complete operator experience. Adjacent
behavior needing separate specs: harness configuration (partially in
spec:mill-factory-floor), and the scheduling agent's pull logic for transitioning
shaped work to execution.

## Problem

Today, shaping happens in a chat conversation. The operator describes records over
the phone, so to speak. There is no coupled view of the document being shaped. No
graph showing what's linked to what. No way to highlight a section and say "this
part." No visibility into which work is ready for the factory and which still needs
human attention. The operator's most valuable time (shaping) has the worst tooling.

## Desired Behavior

The Design Room presents a three-panel layout: a graph sidebar (left), a document
editor (center), and a chat panel (right). These three panels are coupled:
clicking a record in the graph opens it in the editor and focuses the chat on that
record. Editing the document saves to disk. When the AI edits a file in response
to chat, the editor updates live. Highlighting text in the editor and sending it
to chat provides precise context for the AI.

The operator can create new records, navigate the full record graph, shape work
through conversation, think aloud via voice, and see at a glance which tickets are
ready for the Factory Floor.

## Not Doing

- The Design Room does not execute tickets (that's the Factory Floor)
- The Design Room does not interpret record prose (it renders and edits it)
- The Design Room does not own record validation (the model does, via chat)
- No real-time collaborative editing (single operator)
- No version control UI (git is background infrastructure)
- No inline AI suggestions while typing (only through explicit chat)
- No custom record templates in the UI (use chat: "create a ticket for...")

## Requirements

- REQ-001: The Mill UI MUST provide a top-level navigation between "Design Room"
  and "Factory Floor" modes that preserves each mode's state when switching.

- REQ-002: The Design Room MUST render a three-panel layout: graph sidebar (left,
  collapsible, default 240px), document editor (center, flex), and chat panel
  (right, collapsible, default 360px).

- REQ-003: The graph sidebar MUST display all records from `.loom/` as a tree
  organized by surface (constitution, specs, plans, tickets, research, evidence,
  audit, knowledge) with status-colored indicators.

- REQ-004: Each record in the graph MUST show: a status dot (green=closed/accepted,
  blue=active, amber=open/draft, red=blocked, gray=cancelled/retired), the record
  title (first heading or ID), and child records (tickets under their plan, tickets
  citing a spec).

- REQ-005: Clicking a record in the graph MUST open it in the document editor and
  set it as the active document for the chat panel context.

- REQ-006: The document editor MUST use CodeMirror 6 with Markdown syntax
  highlighting, line numbers, and the theme matching Mill's dark/light mode.

- REQ-007: The document editor MUST save changes to disk on Ctrl+S (or Cmd+S) by
  calling the `PUT /records/{record_id}` endpoint.

- REQ-008: When a file changes on disk (detected by the file watcher), the editor
  MUST update its content live if the document is not currently being edited by the
  user (no unsaved local changes).

- REQ-009: The editor MUST show a "modified" indicator when the user has unsaved
  changes, and MUST warn before navigating away from an unsaved document.

- REQ-010: The chat panel MUST support multi-turn conversation with the configured
  harness. Mill owns the conversation history. Each turn constructs a prompt
  including: system context, conversation history, current document content, and
  any highlighted context.

- REQ-011: The chat panel MUST stream responses token-by-token via WebSocket as the
  harness produces output.

- REQ-012: When the AI edits files during a chat turn (detected by file watcher),
  the document editor MUST update live, even mid-response.

- REQ-013: The user MUST be able to select text in the editor and send it to the
  chat as context. A floating action appears on selection: "Send to chat." Clicking
  it appends the selection with file path and line range to the chat input.

- REQ-014: The chat panel MUST support voice input via the Web Speech API. A
  microphone button starts transcription; the transcribed text appears in the chat
  input field for review before sending.

- REQ-015: The graph sidebar MUST show "ready to fab" indicators on tickets. A
  ticket is ready when: Status is open, all Depends On records are closed, linked
  spec (if any) is active or accepted, and at least one ACC-* criterion exists.

- REQ-016: The Design Room MUST support creating new records. A "+ New" button in
  the graph sidebar opens a dropdown: Ticket, Spec, Plan, Research, Knowledge.
  Selecting one creates a new file from a minimal template and opens it in the
  editor.

- REQ-017: The graph sidebar MUST show edges between records: plan → child tickets,
  spec → citing tickets, ticket → depends-on tickets. These appear as tree
  nesting and/or subtle connection lines.

- REQ-018: The chat session MUST persist across tab switches (Design Room ↔
  Factory Floor). Returning to Design Room restores the conversation.

- REQ-019: The chat session state MUST be stored in `.mill/chat-sessions/` (runtime
  state, not committed). Each session includes: messages, active document path,
  harness command used, timestamps.

- REQ-020: The user MUST be able to start a new chat session (clearing history) via
  a "New Session" button in the chat panel header.

## Scenarios

### SCN-001: Open Record From Graph

Exercises: REQ-003, REQ-004, REQ-005, REQ-006

GIVEN the Design Room is active and `.loom/tickets/20260526-mill-foundation-fixes.md` exists
WHEN the operator clicks "mill-foundation-fixes" under the Tickets section in the graph
THEN the document editor opens that file with Markdown syntax highlighting
AND the chat panel context updates to reference that document
AND the graph shows the record as selected (highlight/ring)

### SCN-002: Edit And Save Document

Exercises: REQ-006, REQ-007, REQ-009

GIVEN a record is open in the editor
WHEN the operator types changes to the document
THEN the "modified" indicator appears
AND when the operator presses Cmd+S, the file is written to disk via PUT endpoint
AND the modified indicator disappears
AND the file watcher detects the change and broadcasts to other connected clients

### SCN-003: Multi-Turn Chat Shaping

Exercises: REQ-010, REQ-011, REQ-012, REQ-018

GIVEN a ticket is open in the editor and the chat panel is visible
WHEN the operator types "Add an acceptance criterion for error handling" and sends
THEN the harness is invoked with a prompt containing conversation history + document content
AND the response streams token-by-token into the chat panel
AND if the AI edits the ticket file, the editor updates live with the new ACC-* item
AND the operator sends a follow-up "Make it more specific about timeout behavior"
AND the harness receives the full conversation history including the first exchange

### SCN-004: Highlight-To-Chat Context

Exercises: REQ-013

GIVEN a spec is open in the editor with multiple requirements listed
WHEN the operator selects the text of REQ-003
THEN a floating action "📎 Send to chat" appears near the selection
AND clicking it appends to the chat input: "> [spec:mill-design-room, lines 45-47]\n> REQ-003: The graph sidebar MUST...\n\n"
AND the operator can add their message below the context before sending

### SCN-005: Voice Input

Exercises: REQ-014

GIVEN the chat panel is active
WHEN the operator clicks the microphone button
THEN the browser Speech Recognition API activates (microphone icon pulses)
AND as the operator speaks, transcribed text appears in the chat input
AND when the operator stops speaking (or clicks the mic button again), transcription ends
AND the text remains in the input for editing before sending

### SCN-006: Ready-To-Fab Indicator

Exercises: REQ-015

GIVEN a ticket exists with Status=open, no unresolved Depends On, linked to an active spec, and has ACC-001 defined
THEN the graph sidebar shows a green "ready" indicator (e.g., filled circle or checkmark) on that ticket
AND given another ticket has Status=open but Depends On a still-open ticket
THEN that ticket shows a gray/pending indicator instead

### SCN-007: Create New Record

Exercises: REQ-016

GIVEN the Design Room is active
WHEN the operator clicks "+ New" and selects "Ticket"
THEN a new file is created at `.loom/tickets/YYYYMMDD-untitled.md` with minimal template
AND it opens in the editor
AND the graph sidebar adds it under Tickets
AND the chat context updates to the new document

### SCN-008: Live File Update From External Edit

Exercises: REQ-008, REQ-012

GIVEN a record is open in the editor with no unsaved changes
WHEN an external process (harness, another editor) modifies the file on disk
THEN the file watcher detects the change
AND the editor content updates to reflect the new file content without losing cursor position
AND given the editor HAS unsaved changes, the editor does NOT auto-update but shows a conflict indicator

## Evidence Plan

- REQ-001 / SCN-001: Playwright screenshot showing tab navigation and graph interaction
- REQ-006 / SCN-002: Playwright screenshot of CodeMirror editor with syntax highlighting; verify save via file read
- REQ-010 / SCN-003: Backend integration test showing multi-turn prompt construction with history
- REQ-013 / SCN-004: Playwright interaction test: select text → floating action → chat input populated
- REQ-014 / SCN-005: Manual verification (Web Speech API requires microphone permission)
- REQ-015 / SCN-006: Playwright screenshot showing ready/not-ready indicators on tickets
- REQ-016 / SCN-007: Playwright test: create record → file exists on disk → opens in editor

## Open Questions

- None blocking - current contract is ready for downstream tickets.

## Quality Bar

The Design Room should feel like a purpose-built shaping environment, not a
markdown editor with a chat bolted on. The coupling between panels is the key
quality signal:

- Clicking in the graph immediately opens in editor. No loading spinners for local files.
- Chat responses that edit files should show the edit appearing in real-time (within 1 frame of file watcher detection).
- The graph should update readiness indicators within 1 second of a record status change.
- Voice input should feel like dictation, not a separate mode.
- The editor should feel as responsive as VS Code (CodeMirror 6 achieves this).

Non-examples of quality:
- Chat that opens in a separate window
- Editor that requires page reload to see file changes
- Graph that shows stale status after saves
- Highlight-to-chat that loses the selection context
- Voice that blocks the UI while transcribing

## Interface Contract

### Backend Endpoints

- `PUT /records/{record_id}` 
  - Input: `{ "content": "raw markdown string" }`
  - Output: `{ "id": "...", "path": "...", "updated": true }`
  - Side effects: writes file to disk, file watcher broadcasts RecordChanged
  - Error: 404 if record not found, 409 if file changed since last read (optional optimistic lock)

- `POST /records`
  - Input: `{ "surface": "tickets|specs|plans|...", "slug": "optional-slug" }`
  - Output: `{ "id": "...", "path": "...", "content": "template content" }`
  - Side effects: creates file on disk with template content

- `POST /chat/sessions`
  - Input: `{ "harness_command": "opencode run", "document_path": "optional" }`
  - Output: `{ "session_id": "...", "created_at": "..." }`
  - Side effects: creates session in `.mill/chat-sessions/`

- `POST /chat/sessions/{session_id}/messages`
  - Input: `{ "content": "user message", "context": { "path": "...", "selected_text": "...", "line_range": [n, m] } | null }`
  - Output: streaming via WebSocket event `chat_stream`
  - Side effects: spawns harness subprocess, streams response, saves to session

- `DELETE /chat/sessions/{session_id}`
  - Side effects: terminates any active harness subprocess, marks session ended

### WebSocket Events (new)

- `chat_stream`: `{ "session_id": "...", "delta": "token text", "done": false }`
- `chat_complete`: `{ "session_id": "...", "message": { "role": "assistant", "content": "full response" } }`
- `chat_error`: `{ "session_id": "...", "error": "message" }`

### Frontend State

- `activeMode: 'design' | 'factory'`
- `activeDocument: { path, content, modified, record } | null`
- `chatSession: { id, messages[], streaming } | null`
- `graphState: { records[], edges[], selectedId } `

## Constraints

- CodeMirror 6 is the only acceptable editor (no textarea, no contentEditable, no Monaco)
- Chat prompt construction happens server-side (the frontend never sees raw harness commands)
- Voice uses Web Speech API only (no external transcription service dependency)
- Session state lives in `.mill/chat-sessions/` (gitignored, runtime only)
- The Design Room never reasons about records; only the model (via harness) does
- File saves are atomic (write to temp, rename) to prevent corruption
- The graph derives edges from record metadata (references, depends_on, IDs) without parsing prose

## Related Records

- `spec:mill-factory-floor` - the execution mode counterpart; shares the tab navigation and WebSocket infrastructure
- `spec:mill-scheduling-agent` - defines how shaped work transitions to execution
- `.loom/knowledge/frontend-expert-agent-preferences.md` - agent dispatch preferences for implementation
