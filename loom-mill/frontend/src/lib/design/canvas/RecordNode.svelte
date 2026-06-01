<script lang="ts">
  import { Node, Anchor } from 'svelvet';
  import RecordModal from './RecordModal.svelte';

  let { node, position, connections = [], highlighted = false, onAccept, onReject, onEdit } = $props();

  let modalOpen = $state(false);

  let surfaceColor = $derived(() => {
    const s = node.content.surface?.toLowerCase() || '';
    if (s === 'tickets') return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
    if (s === 'specs') return 'bg-purple-500/20 text-purple-400 border-purple-500/30';
    if (s === 'plans') return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
    if (s === 'research') return 'bg-amber-500/20 text-amber-400 border-amber-500/30';
    return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
  });
</script>

<Node id={node.id} {position} let:selected>
  <div class="bg-bg-surface border rounded-lg p-3 min-w-[260px] max-w-[360px] shadow-sm transition-all
    {selected ? 'ring-2 ring-accent-primary/50' : ''}
    {highlighted ? 'ring-4 ring-accent-primary shadow-[0_0_30px_rgba(59,130,246,0.45)] animate-pulse' : ''}
      {node.status === 'active' ? 'border-border-default opacity-100' : ''}
    {node.status === 'accepted' ? 'border-l-4 border-l-green-500 border-border-default opacity-100' : ''}
    {node.status === 'rejected' ? 'border-l-4 border-l-red-500 border-border-subtle opacity-60 grayscale' : ''}
    {node.status === 'dead' ? 'border-l-4 border-l-red-500/50 border-border-subtle opacity-40 grayscale' : ''}
    {node.status === 'stale' ? 'border-dashed border-border-subtle opacity-60 animate-pulse' : ''}
  ">
    <div class="flex justify-between items-start mb-2">
      <div class="px-2 py-0.5 rounded text-[10px] font-medium border {surfaceColor()} uppercase tracking-wider">
        {node.content.surface || 'Record'}
      </div>
      {#if node.status === 'accepted'}
        <div class="text-green-500" title="Accepted">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
        </div>
      {:else if node.status === 'rejected'}
        <div class="text-red-500" title="Rejected">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
        </div>
      {/if}
    </div>
    
    <div class="text-[13px] font-bold text-text-primary mb-1 {node.status === 'rejected' ? 'line-through' : ''}">
      {node.content.title}
    </div>

    <div class="text-[11px] text-text-secondary line-clamp-2 mt-1">
      {(node.content.content || '').split('\n').find((l) => l.trim() && !l.startsWith('#')) || ''}
    </div>
    <button class="mt-2 text-[11px] text-accent-primary hover:underline" onclick={() => (modalOpen = true)}>Open document</button>
    
    {#if node.status === 'active'}
      <div class="flex gap-2 mt-3 pt-3 border-t border-border-subtle">
        <button
          class="flex-1 flex items-center justify-center gap-1 py-1.5 bg-green-500/10 text-green-500 border border-green-500/20 rounded hover:bg-green-500/20 transition-colors text-[11px]"
          onclick={() => onAccept && onAccept(node.id)}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
          Accept
        </button>
        <button
          class="flex-1 flex items-center justify-center gap-1 py-1.5 bg-red-500/10 text-red-500 border border-red-500/20 rounded hover:bg-red-500/20 transition-colors text-[11px]"
          onclick={() => onReject && onReject(node.id)}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
          Reject
        </button>
      </div>
    {/if}
  </div>

  <div slot="anchorNorth">
    <Anchor id="{node.id}-in" input />
  </div>

  <div slot="anchorSouth">
    {#if connections && connections.length > 0}
      <Anchor id="{node.id}-out" output {connections} edgeStyle="step" edgeColor="#52525b" />
    {:else}
      <Anchor id="{node.id}-out" output edgeStyle="step" edgeColor="#52525b" />
    {/if}
  </div>
</Node>

{#if modalOpen}
  <RecordModal {node} onClose={() => (modalOpen = false)} onSave={onEdit} />
{/if}
