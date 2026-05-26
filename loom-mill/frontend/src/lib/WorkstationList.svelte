<script lang="ts">
  import type { LoomRecord, WorkstationState } from './types';
  import ReadyTicketRow from './ReadyTicketRow.svelte';
  import WorkstationRow from './WorkstationRow.svelte';
  import TicketRow from './TicketRow.svelte';

  const WIP_LIMIT = 3;

  let { 
    records, 
    workstations,
    selectedId,
    onSelect
  }: { 
    records: LoomRecord[]; 
    workstations: Record<string, WorkstationState>;
    selectedId: string | null;
    onSelect: (id: string) => void;
  } = $props();

  let readyExpanded = $state(true);
  let completedExpanded = $state(false);

  let tickets = $derived(records.filter(r => r.metadata.type?.toLowerCase() === 'ticket' || r.path.includes('tickets/')));

  // Helper to check if a ticket has a workstation
  function hasWorkstation(ticketId: string) {
    const normalizedId = ticketId.replace(/^ticket:/, '');
    return Object.values(workstations).some(ws => (ws.ticket_id || '').replace(/^ticket:/, '') === normalizedId);
  }

  let readyTickets = $derived(() => {
    const readyStatuses = new Set(['open', 'shaped', 'todo']);
    return tickets.filter(r => {
      const status = (r.metadata.status || '').toLowerCase();
      const ticketId = (r.metadata.id || r.path.split('/').pop()?.replace(/\.md$/, '') || '');
      return readyStatuses.has(status) && !hasWorkstation(ticketId);
    }).sort((a, b) => {
      const titleA = a.headings[0]?.[1] || a.metadata.id || a.path;
      const titleB = b.headings[0]?.[1] || b.metadata.id || b.path;
      return titleA.localeCompare(titleB);
    });
  });

  let externallyExecuting = $derived(() => {
    return tickets.filter(r => {
      const status = (r.metadata.status || '').toLowerCase();
      const ticketId = (r.metadata.id || r.path.split('/').pop()?.replace(/\.md$/, '') || '');
      return (status === 'active' || status === 'in progress') && !hasWorkstation(ticketId);
    });
  });

  let activeWorkstations = $derived(() => {
    const active: { id: string; record?: LoomRecord; state: WorkstationState }[] = [];
    for (const [id, state] of Object.entries(workstations)) {
      if (state.status === 'running' || state.status === 'paused' || state.status === 'idle' || state.status === 'stopped' || state.status === 'conflict') {
        const record = records.find(r => r.metadata.id === `ticket:${state.ticket_id}`);
        active.push({ id, record, state });
      }
    }
    return active;
  });

  let reviewTickets = $derived(() => {
    return tickets.filter(r => (r.metadata.status || '').toLowerCase() === 'review' || (r.metadata.status || '').toLowerCase() === 'evidence');
  });

  let blockedTickets = $derived(() => {
    return tickets.filter(r => (r.metadata.status || '').toLowerCase() === 'blocked');
  });

  let completedWorkstations = $derived(() => {
    const completed: { id: string; record?: LoomRecord; state: WorkstationState }[] = [];
    for (const [id, state] of Object.entries(workstations)) {
      if (state.status === 'completed' || state.status === 'finished') {
        const record = records.find(r => r.metadata.id === `ticket:${state.ticket_id}`);
        completed.push({ id, record, state });
      }
    }
    return completed;
  });

  let recentlyClosed = $derived(() => {
    return tickets
      .filter(r => {
        const status = (r.metadata.status || '').toLowerCase();
        const ticketId = (r.metadata.id || r.path.split('/').pop()?.replace(/\.md$/, '') || '');
        return (status === 'closed' || status === 'done' || status === 'cancelled') && !hasWorkstation(ticketId);
      })
      .sort((a, b) => (b.metadata.updated || '').localeCompare(a.metadata.updated || ''))
      .slice(0, 5);
  });

  let atWipLimit = $derived(activeWorkstations().length >= WIP_LIMIT);

  let totalVisible = $derived(
    readyTickets().length + 
    externallyExecuting().length + 
    activeWorkstations().length + 
    reviewTickets().length + 
    blockedTickets().length
  );

  async function clearAllCompleted(e: Event) {
    e.stopPropagation();
    const apiBase = `${window.location.protocol}//${window.location.hostname}:8765`;
    const completed = completedWorkstations();
    for (const ws of completed) {
      try {
        await fetch(`${apiBase}/workstations/${ws.id}`, { method: 'DELETE' });
      } catch (err) {
        console.error(`Failed to dismiss workstation ${ws.id}:`, err);
      }
    }
  }
</script>

<div class="flex flex-col h-full bg-bg-surface">
  <!-- List header with WIP indicator -->
  <div class="flex items-center justify-between px-3 py-2 border-b border-border-default shrink-0">
    <span class="text-[11px] font-medium text-text-secondary uppercase tracking-wider">Tickets</span>
    <span class="text-[10px] text-text-tertiary">{activeWorkstations().length}/{WIP_LIMIT} WIP</span>
  </div>
  
  <div class="flex-1 overflow-y-auto">
    <!-- Ready tickets -->
    {#if readyTickets().length > 0}
      <!-- svelte-ignore a11y_click_events_have_key_events -->
      <!-- svelte-ignore a11y_no_static_element_interactions -->
      <div id="section-shaped" class="flex items-center justify-between px-3 py-1.5 border-b border-border-subtle cursor-pointer hover:bg-bg-surface-elevated transition-colors" onclick={() => readyExpanded = !readyExpanded}>
        <div class="flex items-center gap-2">
          <span class="text-[9px] font-medium text-text-tertiary uppercase tracking-widest">Ready</span>
          <span class="text-[9px] text-text-tertiary">({readyTickets().length})</span>
        </div>
        <span class="text-[10px] text-text-tertiary">{readyExpanded ? '▾' : '▸'}</span>
      </div>
      {#if readyExpanded}
        {#each readyTickets() as record (record.path)}
          <ReadyTicketRow {record} {atWipLimit} onSelect={() => onSelect(record.metadata.id || record.path)} />
        {/each}
      {/if}
    {/if}

    <!-- In Progress (external) -->
    {#if externallyExecuting().length > 0}
      <div id="section-executing-external" class="flex items-center justify-between px-3 py-1.5 border-b border-border-subtle">
        <div class="flex items-center gap-2">
          <span class="text-[9px] font-medium text-text-tertiary uppercase tracking-widest">In Progress</span>
          <span class="text-[9px] text-text-tertiary">({externallyExecuting().length})</span>
        </div>
      </div>
      {#each externallyExecuting() as record (record.path)}
        <TicketRow 
          {record} 
          badge="external" 
          statusColor="bg-status-info-text animate-pulse"
          onSelect={() => onSelect(record.metadata.id || record.path)}
        />
      {/each}
    {/if}

    <!-- Active workstations -->
    {#if activeWorkstations().length > 0}
      <div id="section-executing" class="flex items-center justify-between px-3 py-1.5 border-b border-border-subtle">
        <div class="flex items-center gap-2">
          <span class="text-[9px] font-medium text-text-tertiary uppercase tracking-widest">Workstations</span>
          <span class="text-[9px] text-text-tertiary">({activeWorkstations().length})</span>
        </div>
      </div>
      {#each activeWorkstations() as ws (ws.id)}
        <WorkstationRow
          workstationId={ws.id}
          record={ws.record}
          workstation={ws.state}
          selected={selectedId === ws.id}
          dimmed={ws.state.status === 'stopped'}
          onSelect={() => onSelect(ws.id)}
        />
      {/each}
    {/if}

    <!-- Review tickets -->
    {#if reviewTickets().length > 0}
      <div id="section-audit" class="flex items-center justify-between px-3 py-1.5 border-b border-border-subtle">
        <div class="flex items-center gap-2">
          <span class="text-[9px] font-medium text-text-tertiary uppercase tracking-widest">Review</span>
          <span class="text-[9px] text-text-tertiary">({reviewTickets().length})</span>
        </div>
      </div>
      {#each reviewTickets() as record (record.path)}
        <TicketRow 
          {record} 
          statusColor="bg-status-warning-text"
          onSelect={() => onSelect(record.metadata.id || record.path)}
        />
      {/each}
    {/if}

    <!-- Blocked tickets -->
    {#if blockedTickets().length > 0}
      <div id="section-blocked" class="flex items-center justify-between px-3 py-1.5 border-b border-border-subtle">
        <div class="flex items-center gap-2">
          <span class="text-[9px] font-medium text-text-tertiary uppercase tracking-widest">Blocked</span>
          <span class="text-[9px] text-text-tertiary">({blockedTickets().length})</span>
        </div>
      </div>
      {#each blockedTickets() as record (record.path)}
        <TicketRow 
          {record} 
          statusColor="bg-status-error-text"
          onSelect={() => onSelect(record.metadata.id || record.path)}
        />
      {/each}
    {/if}
    
    <!-- Completed section (collapsible) -->
    {#if completedWorkstations().length > 0 || recentlyClosed().length > 0}
      <!-- svelte-ignore a11y_click_events_have_key_events -->
      <!-- svelte-ignore a11y_no_static_element_interactions -->
      <div id="section-shipping" class="flex items-center justify-between px-3 py-1.5 border-t border-border-subtle hover:bg-bg-surface-elevated transition-colors cursor-pointer" onclick={() => completedExpanded = !completedExpanded}>
        <div class="flex items-center gap-2">
          <span class="text-[10px] text-text-tertiary">Completed ({completedWorkstations().length + recentlyClosed().length})</span>
          <span class="text-[10px] text-text-tertiary">{completedExpanded ? '▾' : '▸'}</span>
        </div>
        {#if completedWorkstations().length > 0}
          <button class="text-[10px] text-text-tertiary hover:text-text-secondary underline" onclick={clearAllCompleted}>Clear workstations</button>
        {/if}
      </div>
      {#if completedExpanded}
        {#each completedWorkstations() as ws (ws.id)}
          <WorkstationRow 
            workstationId={ws.id}
            record={ws.record} 
            workstation={ws.state} 
            selected={selectedId === ws.id} 
            dimmed={true}
            onSelect={() => onSelect(ws.id)} 
          />
        {/each}
        {#each recentlyClosed() as record (record.path)}
          <TicketRow 
            {record} 
            statusColor="bg-text-tertiary opacity-50"
            onSelect={() => onSelect(record.metadata.id || record.path)}
          />
        {/each}
      {/if}
    {/if}

    <!-- Global empty state -->
    {#if totalVisible === 0 && completedWorkstations().length === 0 && recentlyClosed().length === 0}
      <div class="m-4 flex items-center justify-center rounded-lg border border-dashed border-border-default p-6 text-center">
        <p class="text-[12px] text-text-tertiary">All caught up.</p>
        <p class="mt-1 text-[11px] text-text-tertiary opacity-70">No tickets are currently in progress, ready, or under review.</p>
      </div>
    {/if}
  </div>
</div>
