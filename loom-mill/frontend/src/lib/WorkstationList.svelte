<script lang="ts">
  import type { LoomRecord, WorkstationState } from './types';
  import WorkstationRow from './WorkstationRow.svelte';

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

  let expanded = $state(false);

  let activeWorkstations = $derived(() => {
    const active: { id: string; record?: LoomRecord; state: WorkstationState }[] = [];
    for (const [id, state] of Object.entries(workstations)) {
      if (state.status === 'running' || state.status === 'paused' || state.status === 'idle' || state.status === 'conflict') {
        const record = records.find(r => r.metadata.id === `ticket:${state.ticket_id}`);
        active.push({ id, record, state });
      }
    }
    return active;
  });

  let completedWorkstations = $derived(() => {
    const completed: { id: string; record?: LoomRecord; state: WorkstationState }[] = [];
    for (const [id, state] of Object.entries(workstations)) {
      if (state.status === 'completed' || state.status === 'stopped') {
        const record = records.find(r => r.metadata.id === `ticket:${state.ticket_id}`);
        completed.push({ id, record, state });
      }
    }
    return completed;
  });

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
    <span class="text-[11px] font-medium text-text-secondary uppercase tracking-wider">Workstations</span>
    <span class="text-[10px] text-text-tertiary">{activeWorkstations().length}/3 WIP</span>
  </div>
  
  <div class="flex-1 overflow-y-auto">
    <!-- Active workstations -->
    {#each activeWorkstations() as ws (ws.id)}
      <WorkstationRow 
        ticketId={ws.id} 
        record={ws.record} 
        workstation={ws.state} 
        selected={selectedId === ws.id} 
        onSelect={() => onSelect(ws.id)} 
      />
    {/each}
    
    <!-- Completed section (collapsible) -->
    {#if completedWorkstations().length > 0}
      <!-- svelte-ignore a11y_click_events_have_key_events -->
      <!-- svelte-ignore a11y_no_static_element_interactions -->
      <div class="flex items-center justify-between px-3 py-1.5 border-t border-border-subtle hover:bg-bg-surface-elevated transition-colors cursor-pointer" onclick={() => expanded = !expanded}>
        <div class="flex items-center gap-2">
          <span class="text-[10px] text-text-tertiary">Completed ({completedWorkstations().length})</span>
          <span class="text-[10px] text-text-tertiary">{expanded ? '▾' : '▸'}</span>
        </div>
        <button class="text-[10px] text-text-tertiary hover:text-text-secondary underline" onclick={clearAllCompleted}>Clear all</button>
      </div>
      {#if expanded}
        {#each completedWorkstations() as ws (ws.id)}
          <WorkstationRow 
            ticketId={ws.id} 
            record={ws.record} 
            workstation={ws.state} 
            selected={selectedId === ws.id} 
            dimmed={true}
            onSelect={() => onSelect(ws.id)} 
          />
        {/each}
      {/if}
    {/if}
  </div>
</div>
