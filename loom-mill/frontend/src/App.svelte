<script lang="ts">
  import { onMount } from 'svelte';
  import { store } from './lib/ws.svelte';
  import Pipeline from './lib/Pipeline.svelte';
  import GitPanel from './lib/GitPanel.svelte';
  import HarnessConfig from './lib/HarnessConfig.svelte';
  import AndonBoard from './lib/AndonBoard.svelte';
  import Metrics from './lib/Metrics.svelte';
  import Changelog from './lib/Changelog.svelte';
  import IterationSummary from './lib/IterationSummary.svelte';
  import ThemeToggle from './lib/ThemeToggle.svelte';
  import Playback from './lib/Playback.svelte';
  import WorkstationGrid from './lib/WorkstationGrid.svelte';

  let playbackWorkstationId = $state<string | null>(null);

  onMount(() => {
    store.connect();
    
    // Listen for custom event from WorkstationControls
    window.addEventListener('open-playback', (e: any) => {
      playbackWorkstationId = e.detail.workstationId;
    });
  });

  $effect(() => {
    document.title = `Loom Mill - ${store.connected ? 'Connected' : 'Disconnected'}`;
  });
</script>

<main class="flex h-screen flex-col bg-bg-primary text-text-primary overflow-hidden font-sans">
  <header class="flex items-center justify-between border-b border-border-default bg-bg-surface px-6 py-3">
    <div class="flex items-center gap-3">
      <h1 class="text-sm font-semibold tracking-tight text-text-primary">Loom Mill</h1>
      <span class="rounded-full bg-bg-surface-active px-2 py-0.5 text-[10px] font-medium uppercase tracking-widest text-text-secondary border border-border-subtle">
        Factory Floor
      </span>
    </div>
    <div class="flex items-center gap-4">
      <div class="flex items-center gap-2 text-xs font-medium">
        <span class="relative flex h-2 w-2">
          {#if store.connected}
            <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-status-success-text opacity-75"></span>
            <span class="relative inline-flex h-2 w-2 rounded-full bg-status-success-text"></span>
          {:else}
            <span class="relative inline-flex h-2 w-2 rounded-full bg-status-error-text"></span>
          {/if}
        </span>
        <span class={store.connected ? 'text-status-success-text' : 'text-status-error-text'}>
          {store.connected ? 'Connected' : 'Disconnected'}
        </span>
      </div>
      <div class="h-4 w-[1px] bg-border-default"></div>
      <ThemeToggle />
    </div>
  </header>

  <div class="flex flex-1 overflow-hidden">
    <div class="flex-1 overflow-hidden p-6">
      <div class="flex h-full flex-col gap-4">
        <div class="h-72 shrink-0 overflow-hidden">
          <Pipeline records={store.state.records} workstations={store.state.workstations} />
        </div>
        <div class="min-h-0 flex-1 overflow-hidden">
          <WorkstationGrid workstations={store.state.workstations} records={store.state.records} />
        </div>
      </div>
    </div>
    
    <aside class="w-80 border-l border-border-default bg-bg-surface p-4 overflow-y-auto flex flex-col gap-4">
      <AndonBoard records={store.state.records} workstations={store.state.workstations} andonEvents={store.state.andon_events} />
      <Metrics records={store.state.records} workstations={store.state.workstations} andonEvents={store.state.andon_events} shippingEvents={store.state.shipping_events} />
      <Changelog records={store.state.records} shippingEvents={store.state.shipping_events} />
      <div class="border-t border-border-default"></div>
      <HarnessConfig />
      <div class="border-t border-border-default"></div>
      <IterationSummary workstations={store.state.workstations} />
      <div class="border-t border-border-default"></div>
      <GitPanel git={store.state.git} />
    </aside>
  </div>

  {#if playbackWorkstationId}
    <Playback workstationId={playbackWorkstationId} onClose={() => playbackWorkstationId = null} />
  {/if}
</main>
