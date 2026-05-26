<script lang="ts">
  import type { WorkstationState } from './types';
  import LogViewer from './LogViewer.svelte';
  import IterationsTab from './IterationsTab.svelte';
  import Playback from './Playback.svelte';

  let { 
    selectedId, 
    workstation 
  }: { 
    selectedId: string | null; 
    workstation: WorkstationState | undefined;
  } = $props();

  let activeTab = $state<'logs' | 'iterations' | 'playback'>('logs');

  // Auto-switch default tab based on status
  $effect(() => {
    if (workstation) {
      if (workstation.status === 'completed' || workstation.status === 'stopped') {
        if (activeTab === 'logs') activeTab = 'iterations';
      } else {
        if (activeTab === 'iterations') activeTab = 'logs';
      }
    }
  });

  let tabs = [
    { id: 'logs', label: 'Logs' },
    { id: 'iterations', label: 'Iterations' },
    { id: 'playback', label: 'Playback' }
  ] as const;

  let exitCode = $derived(workstation?.exit_code ?? workstation?.iteration_summary?.exit_code);
  let iterationCount = $derived(workstation?.iteration_summary?.iteration ?? workstation?.takt?.iteration ?? 0);
  let baseDurationSeconds = $derived(workstation?.takt?.duration_seconds ?? workstation?.iteration_summary?.duration_seconds ?? 0);

  let liveDuration = $state(0);
  let timer: ReturnType<typeof setInterval>;

  $effect(() => {
    liveDuration = baseDurationSeconds;
    if (workstation?.status === 'running') {
      clearInterval(timer);
      timer = setInterval(() => {
        liveDuration += 1;
      }, 1000);
    } else {
      clearInterval(timer);
    }
    return () => clearInterval(timer);
  });

  let formattedTotalDuration = $derived(() => {
    const s = liveDuration;
    if (s === 0) return '0s';
    if (s < 60) return `${Math.floor(s)}s`;
    if (s < 3600) return `${Math.floor(s / 60)}m ${Math.floor(s % 60)}s`;
    return `${Math.floor(s / 3600)}h ${Math.floor((s % 3600) / 60)}m`;
  });
</script>

<div class="flex flex-col h-full bg-bg-primary">
  {#if !selectedId || !workstation}
    <!-- Empty state -->
    <div class="flex flex-1 items-center justify-center">
      <p class="text-[13px] text-text-tertiary">Select a workstation to view details</p>
    </div>
  {:else}
    <!-- Tab bar -->
    <div class="flex items-center gap-0 border-b border-border-default px-4 shrink-0 bg-bg-surface">
      {#each tabs as tab}
        <button class="px-3 py-2 text-[11px] font-medium border-b-2 transition-colors
          {activeTab === tab.id ? 'border-accent-primary text-text-primary' : 'border-transparent text-text-tertiary hover:text-text-secondary'}"
          onclick={() => activeTab = tab.id}>
          {tab.label}
        </button>
      {/each}
      
      <!-- Workstation info in tab bar (right side) -->
      <div class="ml-auto flex items-center gap-3 text-[10px] text-text-tertiary">
        {#if workstation.status === 'conflict'}
          <span class="text-status-error-text animate-pulse">Conflict</span>
        {/if}
        <span>Exit: {exitCode ?? '—'}</span>
        <span>Iter {iterationCount}</span>
        <span>{formattedTotalDuration()}</span>
      </div>
    </div>
    
    <!-- Tab content -->
    <div class="flex-1 min-h-0 overflow-hidden relative">
      {#if activeTab === 'logs'}
        <LogViewer logs={workstation.output || []} />
      {:else if activeTab === 'iterations'}
        <IterationsTab workstationId={selectedId} />
      {:else if activeTab === 'playback'}
        <Playback workstationId={selectedId} onClose={() => {}} embedded={true} />
      {/if}
    </div>
  {/if}
</div>
