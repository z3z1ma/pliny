<script lang="ts">
  import type { LoomRecord, WorkstationState } from './types';
  import TicketCard from './TicketCard.svelte';

  let { records, workstations }: { records: LoomRecord[]; workstations: Record<string, WorkstationState> } = $props();

  let tickets = $derived(records.filter(r => r.metadata.type?.toLowerCase() === 'ticket' || r.path.includes('tickets/')));

  let columns = [
    { id: 'shaped', label: 'Shaped' },
    { id: 'executing', label: 'Executing' },
    { id: 'evidence', label: 'Evidence' },
    { id: 'audit', label: 'Audit' },
    { id: 'shipping', label: 'Shipping' },
    { id: 'closed', label: 'Closed' }
  ];

  let groupedTickets = $derived(() => {
    const groups: Record<string, LoomRecord[]> = {
      shaped: [],
      executing: [],
      evidence: [],
      audit: [],
      shipping: [],
      closed: [],
      other: []
    };

    for (const ticket of tickets) {
      const ticketId = ticket.metadata.id?.replace('ticket:', '') || '';
      const ws = workstations[ticketId];
      const status = ticket.metadata.status?.toLowerCase() || 'open';

      if (ws && (ws.status === 'completed' || ws.status === 'finished' || ws.status === 'conflict')) {
        // If workstation is completed/finished/conflict, it's in shipping phase
        groups.shipping.push(ticket);
      } else if (status === 'closed' || status === 'done') {
        groups.closed.push(ticket);
      } else if (status === 'review') {
        groups.audit.push(ticket);
      } else if (status === 'evidence') {
        groups.evidence.push(ticket);
      } else if (status === 'active' || status === 'in progress' || (ws && (ws.status === 'running' || ws.status === 'paused' || ws.status === 'stopped'))) {
        groups.executing.push(ticket);
      } else if (status === 'open' || status === 'shaped' || status === 'todo') {
        groups.shaped.push(ticket);
      } else {
        // Fallback
        if (status.includes('exec') || status.includes('prog')) groups.executing.push(ticket);
        else if (status.includes('review') || status.includes('audit')) groups.audit.push(ticket);
        else groups.shaped.push(ticket);
      }
    }

    return groups;
  });
</script>

<div class="flex h-full gap-4 overflow-x-auto pb-4">
  {#each columns as col}
    <div class="flex w-72 shrink-0 flex-col gap-3 rounded-lg bg-bg-surface p-3 border border-border-subtle">
      <div class="flex items-center justify-between px-1">
        <h2 class="text-[11px] font-medium text-text-secondary uppercase tracking-wider">{col.label}</h2>
        <span class="rounded-full bg-bg-surface-active px-2 py-0.5 text-[10px] font-medium text-text-secondary border border-border-subtle">
          {groupedTickets()[col.id].length}
        </span>
      </div>
      
      <div class="flex flex-col gap-2 overflow-y-auto">
        {#each groupedTickets()[col.id] as ticket (ticket.path)}
          <TicketCard record={ticket} workstation={workstations[ticket.metadata.id?.replace('ticket:', '') || '']} />
        {/each}
      </div>
    </div>
  {/each}
</div>
