<script lang="ts">
  import type { ShippingEvent, LoomRecord } from './types';

  let { shippingEvents, records }: { 
    shippingEvents: ShippingEvent[];
    records: LoomRecord[];
  } = $props();

  let shippedTickets = $derived(() => {
    return shippingEvents
      .filter(e => e.action === 'merged')
      .map(event => {
        const record = records.find(r => r.metadata.id?.replace('ticket:', '') === event.ticket_id);
        return {
          event,
          record
        };
      })
      .sort((a, b) => new Date(b.event.timestamp).getTime() - new Date(a.event.timestamp).getTime());
  });
</script>

<div class="flex flex-col gap-3 rounded-lg border border-border-default bg-bg-surface p-4 flex-1 min-h-0">
  <h2 class="text-sm font-semibold text-text-primary">Session Changelog</h2>
  
  {#if shippedTickets().length === 0}
    <div class="flex flex-1 items-center justify-center rounded border border-dashed border-border-subtle min-h-[100px]">
      <p class="text-xs text-text-muted">No tickets shipped yet</p>
    </div>
  {:else}
    <div class="flex flex-col gap-3 overflow-y-auto pr-1">
      {#each shippedTickets() as item (item.event.ticket_id + item.event.timestamp)}
        <div class="flex flex-col gap-2 rounded-md border border-border-subtle bg-bg-primary p-3">
          <div class="flex items-start justify-between gap-2">
            <div class="flex items-center gap-2">
              <span class="rounded-full bg-status-success-bg px-1.5 py-0.5 text-[10px] font-medium text-status-success-text border border-status-success-border">
                Shipped
              </span>
              <span class="text-xs font-medium text-text-primary">
                {item.record?.headings[0]?.[1] || item.event.ticket_id}
              </span>
            </div>
            <span class="text-[10px] text-text-tertiary">
              {new Date(item.event.timestamp).toLocaleTimeString()}
            </span>
          </div>
          
          <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-[11px] text-text-secondary">
            <div class="flex items-center gap-1">
              <span class="text-text-tertiary">Branch:</span>
              <span class="font-mono">{item.event.target_branch}</span>
            </div>
            
            {#if item.event.merge_sha}
              <div class="flex items-center gap-1">
                <span class="text-text-tertiary">Commit:</span>
                <span class="font-mono">{item.event.merge_sha.substring(0, 7)}</span>
              </div>
            {/if}
            
            {#if item.event.diff_stat}
              <div class="flex items-center gap-1 font-mono">
                {item.event.diff_stat}
              </div>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>