<script lang="ts">
  import type { WorkstationState } from './types';

  let { ticketId, workstation, compact = false }: { ticketId: string; workstation?: WorkstationState; compact?: boolean } = $props();

  let busy = $state(false);
  let error = $state('');
  let status = $derived(workstation?.status || 'idle');
  let canStart = $derived(status === 'idle' || status === 'stopped' || status === 'completed');
  let canPause = $derived(status === 'running');
  let canStop = $derived(status === 'running' || status === 'paused');
  let canSteer = $derived(status === 'paused');
  const apiBase = `${window.location.protocol}//${window.location.hostname}:8765`;

  async function command(path: string, body?: unknown) {
    busy = true;
    error = '';
    const response = await fetch(`${apiBase}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined
    });
    busy = false;
    if (!response.ok) {
      const data = await response.json();
      error = data.error || 'Command failed';
    }
  }

  function start() {
    return command('/api/workstation/start', { ticket_id: ticketId });
  }

  function pause() {
    return command(`/api/workstation/${ticketId}/pause`);
  }

  function stop() {
    return command(`/api/workstation/${ticketId}/stop`);
  }

  function edit() {
    return command(`/api/workstation/${ticketId}/edit`);
  }

  function resume() {
    return command(`/api/workstation/${ticketId}/resume`);
  }

  function viewHistory() {
    window.dispatchEvent(new CustomEvent('open-playback', { detail: { workstationId: ticketId } }));
  }
</script>

<div class={compact ? "space-y-2" : "space-y-2 rounded border border-border-subtle bg-bg-surface p-2"}>
  {#if !compact}
    <div class="flex items-center justify-between gap-2 text-[11px]">
      <span class="font-medium text-text-secondary">Workstation</span>
      <span class="rounded-full px-1.5 py-0.5 font-medium ring-1 ring-inset
        {status === 'running' ? 'bg-status-success-bg text-status-success-text ring-status-success-border' :
         status === 'paused' ? 'bg-status-warning-bg text-status-warning-text ring-status-warning-border' :
         status === 'stopped' ? 'bg-status-error-bg text-status-error-text ring-status-error-border' :
         status === 'completed' ? 'bg-accent-subtle text-accent-text ring-accent-subtle' :
         'bg-status-neutral-bg text-status-neutral-text ring-status-neutral-border'}">
        {status}
      </span>
    </div>
  {/if}

  {#if workstation?.exit_code !== null && workstation?.exit_code !== undefined}
    <p class="text-[10px] text-text-tertiary">Exit: {workstation.exit_code}</p>
  {/if}

  <div class="grid grid-cols-3 gap-1.5">
    <button type="button" onclick={start} disabled={busy || !canStart} class="rounded bg-bg-surface-active px-2 py-1 text-[10px] font-medium text-text-primary ring-1 ring-border-default hover:bg-bg-surface-hover disabled:cursor-not-allowed disabled:opacity-50 transition-colors">Start</button>
    <button type="button" onclick={pause} disabled={busy || !canPause} class="rounded bg-bg-surface-active px-2 py-1 text-[10px] font-medium text-text-primary ring-1 ring-border-default hover:bg-bg-surface-hover disabled:cursor-not-allowed disabled:opacity-50 transition-colors">Pause</button>
    <button type="button" onclick={stop} disabled={busy || !canStop} class="rounded bg-bg-surface-active px-2 py-1 text-[10px] font-medium text-text-primary ring-1 ring-border-default hover:bg-bg-surface-hover disabled:cursor-not-allowed disabled:opacity-50 transition-colors">Stop</button>
  </div>

  {#if canSteer}
    <div class="grid grid-cols-2 gap-1.5">
      <button type="button" onclick={edit} disabled={busy} class="rounded bg-accent-subtle px-2 py-1 text-[10px] font-medium text-accent-text ring-1 ring-accent-subtle hover:bg-accent-hover hover:text-white disabled:cursor-not-allowed disabled:opacity-50 transition-colors">Edit</button>
      <button type="button" onclick={resume} disabled={busy} class="rounded bg-accent-subtle px-2 py-1 text-[10px] font-medium text-accent-text ring-1 ring-accent-subtle hover:bg-accent-hover hover:text-white disabled:cursor-not-allowed disabled:opacity-50 transition-colors">Resume</button>
    </div>
  {/if}

  {#if !compact}
    <button type="button" onclick={viewHistory} class="w-full rounded bg-bg-surface-active px-2 py-1 text-[10px] font-medium text-text-secondary ring-1 ring-border-default hover:bg-bg-surface-hover hover:text-text-primary transition-colors">
      View History
    </button>
  {/if}

  {#if error}
    <p class="text-[10px] text-status-error-text">{error}</p>
  {/if}
</div>
