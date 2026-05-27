<script lang="ts">
  import { Node, Anchor } from 'svelvet';

  let { node, position, connections = [], highlighted = false, onAccept, onReject, onEdit } = $props();

  let expanded = $state(false);
  let editing = $state(false);
  let editContent = $state('');
  let saving = $state(false);

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
    
    {#if editing}
      <div class="flex flex-col gap-2 mt-2">
        <textarea
          bind:value={editContent}
          class="w-full h-48 p-2 rounded border border-accent-primary/50 bg-bg-primary text-[12px] text-text-primary font-mono resize-y focus:outline-none focus:border-accent-primary"
        ></textarea>
        <div class="flex justify-end gap-2">
          <button
            class="px-2 py-1 text-[11px] rounded border border-border-default text-text-secondary hover:text-text-primary hover:bg-bg-surface-hover"
            onclick={() => { editing = false; editContent = node.content.content || ''; }}
            disabled={saving}
          >
            Cancel
          </button>
          <button
            class="px-2 py-1 text-[11px] rounded bg-accent-primary text-white hover:bg-accent-primary/90 disabled:opacity-50"
            onclick={async () => {
              if (!onEdit) return;
              saving = true;
              try {
                await onEdit(node.id, editContent);
                editing = false;
              } finally {
                saving = false;
              }
            }}
            disabled={saving || editContent === node.content.content}
          >
            {saving ? 'Saving...' : 'Save'}
          </button>
        </div>
      </div>
    {:else}
      <div class="text-[12px] text-text-secondary whitespace-pre-wrap break-words font-mono bg-bg-primary p-2 rounded mt-2 {expanded ? '' : 'line-clamp-6'}">
        {node.content.content}
      </div>
    {/if}
    
    {#if !editing && node.content.content && node.content.content.split('\n').length > 6}
      <button 
        class="text-[10px] text-text-tertiary hover:text-text-primary mt-1 w-full text-center py-1"
        onclick={() => expanded = !expanded}
      >
        {expanded ? 'Collapse' : 'Expand'}
      </button>
    {/if}
    
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
        <button 
          class="px-2 py-1.5 bg-bg-surface-hover text-text-secondary border border-border-default rounded hover:text-text-primary transition-colors text-[11px]"
          onclick={() => { editContent = node.content.content || ''; editing = true; }}
          title="Edit"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/></svg>
        </button>
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
