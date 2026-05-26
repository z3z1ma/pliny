# Left Panel: Full Ticket Lifecycle View

ID: ticket:20260525-mill-ticket-lifecycle-panel
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - redesigns the left panel from workstation-centric to ticket-centric; touches WorkstationList, StatusBar, and filtering logic.
Priority: high - the left panel currently shows nothing useful and has a filtering bug.

## Summary

Redesign the left panel from a "Workstations" panel (only Mill-managed execution) into a full ticket lifecycle panel showing ALL active tickets organized by their stage: Ready, In Progress (both Mill-managed and external), Review, and recently Closed. Fix the filtering bug where Ready tickets don't appear despite being counted in the StatusBar. Make StatusBar pills interactive (clicking a pill scrolls/highlights that section).

This resolves two problems:
1. The Ready section shows "No tickets" despite "Shaped 2" in the StatusBar (filtering bug).
2. Tickets executing outside Mill (status=active but no workstation) are invisible. The operator has no way to see which tickets are in flight without checking `.loom/` manually.

Closure claim: The left panel shows the complete ticket lifecycle with all status categories, external execution is visible, the StatusBar pills are interactive, and the filtering bug is fixed.

## Related Records

- `spec:mill-factory-floor` REQ-010 - pipeline showing all lifecycle stages
- `loom-mill/frontend/src/lib/WorkstationList.svelte` - component to redesign
- `loom-mill/frontend/src/lib/StatusBar.svelte` - make pills interactive
- `loom-mill/frontend/src/lib/ReadyTicketRow.svelte` - keep for Ready section
- `loom-mill/frontend/src/lib/WorkstationRow.svelte` - keep for workstation entries
- `loom-mill/frontend/src/lib/ws.svelte.ts` - data source for records + workstations

## Scope

Write:
- `loom-mill/frontend/src/lib/WorkstationList.svelte` - rename concept to TicketLifecyclePanel, restructure sections
- `loom-mill/frontend/src/lib/TicketRow.svelte` (new) - generic row for non-workstation tickets (In Progress external, Review, etc.)
- `loom-mill/frontend/src/lib/StatusBar.svelte` - make pills clickable with scroll-to behavior
- `loom-mill/frontend/src/lib/ReadyTicketRow.svelte` - fix filtering logic
- `loom-mill/frontend/src/App.svelte` - update prop names if component renamed

Non-goals:
- Do NOT rename the file from WorkstationList.svelte if it would break too many imports (rename the visual label only)
- Do NOT implement ticket detail view in the right panel for non-workstation tickets (just show record info)
- Do NOT implement drag-and-drop between sections
- Do NOT show all 58 closed tickets expanded (collapsible, show last 5 max)

## Detailed Design

### Left Panel Structure

The panel header changes from "WORKSTATIONS" to just showing context-appropriate info. The panel body is organized into lifecycle sections, each showing tickets in that stage:

```svelte
<div class="flex flex-col h-full bg-bg-surface">
  <!-- Panel header -->
  <div class="flex items-center justify-between px-3 py-2 border-b border-border-default shrink-0">
    <span class="text-[11px] font-medium text-text-secondary uppercase tracking-wider">Tickets</span>
    <span class="text-[10px] text-text-tertiary">{activeWorkstationCount}/{wipLimit} WIP</span>
  </div>
  
  <div class="flex-1 overflow-y-auto">
    <!-- READY section -->
    {#if readyTickets.length > 0}
      <SectionHeader label="Ready" count={readyTickets.length} />
      {#each readyTickets as record}
        <ReadyTicketRow {record} {atWipLimit} />
      {/each}
    {/if}
    
    <!-- IN PROGRESS section (external - tickets with status=active but NO workstation) -->
    {#if externallyExecuting.length > 0}
      <SectionHeader label="In Progress" count={externallyExecuting.length} badge="external" />
      {#each externallyExecuting as record}
        <TicketRow {record} badge="external" />
      {/each}
    {/if}
    
    <!-- WORKSTATIONS section (Mill-managed execution) -->
    {#if activeWorkstations.length > 0}
      <SectionHeader label="Workstations" count={activeWorkstations.length} badge="{activeWorkstationCount}/{wipLimit}" />
      {#each activeWorkstations as ws}
        <WorkstationRow ... />
      {/each}
    {/if}
    
    <!-- REVIEW section -->
    {#if reviewTickets.length > 0}
      <SectionHeader label="Review" count={reviewTickets.length} />
      {#each reviewTickets as record}
        <TicketRow {record} />
      {/each}
    {/if}
    
    <!-- BLOCKED section -->
    {#if blockedTickets.length > 0}
      <SectionHeader label="Blocked" count={blockedTickets.length} />
      {#each blockedTickets as record}
        <TicketRow {record} statusColor="text-status-error-text" />
      {/each}
    {/if}
    
    <!-- COMPLETED section (collapsible, last 5) -->
    {#if completedWorkstations.length > 0 || recentlyClosed.length > 0}
      <SectionHeader label="Completed" count={completedWorkstations.length + recentlyClosed.length} collapsible={true} />
      ...
    {/if}
    
    <!-- Global empty state (nothing in any section) -->
    {#if totalVisible === 0}
      <EmptyState />
    {/if}
  </div>
</div>
```

### Section Derivations

```typescript
// Ready: status in open/shaped, no active workstation
let readyTickets = $derived(() => {
  const readyStatuses = new Set(['open', 'shaped']);
  return tickets.filter(r => {
    const status = (r.metadata.status || '').toLowerCase();
    const ticketId = (r.metadata.id || '').replace('ticket:', '');
    const hasWorkstation = Object.values(workstations).some(ws => ws.ticket_id === ticketId);
    return readyStatuses.has(status) && !hasWorkstation;
  });
});

// In Progress (external): status=active, no Mill workstation
let externallyExecuting = $derived(() => {
  return tickets.filter(r => {
    const status = (r.metadata.status || '').toLowerCase();
    const ticketId = (r.metadata.id || '').replace('ticket:', '');
    const hasWorkstation = Object.values(workstations).some(ws => ws.ticket_id === ticketId);
    return status === 'active' && !hasWorkstation;
  });
});

// Review: status=review
let reviewTickets = $derived(() => {
  return tickets.filter(r => (r.metadata.status || '').toLowerCase() === 'review');
});

// Blocked: status=blocked
let blockedTickets = $derived(() => {
  return tickets.filter(r => (r.metadata.status || '').toLowerCase() === 'blocked');
});

// Recently closed: status=closed, limit to last 5 by date
let recentlyClosed = $derived(() => {
  return tickets
    .filter(r => (r.metadata.status || '').toLowerCase() === 'closed')
    .sort((a, b) => (b.metadata.updated || '').localeCompare(a.metadata.updated || ''))
    .slice(0, 5);
});
```

### TicketRow.svelte (new)

A generic compact row for tickets that aren't in a workstation. Simpler than WorkstationRow (no timer, no controls):

```svelte
<div class="flex items-center gap-2 px-3 py-2 hover:bg-bg-surface-elevated transition-colors duration-150 cursor-pointer"
  onclick={onSelect}>
  <!-- Status dot -->
  <span class="w-2 h-2 rounded-full shrink-0 {statusColor}"></span>
  
  <!-- Title -->
  <span class="flex-1 truncate text-[12px] text-text-primary">{title}</span>
  
  <!-- Badge (optional: "external", "blocked", etc.) -->
  {#if badge}
    <span class="rounded-full px-1.5 py-0.5 text-[9px] font-medium bg-bg-surface-active text-text-tertiary border border-border-subtle">
      {badge}
    </span>
  {/if}
</div>
```

Status dot colors:
- active (external): pulsing blue dot (it's executing, just not here)
- review: yellow dot
- blocked: red dot
- closed: gray dot

### StatusBar Interaction

Make pills clickable. When clicked, emit a custom event or call a shared scroll function that scrolls the left panel to that section:

```svelte
<button onclick={() => scrollToSection(stage.id)} ...>
  ...
</button>
```

The scroll target: each section header has an `id` attribute (`id="section-ready"`, `id="section-executing"`, etc.) and `scrollIntoView({ behavior: 'smooth' })` is called.

### Filtering Bug Fix

The current bug: the `readyTickets` filter in WorkstationList uses `activeTicketIds()` to exclude tickets that have workstations. But the way it checks ticket IDs against workstation `ticket_id` fields likely has a string format mismatch (e.g., workstation stores `"20260525-mill-spc-jidoka"` but the record ID is `"ticket:20260525-mill-spc-jidoka"`).

The fix: normalize both sides. Always strip `ticket:` prefix before comparing:
```typescript
const ticketId = (r.metadata.id || '').replace(/^ticket:/, '');
const hasWorkstation = Object.values(workstations).some(
  ws => (ws.ticket_id || '').replace(/^ticket:/, '') === ticketId
);
```

### Detail Panel for Non-Workstation Tickets

When a non-workstation ticket is selected in the left panel (e.g., an externally executing ticket or a review ticket), the right DetailPanel should show:
- The ticket title and status
- The raw record content (or at minimum: summary, acceptance criteria, current state from the record)
- No logs/playback tabs (those only apply to workstations)

For this ticket, a minimal approach is fine: show "This ticket is executing externally (not managed by Mill)" with the ticket ID and status. Full record rendering is future work.

### Empty State

When there are truly no tickets in any non-closed state:
```
All caught up.
No tickets are currently in progress, ready, or under review.
```

## Acceptance

- ACC-001: Ready tickets (status=open/shaped) appear in the Ready section with Start buttons. The filtering bug is fixed.
  - Evidence: Playwright screenshot showing Ready section populated with tickets matching StatusBar "Shaped N" count.
  - Audit: verify filter logic normalizes ticket IDs correctly.

- ACC-002: Tickets with status=active but no Mill workstation appear in an "In Progress" section with "external" badge.
  - Evidence: Playwright screenshot showing externally executing ticket with badge.
  - Audit: verify these tickets are NOT shown in Ready or Workstations sections.

- ACC-003: Tickets with status=review appear in a Review section. Tickets with status=blocked appear in a Blocked section.
  - Evidence: Playwright screenshot showing review/blocked sections.

- ACC-004: StatusBar pills are clickable and scroll the left panel to the corresponding section.
  - Evidence: Playwright test clicking "Executing" pill and verifying scroll.

- ACC-005: Recently closed tickets (last 5) appear in a collapsible Completed section, sorted by updated date descending.
  - Evidence: Playwright screenshot showing collapsed/expanded completed section.

- ACC-006: The left panel works as a full ticket lifecycle view - every non-cancelled ticket appears in exactly one section based on its status.
  - Evidence: Playwright full-page screenshot showing multiple sections populated.
  - Audit: verify no ticket appears in multiple sections, verify status→section mapping is correct.

- ACC-007: `npm --prefix loom-mill/frontend run build` passes.
  - Evidence: build output.

## Current State

Ready to start. The filtering bug and the design gap are both well-understood.

## Journal

- 2026-05-25: Created ticket. Source: operator observed that (1) Ready section is empty despite StatusBar showing "Shaped 2" and (2) externally-executing tickets (status=active without Mill workstation) are invisible.
