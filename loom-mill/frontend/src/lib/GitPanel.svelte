<script lang="ts">
  import type { GitState } from './types';

  let { git }: { git: GitState } = $props();

  let commits = $derived(git.recent_commits.slice(0, 3));
</script>

<div class="flex flex-col gap-3 rounded-xl border border-slate-800 bg-slate-900/50 p-4">
  <div class="flex items-center justify-between">
    <h2 class="text-sm font-medium text-slate-400 uppercase tracking-wider">Git State</h2>
    {#if git.dirty}
      <span class="inline-flex items-center rounded-full bg-amber-400/10 px-2 py-0.5 text-xs font-medium text-amber-400 ring-1 ring-inset ring-amber-400/30">
        Dirty
      </span>
    {:else}
      <span class="inline-flex items-center rounded-full bg-emerald-400/10 px-2 py-0.5 text-xs font-medium text-emerald-400 ring-1 ring-inset ring-emerald-400/30">
        Clean
      </span>
    {/if}
  </div>

  <div class="flex items-center gap-2 text-sm">
    <svg class="h-4 w-4 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
    </svg>
    <span class="font-mono text-cyan-300">{git.current_branch || 'detached HEAD'}</span>
  </div>

  <div class="flex flex-col gap-1.5">
    {#each commits as commit}
      {@const [hash, ...msgParts] = commit.split(' ')}
      <div class="flex items-baseline gap-2 text-xs">
        <span class="font-mono text-slate-500">{hash}</span>
        <span class="truncate text-slate-300">{msgParts.join(' ')}</span>
      </div>
    {/each}
  </div>
</div>
