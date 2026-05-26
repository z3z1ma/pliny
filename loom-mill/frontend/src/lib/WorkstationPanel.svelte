<script lang="ts">
  import type { WorkstationState, LoomRecord } from './types';
  import WorkstationControls from './WorkstationControls.svelte';

  let { workstationId, workstation, record, selected, onSelect }: { workstationId: string; workstation: WorkstationState; record?: LoomRecord; selected: boolean; onSelect: () => void } = $props();

  let slug = $derived(workstationId.replace('ticket:', ''));
  let status = $derived(workstation.status);
  let iteration = $derived(workstation.iteration_summary?.iteration || workstation.takt?.iteration || 0);
  let taktDuration = $derived(workstation.takt?.duration_seconds || workstation.iteration_summary?.duration_seconds || 0);
  let updated = $derived(record?.metadata?.updated || record?.metadata?.created || '');
  
  // Takt threshold: > 60s is warning, > 120s is error
  let taktColor = $derived(
    taktDuration > 120 ? 'text-status-error-text' :
    taktDuration > 60 ? 'text-status-warning-text' :
    'text-text-tertiary'
  );
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div 
  class="flex flex-col gap-3 rounded-md border p-3 shadow-sm transition-colors cursor-pointer
    {selected ? 'border-accent-primary bg-bg-surface-active' : 'border-border-default bg-bg-surface-elevated hover:border-border-strong'}"
  onclick={onSelect}
>
  <div class="flex items-start justify-between gap-2">
    <span class="text-[12px] font-mono font-medium text-text-primary truncate" title={workstationId}>{slug}</span>
    <span class="inline-flex items-center rounded-full px-1.5 py-0.5 text-[10px] font-medium ring-1 ring-inset
      {status === 'running' ? 'bg-status-success-bg text-status-success-text ring-status-success-border' :
       status === 'paused' ? 'bg-status-warning-bg text-status-warning-text ring-status-warning-border' :
       status === 'stopped' ? 'bg-status-error-bg text-status-error-text ring-status-error-border' :
       status === 'completed' ? 'bg-status-info-bg text-status-info-text ring-status-info-border' :
       'bg-status-neutral-bg text-status-neutral-text ring-status-neutral-border'}">
      {status}
    </span>
  </div>

  <div class="flex items-center justify-between text-[11px]">
    <div class="flex items-center gap-3">
      <span class="text-text-secondary">Iter {iteration}</span>
      {#if taktDuration > 0}
        <span class="flex items-center gap-1 {taktColor}" title="Takt time">
          <svg xmlns="http://www.w3.org/0000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          {taktDuration}s
        </span>
      {/if}
    </div>
    {#if updated}
      <span class="text-text-tertiary">{updated}</span>
    {/if}
  </div>

  <div onclick={(e) => e.stopPropagation()}>
    <WorkstationControls ticketId={workstationId} workstation={workstation} compact={true} />
  </div>
</div>
