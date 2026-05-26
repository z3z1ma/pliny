<script lang="ts">
  import type { LoomRecord, WorkstationState, AndonEventPayload, ShippingEvent } from './types';

  let { records, workstations, andonEvents, shippingEvents }: { 
    records: LoomRecord[]; 
    workstations: Record<string, WorkstationState>;
    andonEvents: Record<string, AndonEventPayload[]>;
    shippingEvents: ShippingEvent[];
  } = $props();

  let metrics = $derived(() => {
    const wsList = Object.values(workstations);
    
    // Iterations per ticket (avg)
    const workstationsWithTakt = wsList.filter(ws => ws.takt);
    const totalIterations = workstationsWithTakt.reduce((sum, ws) => sum + (ws.takt?.iteration || 0), 0);
    const avgIterations = workstationsWithTakt.length ? (totalIterations / workstationsWithTakt.length).toFixed(1) : '0.0';

    // Average iteration duration
    const totalDuration = workstationsWithTakt.reduce((sum, ws) => sum + (ws.takt?.duration_seconds || 0), 0);
    const avgDurationSecs = workstationsWithTakt.length ? Math.round(totalDuration / workstationsWithTakt.length) : 0;
    const avgDurationStr = avgDurationSecs > 60 
      ? `${Math.floor(avgDurationSecs / 60)}m ${avgDurationSecs % 60}s`
      : `${avgDurationSecs}s`;

    // SPC stop count
    let spcStops = 0;
    for (const events of Object.values(andonEvents)) {
      spcStops += events.filter(e => e.signal === 'stop').length;
    }

    // Rework count (resumed after steering)
    let reworkCount = 0;
    for (const [wsId, events] of Object.entries(andonEvents)) {
      if (events.length > 0) {
        const ws = workstations[wsId];
        if (ws && (ws.status === 'running' || ws.status === 'completed')) {
          reworkCount++;
        }
      }
    }

    // Completion rate
    const tickets = records.filter(r => r.metadata.type?.toLowerCase() === 'ticket' || r.path.includes('tickets/'));
    const shippedCount = shippingEvents.filter(e => e.action === 'merged').length;
    const completionRate = tickets.length ? Math.round((shippedCount / tickets.length) * 100) : 0;

    return {
      completed: shippedCount,
      avgIterations,
      avgDuration: avgDurationStr,
      spcStops,
      reworkCount,
      completionRate: `${completionRate}%`
    };
  });
</script>

<div class="flex flex-col gap-3 rounded-lg border border-border-default bg-bg-surface p-4">
  <h2 class="text-sm font-semibold text-text-primary">Quality Metrics</h2>
  
  <div class="grid grid-cols-2 gap-3">
    <div class="flex flex-col rounded bg-bg-primary p-3 border border-border-subtle">
      <span class="text-2xl font-light text-text-primary">{metrics().completed}</span>
      <span class="text-[10px] font-medium uppercase tracking-wider text-text-secondary mt-1">Tickets Completed</span>
    </div>
    
    <div class="flex flex-col rounded bg-bg-primary p-3 border border-border-subtle">
      <span class="text-2xl font-light text-text-primary">{metrics().completionRate}</span>
      <span class="text-[10px] font-medium uppercase tracking-wider text-text-secondary mt-1">Completion Rate</span>
    </div>
    
    <div class="flex flex-col rounded bg-bg-primary p-3 border border-border-subtle">
      <span class="text-2xl font-light text-text-primary">{metrics().avgIterations}</span>
      <span class="text-[10px] font-medium uppercase tracking-wider text-text-secondary mt-1">Avg Iterations</span>
    </div>
    
    <div class="flex flex-col rounded bg-bg-primary p-3 border border-border-subtle">
      <span class="text-2xl font-light text-text-primary">{metrics().avgDuration}</span>
      <span class="text-[10px] font-medium uppercase tracking-wider text-text-secondary mt-1">Avg Duration</span>
    </div>
    
    <div class="flex flex-col rounded bg-bg-primary p-3 border border-border-subtle">
      <span class="text-2xl font-light text-status-error-text">{metrics().spcStops}</span>
      <span class="text-[10px] font-medium uppercase tracking-wider text-text-secondary mt-1">SPC Stops</span>
    </div>
    
    <div class="flex flex-col rounded bg-bg-primary p-3 border border-border-subtle">
      <span class="text-2xl font-light text-status-warning-text">{metrics().reworkCount}</span>
      <span class="text-[10px] font-medium uppercase tracking-wider text-text-secondary mt-1">Rework Count</span>
    </div>
  </div>
</div>