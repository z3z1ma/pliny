<script lang="ts">
  import HarnessConfig from './HarnessConfig.svelte';
  import Metrics from './Metrics.svelte';
  import Changelog from './Changelog.svelte';
  import AndonBoard from './AndonBoard.svelte';
  import GitPanel from './GitPanel.svelte';
  import { store } from './ws.svelte';

  let { open, onClose } = $props<{ open: boolean; onClose: () => void }>();

  let tab = $state<'harness' | 'metrics' | 'alerts' | 'git'>('harness');
</script>

<div class="fixed inset-0 z-50 {open ? '' : 'pointer-events-none'}">
  <!-- Backdrop -->
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div class="absolute inset-0 bg-black/30 transition-opacity {open ? 'opacity-100' : 'opacity-0'}"
    onclick={onClose}></div>
  
  <!-- Drawer -->
  <div class="absolute right-0 top-0 h-full w-[400px] bg-bg-surface border-l border-border-default flex flex-col
    transform transition-transform duration-200 ease-in-out {open ? 'translate-x-0' : 'translate-x-full'}">
    
    <!-- Header -->
    <div class="flex items-center justify-between px-4 py-3 border-b border-border-default shrink-0">
      <h2 class="text-[13px] font-semibold text-text-primary">Settings & Info</h2>
      <button onclick={onClose} class="text-text-tertiary hover:text-text-primary transition-colors" aria-label="Close settings">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </button>
    </div>
    
    <!-- Tabs -->
    <div class="flex border-b border-border-default shrink-0">
      <button 
        class="flex-1 px-4 py-2 text-[11px] font-medium border-b-2 transition-colors {tab === 'harness' ? 'border-accent-primary text-text-primary' : 'border-transparent text-text-secondary hover:text-text-primary hover:bg-bg-surface-hover'}"
        onclick={() => tab = 'harness'}>
        Harness
      </button>
      <button 
        class="flex-1 px-4 py-2 text-[11px] font-medium border-b-2 transition-colors {tab === 'metrics' ? 'border-accent-primary text-text-primary' : 'border-transparent text-text-secondary hover:text-text-primary hover:bg-bg-surface-hover'}"
        onclick={() => tab = 'metrics'}>
        Metrics
      </button>
      <button 
        class="flex-1 px-4 py-2 text-[11px] font-medium border-b-2 transition-colors {tab === 'alerts' ? 'border-accent-primary text-text-primary' : 'border-transparent text-text-secondary hover:text-text-primary hover:bg-bg-surface-hover'}"
        onclick={() => tab = 'alerts'}>
        Alerts
      </button>
      <button 
        class="flex-1 px-4 py-2 text-[11px] font-medium border-b-2 transition-colors {tab === 'git' ? 'border-accent-primary text-text-primary' : 'border-transparent text-text-secondary hover:text-text-primary hover:bg-bg-surface-hover'}"
        onclick={() => tab = 'git'}>
        Git
      </button>
    </div>
    
    <!-- Content -->
    <div class="flex-1 overflow-y-auto p-4 space-y-6">
      {#if tab === 'harness'}
        <HarnessConfig />
      {:else if tab === 'metrics'}
        <Metrics 
          records={store.state.records} 
          workstations={store.state.workstations} 
          andonEvents={store.state.andon_events} 
          shippingEvents={store.state.shipping_events} 
        />
        <Changelog 
          records={store.state.records} 
          shippingEvents={store.state.shipping_events} 
        />
      {:else if tab === 'alerts'}
        <AndonBoard 
          records={store.state.records} 
          workstations={store.state.workstations} 
          andonEvents={store.state.andon_events} 
        />
      {:else if tab === 'git'}
        <GitPanel git={store.state.git} />
      {/if}
    </div>
  </div>
</div>
