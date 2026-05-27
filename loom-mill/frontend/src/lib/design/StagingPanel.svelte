<script lang="ts">
  import type { StagedRecord } from '../types';

  let { 
    sessionId, 
    records, 
    branches, 
    activeBranch, 
    onCommit 
  }: { 
    sessionId: string; 
    records: StagedRecord[]; 
    branches: string[]; 
    activeBranch: string; 
    onCommit: () => void;
  } = $props();

  let acceptedCount = $derived(records.filter(r => r.status === 'accepted').length);
  let totalCount = $derived(records.length);

  let countsBySurface = $derived(() => {
    const counts: Record<string, number> = {};
    for (const r of records) {
      if (r.status !== 'rejected') {
        counts[r.surface] = (counts[r.surface] || 0) + 1;
      }
    }
    return counts;
  });

  function surfaceIcon(surface: string) {
    switch (surface) {
      case 'tickets': return '🎫';
      case 'specs': return '📐';
      case 'plans': return '📊';
      case 'research': return '🔬';
      case 'knowledge': return '💡';
      default: return '📄';
    }
  }

  function scrollToProposal(tempId: string) {
    // A simple way to scroll to a proposal is to find it in the DOM
    // We can add data-temp-id attributes to the ProposalCards
    const el = document.querySelector(`[data-temp-id="${tempId}"]`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      // Add a brief highlight effect
      el.classList.add('ring-2', 'ring-accent-primary');
      setTimeout(() => el.classList.remove('ring-2', 'ring-accent-primary'), 1500);
    }
  }
</script>

<div class="flex flex-col h-full">
  <!-- Header -->
  <div class="p-4 border-b border-border-default flex flex-col gap-2 shrink-0">
    <div class="flex items-center justify-between">
      <h3 class="text-[13px] font-semibold text-text-primary">Staged Records</h3>
      <div class="text-[11px] font-medium text-text-secondary bg-bg-surface-hover px-2 py-0.5 rounded">
        {acceptedCount} / {totalCount}
      </div>
    </div>
    
    {#if branches.length > 1}
      <div class="flex items-center gap-2 mt-2">
        <span class="text-[11px] text-text-tertiary">Branch:</span>
        <select 
          class="flex-1 bg-bg-primary border border-border-default rounded px-2 py-1 text-[11px] text-text-primary focus:outline-none focus:border-accent-primary"
          value={activeBranch}
          disabled
        >
          {#each branches as branch}
            <option value={branch}>{branch}</option>
          {/each}
        </select>
      </div>
    {/if}
  </div>

  <!-- Surface Counts -->
  <div class="p-4 border-b border-border-subtle shrink-0 flex flex-col gap-2">
    {#each Object.entries(countsBySurface()) as [surface, count]}
      <div class="flex items-center justify-between text-[12px]">
        <div class="flex items-center gap-2 text-text-secondary capitalize">
          <span>{surfaceIcon(surface)}</span>
          {surface}
        </div>
        <div class="font-medium text-text-primary">{count}</div>
      </div>
    {/each}
    {#if Object.keys(countsBySurface()).length === 0}
      <div class="text-[11px] text-text-tertiary italic text-center py-2">
        No records staged yet
      </div>
    {/if}
  </div>

  <!-- Record List -->
  <div class="flex-1 overflow-y-auto p-2 flex flex-col gap-1">
    {#each records as record}
      <button 
        class="flex flex-col gap-1 p-2 rounded text-left hover:bg-bg-surface-hover transition-colors {record.status === 'rejected' ? 'opacity-50' : ''}"
        onclick={() => scrollToProposal(record.temp_id)}
      >
        <div class="flex items-center justify-between w-full">
          <div class="flex items-center gap-1.5 overflow-hidden">
            <span class="text-[12px]">{surfaceIcon(record.surface)}</span>
            <span class="text-[11px] font-medium text-text-primary truncate">{record.title}</span>
          </div>
          {#if record.status === 'accepted'}
            <span class="text-status-success-text text-[10px]">✓</span>
          {:else if record.status === 'rejected'}
            <span class="text-status-error-text text-[10px]">✗</span>
          {:else}
            <span class="w-1.5 h-1.5 rounded-full bg-accent-secondary"></span>
          {/if}
        </div>
        <div class="text-[9px] font-mono text-text-tertiary truncate">
          {record.temp_id}
        </div>
      </button>
    {/each}
  </div>

  <!-- Commit Action -->
  <div class="p-4 border-t border-border-default shrink-0 bg-bg-surface">
    <button 
      class="w-full py-2 rounded text-[12px] font-medium transition-colors flex items-center justify-center gap-2
        {acceptedCount > 0 
          ? 'bg-accent-primary text-white hover:bg-accent-primary/90 shadow-sm' 
          : 'bg-bg-surface-hover text-text-tertiary cursor-not-allowed'}"
      disabled={acceptedCount === 0}
      onclick={onCommit}
    >
      <span>✓</span>
      Commit ({acceptedCount} accepted)
    </button>
  </div>
</div>
