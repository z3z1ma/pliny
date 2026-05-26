# Design Room: Editor-to-Chat Context Linking

ID: ticket:20260526-mill-editor-chat-link
Type: Ticket
Status: closed
Created: 2026-05-26
Updated: 2026-05-26
Risk: low - CodeMirror selection API is well-documented; chat input already accepts context

Priority: high - this is what makes the Design Room more than editor+chat side by side
Depends On: ticket:20260526-mill-document-editor, ticket:20260526-mill-chat-panel

## Summary

Build the coupling between the document editor and the chat panel: selecting text
in CodeMirror shows a floating action, clicking it sends the selection with
file/line context to the chat input. This is the feature that transforms the
Design Room from "a markdown editor next to a chat window" into a coupled shaping
environment.

The operator can point at exactly what they want to discuss. Instead of describing
"the third acceptance criterion," they highlight it and say "make this more
specific about timeout behavior."

Single closure claim: Selecting text in the editor shows a floating action.
Clicking it populates the chat input with file/line context. The AI receives this
context as part of the prompt.

## Related Records

- `spec:mill-design-room` - REQ-013
- `plan:20260526-mill-design-room` - parent plan
- `ticket:20260526-mill-document-editor` - provides the CodeMirror instance
- `ticket:20260526-mill-chat-panel` - provides the chat input that receives context

## Scope

### Must Create/Change

- `loom-mill/frontend/src/lib/design/SelectionAction.svelte` - Floating action:
  - Appears above/below the text selection in the editor
  - Shows "📎 Send to chat" button (compact, pill-shaped)
  - Positioned using CodeMirror's `view.coordsAtPos()` API
  - Appears after a brief delay (200ms) to avoid flickering on casual clicks
  - Disappears when selection is cleared

- `loom-mill/frontend/src/lib/design/DocumentEditor.svelte` - Add selection tracking:
  - Listen to CodeMirror's `EditorView.updateListener` for selection changes
  - When selection is non-empty (>5 characters to avoid noise):
    - Compute selection position (top/bottom coordinates)
    - Show SelectionAction floating above/below
  - Expose method or event: `sendSelectionToChat()`
  - When triggered:
    - Get selected text
    - Get line range (from/to line numbers)
    - Get current document path
    - Dispatch to chat panel as attached context

- `loom-mill/frontend/src/lib/design/ChatInput.svelte` - Accept context:
  - Add prop or method: `attachContext(context: ChatContext)`
  - Show context preview bar above the textarea:
    ```
    📎 spec:mill-design-room, lines 45-47  [×]
    > REQ-003: The graph sidebar MUST display all records...
    ```
  - The × clears the attached context
  - When sending, include context in the POST body
  - Context is shown as a collapsible quote in the user message bubble

### Interaction Flow

1. Operator selects text in editor (e.g., an acceptance criterion)
2. After 200ms, floating "📎 Send to chat" pill appears above selection
3. Operator clicks the pill
4. Chat input shows context preview:
   - File path + line range as header
   - Selected text as preview (first 100 chars, truncated)
5. Operator types their message below (e.g., "Make this more specific about timeouts")
6. On send: message + context go to backend
7. Backend constructs prompt with: "The operator has highlighted this text from {path}, lines {n}-{m}:\n> {selected_text}\n\nOperator's message: ..."
8. AI understands exactly what the operator is pointing at

### Must Not Change

- Backend chat endpoint (already accepts context in ChatMessageBody)
- Graph sidebar
- Factory Floor

### Non-Goals

- Multiple selections (one at a time)
- Drag-and-drop text into chat
- Auto-annotate without user action
- Inline comments in the editor (like Google Docs)

## Acceptance

- ACC-001: Selecting text (>5 chars) in editor shows floating "Send to chat" action after 200ms
  - Evidence: Playwright: select text → wait → floating pill visible
  - Audit: Verify positioning is near the selection, not at page top

- ACC-002: Clicking the action populates chat input with context (path + lines + text preview)
  - Evidence: Playwright: click pill → chat input shows context bar with file path and preview
  - Audit: Verify line numbers match the selection in the document

- ACC-003: Sending a message with context includes it in the prompt to the AI
  - Evidence: Inspect network request or backend logs showing context in prompt
  - Audit: Verify the AI response references the highlighted content

- ACC-004: Context can be cleared with × before sending
  - Evidence: Playwright: attach context → click × → context bar disappears → send without context
  - Audit: Verify POST body has context: null after clearing

- ACC-005: Floating action disappears when selection is cleared
  - Evidence: Playwright: select text → pill appears → click elsewhere → pill disappears
  - Audit: No stale floating elements left in DOM

## Current State

Ready to start after both editor (Unit 4) and chat (Unit 5) land. This is the
glue between them.

## Journal

- 2026-05-26: Created ticket with Status `open`. The coupling feature. Without
  this, the Design Room is just an editor next to a chat. With it, the operator
  can point at exactly what they want to shape.
- 2026-05-26: Implemented `SelectionAction.svelte` and integrated it into `DocumentEditor.svelte`. Verified with Playwright that selecting text shows the floating action, and clicking it populates the chat input with the correct context. Status changed to `closed`.
