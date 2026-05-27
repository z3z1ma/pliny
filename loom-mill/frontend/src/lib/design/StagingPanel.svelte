<script lang="ts">
  import type { StagedRecord } from '../types';

  let { 
    sessionId, 
    records, 
    branches, 
    activeBranch, 
    onCommit,
    onRecordClick
  }: { 
    sessionId: string; 
    records: StagedRecord[]; 
    branches: string[]; 
    activeBranch: string; 
    onCommit: () => void;
    onRecordClick?: (tempId: string) => void;
  } = $props();

  let acceptedCount = $derived(records.filter(r => r.status === 'accepted').length);
  let totalCount = $derived(records.length);
  let allAccepted = $derived(totalCount > 0 && acceptedCount === totalCount);

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

  function selectRecord(tempId: string) {
    onRecordClick?.(tempId);
  }
</script>

<div class="flex flex-col h-full bg-bg-surface border-l border-border-default">
  <!-- Header -->
  <div class="p-4 border-b border-border-default flex flex-col gap-2 shrink-0 bg-bg-primary">
    <div class="flex items-center justify-between">
      <h3 class="text-[13px] font-semibold text-text-primary flex items-center gap-2">
        <span class="text-accent-primary">📦</span> Staging Area
      </h3>
      <div class="text-[11px] font-medium {allAccepted ? 'text-status-success-text bg-status-success-bg/20' : 'text-text-secondary bg-bg-surface-hover'} px-2 py-0.5 rounded-full transition-colors">
        {acceptedCount} / {totalCount} Ready
      </div>
    </div>
    
    {#if branches.length > 1}
      <div class="flex items-center gap-2 mt-2">
        <span class="text-[11px] text-text-tertiary">Branch:</span>
        <select 
          class="flex-1 bg-bg-surface border border-border-default rounded px-2 py-1 text-[11px] text-text-primary focus:outline-none focus:border-accent-primary"
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

  <!-- Mini Graph Visualization -->
  {#if records.length > 0}
    <div class="p-4 border-b border-border-subtle shrink-0 bg-bg-surface flex justify-center items-center min-h-[100px] relative overflow-hidden">
      <div class="absolute inset-0 opacity-10 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-accent-primary to-transparent"></div>
      <div class="flex flex-wrap justify-center gap-3 relative z-10">
        {#each records as record}
          <button 
            class="w-8 h-8 rounded-full flex items-center justify-center text-[14px] shadow-sm border-2 transition-all duration-300 cursor-pointer hover:scale-110
              {record.status === 'accepted' ? 'bg-status-success-bg/20 border-status-success-border text-status-success-text' : 
               record.status === 'rejected' ? 'bg-status-error-bg/10 border-status-error-border/30 text-status-error-text opacity-50 grayscale' : 
               'bg-accent-primary/10 border-accent-primary/50 text-accent-primary animate-pulse'}"
            title={record.title}
            onclick={() => selectRecord(record.temp_id)}
          >
            {surfaceIcon(record.surface)}
          </button>
        {/each}
      </div>
    </div>
  {/if}

  <!-- Record List -->
  <div class="flex-1 overflow-y-auto p-2 flex flex-col gap-1 bg-bg-primary">
    {#if records.length === 0}
      <div class="flex flex-col items-center justify-center h-full text-text-tertiary gap-3 opacity-50">
        <span class="text-4xl">🫙</span>
        <span class="text-[12px]">No records staged yet</span>
      </div>
    {/if}
    {#each records as record}
      <button 
        class="flex flex-col gap-1.5 p-3 rounded-lg text-left hover:bg-bg-surface transition-all border border-transparent hover:border-border-default group
          {record.status === 'rejected' ? 'opacity-50' : ''}
          {record.status === 'accepted' ? 'bg-status-success-bg/5' : ''}"
        onclick={() => selectRecord(record.temp_id)}
      >
        <div class="flex items-center justify-between w-full">
          <div class="flex items-center gap-2 overflow-hidden">
            <span class="text-[14px] bg-bg-surface w-6 h-6 rounded flex items-center justify-center shadow-sm border border-border-subtle group-hover:border-border-default transition-colors">{surfaceIcon(record.surface)}</span>
            <span class="text-[12px] font-medium text-text-primary truncate">{record.title}</span>
          </div>
          {#if record.status === 'accepted'}
            <span class="text-status-success-text text-[12px] bg-status-success-bg/20 w-5 h-5 rounded-full flex items-center justify-center">✓</span>
          {:else if record.status === 'rejected'}
            <span class="text-status-error-text text-[12px] bg-status-error-bg/20 w-5 h-5 rounded-full flex items-center justify-center">✗</span>
          {:else}
            <span class="w-2 h-2 rounded-full bg-accent-primary animate-ping mr-1.5"></span>
          {/if}
        </div>
        <div class="text-[10px] font-mono text-text-tertiary truncate pl-8">
          {record.temp_id}
        </div>
      </button>
    {/each}
  </div>

  <!-- Commit Action -->
  <div class="p-4 border-t border-border-default shrink-0 bg-bg-surface relative overflow-hidden">
    {#if allAccepted}
      <div class="absolute inset-0 bg-status-success-bg/10 animate-pulse"></div>
    {/if}
    <button 
      class="w-full py-2.5 rounded-md text-[13px] font-medium transition-all flex items-center justify-center gap-2 relative z-10
        {acceptedCount > 0 
          ? allAccepted 
            ? 'bg-status-success-text text-white shadow-md hover:bg-status-success-text/90 scale-105 transform' 
            : 'bg-accent-primary text-white hover:bg-accent-primary/90 shadow-sm' 
          : 'bg-bg-surface-hover text-text-tertiary cursor-not-allowed border border-border-default'}"
      disabled={acceptedCount === 0}
      onclick={onCommit}
    >
      {#if allAccepted}
        <span class="animate-bounce">🚀</span>
        Commit All Records
      {:else}
        <span>✓</span>
        Commit ({acceptedCount} accepted)
      {/if}
    </button>
  </div>
</div>
