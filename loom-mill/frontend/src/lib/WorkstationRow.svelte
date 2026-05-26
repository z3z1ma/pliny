<script lang="ts">
  import type { LoomRecord, WorkstationState } from './types';
  import { formatDuration } from './utils';
  import { apiUrl } from './api';

  let { 
    workstationId,
    record, 
    workstation, 
    selected = false, 
    dimmed = false,
    onSelect
  }: { 
    workstationId: string;
    record: LoomRecord | undefined;
    workstation: WorkstationState | undefined;
    selected?: boolean;
    dimmed?: boolean;
    onSelect: () => void;
  } = $props();

  let ticketTitle = $derived(() => {
    if (record && record.headings && record.headings.length > 0) {
      return record.headings[0][1];
    }
    return workstation?.ticket_id || workstationId;
  });

  let status = $derived(workstation?.status || 'idle');
  let hasError = $derived(!record);

  let statusColor = $derived(() => {
    switch (status) {
      case 'running': return 'bg-status-success-text animate-pulse-dot';
      case 'paused': return 'bg-status-warning-text';
      case 'stopped': return 'bg-status-error-text';
      case 'completed': return 'bg-text-tertiary';
      case 'conflict': return 'bg-status-error-text animate-pulse';
      default: return 'bg-text-tertiary opacity-50';
    }
  });

  let iteration = $derived(workstation?.iteration_summary?.iteration ?? workstation?.takt?.iteration ?? 0);

  let baseDurationSeconds = $derived(workstation?.takt?.duration_seconds ?? workstation?.iteration_summary?.duration_seconds ?? 0);
  
  let liveDuration = $state(0);
  let timer: ReturnType<typeof setInterval>;

  $effect(() => {
    liveDuration = baseDurationSeconds;
    if (status === 'running') {
      clearInterval(timer);
      timer = setInterval(() => {
        liveDuration += 1;
      }, 1000);
    } else {
      clearInterval(timer);
    }
    return () => clearInterval(timer);
  });

  let formattedDuration = $derived(() => {
    return formatDuration(liveDuration);
  });

  async function handleAction(action: string, e: Event) {
    e.stopPropagation();
    try {
      if (action === 'dismiss') {
        await fetch(apiUrl(`/workstations/${workstationId}`), { method: 'DELETE' });
      } else if (action === 'stop') {
        await fetch(apiUrl(`/api/workstation/${workstationId}/stop`), { method: 'POST' });
      } else if (action === 'resolve' || action === 'abort') {
        await fetch(apiUrl(`/shipping/${workstationId}/${action}`), { method: 'POST' });
      } else {
        await fetch(apiUrl(`/workstations/${workstationId}/${action}`), { method: 'POST' });
      }
    } catch (err) {
      console.error(`Failed to ${action} workstation:`, err);
    }
  }
</script>

<!-- Single row: [status dot] [ticket title] [iteration] [duration] [hover: actions] -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="group flex flex-col px-3 py-2 cursor-pointer transition-all duration-150 ease-out
  {selected ? 'bg-bg-surface-active border-l-2 border-l-accent-primary' : 'border-l-2 border-l-transparent hover:bg-bg-surface-elevated'}
  {status === 'conflict' ? '!border-l-status-error-text' : ''}
  {dimmed ? 'opacity-60' : ''}"
  onclick={onSelect}>
  
  <div class="flex items-center gap-2">
    <!-- Status indicator (colored dot) -->
    <span class="w-2 h-2 rounded-full shrink-0 {statusColor()}"></span>
    
    <!-- Ticket title (truncated) -->
    <span class="flex-1 truncate text-[12px] font-medium {status === 'conflict' ? 'text-status-error-text' : 'text-text-primary'}">{ticketTitle()}</span>
    
    <!-- Iteration badge -->
    {#if iteration > 0}
      <span class="text-[10px] text-text-tertiary tabular-nums">#{iteration}</span>
    {/if}
    
    <!-- Duration (formatted: "3m 22s" not "202s") -->
    <span class="text-[10px] text-text-tertiary tabular-nums w-14 text-right">{formattedDuration()}</span>
    
    <!-- Hover actions (appear on group hover) -->
    <div class="hidden group-hover:flex items-center gap-1">
      {#if hasError}
        <button title="Dismiss" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary" onclick={(e) => handleAction('dismiss', e)}>✕</button>
      {:else if status === 'running'}
        <button title="Pause" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary" onclick={(e) => handleAction('pause', e)}>⏸</button>
        <button title="Stop" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-status-error-text" onclick={(e) => handleAction('stop', e)}>■</button>
      {:else if status === 'paused'}
        <button title="Resume" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary" onclick={(e) => handleAction('resume', e)}>▶</button>
        <button title="Stop" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-status-error-text" onclick={(e) => handleAction('stop', e)}>■</button>
      {:else if status === 'stopped'}
        <button title="Resume" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary" onclick={(e) => handleAction('resume', e)}>▶</button>
        <button title="Dismiss" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary" onclick={(e) => handleAction('dismiss', e)}>✕</button>
      {:else if status === 'completed' || status === 'finished'}
        <button title="View Summary" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary" onclick={(e) => { e.stopPropagation(); onSelect(); }}>▣</button>
        <button title="Dismiss" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary" onclick={(e) => handleAction('dismiss', e)}>✕</button>
      {:else if status === 'conflict'}
        <button title="Resolve" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary" onclick={(e) => handleAction('resolve', e)}>✓</button>
        <button title="Abort" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-status-error-text" onclick={(e) => handleAction('abort', e)}>✕</button>
      {/if}
    </div>
  </div>

  {#if !record}
    <div class="text-[10px] text-status-error-text mt-1 ml-4 truncate" title="Ticket not found">Ticket not found</div>
  {/if}
</div>
