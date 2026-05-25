<script lang="ts">
  import type { LoomRecord, WorkstationState } from './types';
  import WorkstationControls from './WorkstationControls.svelte';

  let { record, workstation }: { record: LoomRecord; workstation?: WorkstationState } = $props();

  // The parser now captures #, ##, and ### headings.
  // The first heading is usually the title.
  let title = $derived(record.headings.length > 0 ? record.headings[0][1] : record.path.split('/').pop() || 'Unknown');
  let id = $derived(record.metadata.id?.replace('ticket:', '') || 'unknown');
  let status = $derived(record.metadata.status || 'unknown');
  let updated = $derived(record.metadata.updated || record.metadata.created || '');

  // Find linked evidence and audit
  let hasEvidence = $derived(record.references.some(ref => ref.includes('evidence:')));
  let hasAudit = $derived(record.references.some(ref => ref.includes('audit:')));
</script>

<div class="flex flex-col gap-2 rounded-lg border border-slate-800 bg-slate-900 p-3 shadow-sm transition-colors hover:border-slate-700">
  <div class="flex items-start justify-between gap-2">
    <span class="text-xs font-mono text-slate-500">{id}</span>
    <span class="inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset
      {status === 'active' ? 'bg-cyan-400/10 text-cyan-400 ring-cyan-400/30' :
       status === 'blocked' ? 'bg-rose-400/10 text-rose-400 ring-rose-400/30' :
       status === 'review' ? 'bg-amber-400/10 text-amber-400 ring-amber-400/30' :
       status === 'closed' ? 'bg-slate-400/10 text-slate-400 ring-slate-400/30' :
       'bg-slate-400/10 text-slate-400 ring-slate-400/30'}">
      {status}
    </span>
  </div>
  
  <h3 class="text-sm font-medium text-slate-200 line-clamp-2">{title}</h3>

  <WorkstationControls ticketId={id} workstation={workstation} />

  <div class="mt-2 flex items-center justify-between text-xs text-slate-500">
    <div class="flex gap-1.5">
      {#if hasEvidence}
        <span class="flex h-5 w-5 items-center justify-center rounded bg-indigo-500/20 text-indigo-300" title="Has Evidence">E</span>
      {/if}
      {#if hasAudit}
        <span class="flex h-5 w-5 items-center justify-center rounded bg-fuchsia-500/20 text-fuchsia-300" title="Has Audit">A</span>
      {/if}
    </div>
    {#if updated}
      <span>{updated}</span>
    {/if}
  </div>
</div>
