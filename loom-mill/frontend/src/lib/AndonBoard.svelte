<script lang="ts">
  import type { LoomRecord, WorkstationState, AndonEventPayload } from './types';
  import { formatRelativeTime } from './utils';
  import { apiUrl } from './api';
  import { store } from './ws.svelte.ts';

  let { records, workstations, andonEvents }: { 
    records: LoomRecord[]; 
    workstations: Record<string, WorkstationState>;
    andonEvents: Record<string, AndonEventPayload[]>;
  } = $props();

  let busy = $state<Record<string, boolean>>({});

  let activeAlerts = $derived(() => {
    const alerts: Array<{
      workstationId: string;
      ticketId: string;
      record: LoomRecord | undefined;
      event: AndonEventPayload;
      isActive: boolean;
    }> = [];

    for (const [workstationId, events] of Object.entries(andonEvents)) {
      if (!events.length) continue;
      
      const workstation = workstations[workstationId];
      // Only show if workstation is still paused/stopped or has active andon state
      const isActive = workstation?.status === 'paused' || workstation?.status === 'stopped' || workstation?.andon?.active;
      
      // Get the most recent event
      const latestEvent = events[events.length - 1];
      
      const record = records.find(r => r.metadata.id?.replace('ticket:', '') === workstationId);
      
      alerts.push({
        workstationId,
        ticketId: workstationId,
        record,
        event: latestEvent,
        isActive: !!isActive
      });
    }

    return alerts.sort((a, b) => new Date(b.event.timestamp).getTime() - new Date(a.event.timestamp).getTime());
  });

  let error = $state<Record<string, string>>({});

  async function acknowledge(ticketId: string) {
    busy[ticketId] = true;
    error[ticketId] = '';
    try {
      const response = await fetch(apiUrl(`/api/workstation/${ticketId}/acknowledge-andon`), { method: 'POST' });
      if (!response.ok) {
        let msg = `${response.status}: ${response.statusText}`;
        try {
          const body = await response.json();
          if (body.error) msg = body.error;
        } catch (e) {}
        throw new Error(msg);
      }
    } catch (err) {
      error[ticketId] = err instanceof Error ? err.message : 'Failed to acknowledge';
      setTimeout(() => error[ticketId] = '', 5000);
    } finally {
      busy[ticketId] = false;
    }
  }

  function clearResolved() {
    for (const alert of activeAlerts()) {
      if (!alert.isActive) {
        store.clearAndonEvents(alert.workstationId);
      }
    }
  }
</script>

<div class="flex flex-col gap-3 rounded-lg border border-border-default bg-bg-surface p-4">
  <div class="flex items-center justify-between">
    <h2 class="text-sm font-semibold text-text-primary">Andon Board</h2>
    {#if activeAlerts().some(a => !a.isActive)}
      <button 
        onclick={clearResolved}
        class="text-[11px] font-medium text-text-secondary hover:text-text-primary transition-colors"
      >
        Clear resolved
      </button>
    {/if}
  </div>

  {#if activeAlerts().length === 0}
    <div class="flex h-20 items-center justify-center rounded border border-dashed border-border-subtle">
      <div class="flex items-center gap-2 text-text-tertiary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-status-success-text"><path d="M20 6 9 17l-5-5"/></svg>
        <p class="text-xs">All clear.</p>
      </div>
    </div>
  {:else}
    <div class="flex flex-col gap-3 max-h-64 overflow-y-auto pr-1">
      {#each activeAlerts() as alert (alert.workstationId)}
        <div class="flex flex-col gap-2 rounded-md border p-3 {alert.event.signal === 'stop' ? 'border-status-error-border bg-status-error-bg/30' : 'border-status-warning-border bg-status-warning-bg/30'} {alert.isActive ? '' : 'opacity-60'}">
          <div class="flex items-start justify-between gap-2">
            <div class="flex items-center gap-2">
              <span class="badge {alert.event.signal === 'stop' ? 'bg-status-error-text text-white' : 'bg-status-warning-text text-white'}">
                {alert.event.signal}
              </span>
              <span class="text-xs font-medium text-text-primary">
                {alert.record?.headings[0]?.[1] || alert.ticketId}
              </span>
            </div>
            <span class="text-[10px] text-text-tertiary" title={alert.event.timestamp}>
              {formatRelativeTime(alert.event.timestamp)}
            </span>
          </div>
          
          <p class="text-xs text-text-secondary">{alert.event.reasoning}</p>
          
          {#if alert.event.patterns?.length}
            <div class="flex flex-wrap gap-1 mt-1">
              {#each alert.event.patterns as pattern}
                <span class="rounded bg-bg-surface-active px-1.5 py-0.5 text-[10px] text-text-secondary border border-border-subtle">
                  {pattern}
                </span>
              {/each}
            </div>
          {/if}

          <div class="mt-2 flex items-center justify-between border-t border-border-subtle pt-2">
            <button 
              class="text-[11px] font-medium text-text-secondary hover:text-text-primary transition-colors"
              onclick={() => {
                const event = new CustomEvent('open-playback', { detail: { workstationId: alert.workstationId, source: 'andon' } });
                window.dispatchEvent(event);
              }}
            >
              View Workstation
            </button>
            
            {#if alert.isActive && alert.event.signal === 'stop'}
              <div class="flex items-center gap-2">
                {#if error[alert.ticketId]}
                  <span class="text-[10px] text-status-error-text">{error[alert.ticketId]}</span>
                {/if}
                <button 
                  type="button" 
                  onclick={() => acknowledge(alert.ticketId)} 
                  disabled={busy[alert.ticketId]} 
                  class="rounded bg-status-error-text px-2 py-1 text-[10px] font-medium text-white hover:opacity-90 disabled:opacity-50 transition-opacity"
                >
                  Acknowledge
                </button>
              </div>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>