# Factory Floor Review UX

ID: ticket:20260526-mill-review-ux
Type: Ticket
Status: review
Created: 2026-05-26
Updated: 2026-05-26
Risk: low - adds UI actions that map to existing record update mechanics

## Summary

When a ticket is in `review` status in the Factory Floor, there's no convenient way
to act on it from the UI. Operators need action buttons directly in the detail
panel:
- **Accept**: closes the ticket (Status: closed, journal entry)
- **Escalate**: marks for operator attention (adds a note, could set risk: high)
- **Request a change**: sends back to active (Status: active, journal entry with what needs to change)

Plus a text input field for notes about what still needs to be done or what was observed.

Note: Many tickets go straight from active → closed without entering review. This
UX only applies when a ticket ends up in review status, typically after a workstation
run completes and the agent moved it to review.

Closure claim: Operators can close, escalate, or request changes on review tickets
directly from the Factory Floor detail panel without editing Markdown.

## Related Records

- `plan:20260526-mill-next-gen` - parent plan
- `loom-mill/frontend/src/lib/DetailPanel.svelte` - where the actions render
- `loom-mill/src/loom_mill/api/design.py` - existing record update endpoint (PUT /records/{id})
- `loom-mill/frontend/src/lib/types.ts` - LoomRecord metadata shape

## Scope

Write:
- `loom-mill/frontend/src/lib/DetailPanel.svelte` - add review actions panel when showing a ticket in review status
- `loom-mill/frontend/src/lib/ReviewActions.svelte` (new) - the action buttons + notes component
- `loom-mill/src/loom_mill/api/design.py` - add endpoint to transition ticket status with journal entry

Read:
- `loom-mill/src/loom_mill/api/records.py` - existing content endpoint
- `loom-mill/src/loom_mill/parser/parse.py` - how records are parsed (for programmatic status update)

Non-goals:
- Do NOT add workflow automation (auto-close on test pass, etc.)
- Do NOT change how tickets reach review status
- Do NOT add approval workflows or multi-step review
- Do NOT change the Design Room editor's ticket handling

### Detailed Design

**When to show**: In the Factory Floor DetailPanel, when showing a ticket (non-workstation)
record whose `metadata.status === 'review'`.

**UI**: Below the record content, show a review actions panel:

```
┌─────────────────────────────────────────────────────────┐
│ Review Actions                                          │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Notes (optional)                                    │ │
│ │ __________________________________________________ │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ [✓ Accept]    [⚠ Escalate]    [↺ Request Change]       │
└─────────────────────────────────────────────────────────┘
```

**Actions**:
- Accept: PATCH endpoint sets Status: closed, appends "Accepted" + notes to Journal
- Escalate: PATCH endpoint sets Risk: high, appends "Escalated" + notes to Journal
- Request Change: PATCH endpoint sets Status: active, appends "Change requested" + notes to Journal

**Backend endpoint**: `POST /records/{record_id}/transition`
```json
{
  "action": "accept" | "escalate" | "request_change",
  "notes": "optional text"
}
```

The backend reads the file, applies the status/risk change, appends a journal entry
with timestamp and notes, and writes atomically. The watcher picks up the change
and broadcasts it.

## Acceptance

- ACC-001: When viewing a ticket in review status in Factory Floor, action buttons appear.
  - Evidence: Screenshot showing review actions panel on a review ticket.
  - Audit: Verify buttons only appear for status=review.

- ACC-002: Clicking Accept changes ticket status to closed and adds a journal entry.
  - Evidence: After accept, verify file on disk has Status: closed and journal entry.
  - Audit: Verify the file write is atomic and the watcher picks up the change.

- ACC-003: Request Change sends ticket back to active with notes in journal.
  - Evidence: After request change with notes, verify file has Status: active and journal.
  - Audit: Verify notes appear in journal entry.

- ACC-004: `npm --prefix loom-mill/frontend run build` passes.
  - Evidence: Build output.

- ACC-005: Backend tests pass.
  - Evidence: Test output.

## Current State

Implementation complete and awaiting review. The transition endpoint, route
registration, review action panel, DetailPanel wiring, and backend transition tests
are in place. Evidence is recorded in evidence:20260526-mill-review-ux-validation.
Remaining review gap: no browser screenshot or adversarial audit has been captured
yet, so ACC-001's screenshot evidence is still pending.

## Journal

- 2026-05-26: Created ticket. Source: operator wants convenient review actions
  without editing Markdown.
- 2026-05-26: Started bounded implementation run in current session. Scope is the
  transition endpoint, route registration, review action component, DetailPanel
  wiring, and backend test coverage.
- 2026-05-26: Implemented the scoped backend endpoint and frontend review actions.
  Verification: frontend build passed, backend tests passed (`61 passed`), and
  scoped diff whitespace check passed. Evidence: evidence:20260526-mill-review-ux-validation.
  Moved to review because screenshot evidence and audit remain pending.
