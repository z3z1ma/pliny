# Design Room Backend: Record CRUD + Chat Sessions

ID: ticket:20260526-mill-design-room-backend
Type: Ticket
Status: closed
Created: 2026-05-26
Updated: 2026-05-26
Risk: high - harness subprocess management with streaming is architecturally novel for this codebase

Priority: high - blocks all Design Room frontend work

## Summary

Add the backend endpoints the Design Room frontend needs: record creation, record
content update (save from editor), chat session lifecycle, and chat message
handling that spawns a harness subprocess, captures streaming output, and relays
it via WebSocket.

The chat architecture: Mill owns conversation history in `.mill/chat-sessions/`.
Each turn, the backend constructs a rich prompt (system context + conversation
history + current document content + highlighted context) and shells out to the
configured harness command. The response streams back token-by-token via WebSocket
events. The harness has access to `.loom/` so its file edits are detected by the
existing file watcher.

Single closure claim: All Design Room API endpoints work with tests passing. Chat
messages spawn a configurable harness subprocess and stream output via WebSocket.

## Related Records

- `spec:mill-design-room` - full behavior contract (interface contract section)
- `plan:20260526-mill-design-room` - parent plan
- `loom-mill/src/loom_mill/app.py` - existing app; add new router
- `loom-mill/src/loom_mill/api/ws.py` - existing WebSocket; add new event types

## Scope

### Must Change/Create

- `loom-mill/src/loom_mill/api/design.py` - New module with all Design Room endpoints:

  **Record CRUD:**
  ```python
  @router.put("/records/{record_id:path}")
  async def update_record(record_id: str, body: RecordUpdateBody):
      """Write content to an existing record file. Atomic write (tmp+rename)."""
  
  @router.post("/records")
  async def create_record(body: RecordCreateBody):
      """Create a new record from a minimal template. Returns path and content."""
  ```

  **Chat Sessions:**
  ```python
  @router.post("/chat/sessions")
  async def create_chat_session(body: ChatSessionCreate):
      """Create a new chat session. Stores in .mill/chat-sessions/{id}.json"""
  
  @router.post("/chat/sessions/{session_id}/messages")
  async def send_chat_message(session_id: str, body: ChatMessageBody):
      """Send a message. Constructs prompt, spawns harness, streams via WS."""
  
  @router.delete("/chat/sessions/{session_id}")
  async def end_chat_session(session_id: str):
      """End session. Kill harness subprocess if running."""
  
  @router.get("/chat/sessions/{session_id}")
  async def get_chat_session(session_id: str):
      """Return full session state (messages, metadata)."""
  ```

- `loom-mill/src/loom_mill/chat/` - New package for chat logic:
  - `session.py` - ChatSession model, persistence to `.mill/chat-sessions/`
  - `prompt.py` - Prompt construction: system message + history + document + context
  - `harness.py` - Subprocess management: spawn harness, capture streaming stdout,
    relay via WebSocket, handle exit/error

- `loom-mill/src/loom_mill/api/ws.py` - Add new WebSocket event types:
  - `chat_stream`: `{ "session_id", "delta": "token", "done": false }`
  - `chat_complete`: `{ "session_id", "message": { "role", "content" } }`
  - `chat_error`: `{ "session_id", "error": "message" }`

- `loom-mill/src/loom_mill/app.py` - Register the design router

- `loom-mill/tests/test_design_api.py` - Tests for all endpoints

### Data Models

```python
class ChatSessionCreate(BaseModel):
    harness_command: str = "opencode run"  # configurable
    document_path: str | None = None

class ChatMessageBody(BaseModel):
    content: str
    context: ChatContext | None = None

class ChatContext(BaseModel):
    path: str  # file path of highlighted text
    selected_text: str
    line_range: tuple[int, int] | None = None

class RecordUpdateBody(BaseModel):
    content: str

class RecordCreateBody(BaseModel):
    surface: str  # tickets, specs, plans, research, knowledge
    slug: str | None = None  # auto-generated if not provided
```

### Prompt Construction (prompt.py)

Each turn constructs:
```
You are a Loom Weaver helping the operator shape records in the Design Room.

Current document: {document_path}
Document content:
```
{file content}
```

Conversation so far:
Human: {msg1}
Assistant: {response1}
Human: {msg2}
...

{if context: "The operator has highlighted this text from {path}, lines {n}-{m}:
> {selected_text}
"}

Operator's message: {new_message}

You may edit files in .loom/ as needed. Your edits will appear live in the editor.
```

### Harness Subprocess (harness.py)

```python
async def run_harness(command: str, prompt: str, session_id: str, ws_broadcast):
    """Spawn harness subprocess, stream stdout line-by-line via WebSocket."""
    # Split command into argv
    # Spawn with asyncio.create_subprocess_exec
    # Pipe stdin (send prompt), capture stdout/stderr
    # For each line of stdout, broadcast chat_stream event
    # On process exit, broadcast chat_complete with full response
    # On error, broadcast chat_error
```

The harness command is configurable. Default: `opencode run`. The prompt is piped
to stdin or passed as an argument depending on the harness. For `opencode run`,
it's passed as the positional prompt argument. For `claude`, it's piped to stdin
with `-p`.

### Record Templates (for POST /records)

Minimal templates per surface type:
- Ticket: ID + Type + Status + Created + Updated + `## Summary` + `## Scope` + `## Acceptance`
- Spec: ID + Type + Status + Created + Updated + `## Summary` + `## Requirements`
- Plan: ID + Type + Status + Created + Updated + `## Summary` + `## Execution Units`
- Research: ID + Type + Status + Created + Updated + `## Summary` + `## Findings`
- Knowledge: ID + Type + Status + Created + Updated + `## Summary`

### Must Not Change

- Existing Factory Floor endpoints
- Existing WebSocket event handling for workstations
- The record parser (reuse existing parsing)
- The file watcher (it already broadcasts RecordChanged events)

### Non-Goals

- Implementing the frontend
- Harness-specific session resume (we construct full context each turn)
- Authentication or multi-user
- File locking or optimistic concurrency (single operator)

## Acceptance

- ACC-001: `PUT /records/ticket:20260526-mill-foundation-fixes` updates the file on disk and the watcher broadcasts RecordChanged
  - Evidence: Integration test that PUTs content, reads file, verifies content matches
  - Audit: Verify atomic write (no partial file on crash)

- ACC-002: `POST /records` with `surface=tickets` creates a new file at `.loom/tickets/YYYYMMDD-{slug}.md` with template content
  - Evidence: Integration test that creates record, verifies file exists with expected template
  - Audit: Verify slug generation and collision handling

- ACC-003: `POST /chat/sessions` creates a session file in `.mill/chat-sessions/` and returns session_id
  - Evidence: Test that creates session, verifies JSON file exists
  - Audit: Verify session state structure

- ACC-004: `POST /chat/sessions/{id}/messages` constructs correct prompt with history + document + context
  - Evidence: Unit test on prompt construction with mocked harness subprocess
  - Audit: Verify prompt includes all prior messages and current document content

- ACC-005: Chat message spawns harness subprocess and streams output via WebSocket `chat_stream` events
  - Evidence: Integration test with a simple echo harness (`echo "hello"`) that verifies stream events
  - Audit: Verify subprocess cleanup on completion and error

- ACC-006: All tests pass: `python -m pytest loom-mill/tests/ -v`
  - Evidence: Test output showing pass count
  - Audit: No test isolation issues

## Current State

Implementation completed in the current session and is ready for review/audit.
The backend now has Design Room record CRUD endpoints, chat session persistence,
prompt construction, harness subprocess streaming, WebSocket chat events, route
registration, and tests.

Evidence: `evidence:20260526-mill-design-room-backend-tests` records the full
`loom-mill/tests/` pass and scoped whitespace check. Separate audit is still the
next honest step before closure because the ticket risk is high and the harness
subprocess path is architecturally novel for this codebase.

## Journal

- 2026-05-26: Created ticket with Status `open`. Backend-first to unblock all
  frontend Design Room work. Chat architecture: Mill-owned history, per-turn
  prompt construction, configurable harness command.
- 2026-05-26: Status set to `active`; implementation running in current session
  as a bounded Ralph slice over backend API, chat package, route registration,
  and tests.
- 2026-05-26: Implemented backend endpoints, chat package, WebSocket chat event
  support, route registration, and tests. Full test suite passed: `57 passed in
  29.64s`. Scoped `git diff --check` passed for backend/ticket files. Status set
  to `review` pending audit.
