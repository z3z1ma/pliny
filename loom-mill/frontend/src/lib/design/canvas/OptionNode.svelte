<script lang="ts">
  import { Node, Anchor } from 'svelvet';

  let { node, position, connections = [], onSelect } = $props();
  
  let isSelected = $derived(node.status === 'active' && node.selected);
</script>

<Node id={node.id} {position} let:selected>
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div 
    class="border rounded-lg p-3 min-w-[200px] max-w-[280px] shadow-sm transition-all
      {selected ? 'ring-2 ring-accent-primary/50' : ''}
      {isSelected ? 'bg-accent-primary/10 border-accent-primary text-text-primary' : ''}
      {node.status === 'active' && !node.selected ? 'bg-bg-surface border-border-default hover:border-border-subtle cursor-pointer' : ''}
      {node.status === 'dead' ? 'bg-bg-surface border-red-500/30 opacity-40 grayscale cursor-not-allowed' : ''}
      {node.status === 'stale' ? 'bg-bg-surface border-dashed border-border-subtle opacity-60 animate-pulse cursor-not-allowed' : ''}
    "
    onclick={() => {
      if (node.status === 'active' && onSelect) {
        onSelect(node.id);
      }
    }}
  >
    <div class="flex items-start gap-2">
      <div class="mt-0.5 shrink-0">
        {#if isSelected}
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-accent-primary"><path d="M20 6 9 17l-5-5"/></svg>
        {:else if node.status === 'dead'}
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-red-400"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
        {:else}
          <div class="w-3.5 h-3.5 rounded-full border border-border-default"></div>
        {/if}
      </div>
      <div>
        <div class="text-[13px] font-medium {node.status === 'dead' ? 'line-through text-text-tertiary' : 'text-text-primary'}">
          {node.content.label}
        </div>
        {#if node.content.content}
          <div class="text-[11px] mt-1 {node.status === 'dead' ? 'text-text-tertiary' : 'text-text-secondary'}">
            {node.content.content}
          </div>
        {/if}
      </div>
    </div>
  </div>

  <div slot="anchorNorth">
    <Anchor id="{node.id}-in" input />
  </div>

  <div slot="anchorSouth">
    <Anchor id="{node.id}-out" output {connections} />
  </div>
</Node>
