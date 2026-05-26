<script lang="ts">
  import type { WorkstationState, LoomRecord } from './types';
  import LogViewer from './LogViewer.svelte';
  import IterationsTab from './IterationsTab.svelte';
  import Playback from './Playback.svelte';
  import { formatDuration } from './utils';

  let { 
    selectedId, 
    workstation,
    record
  }: { 
    selectedId: string | null; 
    workstation: WorkstationState | undefined;
    record?: LoomRecord | undefined;
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
    return formatDuration(liveDuration);
  });

  let statusMessage = $derived(() => {
    switch (workstation?.status) {
      case 'running': return 'Running now. Logs update live while the workstation works.';
      case 'paused': return 'Paused for operator intervention. Resume after steering the record or dismiss if this run should be cleared.';
      case 'stopped': return 'Stopped before completion. Iteration history remains available for review.';
      case 'completed': return 'Completed. Review the iteration summary, playback, or dismiss it from the workstation list.';
      case 'finished': return 'Finished. Review the iteration summary, playback, or dismiss it from the workstation list.';
      case 'conflict': return 'Conflict requires operator resolution before this workstation can proceed.';
      default: return 'Idle workstation.';
    }
  });

  let recordTitle = $derived(() => {
    if (!record) return '';
    if (record.headings.length > 0) {
      return record.headings[0][1];
    }
    return record.metadata.id || record.path;
  });
</script>

<div class="flex flex-col h-full bg-bg-primary">
  {#if !selectedId}
    <!-- Empty state -->
    <div class="flex flex-1 items-center justify-center">
      <div class="flex flex-col items-center gap-2 text-text-tertiary">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="opacity-50"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>
        <p class="text-[13px]">Select a ticket or workstation from the left panel to view details.</p>
      </div>
    </div>
  {:else if !workstation && record}
    <!-- Non-workstation ticket state -->
    <div class="flex flex-col h-full">
      <div class="flex items-center gap-0 border-b border-border-default px-4 py-3 shrink-0 bg-bg-surface">
        <h2 class="text-[13px] font-medium text-text-primary">{recordTitle()}</h2>
        <div class="ml-auto flex items-center gap-2">
          <span class="rounded-full px-2 py-0.5 text-[10px] font-medium bg-bg-surface-active text-text-secondary border border-border-subtle">
            {record.metadata.status || 'unknown'}
          </span>
        </div>
      </div>
      <div class="flex flex-1 items-center justify-center p-8 text-center">
        <div class="flex flex-col items-center gap-3 max-w-md">
          <div class="w-12 h-12 rounded-full bg-bg-surface-active flex items-center justify-center text-text-tertiary mb-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
          </div>
          <p class="text-[13px] text-text-secondary font-medium">This ticket is not currently executing in Mill</p>
          <p class="text-[12px] text-text-tertiary">Ticket ID: {record.metadata.id || 'unknown'}</p>
          <p class="text-[12px] text-text-tertiary mt-2">Full record rendering is future work.</p>
        </div>
      </div>
    </div>
  {:else if workstation}
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
    <div class="flex-1 min-h-0 overflow-hidden relative transition-opacity duration-100 ease-in-out">
      {#if workstation.status !== 'running'}
        <div class="border-b border-border-subtle bg-bg-surface px-4 py-2 text-[11px] {workstation.status === 'conflict' ? 'text-status-error-text' : 'text-text-tertiary'}">
          {statusMessage()}
        </div>
      {/if}
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
