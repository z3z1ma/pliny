<script lang="ts">
  import { store } from '../../ws.svelte.ts';
  
  let { invocationId, sessionId, onClose }: {
    invocationId: string | null;
    sessionId: string;
    onClose: () => void;
  } = $props();
  
  // Get log lines from store
  let lines = $derived(
    store.shapingSession?.explorationLogs?.[invocationId ?? ''] ?? []
  );

  let status = $derived(
    store.shapingSession?.explorationStatus?.[invocationId ?? ''] ?? 'unknown'
  );

  // If status is unknown and no lines, the subprocess is not active (old session)
  let displayStatus = $derived(
    status === 'unknown'
      ? (lines.length > 0 ? 'completed' : 'inactive')
      : status
  );
  
  let logContainer: HTMLDivElement;
  let autoScroll = $state(true);
  
  // Auto-scroll to bottom when new lines arrive
  $effect(() => {
    if (lines.length && autoScroll && logContainer) {
      logContainer.scrollTop = logContainer.scrollHeight;
    }
  });

  function handleScroll() {
    if (!logContainer) return;
    const { scrollTop, scrollHeight, clientHeight } = logContainer;
    // If we scroll up, disable auto-scroll. If we scroll to bottom, enable it.
    const isAtBottom = Math.abs(scrollHeight - clientHeight - scrollTop) < 10;
    autoScroll = isAtBottom;
  }
</script>

<div class="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 backdrop-blur-sm" onclick={onClose} onkeydown={(e) => e.key === 'Escape' && onClose()} role="dialog" aria-modal="true">
  <div 
    class="flex flex-col w-[80%] h-[70%] bg-[#0d1117] border border-border-primary rounded-lg shadow-2xl overflow-hidden"
    onclick={(e) => e.stopPropagation()}
    onkeydown={(e) => e.stopPropagation()}
    role="document"
  >
    <!-- Header -->
    <div class="flex items-center justify-between px-4 py-3 border-b border-border-primary bg-bg-primary">
      <div class="flex items-center gap-3">
        <h3 class="text-sm font-medium text-text-primary">Harness Output</h3>
        <span class="text-xs text-text-muted font-mono">{invocationId}</span>
      </div>
      <button 
        class="p-1 text-text-muted hover:text-text-primary hover:bg-bg-secondary rounded transition-colors"
        onclick={onClose}
        aria-label="Close logs"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
      </button>
    </div>

    <!-- Logs Area -->
    <div 
      bind:this={logContainer}
      onscroll={handleScroll}
      class="flex-1 overflow-y-auto p-4 font-mono text-[12px] leading-relaxed text-green-400/90"
    >
      {#if lines.length === 0 && displayStatus === 'inactive'}
        <div class="text-text-muted italic">No output captured for this exploration. The subprocess is no longer running.</div>
      {:else if lines.length === 0 && displayStatus === 'running'}
        <div class="text-text-muted italic">Waiting for output...</div>
      {:else if lines.length === 0}
        <div class="text-text-muted italic">No output captured.</div>
      {:else}
        {#each lines as line}
          <div class="whitespace-pre-wrap break-words">{line}</div>
        {/each}
      {/if}
    </div>

    <!-- Footer -->
    <div class="flex items-center justify-between px-4 py-2 border-t border-border-primary bg-bg-primary text-xs text-text-muted">
      <div class="flex items-center gap-4">
        <span>{lines.length} lines</span>
        <span class="flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full {displayStatus === 'running' ? 'bg-blue-500 animate-pulse' : displayStatus === 'completed' ? 'bg-green-500' : displayStatus === 'inactive' ? 'bg-gray-500' : 'bg-red-500'}"></span>
          <span class="capitalize">{displayStatus}</span>
        </span>
      </div>
      <div class="flex items-center gap-2">
        <label class="flex items-center gap-2 cursor-pointer hover:text-text-primary transition-colors">
          <input type="checkbox" bind:checked={autoScroll} class="rounded border-border-primary bg-bg-secondary text-blue-500 focus:ring-blue-500 focus:ring-offset-bg-primary" />
          Auto-scroll
        </label>
      </div>
    </div>
  </div>
</div>
