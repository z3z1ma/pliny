<script lang="ts">
  import { onMount } from 'svelte';
  import { store } from './lib/ws.svelte';
  import StatusBar from './lib/StatusBar.svelte';
  import WorkstationList from './lib/WorkstationList.svelte';
  import DetailPanel from './lib/DetailPanel.svelte';
  import ThemeToggle from './lib/ThemeToggle.svelte';
  import SettingsDrawer from './lib/SettingsDrawer.svelte';

  let selectedWorkstationId = $state<string | null>(null);
  let settingsOpen = $state(false);

  onMount(() => {
    store.connect();
  });

  $effect(() => {
    document.title = `Loom Mill - ${store.connected ? 'Connected' : 'Disconnected'}`;
  });

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
    const avg = total / count;
    if (avg < 60) return `${Math.floor(avg)}s`;
    return `${Math.floor(avg / 60)}m ${Math.floor(avg % 60)}s`;
  });
</script>

<main class="flex h-screen flex-col bg-bg-primary text-text-primary overflow-hidden font-sans">
  <!-- Header: 48px -->
  <header class="flex items-center justify-between h-12 border-b border-border-default bg-bg-surface px-4 shrink-0">
    <div class="flex items-center gap-2">
      <h1 class="text-[13px] font-semibold text-text-primary">Loom Mill</h1>
    </div>
    
    <StatusBar records={store.state.records} workstations={store.state.workstations} />
    
    <div class="flex items-center gap-3">
      <div class="flex items-center gap-2 text-[11px] font-medium">
        <span class="relative flex h-2 w-2">
          {#if store.connected}
            <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-status-success-text opacity-75"></span>
            <span class="relative inline-flex h-2 w-2 rounded-full bg-status-success-text"></span>
          {:else}
            <span class="relative inline-flex h-2 w-2 rounded-full bg-status-error-text"></span>
          {/if}
        </span>
      </div>
      <div class="h-4 w-[1px] bg-border-default"></div>
      <ThemeToggle />
      <button 
        onclick={() => settingsOpen = !settingsOpen}
        class="relative p-1 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary transition-colors"
        title="Settings & Info">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
        {#if andonCount() > 0}
          <span class="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-status-error-text"></span>
        {/if}
      </button>
    </div>
  </header>

  <!-- Main: flex row -->
  <div class="flex flex-1 overflow-hidden">
    <div class="w-80 shrink-0 border-r border-border-default">
      <WorkstationList 
        records={store.state.records} 
        workstations={store.state.workstations} 
        selectedId={selectedWorkstationId}
        onSelect={(id) => selectedWorkstationId = id}
      />
    </div>
    <div class="flex-1 min-w-0">
      <DetailPanel 
        selectedId={selectedWorkstationId}
        workstation={selectedWorkstationId ? store.state.workstations[selectedWorkstationId] : undefined}
      />
    </div>
  </div>

  <!-- Footer: 32px -->
  <footer class="flex items-center justify-between h-8 border-t border-border-default bg-bg-surface px-4 text-[10px] text-text-tertiary shrink-0">
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

  <SettingsDrawer open={settingsOpen} onClose={() => settingsOpen = false} />
</main>