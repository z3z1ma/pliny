<script lang="ts">
  import type { WorkstationState } from './types';

  let { ticketId, workstation }: { ticketId: string; workstation?: WorkstationState } = $props();

  let busy = $state(false);
  let error = $state('');
  let status = $derived(workstation?.status || 'idle');
  let canStart = $derived(status === 'idle' || status === 'paused' || status === 'stopped' || status === 'completed');
  let canPause = $derived(status === 'running');
  let canStop = $derived(status === 'running' || status === 'paused');
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
</script>

<div class="space-y-2 rounded-md border border-slate-800 bg-slate-950/60 p-2">
  <div class="flex items-center justify-between gap-2 text-xs">
    <span class="font-medium text-slate-400">Workstation</span>
    <span class="rounded-full px-2 py-0.5 font-medium ring-1 ring-inset
      {status === 'running' ? 'bg-emerald-400/10 text-emerald-300 ring-emerald-400/30' :
       status === 'paused' ? 'bg-amber-400/10 text-amber-300 ring-amber-400/30' :
       status === 'stopped' ? 'bg-rose-400/10 text-rose-300 ring-rose-400/30' :
       status === 'completed' ? 'bg-indigo-400/10 text-indigo-300 ring-indigo-400/30' :
       'bg-slate-400/10 text-slate-300 ring-slate-400/30'}">
      {status}
    </span>
  </div>

  {#if workstation?.exit_code !== null && workstation?.exit_code !== undefined}
    <p class="text-xs text-slate-500">Exit: {workstation.exit_code}</p>
  {/if}

  <div class="grid grid-cols-3 gap-1.5">
    <button type="button" onclick={start} disabled={busy || !canStart} class="rounded bg-emerald-500/15 px-2 py-1 text-xs font-medium text-emerald-300 ring-1 ring-emerald-500/30 hover:bg-emerald-500/25 disabled:cursor-not-allowed disabled:bg-slate-800 disabled:text-slate-500 disabled:ring-slate-700">Start</button>
    <button type="button" onclick={pause} disabled={busy || !canPause} class="rounded bg-amber-500/15 px-2 py-1 text-xs font-medium text-amber-300 ring-1 ring-amber-500/30 hover:bg-amber-500/25 disabled:cursor-not-allowed disabled:bg-slate-800 disabled:text-slate-500 disabled:ring-slate-700">Pause</button>
    <button type="button" onclick={stop} disabled={busy || !canStop} class="rounded bg-rose-500/15 px-2 py-1 text-xs font-medium text-rose-300 ring-1 ring-rose-500/30 hover:bg-rose-500/25 disabled:cursor-not-allowed disabled:bg-slate-800 disabled:text-slate-500 disabled:ring-slate-700">Stop</button>
  </div>

  {#if error}
    <p class="text-xs text-rose-400">{error}</p>
  {/if}
</div>
