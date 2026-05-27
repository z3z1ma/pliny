<script lang="ts">
  import { store } from './ws.svelte.ts';
  import StatusBar from './StatusBar.svelte';
  import ConnectionBanner from './ConnectionBanner.svelte';
  import WorkstationList from './WorkstationList.svelte';
  import DetailPanel from './DetailPanel.svelte';
  import { formatDuration } from './utils';

  let { 
    active = true,
    layoutMode, 
    showSidebar = $bindable(), 
    selectedWorkstationId = $bindable(), 
    activeTab = $bindable()
  } = $props<{
    active?: boolean;
    layoutMode: 'desktop' | 'laptop' | 'tablet' | 'mobile';
    showSidebar: boolean;
    selectedWorkstationId: string | null;
    activeTab: 'logs' | 'iterations' | 'playback';
  }>();

  let activeCount = $derived(Object.values(store.state.workstations).filter(ws => ws.status === 'running' || ws.status === 'paused').length);
  let shippedCount = $derived(store.state.shipping_events.filter(e => e.action === 'merged').length);
  
  let andonCount = $derived(() => {
    let count = 0;
    for (const events of Object.values(store.state.andon_events)) {
      count += events.length;
    }
    return count;
  });

  let avgDuration = $derived(() => {
    let total = 0;
    let count = 0;
    for (const ws of Object.values(store.state.workstations)) {
      if (ws.iteration_summary?.duration_seconds) {
        total += ws.iteration_summary.duration_seconds;
        count++;
      }
    }
    if (count === 0) return '—';
    return formatDuration(total / count);
  });

  let selectedRecord = $derived(() => {
    if (!selectedWorkstationId) return undefined;
    const ws = store.state.workstations[selectedWorkstationId];
    if (ws) {
      return store.state.records.find(r => r.metadata.id === `ticket:${ws.ticket_id}`);
    }
    return store.state.records.find(r => r.metadata.id === `ticket:${selectedWorkstationId}` || r.metadata.id === selectedWorkstationId);
  });
</script>

<div class="flex flex-col flex-1 overflow-hidden">
  <!-- Sub-header for StatusBar -->
  <div class="flex items-center justify-center h-8 border-b border-border-default bg-bg-surface px-4 shrink-0 hidden min-[480px]:flex">
    <StatusBar records={store.state.records} workstations={store.state.workstations} />
  </div>

  <ConnectionBanner />

  <!-- Main: flex row -->
  <div role="main" class="flex flex-1 overflow-hidden relative">
    {#if layoutMode === 'desktop' || layoutMode === 'laptop' || showSidebar || (layoutMode === 'mobile' && !selectedWorkstationId)}
      {#if layoutMode === 'tablet' && showSidebar}
        <!-- Backdrop for tablet sidebar -->
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div class="absolute inset-0 bg-black/30 z-40" onclick={() => showSidebar = false}></div>
      {/if}
      <div class="{layoutMode === 'desktop' ? 'w-80 shrink-0 border-r border-border-default' : layoutMode === 'laptop' ? 'w-60 shrink-0 border-r border-border-default' : layoutMode === 'tablet' ? 'absolute left-0 top-0 bottom-0 w-60 z-50 border-r border-border-default shadow-xl' : 'absolute inset-0 z-50'} bg-bg-surface transition-all {layoutMode === 'mobile' && !showSidebar && selectedWorkstationId ? 'hidden' : ''}">
        <WorkstationList 
          {active}
          records={store.state.records} 
          workstations={store.state.workstations} 
          selectedId={selectedWorkstationId}
          onSelect={(id) => {
            selectedWorkstationId = id;
            if (layoutMode === 'tablet' || layoutMode === 'mobile') showSidebar = false;
          }}
        />
      </div>
    {/if}
    
    {#if layoutMode !== 'mobile' || selectedWorkstationId}
      <div class="flex-1 min-w-0 h-full {layoutMode === 'mobile' && !selectedWorkstationId ? 'hidden' : ''}">
        <DetailPanel 
          selectedId={selectedWorkstationId}
          workstation={selectedWorkstationId ? store.state.workstations[selectedWorkstationId] : undefined}
          record={selectedRecord()}
          bind:activeTab
          mobile={layoutMode === 'mobile'}
          onBack={() => selectedWorkstationId = null}
        />
      </div>
    {/if}
  </div>

  <!-- Footer: 32px -->
  <!-- svelte-ignore a11y_no_redundant_roles -->
  <footer role="contentinfo" class="flex items-center justify-between h-8 border-t border-border-default bg-bg-surface px-4 text-[10px] text-text-tertiary shrink-0">
    <div class="flex items-center gap-4">
      <span>WIP: {activeCount}/3</span>
      <span>Shipped: {shippedCount} today</span>
      <span>Avg iteration: {avgDuration()}</span>
    </div>
    <div class="flex items-center gap-4">
      {#if andonCount() > 0}
        <span class="text-status-error-text font-medium">⚠ {andonCount()} alert{andonCount() > 1 ? 's' : ''}</span>
      {/if}
    </div>
  </footer>
</div>
