<script lang="ts">
  import { Node, Anchor } from 'svelvet';

  let { node, position, connections = [] } = $props();
  
  let expanded = $state(false);
</script>

<Node id={node.id} {position} let:selected>
  <div class="bg-bg-surface border rounded-lg p-3 min-w-[200px] max-w-[300px] shadow-sm
    {selected ? 'ring-2 ring-accent-primary/50' : ''}
    {node.status === 'active' ? 'border-l-4 border-l-cyan-500 border-border-default opacity-100' : ''}
    {node.status === 'dead' ? 'border-l-4 border-l-red-500/50 border-border-subtle opacity-40 grayscale' : ''}
    {node.status === 'stale' ? 'border-l-4 border-l-cyan-500/50 border-dashed border-border-subtle opacity-60 animate-pulse' : ''}
  ">
    <div class="text-[13px] text-text-primary whitespace-pre-wrap break-words {expanded ? '' : 'line-clamp-6'}">
      {node.content.text}
    </div>
    
    {#if node.content.text && node.content.text.length > 200}
      <button 
        class="text-[10px] text-text-tertiary hover:text-text-primary mt-1 w-full text-center py-1"
        onclick={() => expanded = !expanded}
      >
        {expanded ? 'Collapse' : 'Expand'}
      </button>
    {/if}
  </div>

  <div slot="anchorNorth">
    {#if node.parent_id}
      <Anchor id="{node.id}-in" input />
    {/if}
  </div>

  <div slot="anchorSouth">
    <Anchor id="{node.id}-out" output {connections} />
  </div>
</Node>
