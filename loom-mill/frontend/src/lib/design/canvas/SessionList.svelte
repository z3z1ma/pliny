<script lang="ts">
  import { onMount } from 'svelte';
  import { apiUrl } from '../../api';

  let { onSelectSession, onNewSession }: {
    onSelectSession: (sessionId: string) => void;
    onNewSession: () => void;
  } = $props();

  type SessionSummary = {
    id: string;
    created_at: string;
    seed_text: string;
    node_count: number;
    status: string;
  };

  let sessions = $state<SessionSummary[]>([]);
  let loading = $state(true);

  function relativeDate(value: string) {
    const created = new Date(value);
    if (Number.isNaN(created.getTime())) return 'Unknown date';

    const diffMs = Date.now() - created.getTime();
    const minutes = Math.floor(diffMs / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (minutes < 1) return 'just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days === 1) return 'yesterday';
    if (days < 7) return `${days}d ago`;

    return created.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  }

  onMount(async () => {
    try {
      const res = await fetch(apiUrl('/shaping/sessions'));
      if (res.ok) sessions = await res.json();
    } finally {
      loading = false;
    }
  });
</script>

<div class="flex h-full w-full items-center justify-center bg-bg-primary p-8">
  <div class="flex w-full max-w-3xl flex-col gap-5">
    <div>
      <h2 class="text-lg font-semibold text-text-primary">Shaping Sessions</h2>
      <p class="mt-1 text-[12px] text-text-tertiary">
        Browse prior decision trees, resume active work, or start a fresh shaping session.
      </p>
    </div>

    <button
      onclick={onNewSession}
      class="group flex w-full items-center gap-4 rounded-lg border border-accent-primary/40 bg-accent-primary/10 p-4 text-left transition-colors hover:border-accent-primary hover:bg-accent-primary/15"
    >
      <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-accent-primary text-xl leading-none text-white shadow-sm">+</span>
      <span class="flex flex-col gap-1">
        <span class="text-[13px] font-semibold text-text-primary">Start new session</span>
        <span class="text-[12px] text-text-tertiary">Begin from a new seed input without losing existing sessions.</span>
      </span>
    </button>

    {#if loading}
      <div class="flex flex-col gap-3">
        {#each [1, 2, 3] as item}
          <div class="rounded-lg border border-border-default bg-bg-surface p-4" aria-label="Loading session">
            <div class="h-4 w-3/4 rounded bg-bg-surface-hover"></div>
            <div class="mt-3 flex items-center gap-2">
              <div class="h-5 w-16 rounded-full bg-bg-surface-hover"></div>
              <div class="h-5 w-20 rounded-full bg-bg-surface-hover"></div>
            </div>
          </div>
        {/each}
      </div>
    {:else if sessions.length === 0}
      <div class="rounded-lg border border-border-default bg-bg-surface p-6 text-center">
        <p class="text-[13px] text-text-secondary">No sessions yet. Start your first one.</p>
      </div>
    {:else}
      <div class="flex flex-col gap-3">
        {#each sessions as session}
          <button
            onclick={() => onSelectSession(session.id)}
            class="flex w-full items-center justify-between gap-4 rounded-lg border border-border-default bg-bg-surface p-4 text-left shadow-sm transition-colors hover:border-accent-primary/60 hover:bg-bg-surface-hover"
          >
            <span class="min-w-0 flex-1">
              <span class="block truncate text-[13px] font-medium text-text-primary">
                {session.seed_text || 'Untitled shaping session'}
              </span>
              <span class="mt-2 flex items-center gap-2 text-[11px] text-text-tertiary">
                <span>{relativeDate(session.created_at)}</span>
                <span aria-hidden="true">/</span>
                <span class="inline-flex items-center gap-1 capitalize">
                  <span class="h-2 w-2 rounded-full {session.status === 'active' ? 'bg-green-500' : 'bg-text-tertiary'}"></span>
                  {session.status}
                </span>
              </span>
            </span>
            <span class="shrink-0 rounded-full border border-border-default bg-bg-primary px-2.5 py-1 text-[11px] font-medium text-text-secondary">
              {session.node_count} {session.node_count === 1 ? 'node' : 'nodes'}
            </span>
          </button>
        {/each}
      </div>
    {/if}
  </div>
</div>
