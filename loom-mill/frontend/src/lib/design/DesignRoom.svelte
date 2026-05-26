<script lang="ts">
  import { store } from '../ws.svelte.ts';
  import { apiUrl } from '../api';
  import { fly } from 'svelte/transition';
  import GraphSidebar from './GraphSidebar.svelte';
  import DocumentEditor from './DocumentEditor.svelte';
  import GraphView from './GraphView.svelte';
  import ChatPanel from './ChatPanel.svelte';

  let selectedDocumentId = $state<string | null>(null);
  let chatContext = $state<any>(null);

  let layoutWidth = $state(0);
  let compactMode = $derived(layoutWidth < 1024);
  let mobileMode = $derived(layoutWidth < 768);

  let showGraph = $state(true);
  let showChat = $state(true);
  let showConnectedGraph = $state(false);
  
  let designRoomContainer: HTMLDivElement;

  import { onMount } from 'svelte';

  onMount(() => {
    const handleResize = () => {
      layoutWidth = window.innerWidth;
      if (layoutWidth < 1024 && layoutWidth >= 768) {
        showGraph = false;
      } else if (layoutWidth >= 1024) {
        showGraph = true;
        showChat = true;
      }
    };
    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  });

  function handleAttachContext(context: { path: string, selected_text: string, line_range: [number, number] }) {
    chatContext = context;
    if (!mobileMode && !showChat) {
      showChat = true;
    }
  }

  async function handleCreateRecord(surface: string) {
    try {
      const response = await fetch(apiUrl('/records'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ surface })
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.path) {
          selectedDocumentId = data.path;
        }
      } else {
        console.error('Failed to create record:', await response.text());
      }
    } catch (err) {
      console.error('Error creating record:', err);
    }
  }

  async function handleSaveDocument(content: string) {
    if (!selectedDocumentId) return;
    
    try {
      const response = await fetch(apiUrl(`/records/${encodeURIComponent(selectedDocumentId)}`), {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content })
      });
      
      if (!response.ok) {
        console.error('Failed to save record:', await response.text());
      }
    } catch (err) {
      console.error('Error saving record:', err);
    }
  }

  function handleNavigate(id: string) {
    const record = store.state.records.find(r => r.metadata.id === id || r.path === id);
    if (record) {
      selectedDocumentId = record.path;
    } else {
      selectedDocumentId = id;
    }
  }
</script>

<div bind:this={designRoomContainer} class="flex h-full w-full overflow-hidden relative">
  {#if mobileMode}
    <div class="flex items-center justify-center h-full w-full bg-bg-surface">
      <p class="text-lg text-text-secondary">Design Room works best on desktop</p>
    </div>
  {:else}
    <!-- Left: Graph sidebar -->
    {#if showGraph}
      <div transition:fly={{ x: -240, duration: 200 }} class="w-60 shrink-0 border-r border-border-default overflow-y-auto bg-bg-surface flex flex-col relative z-10">
        <GraphSidebar 
          records={store.state.records} 
          selectedId={selectedDocumentId} 
          onSelect={(id) => selectedDocumentId = id}
          onCreateRecord={handleCreateRecord}
        />
      </div>
    {/if}
    
    <!-- Center: Document editor -->
    <div class="flex-1 min-w-0 flex flex-col relative z-0">
      <button
        class="absolute right-24 top-1 z-30 flex h-6 items-center gap-1 rounded border border-border-default bg-bg-surface px-2 text-[10px] text-text-tertiary shadow-sm transition-colors hover:bg-bg-surface-hover hover:text-text-primary disabled:cursor-not-allowed disabled:opacity-40"
        onclick={() => showConnectedGraph = !showConnectedGraph}
        disabled={!selectedDocumentId}
        title={showConnectedGraph ? 'Show Editor' : 'Show Connected Graph'}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.59 13.51 15.42 17.49"/><path d="M15.41 6.51 8.59 10.49"/></svg>
        {showConnectedGraph ? 'Editor' : 'Graph'}
      </button>

      {#if !showGraph}
        <button 
          class="absolute left-0 top-1/2 -translate-y-1/2 z-20 bg-bg-surface border border-border-default border-l-0 rounded-r-md p-1 shadow-sm hover:bg-bg-surface-hover text-text-tertiary hover:text-text-primary transition-colors"
          onclick={() => showGraph = true}
          title="Show Graph"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
        </button>
      {:else}
        <button 
          class="absolute left-0 top-1/2 -translate-y-1/2 z-20 bg-bg-surface border border-border-default border-l-0 rounded-r-md p-1 shadow-sm hover:bg-bg-surface-hover text-text-tertiary hover:text-text-primary transition-colors -ml-px"
          onclick={() => showGraph = false}
          title="Hide Graph"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
        </button>
      {/if}

      {#if showConnectedGraph}
        <GraphView documentId={selectedDocumentId} onNavigate={handleNavigate} />
      {:else}
        <DocumentEditor
          documentPath={selectedDocumentId}
          onSave={handleSaveDocument}
          onAttachContext={handleAttachContext}
          onNavigate={handleNavigate}
        />
      {/if}

      {#if !showChat}
        <button 
          class="absolute right-0 top-1/2 -translate-y-1/2 z-20 bg-bg-surface border border-border-default border-r-0 rounded-l-md p-1 shadow-sm hover:bg-bg-surface-hover text-text-tertiary hover:text-text-primary transition-colors"
          onclick={() => showChat = true}
          title="Show Chat"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
        </button>
      {:else}
        <button 
          class="absolute right-0 top-1/2 -translate-y-1/2 z-20 bg-bg-surface border border-border-default border-r-0 rounded-l-md p-1 shadow-sm hover:bg-bg-surface-hover text-text-tertiary hover:text-text-primary transition-colors -mr-px"
          onclick={() => showChat = false}
          title="Hide Chat"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
        </button>
      {/if}
    </div>
    
    <!-- Right: Chat panel -->
    {#if showChat}
      <div transition:fly={{ x: 360, duration: 200 }} class="w-[360px] shrink-0 border-l border-border-default flex flex-col bg-bg-surface relative z-10">
        <ChatPanel 
          documentPath={selectedDocumentId} 
          attachedContext={chatContext}
          onClearContext={() => chatContext = null}
        />
      </div>
    {/if}
  {/if}
</div>
