<script lang="ts">
  let { node, onClose, onSave } = $props();
  let editContent = $state(node.content.content ?? '');
  let saving = $state(false);
  let immutable = $derived(node.status !== 'active');
  let saveError = $state<string | null>(null);
</script>

<svelte:window onkeydown={(e) => { if (e.key === 'Escape') onClose(); }} />

<div class="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 backdrop-blur-sm"
  onclick={onClose} onkeydown={(e) => e.key === 'Escape' && onClose()} role="dialog" aria-modal="true">
  <div class="flex flex-col w-[720px] max-w-[92vw] max-h-[85vh] bg-bg-surface border border-border-default rounded-lg shadow-2xl overflow-hidden"
    onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()} role="document">
    <div class="flex items-center justify-between px-4 py-3 border-b border-border-subtle bg-bg-primary">
      <h3 class="text-sm font-bold text-text-primary">{node.content.title}</h3>
      <button class="p-1 text-text-tertiary hover:text-text-primary rounded transition-colors" onclick={onClose} aria-label="Close">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
      </button>
    </div>
    <div class="flex-1 overflow-auto p-4">
      <textarea bind:value={editContent}
        readonly={immutable}
        class="w-full h-[55vh] p-3 rounded border border-border-default bg-bg-primary text-[12px] font-mono text-text-primary resize-none focus:outline-none focus:border-accent-primary {immutable ? 'opacity-75 cursor-default' : ''}"></textarea>
      {#if saveError}
        <p class="mt-2 text-[11px] text-status-error-text">{saveError}</p>
      {/if}
      {#if immutable}
        <p class="mt-2 text-[11px] text-text-tertiary">Accepted or discarded records are locked. Reopen shaping from an active proposal to edit.</p>
      {/if}
    </div>
    <div class="flex items-center justify-end gap-2 px-4 py-3 border-t border-border-subtle bg-bg-primary">
      <button class="px-3 py-1.5 text-[12px] rounded border border-border-default text-text-secondary hover:text-text-primary" onclick={onClose}>Close</button>
      <button class="px-3 py-1.5 text-[12px] rounded bg-accent-primary text-white disabled:opacity-50"
        disabled={immutable || saving || editContent === node.content.content}
        onclick={async () => { if (!onSave || immutable) return; saveError = null; saving = true; try { const saved = await onSave(node.id, editContent); if (saved === false) saveError = 'Save failed. The staged record was not changed.'; else onClose(); } finally { saving = false; } }}>
        {saving ? 'Saving…' : 'Save'}
      </button>
    </div>
  </div>
</div>
