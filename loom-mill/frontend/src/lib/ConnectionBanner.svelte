<script lang="ts">
  import { store } from './ws.svelte.ts';
</script>

{#if !store.connected}
  <div class="flex items-center justify-between bg-status-error-bg px-4 py-2 text-xs text-status-error-text border-b border-status-error-border shrink-0">
    <div class="flex items-center gap-2">
      <span class="relative flex h-2 w-2">
        <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-status-error-text opacity-75"></span>
        <span class="relative inline-flex h-2 w-2 rounded-full bg-status-error-text"></span>
      </span>
      <span>
        Disconnected. 
        {#if store.reconnecting}
          Reconnecting (attempt {store.reconnectAttempt})...
        {:else if store.error}
          {store.error}
        {/if}
      </span>
    </div>
    {#if store.error}
      <button 
        onclick={() => store.retry()}
        class="rounded bg-status-error-text px-2 py-1 text-[10px] font-medium text-white hover:opacity-90 transition-opacity"
      >
        Retry Connection
      </button>
    {/if}
  </div>
{/if}