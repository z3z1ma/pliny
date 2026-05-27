<script lang="ts">
  import type { LoomRecord, WorkstationState } from './types';
  import ReadyTicketRow from './ReadyTicketRow.svelte';
  import WorkstationRow from './WorkstationRow.svelte';
  import TicketRow from './TicketRow.svelte';
  import { apiUrl } from './api';
  import { fly, fade } from 'svelte/transition';
  import { flip } from 'svelte/animate';

  const WIP_LIMIT = 3;

  let { 
    active = true,
    records, 
    workstations,
    selectedId,
    onSelect
  }: { 
    active?: boolean;
    records: LoomRecord[]; 
    workstations: Record<string, WorkstationState>;
    selectedId: string | null;
    onSelect: (id: string) => void;
  } = $props();

  let readyExpanded = $state(true);
  let completedExpanded = $state(false);
  let searchQuery = $state('');

  let tickets = $derived(records.filter(r => r.metadata.type?.toLowerCase() === 'ticket' || r.path.includes('tickets/')));

  // Helper to check if a ticket has a workstation
  function hasWorkstation(ticketId: string) {
    const normalizedId = ticketId.replace(/^ticket:/, '');
    return Object.values(workstations).some(ws => (ws.ticket_id || '').replace(/^ticket:/, '') === normalizedId);
  }

  function matchesSearch(record?: LoomRecord, wsState?: WorkstationState): boolean {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    
    if (record) {
      const title = (record.headings[0]?.[1] || '').toLowerCase();
      const id = (record.metadata.id || record.path).toLowerCase();
      const status = (record.metadata.status || '').toLowerCase();
      if (title.includes(q) || id.includes(q) || status.includes(q)) return true;
    }
    
    if (wsState) {
      const slug = (wsState.ticket_slug || '').toLowerCase();
      const id = (wsState.ticket_id || '').toLowerCase();
      const status = (wsState.status || '').toLowerCase();
      if (slug.includes(q) || id.includes(q) || status.includes(q)) return true;
    }
    
    return false;
  }

  let readyTickets = $derived(() => {
    const readyStatuses = new Set(['open', 'shaped', 'todo']);
    return tickets.filter(r => {
      const status = (r.metadata.status || '').toLowerCase();
      const ticketId = (r.metadata.id || r.path.split('/').pop()?.replace(/\.md$/, '') || '');
      return readyStatuses.has(status) && !hasWorkstation(ticketId) && matchesSearch(r);
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
      return (status === 'active' || status === 'in progress') && !hasWorkstation(ticketId) && matchesSearch(r);
    });
  });

  let activeWorkstations = $derived(() => {
    const active: { id: string; record?: LoomRecord; state: WorkstationState }[] = [];
    for (const [id, state] of Object.entries(workstations)) {
      if (state.status === 'running' || state.status === 'paused' || state.status === 'idle' || state.status === 'stopped' || state.status === 'conflict') {
        const record = records.find(r => r.metadata.id === `ticket:${state.ticket_id}`);
        if (matchesSearch(record, state)) {
          active.push({ id, record, state });
        }
      }
    }
    return active;
  });

  let reviewTickets = $derived(() => {
    return tickets.filter(r => ((r.metadata.status || '').toLowerCase() === 'review' || (r.metadata.status || '').toLowerCase() === 'evidence') && matchesSearch(r));
  });

  let blockedTickets = $derived(() => {
    return tickets.filter(r => (r.metadata.status || '').toLowerCase() === 'blocked' && matchesSearch(r));
  });

  let completedWorkstations = $derived(() => {
    const completed: { id: string; record?: LoomRecord; state: WorkstationState }[] = [];
    for (const [id, state] of Object.entries(workstations)) {
      if (state.status === 'completed' || state.status === 'finished') {
        const record = records.find(r => r.metadata.id === `ticket:${state.ticket_id}`);
        if (matchesSearch(record, state)) {
          completed.push({ id, record, state });
        }
      }
    }
    return completed;
  });

  let recentlyClosed = $derived(() => {
    return tickets
      .filter(r => {
        const status = (r.metadata.status || '').toLowerCase();
        const ticketId = (r.metadata.id || r.path.split('/').pop()?.replace(/\.md$/, '') || '');
        return (status === 'closed' || status === 'done' || status === 'cancelled') && !hasWorkstation(ticketId) && matchesSearch(r);
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

  let allListItems = $derived(() => {
    const items: { id: string, type: string, record?: LoomRecord, ws?: WorkstationState }[] = [];
    if (readyExpanded) {
      for (const r of readyTickets()) items.push({ id: r.metadata.id || r.path, type: 'ready', record: r });
    }
    for (const r of externallyExecuting()) items.push({ id: r.metadata.id || r.path, type: 'external', record: r });
    for (const ws of activeWorkstations()) items.push({ id: ws.id, type: 'active', record: ws.record, ws: ws.state });
    for (const r of reviewTickets()) items.push({ id: r.metadata.id || r.path, type: 'review', record: r });
    for (const r of blockedTickets()) items.push({ id: r.metadata.id || r.path, type: 'blocked', record: r });
    if (completedExpanded) {
      for (const ws of completedWorkstations()) items.push({ id: ws.id, type: 'completed', record: ws.record, ws: ws.state });
      for (const r of recentlyClosed()) items.push({ id: r.metadata.id || r.path, type: 'closed', record: r });
    }
    return items;
  });

  let focusedIndex = $state(-1);

  function handleKeydown(e: KeyboardEvent) {
    if (!active) return;

    // Don't interfere if user is typing in an input
    if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;

    const items = allListItems();
    if (items.length === 0) return;

    if (e.key === 'j') {
      e.preventDefault();
      focusedIndex = focusedIndex < items.length - 1 ? focusedIndex + 1 : focusedIndex;
      scrollToFocused();
    } else if (e.key === 'k') {
      e.preventDefault();
      focusedIndex = focusedIndex > 0 ? focusedIndex - 1 : 0;
      scrollToFocused();
    } else if (e.key === 'Enter') {
      if (focusedIndex >= 0 && focusedIndex < items.length) {
        e.preventDefault();
        onSelect(items[focusedIndex].id);
      }
    } else if (e.key === 'Escape') {
      e.preventDefault();
      onSelect(''); // Deselect
    }
  }

  function scrollToFocused() {
    setTimeout(() => {
      const el = document.getElementById(`list-item-${focusedIndex}`);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    }, 0);
  }

  // Reset focus when list changes significantly
  $effect(() => {
    allListItems();
    if (focusedIndex >= allListItems().length) {
      focusedIndex = Math.max(0, allListItems().length - 1);
    }
  });

  async function clearAllCompleted(e: Event) {
    e.stopPropagation();
    const completed = completedWorkstations();
    for (const ws of completed) {
      try {
        await fetch(apiUrl(`/workstations/${ws.id}`), { method: 'DELETE' });
      } catch (err) {
        console.error(`Failed to dismiss workstation ${ws.id}:`, err);
      }
    }
  }
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="flex flex-col h-full bg-bg-surface">
  <!-- List header with WIP indicator -->
  <div class="flex items-center justify-between px-3 py-2 border-b border-border-default shrink-0">
    <span class="text-[11px] font-medium text-text-secondary uppercase tracking-wider">Tickets</span>
    <span class="text-[10px] text-text-tertiary">{activeWorkstations().length}/{WIP_LIMIT} WIP</span>
  </div>
  
  <div class="px-3 py-2 border-b border-border-subtle shrink-0">
    <input 
      type="text"
      placeholder="Filter tickets..."
      bind:value={searchQuery}
      class="w-full px-2 py-1 text-[11px] rounded border border-border-default bg-bg-primary text-text-primary placeholder:text-text-tertiary focus:outline-none focus:border-accent-primary"
    />
  </div>
  
  <div class="flex-1 overflow-y-auto" role="listbox" aria-label="Ticket list">
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
          {@const idx = allListItems().findIndex(i => i.id === (record.metadata.id || record.path))}
          <div id="list-item-{idx}">
            <ReadyTicketRow {record} {atWipLimit} focused={focusedIndex === idx} selected={selectedId === (record.metadata.id || record.path)} onSelect={() => onSelect(record.metadata.id || record.path)} />
          </div>
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
        {@const idx = allListItems().findIndex(i => i.id === (record.metadata.id || record.path))}
        <div id="list-item-{idx}">
          <TicketRow 
            {record} 
            badge="external" 
            statusColor="bg-status-info-text animate-pulse"
            focused={focusedIndex === idx}
            selected={selectedId === (record.metadata.id || record.path)}
            onSelect={() => onSelect(record.metadata.id || record.path)}
          />
        </div>
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
        {@const idx = allListItems().findIndex(i => i.id === ws.id)}
        <div id="list-item-{idx}">
          <WorkstationRow
            workstationId={ws.id}
            record={ws.record}
            workstation={ws.state}
            selected={selectedId === ws.id}
            focused={focusedIndex === idx}
            dimmed={ws.state.status === 'stopped'}
            onSelect={() => onSelect(ws.id)}
          />
        </div>
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
        {@const idx = allListItems().findIndex(i => i.id === (record.metadata.id || record.path))}
        <div id="list-item-{idx}">
          <TicketRow 
            {record} 
            statusColor="bg-status-warning-text"
            focused={focusedIndex === idx}
            selected={selectedId === (record.metadata.id || record.path)}
            onSelect={() => onSelect(record.metadata.id || record.path)}
          />
        </div>
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
        {@const idx = allListItems().findIndex(i => i.id === (record.metadata.id || record.path))}
        <div id="list-item-{idx}">
          <TicketRow 
            {record} 
            statusColor="bg-status-error-text"
            focused={focusedIndex === idx}
            selected={selectedId === (record.metadata.id || record.path)}
            onSelect={() => onSelect(record.metadata.id || record.path)}
          />
        </div>
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
          {@const idx = allListItems().findIndex(i => i.id === ws.id)}
          <div id="list-item-{idx}">
            <WorkstationRow 
              workstationId={ws.id}
              record={ws.record} 
              workstation={ws.state} 
              selected={selectedId === ws.id} 
              focused={focusedIndex === idx}
              dimmed={true}
              onSelect={() => onSelect(ws.id)} 
            />
          </div>
        {/each}
        {#each recentlyClosed() as record (record.path)}
          {@const idx = allListItems().findIndex(i => i.id === (record.metadata.id || record.path))}
          <div id="list-item-{idx}">
            <TicketRow 
              {record} 
              statusColor="bg-text-tertiary opacity-50"
              focused={focusedIndex === idx}
              selected={selectedId === (record.metadata.id || record.path)}
              onSelect={() => onSelect(record.metadata.id || record.path)}
            />
          </div>
        {/each}
      {/if}
    {/if}

    <!-- Global empty state -->
    {#if totalVisible === 0 && completedWorkstations().length === 0 && recentlyClosed().length === 0}
      {#if searchQuery}
        <div class="m-4 flex flex-col items-center justify-center rounded-lg border border-dashed border-border-default p-6 text-center">
          <p class="text-[12px] text-text-tertiary">No matching tickets.</p>
          <button class="mt-2 text-[11px] text-accent-primary hover:underline" onclick={() => searchQuery = ''}>Clear filter</button>
        </div>
      {:else}
        <div class="m-4 flex items-center justify-center rounded-lg border border-dashed border-border-default p-6 text-center">
          <p class="text-[12px] text-text-tertiary">All caught up.</p>
          <p class="mt-1 text-[11px] text-text-tertiary opacity-70">No tickets are currently in progress, ready, or under review.</p>
        </div>
      {/if}
    {/if}
  </div>
</div>
