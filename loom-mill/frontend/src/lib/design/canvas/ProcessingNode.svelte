<script lang="ts">
  import { Node, Anchor } from 'svelvet';
  import { onMount, onDestroy } from 'svelte';
  import { apiUrl } from '../../api';
  import { store } from '../../ws.svelte.ts';

  let { node, position, connections = [] } = $props();

  let elapsed = $state(0);
  let timer: ReturnType<typeof setInterval>;

  onMount(() => {
    timer = setInterval(() => { elapsed++; }, 1000);
  });

  onDestroy(() => {
    if (timer) clearInterval(timer);
  });

  async function handleCancel() {
    const sessionId = store.shapingSession?.id;
    if (!sessionId) return;
    
    // Find the active exploration ID for this session
    // The backend endpoint is /shaping/sessions/{session_id}/explorations/{invocation_id}/cancel
    // But we don't have the invocation_id easily available in the node.
    // However, the backend might support cancelling the current advance.
    // Let's just call a generic cancel endpoint or the explorations list to find it.
    try {
      const res = await fetch(apiUrl(`/shaping/sessions/${sessionId}/explorations`));
      if (res.ok) {
        const explorations = await res.json();
        for (const exp of explorations) {
          await fetch(apiUrl(`/shaping/sessions/${sessionId}/explorations/${exp.invocation_id}/cancel`), {
            method: 'POST'
          });
        }
      }
    } catch (err) {
      console.error('Failed to cancel:', err);
    }
  }
</script>

<Node id={node.id} {position} let:selected>
  <div class="bg-bg-surface border border-accent-primary/50 rounded-lg p-3 min-w-[200px] shadow-sm animate-pulse flex flex-col gap-2
    {selected ? 'ring-2 ring-accent-primary/50' : ''}
  ">
    <div class="flex items-center justify-between gap-2">
      <div class="flex items-center gap-2">
        <div class="w-2 h-2 rounded-full bg-accent-primary animate-ping"></div>
        <div class="text-[12px] text-text-secondary italic">
          {node.content.message || 'Processing...'} {elapsed}s
        </div>
      </div>
      <button 
        class="text-[10px] px-1.5 py-0.5 bg-bg-secondary hover:bg-bg-tertiary rounded text-text-secondary hover:text-text-primary transition-colors"
        onclick={handleCancel}
      >
        Cancel
      </button>
    </div>
    {#if elapsed > 30}
      <div class="text-[10px] text-text-tertiary">
        This is taking longer than usual...
      </div>
    {/if}
  </div>

  <div slot="anchorNorth">
    <Anchor id="{node.id}-in" input />
  </div>

  <div slot="anchorSouth">
    {#if connections && connections.length > 0}
      <Anchor id="{node.id}-out" output {connections} />
    {:else}
      <Anchor id="{node.id}-out" output />
    {/if}
  </div>
</Node>
