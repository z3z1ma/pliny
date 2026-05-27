<script lang="ts">
  import { Svelvet, Node, Anchor } from 'svelvet';
  import { store } from '../../ws.svelte.ts';
  import InputNode from './InputNode.svelte';
  import ProcessingNode from './ProcessingNode.svelte';
  import QuestionNode from './QuestionNode.svelte';
  import ObservationNode from './ObservationNode.svelte';
  import OptionNode from './OptionNode.svelte';
  import RecordNode from './RecordNode.svelte';
  import { apiUrl } from '../../api';
  import type { CanvasNode } from '../../types';
  import { computeTreeLayout } from './layout';

  let { sessionId, advancing, highlightedTempId }: { sessionId: string, advancing: boolean, highlightedTempId?: string | null } = $props();

  let allNodes = $derived(store.shapingSession?.nodes ? Object.values(store.shapingSession.nodes) : []);
  let allEdges = $derived(store.shapingSession?.edges ?? []);

  let collapseDead = $state(false);
  let rejectedTempIds = $state<Set<string>>(new Set());

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

  function getChildConnections(nodeId: string) {
    const conns = edges
      .filter(e => e.source_id === nodeId && store.shapingSession?.nodes[e.target_id])
      .map(e => [e.target_id, `${e.target_id}-in`]);
    return conns;
  }

  function computePosition(node: CanvasNode) {
    if (node.position) return node.position;
    return layoutResult.positions[node.id] ?? { x: 0, y: 0 };
  }

  function applySessionState(data: any) {
    if (!data.state || !store.shapingSession) return;
    store.shapingSession.phase = data.state.phase;
    store.shapingSession.nodes = data.state.nodes || {};
    store.shapingSession.edges = data.state.edges || [];
    store.shapingSession.stagedRecords = data.state.staged_records || [];
    store.shapingSession.activeBranch = data.state.active_branch || 'main';
    store.shapingSession.branches = data.state.branches || ['main'];
    store.shapingSession.activeExplorations = data.state.active_explorations || [];
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
    const stagedNode = staged ? { ...node, content: { ...node.content, title: staged.title, content: staged.content } } : node;
    if (staged?.status === 'accepted') return { ...stagedNode, status: 'accepted' };
    if (rejectedTempIds.has(tempId)) return { ...node, status: 'rejected' };
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
    if (!tempId) return;
    const response = await fetch(apiUrl(`/shaping/sessions/${sessionId}/staged/${tempId}`), {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    });
    if (!response.ok) {
      console.error('Failed to edit staged record:', await response.text());
      return;
    }
    if (store.shapingSession?.nodes[nodeId]) {
      store.shapingSession.nodes[nodeId].content = { ...store.shapingSession.nodes[nodeId].content, content };
    }
    await refetchSessionState();
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
</script>

<div class="w-full h-full bg-bg-primary relative">
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

  <Svelvet theme="dark" minimap controls>
    {#each nodes as node (node.id)}
      {#if node.type === 'input'}
        <InputNode {node} {sessionId} position={node.position ?? computePosition(node)} connections={getChildConnections(node.id)} />
      {:else if node.type === 'processing'}
        <ProcessingNode {node} position={node.position ?? computePosition(node)} connections={getChildConnections(node.id)} />
      {:else if node.type === 'question'}
        <QuestionNode {node} position={node.position ?? computePosition(node)} connections={getChildConnections(node.id)} onRespond={(content) => handleRespond(content, node.id)} />
      {:else if node.type === 'observation'}
        <ObservationNode {node} position={node.position ?? computePosition(node)} connections={getChildConnections(node.id)} />
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
              <Anchor id="{node.id}-out" output connections={getChildConnections(node.id)} />
            {:else}
              <Anchor id="{node.id}-out" output />
            {/if}
          </div>
        </Node>
      {/if}
    {/each}
  </Svelvet>
</div>
