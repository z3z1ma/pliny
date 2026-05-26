<script lang="ts">
  import { onMount } from 'svelte';
  import { store } from './lib/ws.svelte';
  import StatusBar from './lib/StatusBar.svelte';
  import WorkstationList from './lib/WorkstationList.svelte';
  import DetailPanel from './lib/DetailPanel.svelte';
  import ThemeToggle from './lib/ThemeToggle.svelte';
  import SettingsDrawer from './lib/SettingsDrawer.svelte';
  import Toast from './lib/Toast.svelte';
  import { formatDuration } from './lib/utils';

  let selectedWorkstationId = $state<string | null>(null);
  let settingsOpen = $state(false);
  let toastRef = $state<Toast>();

  let prevWorkstations: Record<string, { status: string, andonCount: number }> = {};

  onMount(() => {
    store.connect();
  });

  $effect(() => {
    document.title = `Loom Mill - ${store.connected ? 'Connected' : 'Disconnected'}`;
  });

  $effect(() => {
    if (!toastRef) return;
    
    for (const [id, ws] of Object.entries(store.state.workstations)) {
      const prev = prevWorkstations[id];
      if (!prev) {
        if (ws.status === 'running') {
          toastRef.show(`▶ Started: ${ws.ticket_slug}`, 'info');
        }
      } else if (prev.status !== ws.status) {
        if (ws.status === 'completed') {
          const duration = ws.iteration_summary?.duration_seconds ? ` (${formatDuration(ws.iteration_summary.duration_seconds)})` : '';
          toastRef.show(`✓ Completed: ${ws.ticket_slug}${duration}`, 'info');
        } else if (ws.status === 'stopped') {
          toastRef.show(`⛔ Stopped: ${ws.ticket_slug}`, 'error');
        }
      }
    }
    
    for (const [id, events] of Object.entries(store.state.andon_events)) {
      const prevCount = prevWorkstations[id]?.andonCount || 0;
      if (events.length > prevCount) {
        const latest = events[events.length - 1];
        toastRef.show(`⚠ Alert on ${store.state.workstations[id]?.ticket_slug || id}: ${latest.reasoning}`, 'warning');
      }
    }

    prevWorkstations = {};
    for (const [id, ws] of Object.entries(store.state.workstations)) {
      prevWorkstations[id] = { status: ws.status, andonCount: store.state.andon_events[id]?.length || 0 };
    }
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
    return formatDuration(total / count);
  });

  let selectedRecord = $derived(() => {
    if (!selectedWorkstationId) return undefined;
    // If it's a workstation ID, find the record
    const ws = store.state.workstations[selectedWorkstationId];
    if (ws) {
      return store.state.records.find(r => r.metadata.id === `ticket:${ws.ticket_id}`);
    }
    // Otherwise it might be a ticket ID directly
    return store.state.records.find(r => r.metadata.id === `ticket:${selectedWorkstationId}` || r.metadata.id === selectedWorkstationId);
  });
</script>

<main class="flex h-screen flex-col bg-bg-primary text-text-primary overflow-hidden font-sans">
  <Toast bind:this={toastRef} />
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
        record={selectedRecord()}
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
