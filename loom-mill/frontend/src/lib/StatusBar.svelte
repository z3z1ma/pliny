<script lang="ts">
  import type { LoomRecord, WorkstationState } from './types';

  let { records, workstations }: { records: LoomRecord[]; workstations: Record<string, WorkstationState> } = $props();

  let tickets = $derived(records.filter(r => r.metadata.type?.toLowerCase() === 'ticket' || r.path.includes('tickets/')));

  let groupedCounts = $derived(() => {
    const counts = {
      shaped: 0,
      executing: 0,
      evidence: 0,
      audit: 0,
      shipping: 0,
      closed: 0
    };

    for (const ticket of tickets) {
      const ticketId = ticket.metadata.id?.replace(/^ticket:/, '') || '';
      const ws = Object.values(workstations).find(w => (w.ticket_id || '').replace(/^ticket:/, '') === ticketId);
      const status = ticket.metadata.status?.toLowerCase() || 'open';

      if (ws && (ws.status === 'completed' || ws.status === 'finished' || ws.status === 'conflict')) {
        counts.shipping++;
      } else if (status === 'closed' || status === 'done' || status === 'cancelled') {
        counts.closed++;
      } else if (status === 'review') {
        counts.audit++;
      } else if (status === 'evidence') {
        counts.evidence++;
      } else if (status === 'active' || status === 'in progress' || (ws && (ws.status === 'running' || ws.status === 'paused' || ws.status === 'stopped'))) {
        counts.executing++;
      } else if (status === 'open' || status === 'shaped' || status === 'todo' || status === 'blocked') {
        counts.shaped++;
      } else {
        if (status.includes('exec') || status.includes('prog')) counts.executing++;
        else if (status.includes('review') || status.includes('audit')) counts.audit++;
        else counts.shaped++;
      }
    }

    return counts;
  });

  let stages = $derived(() => {
    const counts = groupedCounts();
    return [
      { id: 'shaped', label: 'Shaped', count: counts.shaped, color: 'bg-text-tertiary' },
      { id: 'executing', label: 'Executing', count: counts.executing, color: 'bg-status-success-text' },
      { id: 'evidence', label: 'Evidence', count: counts.evidence, color: 'bg-status-info-text' },
      { id: 'audit', label: 'Audit', count: counts.audit, color: 'bg-status-warning-text' },
      { id: 'shipping', label: 'Shipping', count: counts.shipping, color: 'bg-accent-primary' },
      { id: 'closed', label: 'Closed', count: counts.closed, color: 'bg-text-tertiary opacity-50' }
    ];
  });

  function scrollToSection(id: string) {
    // Some sections might have slightly different IDs in the DOM
    let targetId = `section-${id}`;
    if (id === 'executing') {
      // Try to scroll to workstations first, then external
      const el = document.getElementById('section-executing') || document.getElementById('section-executing-external');
      if (el) el.scrollIntoView({ behavior: 'smooth' });
      return;
    }
    if (id === 'shaped') {
      // Try to scroll to shaped first, then blocked
      const el = document.getElementById('section-shaped') || document.getElementById('section-blocked');
      if (el) el.scrollIntoView({ behavior: 'smooth' });
      return;
    }
    
    const el = document.getElementById(targetId);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  }
</script>

<div class="flex items-center gap-1.5">
  {#each stages() as stage}
    <button 
      onclick={() => scrollToSection(stage.id)}
      aria-label="Scroll to {stage.label} section ({stage.count} tickets)"
      class="flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-medium
      transition-colors hover:bg-bg-surface-active
      {stage.count > 0 ? 'text-text-secondary cursor-pointer' : 'text-text-tertiary cursor-default'}">
      <span class="w-1.5 h-1.5 rounded-full {stage.color}"></span>
      <span class="hidden md:inline">{stage.label}</span>
      <span class="tabular-nums">{stage.count}</span>
    </button>
  {/each}
</div>
