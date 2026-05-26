<script lang="ts">
  import { onMount } from 'svelte';
  import type { IterationRecord } from './types';
  import DiffViewer from './DiffViewer.svelte';
  import { store } from './ws.svelte.ts';
  import { formatDuration } from './utils';
  import { apiUrl } from './api';

  let { workstationId, onClose, embedded = false }: { workstationId: string; onClose: () => void; embedded?: boolean } = $props();

  let iterations = $state<IterationRecord[]>([]);
  let currentStep = $state<number>(-1); // -1 means aggregate view
  let currentDiff = $state<string>('');
  let loading = $state(true);
  let error = $state('');

  async function fetchIterations() {
    loading = true;
    error = '';
    try {
      const res = await fetch(apiUrl(`/workstations/${workstationId}/iterations`));
      if (!res.ok) throw new Error('Failed to fetch iterations');
      iterations = await res.json();
      if (iterations.length > 0) {
        // Default to aggregate view
        await loadDiff(-1);
      }
    } catch (err: any) {
      error = err.message;
    } finally {
      loading = false;
    }
  }

  async function loadDiff(step: number) {
    loading = true;
    error = '';
    currentStep = step;
    try {
      let url = '';
      if (step === -1) {
        url = apiUrl(`/workstations/${workstationId}/diff`);
      } else {
        const iteration = iterations[step];
        url = apiUrl(`/workstations/${workstationId}/iterations/${iteration.iteration}/diff`);
      }
      
      const res = await fetch(url);
      if (!res.ok) {
        if (res.status === 404) {
          currentDiff = ''; // No diff
        } else {
          throw new Error('Failed to fetch diff');
        }
      } else {
        currentDiff = await res.text();
      }
    } catch (err: any) {
      error = err.message;
      currentDiff = '';
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    fetchIterations();
  });

  function next() {
    if (currentStep < iterations.length - 1) {
      loadDiff(currentStep + 1);
    }
  }

  function prev() {
    if (currentStep > -1) {
      loadDiff(currentStep - 1);
    }
  }

  function jumpToFirst() {
    if (iterations.length > 0) {
      loadDiff(0);
    }
  }

  function jumpToLast() {
    if (iterations.length > 0) {
      loadDiff(iterations.length - 1);
    }
  }

  function jumpToAggregate() {
    loadDiff(-1);
  }

  let currentSignal = $derived(() => {
    if (currentStep === -1 || !iterations[currentStep]) return null;
    const iterationNum = iterations[currentStep].iteration;
    const workstation = store.state.workstations[workstationId];
    if (!workstation || !workstation.backpressure_signals) return null;
    return workstation.backpressure_signals.find(s => s.iteration_index === iterationNum) || null;
  });
</script>

<div class={embedded ? "flex h-full w-full flex-col overflow-hidden bg-bg-primary" : "fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-6"}>
  <div class={embedded ? "flex h-full w-full flex-col overflow-hidden" : "flex h-full w-full max-w-6xl flex-col overflow-hidden rounded-lg border border-border-strong bg-bg-primary shadow-2xl"}>
    <!-- Header -->
    {#if !embedded}
    <div class="flex items-center justify-between border-b border-border-default bg-bg-surface px-4 py-3">
      <div class="flex items-center gap-3">
        <h2 class="text-sm font-semibold text-text-primary">Playback: {workstationId}</h2>
        <span class="badge bg-bg-surface-active text-text-secondary border border-border-subtle">
          {iterations.length} iterations
        </span>
      </div>
      <button 
        class="rounded p-1 text-text-tertiary hover:bg-bg-surface-hover hover:text-text-primary transition-colors"
        onclick={onClose}
        aria-label="Close"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </button>
    </div>
    {/if}

    <!-- Timeline Scrubber -->
    <div class="border-b border-border-default bg-bg-surface-elevated px-4 py-3">
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center gap-2">
          <button onclick={jumpToAggregate} class="rounded px-2 py-1 text-xs font-medium transition-colors {currentStep === -1 ? 'bg-accent-primary text-white' : 'bg-bg-surface-active text-text-secondary hover:text-text-primary'}">
            Aggregate
          </button>
          <div class="h-4 w-[1px] bg-border-default mx-1"></div>
          <button onclick={jumpToFirst} disabled={iterations.length === 0 || currentStep === 0} class="rounded p-1 text-text-secondary hover:bg-bg-surface-hover hover:text-text-primary disabled:opacity-50 disabled:cursor-not-allowed" title="First">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="19 20 9 12 19 4 19 20"></polygon><line x1="5" y1="19" x2="5" y2="5"></line></svg>
          </button>
          <button onclick={prev} disabled={currentStep <= -1} class="rounded p-1 text-text-secondary hover:bg-bg-surface-hover hover:text-text-primary disabled:opacity-50 disabled:cursor-not-allowed" title="Previous">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="15 18 9 12 15 6 15 18"></polygon></svg>
          </button>
          <span class="text-xs font-mono text-text-secondary min-w-[60px] text-center">
            {currentStep === -1 ? 'All' : `${currentStep + 1} / ${iterations.length}`}
          </span>
          <button onclick={next} disabled={currentStep >= iterations.length - 1} class="rounded p-1 text-text-secondary hover:bg-bg-surface-hover hover:text-text-primary disabled:opacity-50 disabled:cursor-not-allowed" title="Next">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="9 18 15 12 9 6 9 18"></polygon></svg>
          </button>
          <button onclick={jumpToLast} disabled={iterations.length === 0 || currentStep === iterations.length - 1} class="rounded p-1 text-text-secondary hover:bg-bg-surface-hover hover:text-text-primary disabled:opacity-50 disabled:cursor-not-allowed" title="Last">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 4 15 12 5 20 5 4"></polygon><line x1="19" y1="5" x2="19" y2="19"></line></svg>
          </button>
        </div>
        
        {#if currentStep > -1 && iterations[currentStep]}
          {@const it = iterations[currentStep]}
          {@const signal = currentSignal()}
          <div class="flex items-center gap-4 text-xs">
            <span class="text-text-tertiary">Duration: <span class="text-text-primary font-mono">{formatDuration(it.duration_seconds)}</span></span>
            <span class="text-text-tertiary">Exit: <span class="text-text-primary font-mono">{it.exit_code ?? 'unknown'}</span></span>
            <span class="text-text-tertiary">Files: <span class="text-text-primary font-mono">{it.files_changed.length}</span></span>
            <span class="text-text-tertiary">Lines: <span class="text-status-success-text font-mono">+{it.lines_added}</span> <span class="text-status-error-text font-mono">-{it.lines_removed}</span></span>
            {#if it.commit_sha}
              <span class="text-text-tertiary">Commit: <span class="text-text-primary font-mono">{it.commit_sha.substring(0, 7)}</span></span>
            {/if}
            {#if signal}
              <span class="badge bg-status-warning-bg text-status-warning-text ring-1 ring-inset ring-status-warning-border" title={signal.message}>
                SPC: {signal.kind}
              </span>
            {/if}
          </div>
        {/if}
      </div>

      <!-- Timeline visual -->
      {#if iterations.length > 0}
        <div class="relative flex items-center h-6 mt-2">
          <div class="absolute left-0 right-0 h-0.5 bg-border-default rounded"></div>
          <div class="absolute left-0 h-0.5 bg-accent-primary rounded transition-all duration-300" style="width: {currentStep === -1 ? '100%' : `${(currentStep / (iterations.length - 1 || 1)) * 100}%`}"></div>
          
          {#each iterations as it, i}
            {@const hasSignal = store.state.workstations[workstationId]?.backpressure_signals?.some(s => s.iteration_index === it.iteration)}
            <button 
              class="absolute w-3 h-3 -ml-1.5 rounded-full border-2 transition-all duration-200 
                {currentStep === i ? (hasSignal ? 'bg-status-warning-text border-bg-surface scale-125 z-10' : 'bg-accent-primary border-bg-surface scale-125 z-10') 
                 : currentStep > i || currentStep === -1 ? (hasSignal ? 'bg-status-warning-text border-bg-surface' : 'bg-accent-primary border-bg-surface') 
                 : (hasSignal ? 'bg-bg-surface border-status-warning-text hover:border-status-warning-text' : 'bg-bg-surface border-border-strong hover:border-accent-subtle')}"
              style="left: {iterations.length === 1 ? '50%' : `${(i / (iterations.length - 1)) * 100}%`}"
              onclick={() => loadDiff(i)}
              title="Iteration {it.iteration}{hasSignal ? ' (SPC Signal)' : ''}"
            ></button>
          {/each}
        </div>
      {/if}
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-y-auto p-4 bg-bg-primary">
      {#if loading}
        <div class="flex h-full items-center justify-center text-text-tertiary">
          <div class="flex flex-col items-center gap-2">
            <div class="h-6 w-6 animate-spin rounded-full border-2 border-border-default border-t-accent-primary"></div>
            <span class="text-sm">Loading diff...</span>
          </div>
        </div>
      {:else if error}
        <div class="rounded border border-status-error-border bg-status-error-bg p-4 text-status-error-text flex items-center justify-between">
          <span>{error}</span>
          <button onclick={() => currentStep === -1 ? fetchIterations() : loadDiff(currentStep)} class="px-3 py-1 rounded bg-status-error-text text-white hover:opacity-90 transition-opacity text-xs font-medium">Retry</button>
        </div>
      {:else if iterations.length === 0}
        <div class="flex h-full items-center justify-center text-text-tertiary">
          No iterations found for this workstation.
        </div>
      {:else}
        <div class="mb-4">
          <h3 class="text-sm font-medium text-text-primary mb-1">
            {currentStep === -1 ? 'Aggregate Diff' : `Iteration ${iterations[currentStep].iteration}`}
          </h3>
          {#if currentStep > -1 && iterations[currentStep].files_changed.length > 0}
            <div class="text-xs text-text-secondary mb-2">
              Files changed: {iterations[currentStep].files_changed.join(', ')}
            </div>
          {/if}
        </div>
        <DiffViewer diff={currentDiff} />
      {/if}
    </div>
  </div>
</div>
