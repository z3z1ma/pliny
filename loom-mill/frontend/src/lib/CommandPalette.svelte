<script lang="ts">
  import { onMount } from 'svelte';
  import type { LoomRecord, WorkstationState } from './types';

  let {
    open = $bindable(false),
    records,
    workstations,
    onSelectTicket,
    onSelectWorkstation,
    onToggleSettings,
    onToggleTheme
  }: {
    open: boolean;
    records: LoomRecord[];
    workstations: Record<string, WorkstationState>;
    onSelectTicket: (id: string) => void;
    onSelectWorkstation: (id: string) => void;
    onToggleSettings: () => void;
    onToggleTheme: () => void;
  } = $props();

  let search = $state('');
  let inputRef = $state<HTMLInputElement>();
  let selectedIndex = $state(0);

  let tickets = $derived(records.filter(r => r.metadata.type?.toLowerCase() === 'ticket' || r.path.includes('tickets/')));

  let actions = $derived(() => {
    const query = search.toLowerCase();
    const results = [];

    // Static actions
    if ('toggle settings'.toLowerCase().includes(query)) {
      results.push({ type: 'action', id: 'settings', label: 'Toggle Settings', action: onToggleSettings });
    }
    if ('toggle theme'.toLowerCase().includes(query)) {
      results.push({ type: 'action', id: 'theme', label: 'Toggle Theme', action: onToggleTheme });
    }

    // Workstations
    for (const [id, ws] of Object.entries(workstations)) {
      const slug = ws.ticket_slug || id;
      if (slug.toLowerCase().includes(query)) {
        results.push({ type: 'workstation', id, label: `Workstation: ${slug}`, action: () => onSelectWorkstation(id) });
      }
    }

    // Tickets
    for (const ticket of tickets) {
      const title = ticket.headings[0]?.[1] || ticket.metadata.id || ticket.path;
      if (title.toLowerCase().includes(query)) {
        results.push({ type: 'ticket', id: ticket.metadata.id || ticket.path, label: `Ticket: ${title}`, action: () => onSelectTicket(ticket.metadata.id || ticket.path) });
      }
    }

    return results;
  });

  $effect(() => {
    if (open) {
      search = '';
      selectedIndex = 0;
      setTimeout(() => inputRef?.focus(), 0);
    }
  });

  $effect(() => {
    // Reset selection when search changes
    search;
    selectedIndex = 0;
  });

  function handleKeydown(e: KeyboardEvent) {
    if (!open) return;

    const items = actions();
    if (e.key === 'Escape') {
      e.preventDefault();
      open = false;
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIndex = (selectedIndex + 1) % items.length;
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIndex = (selectedIndex - 1 + items.length) % items.length;
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (items[selectedIndex]) {
        items[selectedIndex].action();
        open = false;
      }
    } else if (e.key === 'Tab') {
      e.preventDefault(); // Trap focus
    }
  }

  function handleBackdropClick() {
    open = false;
  }
</script>

<svelte:window onkeydown={handleKeydown} />

{#if open}
  <div class="fixed inset-0 z-[100] flex items-start justify-center pt-[20vh]">
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" onclick={handleBackdropClick}></div>
    
    <div class="relative w-full max-w-xl rounded-xl border border-border-default bg-bg-surface shadow-2xl overflow-hidden flex flex-col max-h-[60vh]" role="dialog" aria-modal="true" aria-label="Command Palette">
      <div class="flex items-center border-b border-border-default px-4 py-3 shrink-0">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-text-tertiary mr-3"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        <input
          bind:this={inputRef}
          bind:value={search}
          type="text"
          class="flex-1 bg-transparent text-[14px] text-text-primary outline-none placeholder:text-text-tertiary"
          placeholder="Search tickets, workstations, or commands..."
        />
      </div>
      
      <div class="flex-1 overflow-y-auto p-2" role="listbox">
        {#each actions() as action, i}
          <!-- svelte-ignore a11y_click_events_have_key_events -->
          <!-- svelte-ignore a11y_no_static_element_interactions -->
          <div
            role="option"
            tabindex="-1"
            aria-selected={i === selectedIndex}
            class="flex items-center px-3 py-2 rounded-lg cursor-pointer text-[13px] {i === selectedIndex ? 'bg-accent-primary/10 text-accent-primary' : 'text-text-secondary hover:bg-bg-surface-hover'}"
            onclick={() => { action.action(); open = false; }}
            onmousemove={() => selectedIndex = i}
          >
            {#if action.type === 'action'}
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2 opacity-70"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
            {:else if action.type === 'workstation'}
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2 opacity-70"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>
            {:else}
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2 opacity-70"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
            {/if}
            <span class="truncate">{action.label}</span>
          </div>
        {/each}
        {#if actions().length === 0}
          <div class="px-3 py-4 text-center text-[12px] text-text-tertiary">
            No results found.
          </div>
        {/if}
      </div>
    </div>
  </div>
{/if}
