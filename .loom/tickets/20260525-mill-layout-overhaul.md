# Layout Overhaul: Master-Detail Control Room

ID: ticket:20260525-mill-layout-overhaul
Type: Ticket
Status: closed
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - large structural refactor touching App.svelte and most layout components; must not break existing WebSocket/state wiring.
Priority: high - all other UI tickets build on this foundation.

## Summary

Replace the current layout (fat kanban top + card grid + dumping-ground sidebar) with a Linear-inspired master-detail control room layout:

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Header: [Logo] [Factory Floor]               [Status Pills] [●Connected] │
├────────────────────────────────┬─────────────────────────────────────────┤
│  Workstation List (left)       │  Detail Panel (right, 70% width)        │
│  ─────────────────────         │  ─────────────────────────────────      │
│  ● ticket-slug     Running 3m  │  [Logs] [Iterations] [Playback]         │
│  ● ticket-slug-2   Running 45s │                                         │
│  ○ ticket-slug-3   Done   8m   │  (selected workstation's content)       │
│                                │                                         │
│  ─── Completed (2) ──────     │                                         │
│  ✓ ticket-slug-4   8m total   │                                         │
│  ✓ ticket-slug-5   12m total  │                                         │
│                                │                                         │
├────────────────────────────────┴─────────────────────────────────────────┤
│ Footer (optional): [Andon: 0 alerts] [Shipped: 3 today] [WIP: 2/3]      │
└──────────────────────────────────────────────────────────────────────────┘
```

Closure claim: The layout fundamentally restructures into a master-detail pattern where the workstation list is the primary navigation (left, ~30% width) and the detail panel (right, ~70%) shows the selected workstation's logs/iterations/playback, with the pipeline reduced to a compact status bar in the header.

## Related Records

- `spec:mill-factory-floor` REQ-010, REQ-011, REQ-012 - pipeline, panels, andon
- `loom-mill/frontend/src/App.svelte` - current layout to replace
- `loom-mill/frontend/src/lib/Pipeline.svelte` - to be replaced with StatusBar
- `loom-mill/frontend/src/lib/WorkstationGrid.svelte` - to be deleted/replaced

## Scope

Write:
- `loom-mill/frontend/src/App.svelte` - completely rewrite layout structure
- `loom-mill/frontend/src/lib/StatusBar.svelte` (new) - compact pipeline summary
- `loom-mill/frontend/src/lib/WorkstationList.svelte` (new) - replaces WorkstationGrid
- `loom-mill/frontend/src/lib/DetailPanel.svelte` (new) - tabbed detail for selected workstation
- `loom-mill/frontend/src/lib/WorkstationRow.svelte` (new) - replaces WorkstationPanel

Delete:
- `loom-mill/frontend/src/lib/Pipeline.svelte` - replaced by StatusBar
- `loom-mill/frontend/src/lib/WorkstationGrid.svelte` - replaced by WorkstationList
- `loom-mill/frontend/src/lib/WorkstationPanel.svelte` - replaced by WorkstationRow

Keep (move into DetailPanel as tabs):
- `loom-mill/frontend/src/lib/LogViewer.svelte` - becomes a tab in DetailPanel
- `loom-mill/frontend/src/lib/Playback.svelte` - becomes a tab in DetailPanel (remove overlay behavior)
- `loom-mill/frontend/src/lib/DiffViewer.svelte` - used inside iterations tab

Remove from always-visible:
- `loom-mill/frontend/src/lib/HarnessConfig.svelte` - move to a settings modal (separate ticket)
- `loom-mill/frontend/src/lib/GitPanel.svelte` - move to footer or settings
- `loom-mill/frontend/src/lib/IterationSummary.svelte` - data merged into iterations tab

Non-goals:
- Do NOT rewrite the WebSocket store (ws.svelte.ts) - keep existing data flow
- Do NOT change backend APIs
- Do NOT implement keyboard shortcuts (separate ticket)
- Do NOT implement the settings modal yet (separate ticket)

## Detailed Design

### Header (48px height)

```svelte
<header class="flex items-center justify-between h-12 border-b border-border-default bg-bg-surface px-4">
  <!-- Left: brand -->
  <div class="flex items-center gap-2">
    <h1 class="text-[13px] font-semibold text-text-primary">Loom Mill</h1>
  </div>
  
  <!-- Center: StatusBar (pipeline pills) -->
  <StatusBar />
  
  <!-- Right: connection + theme + settings gear -->
  <div class="flex items-center gap-3">
    <ConnectionIndicator />
    <ThemeToggle />
    <button title="Settings">⚙</button>
  </div>
</header>
```

### StatusBar.svelte (replaces Pipeline)

A single row of pill-shaped counters showing ticket counts per lifecycle stage. NOT a kanban. NOT scrollable. Takes max 32px height.

```svelte
<div class="flex items-center gap-1.5">
  {#each stages as stage}
    <button class="flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-medium
      transition-colors hover:bg-bg-surface-active
      {stage.count > 0 ? 'text-text-secondary' : 'text-text-tertiary'}">
      <span class="w-1.5 h-1.5 rounded-full {stage.color}"></span>
      <span>{stage.label}</span>
      <span class="tabular-nums">{stage.count}</span>
    </button>
  {/each}
</div>
```

Stages: Shaped (gray dot), Executing (green dot), Evidence (blue dot), Audit (yellow dot), Shipping (purple dot), Closed (dimmed dot). Clicking a pill could later filter the workstation list. For now, just display counts.

### Main Content Area

```svelte
<div class="flex flex-1 overflow-hidden">
  <!-- Left: Workstation List -->
  <WorkstationList class="w-[320px] shrink-0 border-r border-border-default" />
  
  <!-- Right: Detail Panel -->
  <DetailPanel class="flex-1 min-w-0" />
</div>
```

### WorkstationList.svelte (left panel, 320px)

A scrollable list divided into two sections: "Active" and "Completed". Each workstation is a single compact row (WorkstationRow). Active section shows first, Completed section is collapsible.

```svelte
<div class="flex flex-col h-full bg-bg-surface">
  <!-- List header with WIP indicator -->
  <div class="flex items-center justify-between px-3 py-2 border-b border-border-default">
    <span class="text-[11px] font-medium text-text-secondary uppercase tracking-wider">Workstations</span>
    <span class="text-[10px] text-text-tertiary">{activeCount}/{wipLimit} WIP</span>
  </div>
  
  <div class="flex-1 overflow-y-auto">
    <!-- Active workstations -->
    {#each activeWorkstations as ws}
      <WorkstationRow ... selected={selectedId === ws.id} />
    {/each}
    
    <!-- Completed section (collapsible) -->
    {#if completedWorkstations.length > 0}
      <button class="flex items-center gap-2 px-3 py-1.5 w-full text-left border-t border-border-subtle">
        <span class="text-[10px] text-text-tertiary">Completed ({completedWorkstations.length})</span>
        <span class="text-[10px] text-text-tertiary">{expanded ? '▾' : '▸'}</span>
      </button>
      {#if expanded}
        {#each completedWorkstations as ws}
          <WorkstationRow ... dimmed={true} />
        {/each}
      {/if}
    {/if}
  </div>
</div>
```

### WorkstationRow.svelte (replaces WorkstationPanel)

A single compact row (~40px height) showing the essential info. NO buttons visible by default. Actions appear on hover or right-click context menu.

```svelte
<!-- Single row: [status dot] [ticket title] [iteration] [duration] [hover: actions] -->
<div class="group flex items-center gap-2 px-3 py-2 cursor-pointer transition-colors
  {selected ? 'bg-bg-surface-active border-l-2 border-l-accent-primary' : 'hover:bg-bg-surface-elevated'}
  {dimmed ? 'opacity-50' : ''}">
  
  <!-- Status indicator (colored dot) -->
  <span class="w-2 h-2 rounded-full shrink-0 {statusColor}"></span>
  
  <!-- Ticket title (truncated) -->
  <span class="flex-1 truncate text-[12px] font-medium text-text-primary">{ticketTitle}</span>
  
  <!-- Iteration badge -->
  <span class="text-[10px] text-text-tertiary tabular-nums">#{iteration}</span>
  
  <!-- Duration (formatted: "3m 22s" not "202s") -->
  <span class="text-[10px] text-text-tertiary tabular-nums w-14 text-right">{formattedDuration}</span>
  
  <!-- Hover actions (appear on group hover) -->
  <div class="hidden group-hover:flex items-center gap-1">
    {#if status === 'running'}
      <button title="Pause" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary">⏸</button>
      <button title="Stop" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-status-error-text">■</button>
    {/if}
    {#if status === 'completed' || status === 'stopped'}
      <button title="Dismiss" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary">✕</button>
    {/if}
  </div>
</div>
```

Key details for WorkstationRow:
- `ticketTitle`: Extract from the ticket record's first heading (e.g., "Multi-Workstation Engine"), NOT the ws-UUID. Fall back to ticket slug if heading unavailable.
- `statusColor`: running=`bg-status-success-text`, paused=`bg-status-warning-text`, stopped=`bg-status-error-text`, completed=`bg-text-tertiary`
- `formattedDuration`: Convert seconds to human-readable. Under 60s: "45s". Under 3600s: "3m 22s". Over: "1h 2m".
- `iteration`: Show `#3` for iteration 3. Show nothing for iteration 0.
- Selected state: left border accent + slightly elevated background.

### DetailPanel.svelte (right panel, flex-1)

Tabbed content area for the selected workstation. Three tabs: Logs, Iterations, Playback.

```svelte
<div class="flex flex-col h-full">
  {#if !selectedWorkstation}
    <!-- Empty state -->
    <div class="flex flex-1 items-center justify-center">
      <p class="text-[13px] text-text-tertiary">Select a workstation to view details</p>
    </div>
  {:else}
    <!-- Tab bar -->
    <div class="flex items-center gap-0 border-b border-border-default px-4">
      {#each tabs as tab}
        <button class="px-3 py-2 text-[11px] font-medium border-b-2 transition-colors
          {activeTab === tab.id ? 'border-accent-primary text-text-primary' : 'border-transparent text-text-tertiary hover:text-text-secondary'}">
          {tab.label}
        </button>
      {/each}
      
      <!-- Workstation info in tab bar (right side) -->
      <div class="ml-auto flex items-center gap-3 text-[10px] text-text-tertiary">
        <span>Exit: {exitCode ?? '—'}</span>
        <span>Iter {iterationCount}</span>
        <span>{formattedTotalDuration}</span>
      </div>
    </div>
    
    <!-- Tab content -->
    <div class="flex-1 min-h-0 overflow-hidden">
      {#if activeTab === 'logs'}
        <LogViewer logs={selectedWorkstation.output || []} />
      {:else if activeTab === 'iterations'}
        <!-- Iteration list with inline diffs -->
        <IterationsTab workstationId={selectedId} />
      {:else if activeTab === 'playback'}
        <Playback workstationId={selectedId} onClose={() => {}} embedded={true} />
      {/if}
    </div>
  {/if}
</div>
```

Tabs: "Logs" (default when workstation is running), "Iterations" (default when completed), "Playback".

### Footer (optional, 32px)

A compact status footer with key metrics:

```svelte
<footer class="flex items-center justify-between h-8 border-t border-border-default bg-bg-surface px-4 text-[10px] text-text-tertiary">
  <div class="flex items-center gap-4">
    <span>WIP: {active}/{limit}</span>
    <span>Shipped: {shippedCount} today</span>
    <span>Avg iteration: {avgDuration}</span>
  </div>
  <div class="flex items-center gap-4">
    {#if andonCount > 0}
      <span class="text-status-error-text">⚠ {andonCount} alert{andonCount > 1 ? 's' : ''}</span>
    {/if}
  </div>
</footer>
```

## Acceptance

- ACC-001: The layout renders as a master-detail pattern: left workstation list (320px) + right detail panel (remaining width). No kanban/columns. No right sidebar.
  - Evidence: Playwright full-page screenshot showing the master-detail layout.
  - Audit: visual comparison confirms master-detail pattern matches design spec above.

- ACC-002: Pipeline is replaced by a compact StatusBar in the header taking max 32px height. Shows stage counts as pills.
  - Evidence: Playwright screenshot of header showing status pills.
  - Audit: verify old 280px kanban is gone.

- ACC-003: Workstation rows show ticket TITLE (from record heading), not ws-UUID. Each row is max 40px tall.
  - Evidence: Playwright screenshot showing human-readable ticket titles in the list.
  - Audit: verify UUID is not the primary identifier shown.

- ACC-004: Completed workstations appear in a collapsible "Completed (N)" section below active ones.
  - Evidence: Playwright screenshot showing collapsed section with count.
  - Audit: verify completed workstations don't take the same visual weight as active.

- ACC-005: Detail panel shows tabbed content (Logs/Iterations/Playback) for the selected workstation. "Select a workstation" empty state when none selected.
  - Evidence: Playwright screenshot showing tab bar and log content.
  - Audit: verify tabs switch content correctly.

- ACC-006: Duration displays are human-readable ("3m 22s") not raw seconds ("202s" or "395.017s").
  - Evidence: Screenshot showing formatted durations in workstation rows.
  - Audit: verify no raw seconds anywhere in the UI.

- ACC-007: `npm --prefix loom-mill/frontend run build` passes without errors.
  - Evidence: build output.
  - Audit: no regressions.

## Current State

Ready to start. This is the foundation ticket - all other polish tickets depend on this layout being in place.

## Journal

- 2026-05-25: Created ticket. Source: operator feedback on current layout being fundamentally wrong for the control room use case.
