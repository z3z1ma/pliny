<script lang="ts">
  import { Node, Anchor } from 'svelvet';
  import { causalEdgeColor } from './edge-style';

  let { node, position, connections = [], onContinue, continueDisabled = false } = $props();

  let text = $derived(node.content.tension || node.content.text || 'No content');
</script>

<Node id={node.id} {position} let:selected>
  <div class="bg-bg-surface border border-l-4 border-l-amber-500 rounded-lg p-3 min-w-[220px] max-w-[320px] shadow-sm
    {selected ? 'ring-2 ring-accent-primary/50' : ''}
    {node.status === 'dead' ? 'opacity-40 grayscale' : ''}
    {node.status === 'stale' ? 'border-dashed opacity-60 animate-pulse' : ''}">
    <div class="text-[11px] font-semibold text-amber-400 mb-1 uppercase tracking-wider">⚠ Tension</div>
    <div class="text-[12px] text-text-secondary whitespace-pre-wrap break-words">{text}</div>
    {#if node.status === 'active'}
      <button class="mt-2 text-[10px] text-amber-400 hover:text-amber-300 disabled:opacity-50 disabled:cursor-not-allowed"
        disabled={continueDisabled}
        onclick={() => onContinue && onContinue(node.id)}>Continue from here →</button>
    {/if}
  </div>

  <div slot="anchorNorth">
    <Anchor id="{node.id}-in" input />
  </div>

  <div slot="anchorSouth">
    {#if connections && connections.length > 0}
      <Anchor id="{node.id}-out" output {connections} edgeColor={causalEdgeColor} />
    {:else}
      <Anchor id="{node.id}-out" output edgeColor={causalEdgeColor} />
    {/if}
  </div>
</Node>
