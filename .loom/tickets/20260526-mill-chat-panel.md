# Design Room: Chat Panel + Harness Integration

ID: ticket:20260526-mill-chat-panel
Type: Ticket
Status: open
Created: 2026-05-26
Updated: 2026-05-26
Risk: high - harness subprocess streaming is the most architecturally complex piece

Priority: high - the interaction model that makes the Design Room special
Depends On: ticket:20260526-mill-design-room-backend

## Summary

Build the right panel of the Design Room: a multi-turn chat interface for shaping
records with AI. Mill owns conversation history. Each turn constructs a full-context
prompt (system + history + document + highlighted context) and shells out to the
configured harness. Responses stream token-by-token. The AI's file edits appear
live in the editor via the existing file watcher.

The chat is where the coupling magic happens: the operator discusses the record
while seeing it change in real-time. Multi-turn memory means the AI understands
"make it more specific" without the operator repeating context.

Single closure claim: Multi-turn conversation works with streaming responses. The
AI's file edits appear in the editor. Session persists in `.mill/chat-sessions/`.
New sessions can be started. Harness command is configurable.

## Related Records

- `spec:mill-design-room` - REQ-010, REQ-011, REQ-012, REQ-018, REQ-019, REQ-020
- `plan:20260526-mill-design-room` - parent plan
- `ticket:20260526-mill-design-room-backend` - provides the chat API endpoints

## Scope

### Must Create

- `loom-mill/frontend/src/lib/design/ChatPanel.svelte` - The full chat panel:

  Layout (top to bottom):
  - Header: "Chat" label + session info + "New Session" button
  - Message list (scrollable):
    - User messages: right-aligned, accent-bg, showing content + any attached context
    - Assistant messages: left-aligned, surface-bg, showing streamed content
    - Streaming indicator: typing dots or cursor blink while response arrives
  - Input area (bottom):
    - Textarea (auto-growing, max 5 lines, min 1 line)
    - Context attachment preview (if text was sent from editor)
    - Send button (right side, accent color)
    - Voice button (microphone icon, left of send) - UI only, behavior in Unit 7
    - Keyboard: Enter sends (Shift+Enter for newline)

  State:
  - `sessionId: string | null`
  - `messages: ChatMessage[]`
  - `streaming: boolean`
  - `streamingContent: string` (accumulates deltas)
  - `inputText: string`
  - `attachedContext: ChatContext | null`

  Behavior:
  - On mount: check for existing session in store (preserved across tab switches)
  - On send:
    1. Add user message to local messages array (optimistic)
    2. POST to `/chat/sessions/{id}/messages` with content + context
    3. Clear input and attached context
    4. Listen for WebSocket `chat_stream` events → append deltas to streamingContent
    5. On `chat_complete` → move streamingContent to messages array as assistant message
    6. On `chat_error` → show error in chat (styled as system message, red)
  - On "New Session":
    1. POST to `/chat/sessions` to create new session
    2. Clear messages
    3. Update sessionId
  - Auto-scroll to bottom on new messages (but allow scrolling up to read history)

- `loom-mill/frontend/src/lib/design/ChatMessage.svelte` - Individual message:
  - Role indicator (user vs assistant)
  - Content: rendered as Markdown (reuse RecordRenderer or simple markdown)
  - Context attachment (if present): collapsible quote block showing highlighted text
  - Timestamp (relative: "2m ago")
  - Copy button on hover (for assistant messages)

- `loom-mill/frontend/src/lib/design/ChatInput.svelte` - The input area:
  - Auto-growing textarea with placeholder "Shape this record..."
  - Context preview bar above input (when text sent from editor):
    ```
    📎 spec:mill-design-room, lines 45-47  [×]
    ```
  - Send/voice buttons
  - Disabled state while streaming

### WebSocket Integration

Listen for these events (add to ws.svelte.ts store):
```typescript
case 'chat_stream':
  // Append delta to streaming buffer
  chatStreamDelta(data.session_id, data.delta);
  break;
case 'chat_complete':
  // Finalize message
  chatComplete(data.session_id, data.message);
  break;
case 'chat_error':
  // Show error
  chatError(data.session_id, data.error);
  break;
```

Add chat state to the store:
```typescript
chatSession: {
  id: string | null;
  messages: ChatMessage[];
  streaming: boolean;
  streamingContent: string;
} | null
```

### Visual Direction

- Messages should look like Linear's comment thread: clean, compact, clear hierarchy
- User messages: subtle accent background, right-aligned bubble style (but not rounded like iMessage - more like a flat card)
- Assistant messages: plain, left-aligned, full-width, with slight surface background
- Streaming: content appears character-by-character with a cursor blink at the end
- Context attachments: indented quote block with file icon, gray bg, monospace for code
- Input: borderless textarea with send button that only activates when text is present

### Must Not Change

- Factory Floor components
- Graph sidebar or document editor (they'll communicate via shared state/events)
- Backend chat API (consume it as-is from Unit 1)

### Non-Goals

- Voice transcription (UI button exists but behavior is Unit 7)
- Editor-to-chat context linking mechanics (that's Unit 6)
- Markdown rendering in assistant messages beyond basic formatting
- Code execution or tool use display (the harness handles that; we just show text)
- Multiple concurrent sessions

## Acceptance

- ACC-001: Sending a message shows it in the chat and triggers a response from the harness
  - Evidence: Playwright test: type message → send → user message appears → assistant response streams in
  - Audit: Verify prompt construction includes conversation history

- ACC-002: Responses stream token-by-token (not all-at-once)
  - Evidence: Observe streaming in Playwright (content grows incrementally)
  - Audit: Verify WebSocket chat_stream events arrive with small deltas

- ACC-003: Multi-turn conversation preserves context (second message references first exchange)
  - Evidence: Send "what is REQ-001" → get response → send "make it shorter" → response refers to REQ-001
  - Audit: Inspect prompt sent on second turn, verify it includes first exchange

- ACC-004: "New Session" clears conversation and starts fresh
  - Evidence: Have conversation → click New Session → messages clear → new session_id
  - Audit: Verify old session still exists in .mill/chat-sessions/

- ACC-005: Chat state persists across tab switches (Design Room ↔ Factory Floor)
  - Evidence: Send messages → switch to Factory Floor → switch back → messages still visible
  - Audit: Verify state is in store, not component-local

- ACC-006: Error from harness shows as error message in chat (not crash)
  - Evidence: Configure invalid harness command → send message → error message appears in chat
  - Audit: Verify chat remains usable after error

## Current State

Ready to start after backend (Unit 1) is deployed and shell (Unit 2) provides the
panel slot. The WebSocket events from the backend drive the streaming experience.

## Journal

- 2026-05-26: Created ticket with Status `open`. Chat is the hardest piece but
  the architecture is clean: Mill owns history, constructs prompts, shells out to
  harness, streams back. File edits flow through existing file watcher.
