# Mill Ticket Record Rendering in DetailPanel

ID: ticket:20260526-mill-record-rendering
Type: Ticket
Status: active
Created: 2026-05-26
Updated: 2026-05-26
Risk: medium - rendering arbitrary Markdown requires careful sanitization and styling

Priority: high - the biggest visible feature gap; users see "future work" text
Depends On: ticket:20260526-mill-foundation-fixes

## Summary

When a non-workstation ticket is selected in the left panel, the DetailPanel
currently shows a stub with the text "Full record rendering is future work." This
is unacceptable for production. The panel must render the full ticket record
content: metadata badges, acceptance criteria with check states, all headings and
body sections, references as links, and a status/timeline indicator.

The backend already sends `LoomRecord` with `path`, `surface`, `metadata`,
`headings`, `references`, and `labeled_ids`. The record's raw Markdown content is
not currently in the WebSocket payload - a new API endpoint or expanded payload may
be needed to fetch the full record body.

Single closure claim: Selecting any ticket in the left panel renders its complete
record content with proper formatting, metadata display, and readable layout - no
stubs, no placeholders, no "future work."

## Related Records

- `plan:20260526-mill-production-readiness` - parent plan
- `ticket:20260526-mill-foundation-fixes` - must land first (types + API config)
- `.loom/specs/mill-factory-floor.md` - defines record structure

## Scope

### Must Change

- `loom-mill/frontend/src/lib/DetailPanel.svelte` - Replace the stub (lines 91-112)
  with a full record renderer that shows:
  - Header with ticket title (first heading)
  - Metadata row: status badge, risk badge, priority badge, created/updated dates
  - Section navigation (jump to headings within the record)
  - Full body rendered from Markdown:
    - Headings (h2, h3) with anchor IDs
    - Paragraphs with inline formatting (bold, italic, code)
    - Bullet/numbered lists (including nested)
    - Code blocks with syntax highlighting (use existing theme colors)
    - Blockquotes styled as callouts
    - Tables
    - Acceptance criteria rendered as a checklist (ACC-* items)
  - References section showing linked records as clickable items
  - Footer with metadata (labeled_ids, path)

- `loom-mill/src/loom_mill/api/` - New endpoint `GET /records/{record_id}/content`
  that returns the raw Markdown body of a record file. The parser already reads
  these files; expose the raw content alongside parsed metadata.

- `loom-mill/frontend/src/lib/RecordRenderer.svelte` - New component that takes
  raw Markdown and renders it as styled HTML within the Linear theme. Use a
  lightweight Markdown parser (e.g., `marked` or manual regex for the limited
  subset of Markdown Loom records use).

- `loom-mill/frontend/src/lib/MetadataBadges.svelte` - New component for the
  status/risk/priority badge row, reusable across DetailPanel and potentially
  TicketRow.

### Must Not Change

- Left panel rendering (WorkstationList, TicketRow)
- Workstation detail view (logs/iterations/playback tabs)
- Backend record parsing logic (only expose existing parsed data)

### Non-Goals

- Inline editing of records from the UI
- Live-updating record content on file change (the snapshot handles this)
- Full GitHub-flavored Markdown support (only what Loom records actually use)

## Acceptance

- ACC-001: Selecting a non-workstation ticket shows its full rendered content instead of the stub
  - Evidence: Playwright screenshot showing a ticket's metadata, headings, body, and acceptance criteria rendered in DetailPanel
  - Audit: Visual inspection against the raw .md file content

- ACC-002: Metadata badges (status, risk, priority, dates) render correctly with appropriate colors
  - Evidence: Screenshot showing badges with distinct colors per status (green=closed, blue=active, yellow=open, red=blocked)
  - Audit: Compare rendered badges against record metadata values

- ACC-003: Acceptance criteria render as a styled checklist
  - Evidence: Screenshot showing ACC-* items with check indicators
  - Audit: Compare against source ticket's acceptance section

- ACC-004: Code blocks render with monospace font and theme-appropriate background
  - Evidence: Screenshot of a record containing code blocks
  - Audit: Visual inspection of contrast and readability

- ACC-005: References render as clickable items that select the referenced record
  - Evidence: Click a reference link; left panel highlights and DetailPanel updates to show that record
  - Audit: Verify cross-record navigation works

- ACC-006: Backend endpoint `GET /records/{record_id}/content` returns raw Markdown
  - Evidence: `curl http://localhost:8765/records/ticket:20260526-mill-foundation-fixes/content` returns the file contents
  - Audit: Compare response against the file on disk

- ACC-007: Build passes and no "future work" text exists in the codebase
  - Evidence: `npm --prefix loom-mill/frontend run build` clean; `grep -r "future work" loom-mill/frontend/src/` returns nothing
  - Audit: Build verification

## Current State

Backend endpoint slice is implemented and verified. The full ticket still requires
frontend renderer work and visual acceptance evidence.

First Ralph run should:
1. Add `GET /records/{record_id}/content` endpoint to backend
2. Create `RecordRenderer.svelte` with Markdown parsing
3. Create `MetadataBadges.svelte` for status/risk/priority display
4. Replace the DetailPanel stub with the full renderer
5. Verify with Playwright screenshots

## Journal

- 2026-05-26: Backend endpoint slice started. Scope for this run is limited to
  `GET /records/{record_id}/content`, backend route registration, and backend tests;
  frontend renderer work remains out of scope for this run.
- 2026-05-26: Backend endpoint slice completed. Added route and tests for raw
  Markdown content lookup by record ID. Evidence: `source loom-mill/.venv/bin/activate
  && python -m pytest loom-mill/tests/ -v` passed with 49 tests.
- 2026-05-26: Created ticket with Status `open`. The "future work" stub at
  DetailPanel.svelte:109 is the most visible production gap. Backend already
  parses records; needs endpoint to serve raw content.
