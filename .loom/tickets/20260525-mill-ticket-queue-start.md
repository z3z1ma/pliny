# Ticket Queue & Start Flow

ID: ticket:20260525-mill-ticket-queue-start
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: low - frontend component addition with one existing backend call (POST /workstations).
Priority: high - currently there is NO way to start a workstation from the UI.

## Summary

Add a "Ready" queue section to the WorkstationList that shows tickets eligible for execution (status=open) with a "Start" button on each. This completes the factory pull-flow in a single panel: Ready → Active → Completed. Fix the empty state text to match the actual available action.

Currently there is NO UI affordance to start a workstation. The old TicketCard Start buttons were deleted in the layout overhaul and nothing replaced them. The empty state says "Start one from the pipeline status bar" but the StatusBar is just a display counter with no actions.

Closure claim: The operator can see ready tickets and start workstations directly from the WorkstationList panel, with the entire lifecycle flow (Ready → Active → Completed) visible in one place.

## Related Records

- `spec:mill-factory-floor` REQ-016 - operator controls must include start workstation
- `spec:mill-scheduling-agent` - when scheduling is enabled, ready tickets auto-pull; manual start remains as override
- `loom-mill/frontend/src/lib/WorkstationList.svelte` - the component to modify
- `loom-mill/src/loom_mill/api/workstation.py` - existing POST /workstations endpoint (already works)
- `loom-mill/frontend/src/lib/ws.svelte.ts` - has records with status info

## Scope

Write:
- `loom-mill/frontend/src/lib/WorkstationList.svelte` - add Ready section with start actions
- `loom-mill/frontend/src/lib/ReadyTicketRow.svelte` (new) - compact row for a ready ticket with start button

Non-goals:
- Do NOT change the StatusBar (it remains a display-only counter)
- Do NOT change the backend (POST /workstations already exists and works)
- Do NOT implement the scheduling agent UI toggle (future work)
- Do NOT add drag-and-drop reordering of the queue

## Detailed Design

### WorkstationList New Structure

The panel now has THREE sections in vertical order:

```
┌─────────────────────────────────────────┐
│ Workstations                    2/3 WIP │  ← header
├─────────────────────────────────────────┤
│ READY (3)                               │  ← collapsible section
│ ◇ Protocol Compression Fix        [▶]   │  ← ReadyTicketRow
│ ◇ OpenCode Natural Prompt Probes  [▶]   │
│ ◇ SPC Engine Build Out            [▶]   │
├─────────────────────────────────────────┤
│ ACTIVE                                  │  ← section label (only when items exist)
│ ● Fix Weaver Runtime Wiring   #3  6m 2s│  ← WorkstationRow (existing)
│ ● Log Streaming               #1  45s  │
├─────────────────────────────────────────┤
│ ▸ Completed (2)                   Clear │  ← collapsible (existing)
│   ✓ Parser Module             Done  8m  │
│   ✓ Multi-Workstation         Done 12m  │
└─────────────────────────────────────────┘
```

### Ready Section Behavior

**Which tickets appear in Ready:**
- All records from the WebSocket store where `metadata.type === 'Ticket'` (or path includes `tickets/`)
- AND `metadata.status` is in `['open', 'shaped']` (the ready set)
- AND the ticket does NOT already have an active workstation

**Sorting:** Alphabetical by title, or by priority field if present. Keep it simple.

**Collapsible:** Yes, like Completed. Default: expanded. Toggle with click on the section header. Show count in header.

**Empty state (Ready section is empty):** Don't show the Ready section at all. Just show active workstations (or the global empty state if nothing is active either).

### ReadyTicketRow.svelte

A compact row (36px height) for each ready ticket. Simpler than WorkstationRow since there's less state to show.

```svelte
<div class="group flex items-center gap-2 px-3 py-2 hover:bg-bg-surface-elevated transition-colors duration-150">
  <!-- Diamond icon (indicating "shaped/ready") -->
  <span class="w-2 h-2 rotate-45 border border-text-tertiary shrink-0"></span>
  
  <!-- Ticket title (from first heading) -->
  <span class="flex-1 truncate text-[12px] text-text-secondary">{title}</span>
  
  <!-- Start button (always visible, small) -->
  <button 
    onclick={startWorkstation}
    disabled={starting || atWipLimit}
    title={atWipLimit ? 'WIP limit reached' : 'Start workstation'}
    class="flex items-center gap-1 rounded px-2 py-0.5 text-[10px] font-medium
      transition-colors duration-150
      {atWipLimit 
        ? 'text-text-tertiary cursor-not-allowed' 
        : 'text-accent-primary hover:bg-accent-primary/10 hover:text-accent-primary'}">
    {#if starting}
      <span class="animate-spin text-[10px]">↻</span>
    {:else}
      <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
    {/if}
    Start
  </button>
</div>
```

**Start action flow:**
1. User clicks "Start" on a ready ticket
2. Frontend calls `POST /workstations` with body: `{"ticket_id": "ticket:20260525-slug", "ticket_path": ".loom/tickets/20260525-slug.md"}`
3. Backend creates worktree, launches subprocess, emits state_change event
4. Frontend receives WebSocket event, workstation appears in Active section
5. The ticket disappears from Ready (because it now has an active workstation, or its status changes to "active")
6. Toast: "▶ Started: {ticket-title}"

**WIP limit handling:**
- Read the WIP limit from the footer/config (currently hardcoded "2/3 WIP" display)
- When active count >= WIP limit, the Start buttons show disabled state with tooltip "WIP limit reached"
- The button doesn't disappear - it grays out. The operator can still see what's ready.

### Global Empty State (no ready tickets AND no active workstations)

Replace the current text with:

```
No tickets ready for execution.

Tickets with status "open" in .loom/tickets/ will appear here.
```

This accurately describes what the operator needs to do (shape tickets and set status=open) without referencing non-existent UI.

### Section Labels

Between Ready and Active, use a subtle section divider:

```svelte
{#if activeWorkstations().length > 0}
  <div class="flex items-center px-3 py-1 border-t border-border-subtle">
    <span class="text-[9px] font-medium text-text-tertiary uppercase tracking-widest">Active</span>
  </div>
{/if}
```

Same pattern for the Ready header:

```svelte
<div class="flex items-center justify-between px-3 py-1.5 border-b border-border-subtle cursor-pointer hover:bg-bg-surface-elevated transition-colors" 
  onclick={toggleReadySection}>
  <div class="flex items-center gap-2">
    <span class="text-[9px] font-medium text-text-tertiary uppercase tracking-widest">Ready</span>
    <span class="text-[9px] text-text-tertiary">({readyTickets.length})</span>
  </div>
  <span class="text-[10px] text-text-tertiary">{readyExpanded ? '▾' : '▸'}</span>
</div>
```

### API Call Shape

The existing `POST /workstations` endpoint expects:
```json
{
  "ticket_id": "20260525-mill-spc-jidoka",
  "ticket_path": ".loom/tickets/20260525-mill-spc-jidoka.md"
}
```

Construct `ticket_path` from the record: `record.path` gives the relative path from workspace root.
Construct `ticket_id` from the record: `record.metadata.id.replace('ticket:', '')`.

The backend handles worktree creation, subprocess launch, and WebSocket notification.

### Interaction with Scheduling Agent

When the scheduling agent is enabled (future), the Ready section would show a subtle indicator:
"Auto-scheduling enabled - tickets will be pulled automatically when capacity opens."

But for now, the scheduling agent is code-complete but not visually surfaced. Manual start via the Ready section is the primary flow.

## Acceptance

- ACC-001: Ready tickets (status=open) appear in a "Ready" section at the top of WorkstationList with a "Start" button on each.
  - Evidence: Playwright screenshot showing Ready section with multiple tickets and Start buttons.
  - Audit: verify ready tickets are correctly filtered by status.

- ACC-002: Clicking "Start" calls POST /workstations and the ticket moves from Ready to Active as a running workstation.
  - Evidence: Playwright test: click Start, verify workstation appears in Active section, verify Ready list shrinks by 1.
  - Audit: verify correct API call shape.

- ACC-003: WIP limit is respected - Start buttons are disabled when at capacity.
  - Evidence: Playwright test with WIP=1 and 1 active workstation, verify Start button shows disabled/tooltip.
  - Audit: verify WIP count is read from the correct source.

- ACC-004: Empty state shows accurate guidance text (no references to non-existent UI elements).
  - Evidence: Playwright screenshot of empty state.
  - Audit: verify text is helpful and truthful.

- ACC-005: The overall flow (Ready → Active → Completed) is visible in the WorkstationList as three vertical sections.
  - Evidence: Playwright screenshot showing all three sections populated.
  - Audit: verify visual hierarchy makes the flow direction clear.

- ACC-006: `npm --prefix loom-mill/frontend run build` passes.
  - Evidence: build output.

## Current State

Ready to start. The backend endpoint exists, the WorkstationList component exists, this is adding a new section to it.

## Journal

- 2026-05-25: Created ticket. Source: operator identified that the layout overhaul removed the only way to start workstations and the empty state references non-existent UI.
