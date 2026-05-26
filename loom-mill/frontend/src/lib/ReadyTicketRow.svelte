<script lang="ts">
  import type { LoomRecord } from './types';
  import { apiUrl } from './api';

  let {
    record,
    atWipLimit = false,
    focused = false,
    selected = false,
    onSelect = () => {}
  }: {
    record: LoomRecord;
    atWipLimit?: boolean;
    focused?: boolean;
    selected?: boolean;
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

  let error = $state('');

  async function startWorkstation(e: Event) {
    e.stopPropagation();
    if (starting || atWipLimit) return;

    starting = true;
    error = '';
    try {
      const response = await fetch(apiUrl('/workstations'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticket_id: ticketId(), ticket_path: record.path })
      });

      if (!response.ok) {
        let msg = `${response.status}: ${response.statusText}`;
        try {
          const body = await response.json();
          if (body.error) msg = body.error;
        } catch (e) {}
        throw new Error(msg);
      }
    } catch (err) {
      error = err instanceof Error ? err.message : 'Failed to start workstation';
      setTimeout(() => error = '', 5000);
    } finally {
      starting = false;
    }
  }
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div role="option" tabindex="-1" aria-selected={selected} class="group flex flex-col px-3 py-2 hover:bg-bg-surface-elevated transition-colors duration-150 cursor-pointer {focused ? 'outline outline-2 outline-accent-primary -outline-offset-2' : ''} {selected ? 'bg-bg-surface-active border-l-2 border-l-accent-primary' : 'border-l-2 border-l-transparent'}"
  onclick={onSelect}>
  <div class="flex items-center gap-2">
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
  {#if error}
    <div class="text-[10px] text-status-error-text mt-1 ml-4">{error}</div>
  {/if}
</div>
