<script lang="ts">
  import { store } from '../ws.svelte.ts';
  import { apiUrl } from '../api';
  import ShapingCanvas from './canvas/ShapingCanvas.svelte';
  import StagingPanel from './StagingPanel.svelte';

  let { sessionId = $bindable(), onExit }: { sessionId: string | null, onExit: () => void } = $props();

  let seedInput = $state('');
  let starting = $state(false);
  let advancing = $state(false);
  let highlightedTempId = $state<string | null>(null);
  let highlightTimeout: ReturnType<typeof setTimeout> | null = null;

  import { onMount } from 'svelte';

  function toSessionState(data: any) {
    return data.state ?? data;
  }

  onMount(async () => {
    if (sessionId && !store.shapingSession) {
      try {
        const response = await fetch(apiUrl(`/shaping/sessions/${sessionId}`));
        if (response.ok) {
          const data = await response.json();
          const state = toSessionState(data);
          if (state) {
            store.shapingSession = {
              id: sessionId,
              phase: state.phase,
              nodes: state.nodes || {},
              edges: state.edges || [],
              stagedRecords: state.staged_records || [],
              activeBranch: state.active_branch || 'main',
              branches: state.branches || ['main'],
              activeExplorations: state.active_explorations || [],
              advanceState: 'idle',
              advanceError: null
            };
          }
        } else {
          // Session not found or error, clear it
          sessionId = null;
        }
      } catch (err) {
        console.error('Error fetching session:', err);
        sessionId = null;
      }
    }
  });

  async function startSession() {
    if (!seedInput.trim() || starting) return;
    starting = true;
    try {
      const response = await fetch(apiUrl('/shaping/sessions'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: seedInput })
      });
      if (response.ok) {
        const data = await response.json();
        sessionId = data.session_id || data.id;
        const state = toSessionState(data);
        if (state) {
          store.shapingSession = {
            id: sessionId,
            phase: state.phase,
            nodes: state.nodes || {},
            edges: state.edges || [],
            stagedRecords: state.staged_records || [],
            activeBranch: state.active_branch || 'main',
            branches: state.branches || ['main'],
            activeExplorations: state.active_explorations || [],
            advanceState: 'idle',
            advanceError: null
          };
        }
        // Trigger the engine to start the shaping conversation
        advancing = true;
        fetch(apiUrl(`/shaping/sessions/${sessionId}/advance`), {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        }).catch(err => console.error('Error triggering advance:', err)).finally(() => advancing = false);
      } else {
        console.error('Failed to start session:', await response.text());
      }
    } catch (err) {
      console.error('Error starting session:', err);
    } finally {
      starting = false;
    }
  }

  async function handleCommit() {
    if (!sessionId) return;
    try {
      const response = await fetch(apiUrl(`/shaping/sessions/${sessionId}/commit`), {
        method: 'POST'
      });
      if (response.ok) {
        store.shapingSession = null;
        localStorage.removeItem('loom_shaping_session_id');
        sessionId = null;
        onExit();
      } else {
        console.error('Failed to commit session:', await response.text());
      }
    } catch (err) {
      console.error('Error committing session:', err);
    }
  }

  function highlightRecord(tempId: string) {
    highlightedTempId = tempId;
    if (highlightTimeout) clearTimeout(highlightTimeout);
    highlightTimeout = setTimeout(() => {
      highlightedTempId = null;
      highlightTimeout = null;
    }, 2000);
  }
</script>

<div class="flex h-full w-full">
  {#if !sessionId}
    <!-- Seed input -->
    <div class="flex-1 flex items-center justify-center p-8 bg-bg-primary">
      <div class="w-full max-w-2xl flex flex-col gap-4">
        <h2 class="text-lg font-semibold text-text-primary">Start Shaping</h2>
        <p class="text-[12px] text-text-tertiary">
          Dump your raw thoughts. The agent will explore, ask questions, and
          propose records as the session develops.
        </p>
        <textarea
          bind:value={seedInput}
          class="w-full h-48 p-4 rounded border border-border-default bg-bg-surface
            text-[13px] text-text-primary font-mono resize-none focus:outline-none
            focus:border-accent-primary"
          placeholder="What do you want to shape? Be as raw and unstructured as you want..."
        ></textarea>
        <button
          onclick={startSession}
          disabled={!seedInput.trim() || starting}
          class="self-end px-4 py-2 rounded bg-accent-primary text-white text-[12px]
            font-medium hover:bg-accent-primary/90 disabled:opacity-50 transition-colors"
        >
          {starting ? 'Starting...' : 'Begin Shaping'}
        </button>
      </div>
    </div>
  {:else if !store.shapingSession}
    <div class="flex-1 flex items-center justify-center p-8 bg-bg-primary">
      <div class="text-text-tertiary">Loading session...</div>
    </div>
  {:else}
    <!-- Active session -->
    <div class="flex-1 min-w-0 flex flex-col overflow-hidden bg-bg-primary">
      <ShapingCanvas 
        {sessionId} 
        {advancing}
        {highlightedTempId}
      />
    </div>
    <div class="w-72 shrink-0 border-l border-border-default overflow-y-auto bg-bg-surface">
      <StagingPanel 
        {sessionId} 
        records={store.shapingSession.stagedRecords} 
        branches={store.shapingSession.branches} 
        activeBranch={store.shapingSession.activeBranch} 
        onCommit={handleCommit} 
        onRecordClick={highlightRecord}
      />
    </div>
  {/if}
</div>
