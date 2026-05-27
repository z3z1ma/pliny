<script lang="ts">
  import { Node, Anchor } from 'svelvet';
  import { apiUrl } from '../../api';
  import { store } from '../../ws.svelte.ts';

  let { node, position, connections = [], onOpenLogs } = $props();

  let elapsed = $state(0);
  let timer: ReturnType<typeof setInterval> | null = null;
  let invocationId = $derived(node.content.invocation_id as string | undefined);
  let explorationStatus = $derived(
    invocationId ? store.shapingSession?.explorationStatus?.[invocationId] : undefined
  );
  let isRunning = $derived(explorationStatus === 'running');
  let displayMessage = $derived(
    isRunning
      ? (node.content.message || 'Processing...')
      : explorationStatus === 'failed'
        ? 'Exploration ended'
        : 'Exploration completed'
  );

  $effect(() => {
    if (!isRunning) {
      if (timer) clearInterval(timer);
      timer = null;
      return;
    }

    elapsed = 0;
    timer = setInterval(() => { elapsed++; }, 1000);
    return () => {
      if (timer) clearInterval(timer);
      timer = null;
    };
  });

  async function handleCancel() {
    const sessionId = store.shapingSession?.id;
    if (!sessionId) return;
    
    try {
      if (node.content.invocation_id) {
        await fetch(apiUrl(`/shaping/sessions/${sessionId}/explorations/${node.content.invocation_id}/cancel`), {
          method: 'POST'
        });
      } else {
        const res = await fetch(apiUrl(`/shaping/sessions/${sessionId}/explorations`));
        if (res.ok) {
          const explorations = await res.json();
          for (const exp of explorations) {
            await fetch(apiUrl(`/shaping/sessions/${sessionId}/explorations/${exp.invocation_id}/cancel`), {
              method: 'POST'
            });
          }
        }
      }
    } catch (err) {
      console.error('Failed to cancel:', err);
    }
  }
</script>

<Node id={node.id} {position} let:selected>
  <div class="bg-bg-surface border rounded-lg p-3 min-w-[200px] shadow-sm flex flex-col gap-2
    {isRunning ? 'border-accent-primary/50 animate-pulse' : 'border-border-default opacity-80'}
    {selected ? 'ring-2 ring-accent-primary/50' : ''}
  ">
    <div class="flex items-center justify-between gap-2">
      <div class="flex items-center gap-2">
        <div class="w-2 h-2 rounded-full {isRunning ? 'bg-accent-primary animate-ping' : 'bg-text-muted'}"></div>
        <div class="text-[12px] text-text-secondary italic">
          {displayMessage}{isRunning ? ` ${elapsed}s` : ''}
        </div>
      </div>
      {#if isRunning}
        <button
          class="text-[10px] px-1.5 py-0.5 bg-bg-secondary hover:bg-bg-tertiary rounded text-text-secondary hover:text-text-primary transition-colors"
          onclick={handleCancel}
        >
          Cancel
        </button>
      {/if}
    </div>
    {#if isRunning && invocationId}
      <button
        class="text-[10px] text-left text-blue-400 hover:text-blue-300 transition-colors flex items-center gap-1"
        onclick={() => onOpenLogs?.(invocationId)}
      >
        View logs
      </button>
    {/if}
    {#if isRunning && elapsed > 30}
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
