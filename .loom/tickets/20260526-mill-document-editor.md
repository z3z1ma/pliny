# Design Room: CodeMirror Document Editor

ID: ticket:20260526-mill-document-editor
Type: Ticket
Status: closed
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - CodeMirror 6 integration requires new npm dependency and careful state management for live updates

Priority: high - the center panel where records are authored
Depends On: ticket:20260526-mill-design-room-shell

## Summary

Build the center panel of the Design Room: a CodeMirror 6 Markdown editor with
syntax highlighting, line numbers, Ctrl+S/Cmd+S save to disk, live file update on
external changes, modified indicator, unsaved-changes warning, and theme matching
(dark/light mode).

The editor is where the operator spends most of their time. It must feel as
responsive as VS Code. CodeMirror 6 achieves this with its lean architecture.

Single closure claim: Opening a record shows its content in CodeMirror with full
Markdown highlighting. Cmd+S saves to disk. External file changes update the
editor live. Unsaved changes are indicated and protected.

## Related Records

- `spec:mill-design-room` - REQ-006, REQ-007, REQ-008, REQ-009
- `plan:20260526-mill-design-room` - parent plan

## Scope

### Must Install (npm dependencies)

```bash
cd loom-mill/frontend
npm install @codemirror/view @codemirror/state @codemirror/language @codemirror/lang-markdown @codemirror/commands @codemirror/search @codemirror/autocomplete @codemirror/lint
```

Note: CodeMirror 6 is modular. Each package is small.

### Must Create

- `loom-mill/frontend/src/lib/design/DocumentEditor.svelte` - The editor component:
  
  Props:
  - `documentPath: string | null` - currently open record path
  - `onSave: (content: string) => void` - save handler (calls PUT endpoint)
  
  Behavior:
  - Mount CodeMirror 6 with:
    - Markdown language support (`@codemirror/lang-markdown`)
    - Line numbers
    - Active line highlight
    - Bracket matching
    - Search (Ctrl+F)
    - Custom keybinding: Cmd+S → save
    - Theme: create custom theme from Mill's CSS variables (dark/light)
  - When `documentPath` changes:
    - If current doc has unsaved changes, show confirm dialog
    - Fetch content from `GET /records/{id}/content`
    - Set editor content
    - Reset modified state
  - Track modified state: compare current content to last-saved content
  - Show modified indicator in editor header (dot or "Modified" text)
  - On save (Cmd+S or explicit):
    - Call `PUT /records/{id}` with current content
    - On success: reset modified state, show brief save confirmation
    - On error: show error toast, keep modified state

- `loom-mill/frontend/src/lib/design/EditorHeader.svelte` - Compact header above editor:
  - File path breadcrumb (surface / filename)
  - Modified indicator (blue dot)
  - Save button (visible when modified)
  - File info (line count, character count)

- `loom-mill/frontend/src/lib/design/editor-theme.ts` - Custom CodeMirror theme:
  - Read from CSS custom properties (--color-bg-primary, --color-text-primary, etc.)
  - Dark variant and light variant
  - Markdown-specific styling:
    - Headings: bold, larger font
    - Code: monospace, background highlight
    - Links: accent color
    - Bold/italic: proper weight/style
    - Blockquotes: muted color
    - Lists: proper indentation markers

### Live File Update Behavior

When the WebSocket receives `RecordChanged` for the currently open document:
- If editor has NO unsaved changes: replace content silently, preserve cursor position
- If editor HAS unsaved changes: show a conflict indicator in the header
  ("File changed externally. Reload | Keep yours"). Do NOT auto-replace.

This handles the case where the AI (via chat) edits the file while the operator
is viewing it. If the operator hasn't made local changes, the edit appears
seamlessly.

### Must Not Change

- Backend endpoints (uses existing GET /records/{id}/content + new PUT from Unit 1)
- Factory Floor components
- Other Design Room panels

### Non-Goals

- Collaborative editing (single operator)
- Inline AI suggestions (that's what the chat panel is for)
- Custom Loom syntax extensions like record-link autocomplete (future enhancement)
- Split editor / side-by-side preview
- File tree (the graph sidebar is the navigation)

## Acceptance

- ACC-001: CodeMirror renders with Markdown syntax highlighting (headings colored, code blocks distinct, links underlined)
  - Evidence: Playwright screenshot of a record with varied Markdown content
  - Audit: Visual inspection of syntax colors against theme

- ACC-002: Cmd+S saves content to disk via PUT endpoint; modified indicator clears
  - Evidence: Playwright test: edit text → modified dot appears → Cmd+S → dot disappears → file on disk matches
  - Audit: Verify atomic write behavior

- ACC-003: External file change updates editor when no local modifications exist
  - Evidence: Start backend, open record, externally modify file, verify editor content updates
  - Audit: Verify cursor position is preserved

- ACC-004: External file change shows conflict indicator when local modifications exist
  - Evidence: Edit in editor (don't save), externally modify file → conflict banner appears
  - Audit: Verify "Reload" reloads and "Keep yours" dismisses

- ACC-005: Theme matches Mill dark/light mode (switches live with ThemeToggle)
  - Evidence: Playwright screenshots in both dark and light modes
  - Audit: Verify no hardcoded colors, all from CSS variables

- ACC-006: Frontend builds clean with CodeMirror dependencies
  - Evidence: `npm --prefix loom-mill/frontend run build` passes
  - Audit: Bundle size within reason (CodeMirror 6 should add ~50-80KB gzipped)

## Current State

Ready to start after Unit 2 (shell) lands. CodeMirror 6 needs to be installed as
a dependency first.

## Journal

- 2026-05-26: Created ticket with Status `open`. CodeMirror 6 is the only
  production-grade choice. Its modular architecture keeps bundle size manageable.
  The key challenge is live update without losing cursor position.
