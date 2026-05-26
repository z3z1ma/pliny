<script lang="ts">
  import type { LoomRecord } from './types';

  let {
    record,
    atWipLimit = false,
    onSelect = () => {}
  }: {
    record: LoomRecord;
    atWipLimit?: boolean;
    onSelect?: () => void;
  } = $props();

  let starting = $state(false);

  let title = $derived(() => {
    if (record.headings.length > 0) {
      return record.headings[0][1];
    }
    return record.metadata.id || record.path;
  });

  let ticketId = $derived(() => {
    return (record.metadata.id || record.path.split('/').pop()?.replace(/\.md$/, '') || '').replace(/^ticket:/, '');
  });

  async function startWorkstation(e: Event) {
    e.stopPropagation();
    if (starting || atWipLimit) return;

    starting = true;
    try {
      const apiBase = `${window.location.protocol}//${window.location.hostname}:8765`;
      const response = await fetch(`${apiBase}/workstations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticket_id: ticketId(), ticket_path: record.path })
      });

      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw new Error(body.error || `HTTP ${response.status}`);
      }
    } catch (err) {
      starting = false;
      console.error('Failed to start workstation:', err);
    }
  }
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="group flex items-center gap-2 px-3 py-2 hover:bg-bg-surface-elevated transition-colors duration-150 cursor-pointer"
  onclick={onSelect}>
  <span class="w-2 h-2 rotate-45 border border-text-tertiary shrink-0"></span>
  <span class="flex-1 truncate text-[12px] text-text-secondary">{title()}</span>
  <button
    onclick={startWorkstation}
    disabled={starting || atWipLimit}
    title={atWipLimit ? 'WIP limit reached' : 'Start workstation'}
    class="flex items-center gap-1 rounded px-2 py-0.5 text-[10px] font-medium transition-colors duration-150
      {atWipLimit
        ? 'text-text-tertiary cursor-not-allowed'
        : 'text-accent-primary hover:bg-accent-primary/10 hover:text-accent-primary'}">
    {#if starting}
      <span class="animate-spin text-[10px]">↻</span>
    {:else}
      <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><polygon points="5 3 19 12 5 21 5 3" /></svg>
    {/if}
    Start
  </button>
</div>
