<script lang="ts">
  import { onMount } from 'svelte';
  import { store } from './lib/ws.svelte';
  import Pipeline from './lib/Pipeline.svelte';
  import GitPanel from './lib/GitPanel.svelte';

  onMount(() => {
    store.connect();
  });

  $effect(() => {
    document.title = `Loom Mill - ${store.connected ? 'Connected' : 'Disconnected'}`;
  });
</script>

<main class="flex h-screen flex-col bg-slate-950 text-slate-100 overflow-hidden">
  <header class="flex items-center justify-between border-b border-slate-800 bg-slate-900/50 px-6 py-4">
    <div class="flex items-center gap-4">
      <h1 class="text-xl font-semibold tracking-tight text-cyan-100">Loom Mill</h1>
      <span class="rounded bg-slate-800 px-2 py-1 text-xs font-medium uppercase tracking-widest text-slate-400">
        Factory Floor
      </span>
    </div>
    <div class="flex items-center gap-3">
      <div class="flex items-center gap-2 text-sm">
        <span class="relative flex h-2.5 w-2.5">
          {#if store.connected}
            <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex h-2.5 w-2.5 rounded-full bg-emerald-500"></span>
          {:else}
            <span class="relative inline-flex h-2.5 w-2.5 rounded-full bg-rose-500"></span>
          {/if}
        </span>
        <span class={store.connected ? 'text-emerald-400' : 'text-rose-400'}>
          {store.connected ? 'Connected' : 'Disconnected'}
        </span>
      </div>
    </div>
  </header>

  <div class="flex flex-1 overflow-hidden">
    <div class="flex-1 overflow-hidden p-6">
      <Pipeline records={store.state.records} />
    </div>
    
    <aside class="w-80 border-l border-slate-800 bg-slate-900/20 p-6 overflow-y-auto">
      <GitPanel git={store.state.git} />
    </aside>
  </div>
</main>
