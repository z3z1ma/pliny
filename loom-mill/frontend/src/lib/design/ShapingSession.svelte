<script lang="ts">
  import { store } from '../ws.svelte.ts';
  import { apiUrl } from '../api';
  import ShapingCanvas from './canvas/ShapingCanvas.svelte';
  import ProcessingLogModal from './canvas/ProcessingLogModal.svelte';
  import SessionList from './canvas/SessionList.svelte';
  import StagingPanel from './StagingPanel.svelte';

  let { sessionId = $bindable(), onExit }: { sessionId: string | null, onExit: () => void } = $props();

  let seedInput = $state('');
  let starting = $state(false);
  let advancing = $state(false);
  let view = $state<'list' | 'new' | 'canvas'>(sessionId ? 'canvas' : 'list');
  let highlightedTempId = $state<string | null>(null);
  let showLogModal = $state(false);
  let logModalInvocationId = $state<string | null>(null);
  let lastDiscardedTempId = $state<string | null>(null);
  let discardedVersion = $state(0);
  let highlightTimeout: ReturnType<typeof setTimeout> | null = null;

  function exitShaping() {
    store.shapingSession = null;
    localStorage.removeItem('loom_shaping_session_id');
    sessionId = null;
    showLogModal = false;
    onExit();
  }

  function toSessionState(data: any) {
    return data.state ?? data;
  }

  function applySessionState(id: string, state: any) {
    const current = store.shapingSession?.id === id ? store.shapingSession : null;
    store.shapingSession = {
      id,
      phase: state.phase,
      nodes: state.nodes || {},
      edges: state.edges || [],
      stagedRecords: state.staged_records || [],
      activeBranch: state.active_branch || 'main',
      branches: state.branches || ['main'],
      activeExplorations: state.active_explorations || [],
      explorationLogs: current?.explorationLogs ?? {},
      explorationStatus: current?.explorationStatus ?? {},
      advanceState: current?.advanceState ?? 'idle',
      advanceError: current?.advanceError ?? null,
      thinkingTrace: current?.thinkingTrace ?? ''
    };
  }

  function openLogModal(invocationId: string) {
    logModalInvocationId = invocationId;
    showLogModal = true;
  }

  async function hydrateSession(id: string) {
    if (store.shapingSession?.id === id) return;
    store.shapingSession = null;
    try {
      const response = await fetch(apiUrl(`/shaping/sessions/${id}`));
      if (response.ok) {
        const data = await response.json();
        const state = toSessionState(data);
        if (state) applySessionState(id, state);
      } else {
        sessionId = null;
        view = 'list';
      }
    } catch (err) {
      console.error('Error fetching session:', err);
      sessionId = null;
      view = 'list';
    }
  }

  $effect(() => {
    if (sessionId) {
      view = 'canvas';
      void hydrateSession(sessionId);
    } else if (view === 'canvas') {
      view = 'list';
    }
  });

  function selectSession(id: string) {
    sessionId = id;
    view = 'canvas';
  }

  function showNewSession() {
    sessionId = null;
    store.shapingSession = null;
    showLogModal = false;
    seedInput = '';
    view = 'new';
  }

  function showSessionList() {
    sessionId = null;
    store.shapingSession = null;
    showLogModal = false;
    view = 'list';
  }

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
        view = 'canvas';
        const state = toSessionState(data);
        if (state && sessionId) applySessionState(sessionId, state);
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
        showLogModal = false;
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

  async function refetchStaging(discardedTempId?: string) {
    if (!sessionId) return;
    if (discardedTempId) {
      lastDiscardedTempId = discardedTempId;
      discardedVersion += 1;
    }
    try {
      const resp = await fetch(apiUrl(`/shaping/sessions/${sessionId}`));
      if (resp.ok) {
        const data = await resp.json();
        applySessionState(sessionId, toSessionState(data));
      }
    } catch (err) { console.error('Failed to refetch staging:', err); }
  }
</script>

<div class="flex h-full w-full">
  {#if view === 'list'}
    <div class="relative w-full h-full">
      <button
        onclick={exitShaping}
        class="absolute right-4 top-4 z-20 rounded border border-border-default bg-bg-surface px-2 py-2 text-[12px] text-text-tertiary shadow-sm transition-colors hover:bg-bg-surface-hover hover:text-status-error-text"
        title="Exit to editor"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
      </button>
      <SessionList onSelectSession={selectSession} onNewSession={showNewSession} />
    </div>
  {:else if view === 'new'}
    <!-- Seed input -->
    <div class="flex-1 flex items-center justify-center p-8 bg-bg-primary">
      <div class="w-full max-w-2xl flex flex-col gap-4">
        <button
          onclick={() => view = 'list'}
          class="self-start text-[12px] text-text-tertiary transition-colors hover:text-text-primary"
        >
          &larr; Sessions
        </button>
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
    <div class="flex-1 min-w-0 flex flex-col overflow-hidden bg-bg-primary relative">
      <button
        onclick={showSessionList}
        class="absolute left-4 top-4 z-20 rounded border border-border-default bg-bg-surface px-3 py-2 text-[12px] font-medium text-text-secondary shadow-sm transition-colors hover:bg-bg-surface-hover hover:text-text-primary"
      >
        &larr; Sessions
      </button>
      <ShapingCanvas 
        {sessionId} 
        {advancing}
        {highlightedTempId}
        {lastDiscardedTempId}
        {discardedVersion}
        onOpenLogs={openLogModal}
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
        onChanged={refetchStaging}
      />
    </div>
  {/if}
</div>

{#if showLogModal}
  <ProcessingLogModal
    invocationId={logModalInvocationId}
    sessionId={sessionId ?? ''}
    onClose={() => showLogModal = false}
  />
{/if}
