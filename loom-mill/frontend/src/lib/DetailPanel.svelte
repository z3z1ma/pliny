<script lang="ts">
  import type { WorkstationState, LoomRecord } from './types';
  import LogViewer from './LogViewer.svelte';
  import IterationsTab from './IterationsTab.svelte';
  import Playback from './Playback.svelte';
  import { formatDuration } from './utils';
  import RecordRenderer from './RecordRenderer.svelte';
  import MetadataBadges from './MetadataBadges.svelte';
  import ReviewActions from './ReviewActions.svelte';
  import { apiUrl } from './api';
  import { store } from './ws.svelte';

  let { 
    selectedId, 
    workstation,
    record,
    activeTab = $bindable('logs'),
    mobile = false,
    onBack = () => {}
  }: { 
    selectedId: string | null; 
    workstation: WorkstationState | undefined;
    record?: LoomRecord | undefined;
    activeTab?: 'logs' | 'iterations' | 'playback';
    mobile?: boolean;
    onBack?: () => void;
  } = $props();

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

  let playbackInitialStep = $state<number | undefined>(undefined);

  function handleViewIterationDiff(iterationIndex: number) {
    playbackInitialStep = iterationIndex;
    activeTab = 'playback';
  }

  function handleTabClick(tabId: 'logs' | 'iterations' | 'playback') {
    if (tabId !== 'playback') playbackInitialStep = undefined;
    activeTab = tabId;
  }

  let lastPlaybackWorkstationId = $state<string | null>(null);

  $effect(() => {
    if (selectedId !== lastPlaybackWorkstationId) {
      playbackInitialStep = undefined;
      lastPlaybackWorkstationId = selectedId;
    }
  });

  let hydratingLogs = $state(false);
  let hydratedEmptyLogs = new Set<string>();

  $effect(() => {
    const id = selectedId;
    if (!id || !workstation || workstation.output?.length || workstation.status === 'running') return;
    if (hydratedEmptyLogs.has(id)) return;

    hydratingLogs = true;
    store.hydrateWorkstationLogs(id).finally(() => {
      hydratedEmptyLogs.add(id);
      hydratingLogs = false;
    });
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

  let recordContent = $state<string | null>(null);
  let loadingContent = $state(false);

  async function fetchContent() {
    if (!record || !record.metadata.id) return;
    loadingContent = true;
    try {
      const res = await fetch(apiUrl(`/records/${record.metadata.id}/content`));
      if (res.ok) {
        const data = await res.json();
        recordContent = data.content;
      } else {
        console.error('Failed to fetch record content', res.status);
        recordContent = null;
      }
    } catch (err) {
      console.error('Error fetching record content', err);
      recordContent = null;
    } finally {
      loadingContent = false;
    }
  }

  $effect(() => {
    if (record && !workstation) {
      fetchContent();
    } else {
      recordContent = null;
    }
  });

  function handleTabKeydown(e: KeyboardEvent) {
    const currentIndex = tabs.findIndex(t => t.id === activeTab);
    if (e.key === 'ArrowRight') {
      e.preventDefault();
      const nextIndex = (currentIndex + 1) % tabs.length;
      handleTabClick(tabs[nextIndex].id);
      document.getElementById(`tab-${tabs[nextIndex].id}`)?.focus();
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      const prevIndex = (currentIndex - 1 + tabs.length) % tabs.length;
      handleTabClick(tabs[prevIndex].id);
      document.getElementById(`tab-${tabs[prevIndex].id}`)?.focus();
    }
  }
</script>

<div class="flex flex-col h-full bg-bg-primary">
  {#if mobile && selectedId}
    <button onclick={onBack} class="flex items-center gap-1 px-4 py-2 text-[11px] text-text-secondary hover:text-text-primary bg-bg-surface border-b border-border-default shrink-0">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
      Back to list
    </button>
  {/if}

  <div class="flex-1 min-h-0 flex justify-center">
    <div class="w-full min-[1600px]:max-w-[800px] min-[1600px]:border-x min-[1600px]:border-border-default flex flex-col h-full bg-bg-primary">
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
    <div class="flex flex-col h-full overflow-hidden">
      <!-- Header with title and badges -->
      <div class="flex items-center gap-3 border-b border-border-default px-4 py-3 shrink-0 bg-bg-surface">
        <h2 class="text-[14px] font-semibold text-text-primary truncate">{recordTitle()}</h2>
      </div>
      <!-- Metadata badges row -->
      <div class="px-4 py-2 border-b border-border-subtle bg-bg-surface shrink-0">
        <MetadataBadges metadata={record.metadata} />
      </div>
      <!-- Scrollable content body -->
      <div class="flex-1 overflow-y-auto px-4 py-4">
        {#if recordContent}
          <RecordRenderer content={recordContent} />
          {#if record.metadata.status === 'review' && record.metadata.id}
            <ReviewActions recordId={record.metadata.id} onTransition={fetchContent} />
          {/if}
        {:else if loadingContent}
          <div class="flex items-center gap-2 text-text-tertiary text-[12px]">
            <span class="animate-pulse">Loading record content...</span>
          </div>
        {:else}
          <div class="text-text-tertiary text-[12px]">
            <p>Record metadata is available but content could not be loaded.</p>
            <button class="mt-2 text-accent-primary hover:underline" onclick={fetchContent}>Retry</button>
          </div>
        {/if}
      </div>
      <!-- Footer: references if any -->
      {#if record.references.length > 0}
        <div class="border-t border-border-subtle px-4 py-2 shrink-0">
          <p class="text-[10px] font-medium text-text-tertiary mb-1">References</p>
          <div class="flex flex-wrap gap-1">
            {#each record.references as ref}
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-bg-surface-active text-text-secondary">{ref}</span>
            {/each}
          </div>
        </div>
      {/if}
    </div>
  {:else if workstation}
    <!-- Tab bar -->
    <div role="tablist" tabindex="0" class="flex items-center gap-0 border-b border-border-default px-4 shrink-0 bg-bg-surface" onkeydown={handleTabKeydown}>
      {#each tabs as tab}
        <button 
          id="tab-{tab.id}"
          role="tab"
          aria-selected={activeTab === tab.id}
          aria-controls="panel-{tab.id}"
          tabindex={activeTab === tab.id ? 0 : -1}
          class="px-3 py-2 text-[11px] font-medium border-b-2 transition-colors
          {activeTab === tab.id ? 'border-accent-primary text-text-primary' : 'border-transparent text-text-tertiary hover:text-text-secondary'}"
          onclick={() => handleTabClick(tab.id)}>
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
    <div role="tabpanel" id="panel-{activeTab}" aria-labelledby="tab-{activeTab}" class="flex-1 min-h-0 overflow-hidden relative transition-opacity duration-100 ease-in-out">
      {#if workstation.status !== 'running'}
        <div class="border-b border-border-subtle bg-bg-surface px-4 py-2 text-[11px] {workstation.status === 'conflict' ? 'text-status-error-text' : 'text-text-tertiary'}">
          {statusMessage()}
        </div>
      {/if}
      {#if activeTab === 'logs'}
        <LogViewer logs={workstation.output || []} status={workstation.status} loading={hydratingLogs} />
      {:else if activeTab === 'iterations'}
        <IterationsTab workstationId={selectedId} onViewDiff={handleViewIterationDiff} />
      {:else if activeTab === 'playback'}
        <Playback workstationId={selectedId} onClose={() => {}} embedded={true} initialStep={playbackInitialStep} />
      {/if}
    </div>
  {/if}
    </div>
  </div>
</div>
