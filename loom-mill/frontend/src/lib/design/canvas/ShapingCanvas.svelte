<script lang="ts">
  import { Svelvet, Node, Anchor } from 'svelvet';
  import { store } from '../../ws.svelte.ts';
  import InputNode from './InputNode.svelte';
  import ProcessingNode from './ProcessingNode.svelte';
  import QuestionNode from './QuestionNode.svelte';
  import ObservationNode from './ObservationNode.svelte';
  import FramingNode from './FramingNode.svelte';
  import TensionNode from './TensionNode.svelte';
  import DecisionNode from './DecisionNode.svelte';
  import OptionNode from './OptionNode.svelte';
  import RecordNode from './RecordNode.svelte';
  import CanvasInputBar from './CanvasInputBar.svelte';
  import ContextPeekPanel from './ContextPeekPanel.svelte';
  import { apiUrl } from '../../api';
  import type { CanvasNode } from '../../types';
  import { computeTreeLayout } from './layout';
  import { causalEdgeColor } from './edge-style';

  let { sessionId, advancing, highlightedTempId, discardedTempIds = new Set<string>(), onOpenLogs }: { sessionId: string, advancing: boolean, highlightedTempId?: string | null, discardedTempIds?: Set<string>, onOpenLogs?: (invocationId: string) => void } = $props();

  let allNodes = $derived(store.shapingSession?.nodes ? Object.values(store.shapingSession.nodes) : []);
  let allEdges = $derived(store.shapingSession?.edges ?? []);

  let thinkingTrace = $derived(store.shapingSession?.thinkingTrace ?? '');
  let isThinking = $derived(store.shapingSession?.advanceState === 'thinking');

  let collapseDead = $state(false);
  let rejectedTempIds = $state<Set<string>>(new Set());
  let thinkingDismissed = $state(false);
  let continuePending = $state(false);

  let nodes = $derived(
    collapseDead
      ? allNodes.filter(n => n.status !== 'dead')
      : allNodes
  );

  let edges = $derived(
    collapseDead
      ? allEdges.filter(e => {
          const source = store.shapingSession?.nodes[e.source_id];
          const target = store.shapingSession?.nodes[e.target_id];
          return source?.status !== 'dead' && target?.status !== 'dead';
        })
      : allEdges
  );

  let hiddenCount = $derived(allNodes.length - nodes.length);

  let layoutResult = $derived(computeTreeLayout(nodes, edges));

  // FIX: Defer position application to ensure edges render on load.
  // Bug: Svelvet anchors mount and measure positions before Node.svelte's reactive
  // block syncs the position prop to the internal store, so anchors capture (0,0) and
  // edges render with degenerate paths. Solution: start all nodes at origin, let them
  // mount with anchors, THEN update positions 50ms later. This triggers the reactive
  // position sync in Node.svelte AFTER anchors exist, causing them to recalculate via
  // afterUpdate and draw correct edge geometry.
  let applyPositions = $state(false);
  $effect(() => {
    if (nodes.length > 0) {
      applyPositions = false;
      setTimeout(() => {
        applyPositions = true;
      }, 50);
    }
  });

  $effect(() => {
    if (isThinking) thinkingDismissed = false;
  });

  function getChildConnections(nodeId: string) {
    const conns = edges
      .filter(e => e.source_id === nodeId && store.shapingSession?.nodes[e.target_id])
      .map(e => [e.target_id, `${e.target_id}-in`]);
    return conns;
  }

  function computePosition(node: CanvasNode) {
    if (!applyPositions) return { x: 0, y: 0 }; // Start all nodes at origin
    if (node.position) return node.position;
    return layoutResult.positions[node.id] ?? { x: 0, y: 0 };
  }

  function applySessionState(data: any) {
    const state = data.state ?? data;
    if (!state || !store.shapingSession) return;
    store.shapingSession.phase = state.phase;
    store.shapingSession.nodes = state.nodes || {};
    store.shapingSession.edges = state.edges || [];
    store.shapingSession.stagedRecords = state.staged_records || [];
    store.shapingSession.activeBranch = state.active_branch || 'main';
    store.shapingSession.branches = state.branches || ['main'];
    store.shapingSession.activeExplorations = state.active_explorations || [];
    store.shapingSession.explorationLogs = store.shapingSession.explorationLogs || {};
    store.shapingSession.explorationStatus = store.shapingSession.explorationStatus || {};
  }

  async function refetchSessionState() {
    const response = await fetch(apiUrl(`/shaping/sessions/${sessionId}`));
    if (!response.ok) {
      console.error('Failed to refetch shaping session:', await response.text());
      return;
    }
    applySessionState(await response.json());
  }

  function withStagingStatus(node: CanvasNode): CanvasNode {
    const tempId = node.content.temp_id;
    if (!tempId) return node;
    const staged = store.shapingSession?.stagedRecords.find(record => record.temp_id === tempId);
    if (!staged) {
      if (rejectedTempIds.has(tempId) || discardedTempIds.has(tempId)) return { ...node, status: 'rejected' };
      return node;
    }
    const stagedNode = { ...node, content: { ...node.content, title: staged.title, content: staged.content } };
    if (staged.status === 'accepted') return { ...stagedNode, status: 'accepted' };
    return stagedNode;
  }

  async function handleRecordAccept(nodeId: string) {
    const node = store.shapingSession?.nodes[nodeId];
    const tempId = node?.content.temp_id;
    if (!tempId) return;
    const response = await fetch(apiUrl(`/shaping/sessions/${sessionId}/staged/${tempId}/accept`), { method: 'POST' });
    if (!response.ok) {
      console.error('Failed to accept staged record:', await response.text());
      return;
    }
    rejectedTempIds.delete(tempId);
    rejectedTempIds = new Set(rejectedTempIds);
    await refetchSessionState();
  }

  async function handleRecordReject(nodeId: string) {
    const node = store.shapingSession?.nodes[nodeId];
    const tempId = node?.content.temp_id;
    if (!tempId) return;
    const response = await fetch(apiUrl(`/shaping/sessions/${sessionId}/staged/${tempId}`), { method: 'DELETE' });
    if (!response.ok) {
      console.error('Failed to reject staged record:', await response.text());
      return;
    }
    rejectedTempIds.add(tempId);
    rejectedTempIds = new Set(rejectedTempIds);
    await refetchSessionState();
  }

  async function handleRecordEdit(nodeId: string, content: string) {
    const node = store.shapingSession?.nodes[nodeId];
    const tempId = node?.content.temp_id;
    if (!tempId) return false;
    const response = await fetch(apiUrl(`/shaping/sessions/${sessionId}/staged/${tempId}`), {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    });
    if (!response.ok) {
      console.error('Failed to edit staged record:', await response.text());
      return false;
    }
    if (store.shapingSession?.nodes[nodeId]) {
      store.shapingSession.nodes[nodeId].content = { ...store.shapingSession.nodes[nodeId].content, content };
    }
    await refetchSessionState();
    return true;
  }

  async function handleRespond(content: string, parentNodeId: string) {
    if (!sessionId) return;
    try {
      const inputRes = await fetch(apiUrl(`/shaping/sessions/${sessionId}/input`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: content, parent_node_id: parentNodeId })
      });
      if (!inputRes.ok) {
        console.error('Error sending input:', await inputRes.text());
        return;
      }
      
      // Trigger the engine to produce the next node
      await fetch(apiUrl(`/shaping/sessions/${sessionId}/advance`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
    } catch (err) {
      console.error('Error in shaping respond:', err);
    }
  }

  async function handleSelect(nodeId: string) {
    if (!sessionId) return;
    try {
      const selectRes = await fetch(apiUrl(`/shaping/sessions/${sessionId}/nodes/${nodeId}/select`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      if (!selectRes.ok) {
        console.error('Error selecting option:', await selectRes.text());
        return;
      }

      await fetch(apiUrl(`/shaping/sessions/${sessionId}/advance`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
    } catch (err) {
      console.error('Error in shaping option select:', err);
    }
  }

  async function handleReselect(nodeId: string) {
    if (!sessionId) return;
    try {
      const response = await fetch(apiUrl(`/shaping/sessions/${sessionId}/nodes/${nodeId}/reselect`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      if (!response.ok) {
        console.error('Error reselecting option:', await response.text());
      }
    } catch (err) {
      console.error('Error in shaping option reselect:', err);
    }
  }

  async function handleContinue(nodeId: string) {
    if (!sessionId || isThinking || continuePending) return;
    continuePending = true;
    try {
      const inputRes = await fetch(apiUrl(`/shaping/sessions/${sessionId}/input`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: 'Continue from here.', parent_node_id: nodeId })
      });
      if (!inputRes.ok) {
        console.error('Error adding continue input:', await inputRes.text());
        return;
      }
      await fetch(apiUrl(`/shaping/sessions/${sessionId}/advance`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
    } catch (err) {
      console.error('Error continuing from node:', err);
    } finally {
      continuePending = false;
    }
  }
</script>

<div class="w-full h-full bg-bg-primary relative flex flex-col">
  <ContextPeekPanel {sessionId} />

  <div class="absolute top-4 right-4 z-10 flex items-center gap-2 bg-bg-surface p-2 rounded border border-border-default shadow-sm">
    <label class="flex items-center gap-2 text-sm text-text-primary cursor-pointer">
      <input type="checkbox" bind:checked={collapseDead} class="rounded border-border-default bg-bg-primary text-brand-primary focus:ring-brand-primary" />
      Collapse dead branches
    </label>
    {#if collapseDead && hiddenCount > 0}
      <span class="text-xs bg-bg-secondary text-text-secondary px-1.5 py-0.5 rounded-full">
        {hiddenCount} hidden
      </span>
    {/if}
  </div>

  <div class="flex-1 relative">
    <Svelvet theme="dark" minimap controls>
      {#each nodes as node (node.id)}
        {#if node.type === 'input'}
          <InputNode {node} {sessionId} position={node.position ?? computePosition(node)} connections={getChildConnections(node.id)} />
        {:else if node.type === 'processing'}
          <ProcessingNode {node} position={node.position ?? computePosition(node)} connections={getChildConnections(node.id)} {onOpenLogs} />
        {:else if node.type === 'question'}
          <QuestionNode {node} position={node.position ?? computePosition(node)} connections={getChildConnections(node.id)} onRespond={(content) => handleRespond(content, node.id)} />
        {:else if node.type === 'observation'}
          <ObservationNode {node} position={node.position ?? computePosition(node)} connections={getChildConnections(node.id)} onContinue={handleContinue} continueDisabled={isThinking || continuePending} />
        {:else if node.type === 'framing'}
          <FramingNode {node} position={node.position ?? computePosition(node)} connections={getChildConnections(node.id)} />
        {:else if node.type === 'tension'}
          <TensionNode {node} position={node.position ?? computePosition(node)} connections={getChildConnections(node.id)} onContinue={handleContinue} continueDisabled={isThinking || continuePending} />
        {:else if node.type === 'decision'}
          <DecisionNode {node} position={node.position ?? computePosition(node)} connections={getChildConnections(node.id)} />
        {:else if node.type === 'option'}
          <OptionNode {node} position={node.position ?? computePosition(node)} connections={getChildConnections(node.id)} onSelect={handleSelect} onReselect={handleReselect} />
        {:else if node.type === 'record'}
          <RecordNode node={withStagingStatus(node)} position={node.position ?? computePosition(node)} connections={getChildConnections(node.id)} highlighted={highlightedTempId === node.content.temp_id} onAccept={handleRecordAccept} onReject={handleRecordReject} onEdit={handleRecordEdit} />
        {:else}
          <Node id={node.id} position={node.position ?? computePosition(node)}>
            <div class="p-4 bg-bg-surface border border-border-default rounded text-text-primary">
              Unknown node type: {node.type}
            </div>
            <div slot="anchorNorth">
              {#if node.parent_id}
                <Anchor id="{node.id}-in" input />
              {/if}
            </div>
            <div slot="anchorSouth">
              {#if getChildConnections(node.id).length > 0}
                <Anchor id="{node.id}-out" output connections={getChildConnections(node.id)} edgeColor={causalEdgeColor} />
              {:else}
                <Anchor id="{node.id}-out" output edgeColor={causalEdgeColor} />
              {/if}
            </div>
          </Node>
        {/if}
      {/each}
    </Svelvet>

    {#if isThinking && thinkingTrace && !thinkingDismissed}
      <div class="absolute bottom-4 left-4 z-20 max-w-[420px] max-h-[40vh] overflow-auto
        bg-bg-surface/95 border border-border-default rounded-lg shadow-lg p-3">
        <div class="flex items-center justify-between mb-1">
          <div class="text-[10px] uppercase tracking-wider text-text-tertiary">Thinking…</div>
          <button class="text-text-tertiary hover:text-text-primary text-xs leading-none"
            onclick={() => (thinkingDismissed = true)} aria-label="Dismiss thinking panel">✕</button>
        </div>
        <div class="text-[11px] font-mono text-text-secondary whitespace-pre-wrap break-words">{thinkingTrace}</div>
      </div>
    {/if}
  </div>

  <CanvasInputBar {sessionId} onAdvance={() => {
    fetch(apiUrl(`/shaping/sessions/${sessionId}/advance`), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }).catch(err => console.error('Error triggering advance:', err));
  }} />
  
</div>
