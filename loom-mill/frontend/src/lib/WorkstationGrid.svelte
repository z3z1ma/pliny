<script lang="ts">
  import type { WorkstationState, LoomRecord } from './types';
  import WorkstationPanel from './WorkstationPanel.svelte';
  import LogViewer from './LogViewer.svelte';

  let { workstations, records = [] }: { workstations: Record<string, WorkstationState>, records?: LoomRecord[] } = $props();

  let workstationIds = $derived(Object.keys(workstations));
  let selectedId = $state<string | null>(null);

  // Auto-select first workstation if none selected
  $effect(() => {
    if (workstationIds.length > 0 && (!selectedId || !workstations[selectedId])) {
      selectedId = workstationIds[0];
    } else if (workstationIds.length === 0) {
      selectedId = null;
    }
  });
</script>

<div class="flex h-full gap-4">
  {#if workstationIds.length === 0}
    <div class="flex flex-1 items-center justify-center rounded-lg border border-dashed border-border-strong bg-bg-surface">
      <div class="text-center">
        <p class="text-sm font-medium text-text-secondary">No active workstations</p>
        <p class="mt-1 text-[11px] text-text-tertiary">Start a workstation from the pipeline to see it here.</p>
      </div>
    </div>
  {:else}
    <div class="flex w-80 shrink-0 flex-col gap-3 overflow-y-auto pr-1">
      {#each workstationIds as id (id)}
        <WorkstationPanel 
          workstationId={id} 
          workstation={workstations[id]} 
          record={records.find(r => r.metadata.id === `ticket:${id.replace('ticket:', '')}` || r.metadata.id === id)}
          selected={selectedId === id}
          onSelect={() => selectedId = id}
        />
      {/each}
    </div>
    <div class="flex-1 min-w-0">
      {#if selectedId && workstations[selectedId]}
        <LogViewer logs={workstations[selectedId].output || []} />
      {/if}
    </div>
  {/if}
</div>
