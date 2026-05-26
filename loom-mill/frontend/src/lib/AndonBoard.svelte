<script lang="ts">
  import type { LoomRecord, WorkstationState, AndonEventPayload } from './types';

  let { records, workstations, andonEvents }: { 
    records: LoomRecord[]; 
    workstations: Record<string, WorkstationState>;
    andonEvents: Record<string, AndonEventPayload[]>;
  } = $props();

  const apiBase = `${window.location.protocol}//${window.location.hostname}:8765`;
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

  async function acknowledge(ticketId: string) {
    busy[ticketId] = true;
    try {
      await fetch(`${apiBase}/api/workstation/${ticketId}/acknowledge-andon`, { method: 'POST' });
    } finally {
      busy[ticketId] = false;
    }
  }

  function clearResolved() {
    // In a real app we might want to clear the events from the store,
    // but since we don't have a store mutation for this, we'll just rely on the derived state
    // filtering out inactive ones if we change the logic.
    // Actually, the requirement says "Clear resolved button to dismiss entries for workstations that have resumed"
    // We can just clear the local andonEvents for those workstations.
    for (const alert of activeAlerts()) {
      if (!alert.isActive) {
        andonEvents[alert.workstationId] = [];
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
      <p class="text-xs text-text-muted">No active alerts</p>
    </div>
  {:else}
    <div class="flex flex-col gap-3 max-h-64 overflow-y-auto pr-1">
      {#each activeAlerts() as alert (alert.workstationId)}
        <div class="flex flex-col gap-2 rounded-md border p-3 {alert.event.signal === 'stop' ? 'border-status-error-border bg-status-error-bg/30' : 'border-status-warning-border bg-status-warning-bg/30'} {alert.isActive ? '' : 'opacity-60'}">
          <div class="flex items-start justify-between gap-2">
            <div class="flex items-center gap-2">
              <span class="rounded px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-wider {alert.event.signal === 'stop' ? 'bg-status-error-text text-white' : 'bg-status-warning-text text-white'}">
                {alert.event.signal}
              </span>
              <span class="text-xs font-medium text-text-primary">
                {alert.record?.headings[0]?.[1] || alert.ticketId}
              </span>
            </div>
            <span class="text-[10px] text-text-tertiary">
              {new Date(alert.event.timestamp).toLocaleTimeString()}
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
                const event = new CustomEvent('open-playback', { detail: { workstationId: alert.workstationId } });
                window.dispatchEvent(event);
              }}
            >
              View Workstation
            </button>
            
            {#if alert.isActive && alert.event.signal === 'stop'}
              <button 
                type="button" 
                onclick={() => acknowledge(alert.ticketId)} 
                disabled={busy[alert.ticketId]} 
                class="rounded bg-status-error-text px-2 py-1 text-[10px] font-medium text-white hover:opacity-90 disabled:opacity-50 transition-opacity"
              >
                Acknowledge
              </button>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>