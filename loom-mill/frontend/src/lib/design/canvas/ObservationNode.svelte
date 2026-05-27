<script lang="ts">
  import { Node, Anchor } from 'svelvet';

  let { node, position, connections = [] } = $props();
  
  let expanded = $state(false);
</script>

<Node id={node.id} {position} let:selected>
  <div class="bg-bg-surface border rounded-lg p-3 min-w-[220px] max-w-[320px] shadow-sm
    {selected ? 'ring-2 ring-accent-primary/50' : ''}
    {node.status === 'active' ? 'border-l-4 border-l-green-500 border-border-default opacity-100' : ''}
    {node.status === 'dead' ? 'border-l-4 border-l-red-500/50 border-border-subtle opacity-40 grayscale' : ''}
    {node.status === 'stale' ? 'border-l-4 border-l-green-500/50 border-dashed border-border-subtle opacity-60 animate-pulse' : ''}
  ">
    <div class="text-[11px] font-semibold text-green-400 mb-1 uppercase tracking-wider flex justify-between items-center">
      <span>Observation</span>
    </div>
    
    <div class="text-[12px] text-text-secondary whitespace-pre-wrap break-words {expanded ? '' : 'line-clamp-4'}">
      {node.content.observation}
    </div>
    
    {#if node.content.observation.length > 150 || node.content.evidence}
      <button 
        class="text-[10px] text-text-tertiary hover:text-text-primary mt-2 flex items-center gap-1"
        onclick={() => expanded = !expanded}
      >
        {expanded ? 'Show less' : 'Show more'}
        <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="transition-transform {expanded ? 'rotate-180' : ''}"><path d="m6 9 6 6 6-6"/></svg>
      </button>
    {/if}
    
    {#if expanded && node.content.evidence}
      <div class="mt-3 pt-2 border-t border-border-subtle">
        <div class="text-[10px] text-text-tertiary mb-1">Evidence:</div>
        <div class="text-[11px] font-mono text-text-secondary bg-bg-primary p-2 rounded overflow-x-auto">
          {node.content.evidence}
        </div>
      </div>
    {/if}
  </div>

  <div slot="anchorNorth">
    <Anchor id="{node.id}-in" input />
  </div>

  <div slot="anchorSouth">
    <Anchor id="{node.id}-out" output {connections} />
  </div>
</Node>
