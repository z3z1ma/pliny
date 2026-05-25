<script lang="ts">
  import type { LoomRecord, WorkstationState } from './types';
  import TicketCard from './TicketCard.svelte';

  let { records, workstations }: { records: LoomRecord[]; workstations: Record<string, WorkstationState> } = $props();

  let tickets = $derived(records.filter(r => r.metadata.type?.toLowerCase() === 'ticket' || r.path.includes('tickets/')));

  let columns = ['open', 'active', 'blocked', 'review', 'closed'];

  let groupedTickets = $derived(() => {
    const groups: Record<string, LoomRecord[]> = {
      open: [],
      active: [],
      blocked: [],
      review: [],
      closed: [],
      other: []
    };

    for (const ticket of tickets) {
      const status = ticket.metadata.status?.toLowerCase() || 'open';
      if (groups[status]) {
        groups[status].push(ticket);
      } else {
        groups.other.push(ticket);
      }
    }

    return groups;
  });
</script>

<div class="flex h-full gap-4 overflow-x-auto pb-4">
  {#each columns as col}
    <div class="flex w-80 shrink-0 flex-col gap-3 rounded-xl bg-slate-900/30 p-3">
      <div class="flex items-center justify-between px-1">
        <h2 class="text-sm font-medium text-slate-400 uppercase tracking-wider">{col}</h2>
        <span class="rounded-full bg-slate-800 px-2 py-0.5 text-xs font-medium text-slate-400">
          {groupedTickets()[col].length}
        </span>
      </div>
      
      <div class="flex flex-col gap-2 overflow-y-auto">
        {#each groupedTickets()[col] as ticket (ticket.path)}
          <TicketCard record={ticket} workstation={workstations[ticket.metadata.id?.replace('ticket:', '') || '']} />
        {/each}
      </div>
    </div>
  {/each}
</div>
