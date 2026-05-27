<script lang="ts">
  import type { StagedRecord } from '../types';
  import { apiUrl } from '../api';

  let { proposal, sessionId }: { proposal: StagedRecord, sessionId: string } = $props();

  let expanded = $state(false);
  let editing = $state(false);
  let editContent = $state('');
  let saving = $state(false);

  function surfaceColor(surface: string) {
    switch (surface) {
      case 'tickets': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      case 'specs': return 'bg-purple-500/20 text-purple-400 border-purple-500/30';
      case 'plans': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
      case 'research': return 'bg-amber-500/20 text-amber-400 border-amber-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  }

  function surfaceIcon(surface: string) {
    switch (surface) {
      case 'tickets': return '🎫';
      case 'specs': return '📐';
      case 'plans': return '📊';
      case 'research': return '🔬';
      default: return '📄';
    }
  }

  let previewContent = $derived(() => {
    const lines = proposal.content.split('\n');
    return lines.slice(0, 8).join('\n') + (lines.length > 8 ? '\n...' : '');
  });

  async function handleAction(action: 'accept' | 'reject') {
    try {
      await fetch(apiUrl(`/shaping/sessions/${sessionId}/records/${proposal.temp_id}/${action}`), {
        method: 'POST'
      });
      // State updates will come via WS
    } catch (err) {
      console.error(`Failed to ${action} proposal:`, err);
    }
  }

  async function handleSaveEdit() {
    saving = true;
    try {
      await fetch(apiUrl(`/shaping/sessions/${sessionId}/records/${proposal.temp_id}`), {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: editContent })
      });
      editing = false;
    } catch (err) {
      console.error('Failed to save edit:', err);
    } finally {
      saving = false;
    }
  }
</script>

<div data-temp-id={proposal.temp_id} class="border border-border-default rounded bg-bg-surface overflow-hidden flex flex-col transition-all {proposal.status === 'accepted' ? 'border-l-4 border-l-status-success-border' : ''} {proposal.status === 'rejected' ? 'opacity-50 grayscale' : ''}">
  <!-- Header -->
  <div class="flex items-center justify-between p-2 border-b border-border-subtle bg-bg-surface-hover">
    <div class="flex items-center gap-2">
      <span class="px-2 py-0.5 text-[10px] font-medium rounded border {surfaceColor(proposal.surface)} flex items-center gap-1">
        <span>{surfaceIcon(proposal.surface)}</span>
        {proposal.surface}
      </span>
      <span class="text-[12px] font-medium text-text-primary truncate max-w-[200px]" title={proposal.title}>
        {proposal.title}
      </span>
    </div>
    <div class="text-[10px] text-text-tertiary font-mono">
      {proposal.temp_id}
    </div>
  </div>

  <!-- Content -->
  <div class="p-3">
    {#if editing}
      <div class="flex flex-col gap-2">
        <textarea 
          bind:value={editContent}
          class="w-full h-64 p-2 rounded border border-border-default bg-bg-primary text-[12px] text-text-primary font-mono resize-y focus:outline-none focus:border-accent-primary"
        ></textarea>
        <div class="flex justify-end gap-2">
          <button 
            class="px-3 py-1 text-[11px] rounded hover:bg-bg-surface-hover text-text-secondary"
            onclick={() => { editing = false; editContent = proposal.content; }}
          >
            Cancel
          </button>
          <button 
            class="px-3 py-1 text-[11px] rounded bg-accent-primary text-white hover:bg-accent-primary/90 disabled:opacity-50"
            onclick={handleSaveEdit}
            disabled={saving || editContent === proposal.content}
          >
            {saving ? 'Saving...' : 'Save'}
          </button>
        </div>
      </div>
    {:else}
      <div class="text-[11px] font-mono text-text-secondary whitespace-pre-wrap relative">
        {expanded ? proposal.content : previewContent()}
        
        {#if proposal.content.split('\n').length > 8}
          <button 
            class="absolute bottom-0 right-0 bg-bg-surface px-2 py-0.5 text-[10px] text-accent-primary hover:text-accent-primary-hover rounded shadow-sm border border-border-subtle"
            onclick={() => expanded = !expanded}
          >
            {expanded ? 'Show less' : 'Show more'}
          </button>
        {/if}
      </div>
    {/if}
  </div>

  <!-- Actions -->
  {#if proposal.status === 'proposed' && !editing}
    <div class="flex items-center gap-2 p-2 border-t border-border-subtle bg-bg-primary">
      <button 
        class="flex-1 py-1.5 text-[11px] font-medium rounded bg-status-success-bg/20 text-status-success-text hover:bg-status-success-bg/30 border border-status-success-border/30 transition-colors"
        onclick={() => handleAction('accept')}
      >
        ✓ Accept
      </button>
      <button 
        class="flex-1 py-1.5 text-[11px] font-medium rounded bg-status-error-bg/20 text-status-error-text hover:bg-status-error-bg/30 border border-status-error-border/30 transition-colors"
        onclick={() => handleAction('reject')}
      >
        ✗ Reject
      </button>
      <button 
        class="flex-1 py-1.5 text-[11px] font-medium rounded bg-bg-surface-hover text-text-secondary hover:text-text-primary border border-border-default transition-colors"
        onclick={() => { editContent = proposal.content; editing = true; }}
      >
        ✎ Edit
      </button>
    </div>
  {:else if proposal.status !== 'proposed' && !editing}
    <div class="flex items-center justify-between p-2 border-t border-border-subtle bg-bg-primary">
      <span class="text-[11px] font-medium {proposal.status === 'accepted' ? 'text-status-success-text' : 'text-status-error-text'}">
        {proposal.status === 'accepted' ? '✓ Accepted' : '✗ Rejected'}
      </span>
      <button 
        class="text-[10px] text-text-tertiary hover:text-text-secondary underline"
        onclick={() => handleAction('proposed' as any)} // Reset to proposed
      >
        Undo
      </button>
    </div>
  {/if}
</div>
