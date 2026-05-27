<script lang="ts">
  import { Node, Anchor } from 'svelvet';
  import { apiUrl } from '../../api';

  let { node, position, connections = [], sessionId } = $props();

  let expanded = $state(false);
  let editing = $state(false);
  let draft = $state('');
  let saving = $state(false);

  function startEdit() {
    if (node.status !== 'active') return;
    draft = node.content.text ?? '';
    editing = true;
  }

  async function saveEdit() {
    if (!editing || saving) return;
    const next = draft;
    editing = false;
    if (next === (node.content.text ?? '')) return;
    saving = true;
    try {
      const response = await fetch(apiUrl(`/shaping/sessions/${sessionId}/nodes/${node.id}/edit`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: next })
      });
      if (!response.ok) {
        console.error('Error editing input node:', await response.text());
        editing = true;
      }
    } catch (err) {
      console.error('Error editing input node:', err);
      editing = true;
    } finally {
      saving = false;
    }
  }
</script>

<Node id={node.id} {position} let:selected>
  <div class="group relative bg-bg-surface border rounded-lg p-3 min-w-[200px] max-w-[300px] shadow-sm
    {selected ? 'ring-2 ring-accent-primary/50' : ''}
    {node.status === 'active' ? 'border-l-4 border-l-cyan-500 border-border-default opacity-100' : ''}
    {node.status === 'dead' ? 'border-l-4 border-l-red-500/50 border-border-subtle opacity-40 grayscale' : ''}
    {node.status === 'stale' ? 'border-l-4 border-l-cyan-500/50 border-dashed border-border-subtle opacity-60 animate-pulse' : ''}
  ">
    {#if node.status === 'active' && !editing}
      <button
        class="absolute right-2 top-2 opacity-0 group-hover:opacity-100 transition-opacity rounded border border-border-subtle bg-bg-primary/80 p-1 text-text-tertiary hover:text-text-primary"
        title="Edit input"
        onclick={startEdit}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
      </button>
    {/if}

    {#if editing}
      <textarea
        class="w-full min-h-24 resize-y rounded border border-cyan-500/40 bg-bg-primary p-2 text-[13px] text-text-primary outline-none focus:border-cyan-400"
        bind:value={draft}
        disabled={saving}
        onblur={saveEdit}
        onkeydown={(event) => {
          if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            saveEdit();
          }
        }}
      ></textarea>
    {:else}
      <div class="text-[13px] text-text-primary whitespace-pre-wrap break-words pr-5 {expanded ? '' : 'line-clamp-6'}">
        {node.content.text}
      </div>
    {/if}
    {#if node.status === 'stale'}
      <div class="mt-2 text-[10px] uppercase tracking-wide text-cyan-300/80">Regenerating...</div>
    {/if}
    
    {#if !editing && node.content.text && node.content.text.length > 200}
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
    {#if connections && connections.length > 0}
      <Anchor id="{node.id}-out" output {connections} />
    {:else}
      <Anchor id="{node.id}-out" output />
    {/if}
  </div>
</Node>
