<script lang="ts">
  import type { LoomRecord, WorkstationState } from './types';
  import { formatDuration } from './utils';
  import { apiUrl } from './api';

  let { 
    workstationId,
    record, 
    workstation, 
    selected = false, 
    focused = false,
    dimmed = false,
    onSelect
  }: { 
    workstationId: string;
    record: LoomRecord | undefined;
    workstation: WorkstationState | undefined;
    selected?: boolean;
    focused?: boolean;
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

  let error = $state('');
  let busy = $state(false);

  async function handleAction(action: string, e: Event) {
    e.stopPropagation();
    if (busy) return;
    busy = true;
    error = '';
    try {
      let response;
      if (action === 'dismiss') {
        response = await fetch(apiUrl(`/workstations/${workstationId}`), { method: 'DELETE' });
      } else if (action === 'stop') {
        response = await fetch(apiUrl(`/api/workstation/${workstationId}/stop`), { method: 'POST' });
      } else if (action === 'resolve' || action === 'abort') {
        response = await fetch(apiUrl(`/shipping/${workstationId}/${action}`), { method: 'POST' });
      } else {
        response = await fetch(apiUrl(`/workstations/${workstationId}/${action}`), { method: 'POST' });
      }
      
      if (!response.ok) {
        let msg = `${response.status}: ${response.statusText}`;
        try {
          const body = await response.json();
          if (body.error) msg = body.error;
        } catch (e) {}
        throw new Error(msg);
      }
    } catch (err) {
      error = err instanceof Error ? err.message : `Failed to ${action}`;
      setTimeout(() => error = '', 5000);
    } finally {
      busy = false;
    }
  }
</script>

<!-- Single row: [status dot] [ticket title] [iteration] [duration] [hover: actions] -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div role="option" tabindex="-1" aria-selected={selected} class="group flex flex-col px-3 py-2 cursor-pointer transition-all duration-150 ease-out
  {selected ? 'bg-bg-surface-active border-l-2 border-l-accent-primary' : 'border-l-2 border-l-transparent hover:bg-bg-surface-elevated'}
  {focused ? 'outline outline-2 outline-accent-primary -outline-offset-2' : ''}
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
        <button disabled={busy} title="Dismiss" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary disabled:opacity-50" onclick={(e) => handleAction('dismiss', e)}>✕</button>
      {:else if status === 'running'}
        <button disabled={busy} title="Pause" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary disabled:opacity-50" onclick={(e) => handleAction('pause', e)}>⏸</button>
        <button disabled={busy} title="Stop" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-status-error-text disabled:opacity-50" onclick={(e) => handleAction('stop', e)}>■</button>
      {:else if status === 'paused'}
        <button disabled={busy} title="Resume" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary disabled:opacity-50" onclick={(e) => handleAction('resume', e)}>▶</button>
        <button disabled={busy} title="Stop" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-status-error-text disabled:opacity-50" onclick={(e) => handleAction('stop', e)}>■</button>
      {:else if status === 'stopped'}
        <button disabled={busy} title="Resume" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary disabled:opacity-50" onclick={(e) => handleAction('resume', e)}>▶</button>
        <button disabled={busy} title="Dismiss" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary disabled:opacity-50" onclick={(e) => handleAction('dismiss', e)}>✕</button>
      {:else if status === 'completed' || status === 'finished'}
        <button disabled={busy} title="View Summary" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary disabled:opacity-50" onclick={(e) => { e.stopPropagation(); onSelect(); }}>▣</button>
        <button disabled={busy} title="Dismiss" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary disabled:opacity-50" onclick={(e) => handleAction('dismiss', e)}>✕</button>
      {:else if status === 'conflict'}
        <button disabled={busy} title="Resolve" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary disabled:opacity-50" onclick={(e) => handleAction('resolve', e)}>✓</button>
        <button disabled={busy} title="Abort" class="p-0.5 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-status-error-text disabled:opacity-50" onclick={(e) => handleAction('abort', e)}>✕</button>
      {/if}
    </div>
  </div>

  {#if error}
    <div class="text-[10px] text-status-error-text mt-1 ml-4 truncate" title={error}>{error}</div>
  {:else if !record}
    <div class="text-[10px] text-status-error-text mt-1 ml-4 truncate" title="Ticket not found">Ticket not found</div>
  {/if}
</div>
