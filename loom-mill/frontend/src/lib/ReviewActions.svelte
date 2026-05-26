<script lang="ts">
  import { apiUrl } from './api';

  let { recordId, onTransition }: { recordId: string; onTransition?: () => void } = $props();

  let notes = $state('');
  let loading = $state(false);
  let error = $state<string | null>(null);
  let success = $state<string | null>(null);

  async function transition(action: 'accept' | 'escalate' | 'request_change') {
    loading = true;
    error = null;
    success = null;
    try {
      const res = await fetch(apiUrl(`/records/${encodeURIComponent(recordId)}/transition`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action, notes })
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        error = data.error || 'Failed';
        return;
      }
      notes = '';
      success = 'Transition saved.';
      onTransition?.();
    } catch (err) {
      error = err instanceof Error ? err.message : 'Failed';
    } finally {
      loading = false;
    }
  }
</script>

<section class="mt-4 border-t border-border-subtle pt-3">
  <div class="mb-2 flex items-center justify-between gap-2">
    <h3 class="text-[11px] font-semibold uppercase tracking-wider text-text-secondary">Review Actions</h3>
    {#if loading}
      <span class="text-[10px] text-text-tertiary">Saving...</span>
    {/if}
  </div>
  <textarea
    bind:value={notes}
    disabled={loading}
    placeholder="Notes (optional) - what still needs to be done?"
    rows="3"
    class="w-full resize-none rounded-md border border-border-subtle bg-bg-surface px-2 py-1.5 text-[11px] text-text-primary placeholder:text-text-tertiary focus:border-accent-primary focus:outline-none disabled:cursor-not-allowed disabled:opacity-60"
  ></textarea>
  <div class="mt-2 flex flex-wrap gap-2">
    <button
      type="button"
      disabled={loading}
      class="rounded px-2.5 py-1 text-[11px] font-medium bg-status-success-bg text-status-success-text hover:bg-status-success-bg/80 disabled:cursor-not-allowed disabled:opacity-60"
      onclick={() => transition('accept')}
    >
      Accept
    </button>
    <button
      type="button"
      disabled={loading}
      class="rounded px-2.5 py-1 text-[11px] font-medium bg-status-warning-bg text-status-warning-text hover:bg-status-warning-bg/80 disabled:cursor-not-allowed disabled:opacity-60"
      onclick={() => transition('escalate')}
    >
      Escalate
    </button>
    <button
      type="button"
      disabled={loading}
      class="rounded px-2.5 py-1 text-[11px] font-medium bg-bg-surface-active text-text-secondary hover:bg-bg-surface-hover disabled:cursor-not-allowed disabled:opacity-60"
      onclick={() => transition('request_change')}
    >
      Request Change
    </button>
  </div>
  {#if error}
    <p class="mt-2 text-[11px] text-status-error-text">{error}</p>
  {:else if success}
    <p class="mt-2 text-[11px] text-status-success-text">{success}</p>
  {/if}
</section>
