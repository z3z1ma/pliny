# Mill Design Room Implementation

ID: plan:20260526-mill-design-room
Type: Plan
Status: completed
Created: 2026-05-26
Updated: 2026-05-26
Risk: high - new product surface with harness subprocess management, CodeMirror integration, and real-time sync; high reward justifies the risk

## Summary

Build the complete Design Room mode for Loom Mill: the three-panel shaping
environment where operators author records, build context through AI conversation,
and see their work become ready for the Factory Floor. This is the other half of
the Mill application.

The Design Room is the most valuable human time in the system. Every minute spent
shaping well saves hours of execution drift. This plan delivers the full vision:
CodeMirror editor, record graph, multi-turn chat with harness integration, voice
input, editor-to-chat context linking, and ready-to-fab indicators.

## Related Records

- `spec:mill-design-room` - behavior contract for this surface
- `spec:mill-factory-floor` - the execution counterpart
- `plan:20260526-mill-production-readiness` - completed; Design Room inherits the same quality bar
- `.loom/knowledge/frontend-expert-agent-preferences.md` - agent dispatch preferences

## Strategy

The route builds from infrastructure outward to interaction:

1. **Backend API** (record CRUD, chat session management) - enables everything else
2. **Tab navigation + layout shell** - structural frame before filling panels
3. **Graph sidebar** - the navigation/wayfinding panel; needs records from WebSocket
4. **Document editor** (CodeMirror 6) - the center panel; needs save endpoint
5. **Chat panel + harness integration** - the right panel; the hardest piece
6. **Editor-to-chat context** - couples the editor to chat (needs both to exist)
7. **Voice input + polish** - final layer; Web Speech API, transitions, responsive

Units 1-2 are strictly sequential (backend before frontend shell). Units 3-4 can
parallelize after the shell exists. Unit 5 depends on the backend chat API (Unit 1)
and the layout shell (Unit 2). Unit 6 depends on both editor (Unit 4) and chat
(Unit 5). Unit 7 is final polish after all panels work.

The backend work (Unit 1) uses the `general` agent. All frontend work uses
`frontend-expert` with Playwright verification loops.

Recovery: If harness integration (Unit 5) proves more complex than expected, the
chat can initially work as a styled textarea that shows "Configure harness command
in settings" until subprocess management is stable. The other panels are
independently valuable.

Server startup for all subagent work:
```bash
pkill -f 'uvicorn.*loom_mill' || true
cd /Users/alexanderbutler/code_projects/personal/agent-loom
source loom-mill/.venv/bin/activate
nohup python -m uvicorn loom_mill.app:app --host 127.0.0.1 --port 8765 > /tmp/loom-mill-backend.log 2>&1 < /dev/null &

pkill -f 'vite.*loom-mill' || true
cd /Users/alexanderbutler/code_projects/personal/agent-loom/loom-mill/frontend
nohup npm run dev > /tmp/loom-mill-vite.log 2>&1 < /dev/null &
sleep 3
```

## Execution Units

### Unit 1: Backend API - Record CRUD + Chat Sessions

Ticket: ticket:20260526-mill-design-room-backend

Add backend endpoints for record creation, record content update, chat session
lifecycle, and chat message handling with harness subprocess management. This is
the data layer the Design Room frontend depends on.

Closure claim: `PUT /records/{id}`, `POST /records`, `POST /chat/sessions`,
`POST /chat/sessions/{id}/messages`, and `DELETE /chat/sessions/{id}` all work
with tests passing. Chat messages spawn a configurable harness subprocess and
stream output via WebSocket.

### Unit 2: Tab Navigation + Design Room Layout Shell

Ticket: ticket:20260526-mill-design-room-shell

Add top-level mode switching (Design Room / Factory Floor) and the three-panel
layout shell for the Design Room. No panel content yet - just the structural
frame with correct proportions, collapsibility, and responsive behavior.

Closure claim: Clicking "Design Room" shows a three-panel layout with placeholder
content. Clicking "Factory Floor" returns to the existing execution UI. State is
preserved across switches.

### Unit 3: Record Graph Sidebar

Ticket: ticket:20260526-mill-graph-sidebar

Build the left panel: a tree view of all records organized by surface, with
status-colored dots, titles, hierarchy (plan→tickets, spec→tickets), readiness
indicators, and a "+ New" record creation button.

Closure claim: The graph sidebar renders all records from the WebSocket store
with correct status colors, tree hierarchy from references/depends-on, ready-to-fab
indicators on qualifying tickets, and working record creation via "+ New."

### Unit 4: CodeMirror Document Editor

Ticket: ticket:20260526-mill-document-editor

Build the center panel: a CodeMirror 6 Markdown editor with syntax highlighting,
line numbers, Ctrl+S save, live file update on external changes, modified
indicator, and theme matching.

Closure claim: Opening a record shows its content in CodeMirror with full Markdown
highlighting. Cmd+S saves to disk. External file changes update the editor live.
Unsaved changes are indicated and protected.

### Unit 5: Chat Panel + Harness Integration

Ticket: ticket:20260526-mill-chat-panel

Build the right panel: a multi-turn chat interface that shells out to the
configured harness. Mill owns conversation history. Each turn constructs a prompt
with full context (history + document + highlighted text). Responses stream
token-by-token.

Closure claim: The operator can have a multi-turn conversation with the AI. The
AI's file edits appear live in the editor. Conversation history persists in
`.mill/chat-sessions/`. A new session can be started. The harness command is
configurable.

### Unit 6: Editor-to-Chat Context Linking

Ticket: ticket:20260526-mill-editor-chat-link

Build the coupling between editor and chat: select text in CodeMirror → floating
action → selected text with file/line context appended to chat input. This is
the feature that makes the Design Room more than a markdown editor next to a
chat window.

Closure claim: Selecting text in the editor shows a floating "Send to chat"
action. Clicking it populates the chat input with the selection context
(file path, line range, selected text). The prompt includes this context when sent.

### Unit 7: Voice Input + Final Polish

Ticket: ticket:20260526-mill-voice-polish

Add voice input via Web Speech API, smooth transitions on panel collapse/expand,
responsive behavior for the three-panel layout, and final visual polish matching
the Linear aesthetic.

Closure claim: The microphone button activates browser speech recognition.
Transcribed text appears in chat input. All panels have smooth transitions.
The Design Room is responsive from 768px to 2560px.

## Milestones

### Milestone: Infrastructure Ready

Child tickets: ticket:20260526-mill-design-room-backend, ticket:20260526-mill-design-room-shell

Backend API works. Tab navigation works. The structural frame exists for panels
to fill.

### Milestone: Panels Complete

Child tickets: ticket:20260526-mill-graph-sidebar, ticket:20260526-mill-document-editor, ticket:20260526-mill-chat-panel

All three panels render and function independently. The operator can navigate
records, edit them, and chat with the AI.

### Milestone: Fully Coupled + Polished

Child tickets: ticket:20260526-mill-editor-chat-link, ticket:20260526-mill-voice-polish

The panels are coupled (editor highlights flow to chat). Voice works. Transitions
are smooth. The Design Room is production-ready.

## Current State

Spec written (`spec:mill-design-room`). Plan created. Child tickets being filed.

## Journal

- 2026-05-26: Created plan with Status `open`. Design Room spec accepted. Full
  7-unit decomposition based on dependency analysis. Backend-first strategy to
  unblock all frontend panels.
