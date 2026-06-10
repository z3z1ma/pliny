<script lang="ts">
  import { Node, Anchor } from 'svelvet';
  import { branchEdgeColor } from './edge-style';

  let { node, position, connections = [], onSelect, onReselect, disabled = false, reselectDisabled = false } = $props();
  
  let isSelected = $derived(node.status === 'active' && node.selected);
  let isDisabledActive = $derived(disabled && node.status === 'active');
</script>

<Node id={node.id} {position} let:selected>
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div 
    class="border rounded-lg p-3 min-w-[200px] max-w-[280px] shadow-sm transition-all
      {selected ? 'ring-2 ring-accent-primary/50' : ''}
      {isSelected && !isDisabledActive ? 'bg-accent-primary/10 border-accent-primary text-text-primary' : ''}
      {node.status === 'active' && !node.selected && !disabled ? 'bg-bg-surface border-border-default hover:border-border-subtle cursor-pointer' : ''}
      {isDisabledActive ? 'bg-bg-surface border-border-subtle opacity-60 grayscale cursor-not-allowed' : ''}
      {node.status === 'dead' ? 'bg-bg-surface border-red-500/30 opacity-40 grayscale cursor-not-allowed' : ''}
      {node.status === 'stale' ? 'bg-bg-surface border-dashed border-border-subtle opacity-60 animate-pulse cursor-not-allowed' : ''}
    "
    onclick={() => {
      if (node.status === 'active' && !disabled && onSelect) {
        onSelect(node.id);
      }
    }}
  >
    <div class="flex items-start gap-2">
      <div class="mt-0.5 shrink-0">
        {#if isSelected}
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class={isDisabledActive ? 'text-text-tertiary' : 'text-accent-primary'}><path d="M20 6 9 17l-5-5"/></svg>
        {:else if node.status === 'dead'}
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-red-400"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
        {:else}
          <div class="w-3.5 h-3.5 rounded-full border border-border-default"></div>
        {/if}
      </div>
      <div class="min-w-0 flex-1">
        <div class="text-[13px] font-medium {node.status === 'dead' ? 'line-through text-text-tertiary' : isDisabledActive ? 'text-text-tertiary' : 'text-text-primary'}">
          {node.content.label}
        </div>
        {#if node.content.content}
          <div class="text-[11px] mt-1 {node.status === 'dead' || isDisabledActive ? 'text-text-tertiary' : 'text-text-secondary'}">
            {node.content.content}
          </div>
        {/if}
        {#if node.status === 'dead' && onReselect}
          <button
            class="mt-2 rounded border border-red-500/30 px-2 py-1 text-[10px] uppercase tracking-wide text-red-300 hover:bg-red-500/10"
            disabled={reselectDisabled}
            onclick={(event) => {
              event.stopPropagation();
              if (reselectDisabled) return;

              onReselect(node.id);
            }}
          >
            Re-select
          </button>
        {/if}
      </div>
    </div>
  </div>

  <div slot="anchorNorth">
    <Anchor id="{node.id}-in" input />
  </div>

  <div slot="anchorSouth">
    {#if connections && connections.length > 0}
      <Anchor id="{node.id}-out" output {connections} edgeColor={branchEdgeColor} />
    {:else}
      <Anchor id="{node.id}-out" output edgeColor={branchEdgeColor} />
    {/if}
  </div>
</Node>
