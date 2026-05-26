<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import { forceCenter, forceCollide, forceLink, forceManyBody, forceSimulation, type Simulation, type SimulationLinkDatum, type SimulationNodeDatum } from 'd3-force';
  import type { LoomRecord } from '../types';
  import { store } from '../ws.svelte.ts';

  let { documentId, onNavigate }: { documentId: string | null; onNavigate?: (id: string) => void } = $props();

  interface GraphNode extends SimulationNodeDatum {
    id: string;
    label: string;
    path: string;
    surface: string | null;
    status: string | null;
    isCurrent: boolean;
    layer?: number;
  }

  interface GraphEdge extends SimulationLinkDatum<GraphNode> {
    source: string | GraphNode;
    target: string | GraphNode;
    type: 'references' | 'depends_on' | 'hierarchy';
  }

  type GraphMode = 'connected' | 'hierarchy';
  type HierarchyScope = 'workspace' | 'subtree';

  let containerEl: HTMLDivElement;
  let width = $state(600);
  let height = $state(400);
  let graphNodes = $state<GraphNode[]>([]);
  let graphEdges = $state<GraphEdge[]>([]);
  let hoveredNode = $state<GraphNode | null>(null);
  let mode = $state<GraphMode>('connected');
  let hierarchyScope = $state<HierarchyScope>('workspace');
  let simulation: Simulation<GraphNode, GraphEdge> | null = null;
  let draggingNode: GraphNode | null = null;

  onMount(() => {
    const observer = new ResizeObserver(([entry]) => {
      width = Math.max(320, entry.contentRect.width);
      height = Math.max(240, entry.contentRect.height);
    });

    if (containerEl) observer.observe(containerEl);

    return () => observer.disconnect();
  });

  onDestroy(() => {
    simulation?.stop();
  });

  $effect(() => {
    const records = store.state.records;
    const currentRecord = documentId ? records.find((record) => record.metadata.id === documentId || record.path === documentId) : null;

    if (hierarchyScope === 'subtree' && currentRecord?.surface !== 'plans') {
      hierarchyScope = 'workspace';
      return;
    }

    if (mode === 'connected') {
      if (!documentId) {
        simulation?.stop();
        graphNodes = [];
        graphEdges = [];
        return;
      }

      const graph = computeGraph(documentId, records);
      runSimulation(graph.nodes, graph.edges);
    } else {
      simulation?.stop();
      const graph = computeDag(records, documentId, hierarchyScope);
      layoutDag(graph.nodes);
      graphNodes = [...graph.nodes];
      graphEdges = [...graph.edges];
    }
  });

  function computeGraph(currentRecordId: string, records: LoomRecord[]) {
    const nodes: GraphNode[] = [];
    const edges: GraphEdge[] = [];
    const nodeIds = new Set<string>();
    const edgeIds = new Set<string>();

    const currentRecord = records.find((record) => record.metadata.id === currentRecordId || record.path === currentRecordId);
    if (!currentRecord) return { nodes, edges };

    const currentId = getRecordId(currentRecord);
    addNode(currentRecord, true);

    for (const ref of currentRecord.references || []) {
      const target = findRecord(records, ref);
      if (target) addEdge(currentId, target, 'references');
    }

    for (const record of records) {
      const recordId = getRecordId(record);
      if (recordId === currentId) continue;

      if ((record.references || []).some((ref) => matchesRecordRef(currentRecord, ref))) {
        addEdge(recordId, currentRecord, 'references', record);
      }

      if ((record.metadata.depends_on || []).some((dep) => matchesRecordRef(currentRecord, dep))) {
        addEdge(recordId, currentRecord, 'depends_on', record);
      }
    }

    for (const dep of currentRecord.metadata.depends_on || []) {
      const target = findRecord(records, dep);
      if (target) addEdge(currentId, target, 'depends_on');
    }

    function addNode(record: LoomRecord, isCurrent = false) {
      const id = getRecordId(record);
      if (nodeIds.has(id)) return;

      nodes.push({
        id,
        label: getLabel(record),
        path: record.path,
        surface: record.surface,
        status: record.metadata.status,
        isCurrent,
      });
      nodeIds.add(id);
    }

    function addEdge(sourceId: string, target: LoomRecord, type: GraphEdge['type'], sourceRecord?: LoomRecord) {
      const targetId = getRecordId(target);
      const edgeId = `${sourceId}->${targetId}:${type}`;
      if (edgeIds.has(edgeId)) return;

      if (sourceRecord) addNode(sourceRecord);
      addNode(target);
      edges.push({ source: sourceId, target: targetId, type });
      edgeIds.add(edgeId);
    }

    return { nodes, edges };
  }

  function computeDag(records: LoomRecord[], currentRecordId: string | null, scope: HierarchyScope) {
    const currentRecord = currentRecordId ? records.find((record) => record.metadata.id === currentRecordId || record.path === currentRecordId) : null;
    const scopedRecords = scope === 'subtree' && currentRecord?.surface === 'plans' ? currentSubtree(records, currentRecord) : records;
    const recordIds = new Set(scopedRecords.map(getRecordId));
    const nodes = scopedRecords.map((record) => ({
      id: getRecordId(record),
      label: getLabel(record),
      path: record.path,
      surface: record.surface,
      status: record.metadata.status,
      isCurrent: currentRecord ? matchesRecordRef(record, getRecordId(currentRecord)) : false,
      layer: getLayer(record.surface),
      fx: null,
      fy: null,
    }));
    const edges: GraphEdge[] = [];
    const edgeIds = new Set<string>();

    for (const record of scopedRecords) {
      const childId = getRecordId(record);
      const childLayer = getLayer(record.surface);

      for (const ref of record.references || []) {
        const parent = findRecord(scopedRecords, ref);
        if (!parent) continue;

        const parentId = getRecordId(parent);
        const parentLayer = getLayer(parent.surface);
        if (parentLayer <= childLayer) addDagEdge(parentId, childId, 'hierarchy');
      }

      for (const dep of record.metadata.depends_on || []) {
        const target = findRecord(scopedRecords, dep);
        const targetId = target ? getRecordId(target) : dep;
        if (recordIds.has(targetId)) addDagEdge(childId, targetId, 'depends_on');
      }
    }

    function addDagEdge(sourceId: string, targetId: string, type: GraphEdge['type']) {
      if (sourceId === targetId) return;
      const edgeId = `${sourceId}->${targetId}:${type}`;
      if (edgeIds.has(edgeId)) return;
      edges.push({ source: sourceId, target: targetId, type });
      edgeIds.add(edgeId);
    }

    return { nodes, edges };
  }

  function currentSubtree(records: LoomRecord[], root: LoomRecord) {
    const included = new Set([getRecordId(root)]);
    let changed = true;

    while (changed) {
      changed = false;
      for (const record of records) {
        const recordId = getRecordId(record);
        if (included.has(recordId)) continue;

        const referencesIncludedParent = (record.references || []).some((ref) => {
          const parent = findRecord(records, ref);
          return parent && included.has(getRecordId(parent)) && getLayer(parent.surface) <= getLayer(record.surface);
        });

        if (referencesIncludedParent) {
          included.add(recordId);
          changed = true;
        }
      }
    }

    for (const record of records) {
      if (!included.has(getRecordId(record))) continue;
      for (const dep of record.metadata.depends_on || []) {
        const target = findRecord(records, dep);
        if (target) included.add(getRecordId(target));
      }
    }

    return records.filter((record) => included.has(getRecordId(record)));
  }

  function layoutDag(nodes: GraphNode[]) {
    const layers = new Map<number, GraphNode[]>();
    for (const node of nodes) {
      const layer = node.layer ?? getLayer(node.surface);
      if (!layers.has(layer)) layers.set(layer, []);
      layers.get(layer)?.push(node);
    }

    const sortedLayers = [...layers.keys()].sort((a, b) => a - b);
    const layerHeight = height / (sortedLayers.length + 1);
    const usableWidth = Math.max(240, width - 120);
    const xOffset = width > 520 ? 80 : 24;

    for (const [layerIndex, layer] of sortedLayers.entries()) {
      const layerNodes = layers.get(layer) ?? [];
      const nodeSpacing = usableWidth / (layerNodes.length + 1);
      for (const [nodeIndex, node] of layerNodes.entries()) {
        node.x = xOffset + nodeSpacing * (nodeIndex + 1);
        node.y = layerHeight * (layerIndex + 1);
        node.fx = null;
        node.fy = null;
      }
    }
  }

  function runSimulation(nodes: GraphNode[], edges: GraphEdge[]) {
    simulation?.stop();

    if (nodes.length === 0) {
      graphNodes = [];
      graphEdges = [];
      return;
    }

    nodes.forEach((node, index) => {
      if (node.isCurrent) {
        node.x = width / 2;
        node.y = height / 2;
        node.fx = width / 2;
        node.fy = height / 2;
      } else {
        const angle = (index / Math.max(1, nodes.length - 1)) * Math.PI * 2;
        node.x = width / 2 + Math.cos(angle) * 120;
        node.y = height / 2 + Math.sin(angle) * 120;
        node.fx = null;
        node.fy = null;
      }
    });

    graphNodes = [...nodes];
    graphEdges = [...edges];

    simulation = forceSimulation<GraphNode>(nodes)
      .force('link', forceLink<GraphNode, GraphEdge>(edges).id((node) => node.id).distance(120).strength(0.45))
      .force('charge', forceManyBody().strength(-260))
      .force('center', forceCenter(width / 2, height / 2))
      .force('collide', forceCollide<GraphNode>().radius(42).strength(0.9))
      .alphaDecay(0.08)
      .on('tick', () => {
        graphNodes = [...nodes];
        graphEdges = [...edges];
      });
  }

  function findRecord(records: LoomRecord[], ref: string) {
    return records.find((record) => matchesRecordRef(record, ref));
  }

  function matchesRecordRef(record: LoomRecord, ref: string) {
    const id = record.metadata.id;
    return id === ref || record.path === ref || record.path.includes(ref) || Boolean(id && ref.includes(id));
  }

  function getRecordId(record: LoomRecord) {
    return record.metadata.id || record.path;
  }

  function getLayer(surface: string | null): number {
    switch (surface) {
      case 'plans':
      case 'constitution': return 0;
      case 'specs': return 1;
      case 'tickets': return 2;
      case 'evidence':
      case 'audit':
      case 'knowledge':
      case 'research': return 3;
      default: return 2;
    }
  }

  function getLabel(record: LoomRecord) {
    return record.headings[0]?.[1] || record.metadata.id || record.path.split('/').pop() || record.path;
  }

  function surfaceColor(surface: string | null): string {
    switch (surface) {
      case 'tickets': return '#a78bfa';
      case 'specs': return '#60a5fa';
      case 'plans': return '#34d399';
      case 'evidence': return '#fbbf24';
      case 'research': return '#f472b6';
      case 'knowledge': return '#a3e635';
      case 'audit': return '#f87171';
      case 'constitution': return '#38bdf8';
      default: return '#94a3b8';
    }
  }

  function edgeNode(value: string | GraphNode) {
    return typeof value === 'string' ? graphNodes.find((node) => node.id === value) : value;
  }

  function labelFor(node: GraphNode) {
    return node.label.length > 26 ? `${node.label.slice(0, 26)}...` : node.label;
  }

  function layerLabel(layer: number) {
    switch (layer) {
      case 0: return 'Plans';
      case 1: return 'Specs';
      case 2: return 'Tickets';
      case 3: return 'Evidence';
      default: return 'Other';
    }
  }

  function hierarchyLayerLabels() {
    const labels = new Map<number, number>();
    for (const node of graphNodes) {
      const layer = node.layer ?? getLayer(node.surface);
      if (!labels.has(layer)) labels.set(layer, node.y ?? 0);
    }
    return [...labels.entries()].sort(([a], [b]) => a - b).map(([layer, y]) => ({ layer, y, label: layerLabel(layer) }));
  }

  function isCurrentPlan() {
    const record = documentId ? store.state.records.find((item) => item.metadata.id === documentId || item.path === documentId) : null;
    return record?.surface === 'plans';
  }

  function handlePointerDown(event: PointerEvent, node: GraphNode) {
    draggingNode = node;
    if (mode === 'connected') {
      node.fx = node.x;
      node.fy = node.y;
      simulation?.alphaTarget(0.25).restart();
    }
    (event.currentTarget as SVGGElement).setPointerCapture(event.pointerId);
  }

  function handlePointerMove(event: PointerEvent) {
    if (!draggingNode) return;
    const rect = containerEl.getBoundingClientRect();
    const nextX = event.clientX - rect.left;
    const nextY = event.clientY - rect.top;
    if (mode === 'connected') {
      draggingNode.fx = nextX;
      draggingNode.fy = nextY;
    } else {
      draggingNode.x = nextX;
      draggingNode.y = nextY;
      graphNodes = [...graphNodes];
    }
  }

  function handlePointerUp() {
    if (mode === 'connected' && draggingNode && !draggingNode.isCurrent) {
      draggingNode.fx = null;
      draggingNode.fy = null;
    }
    draggingNode = null;
    simulation?.alphaTarget(0);
  }
</script>

<div bind:this={containerEl} class="relative h-full w-full overflow-hidden bg-bg-primary">
  <div class="absolute left-3 top-3 z-10 flex items-center gap-2 rounded-md border border-border-subtle bg-bg-surface/90 px-2 py-1 shadow-sm">
    <div class="flex rounded border border-border-subtle bg-bg-primary p-0.5 text-[10px]">
      <button
        class="rounded px-2 py-1 transition-colors {mode === 'connected' ? 'bg-accent-primary text-bg-primary' : 'text-text-tertiary hover:text-text-primary'}"
        onclick={() => mode = 'connected'}
      >
        Connected
      </button>
      <button
        class="rounded px-2 py-1 transition-colors {mode === 'hierarchy' ? 'bg-accent-primary text-bg-primary' : 'text-text-tertiary hover:text-text-primary'}"
        onclick={() => mode = 'hierarchy'}
      >
        Hierarchy
      </button>
    </div>

    {#if mode === 'hierarchy'}
      <select
        class="h-6 rounded border border-border-subtle bg-bg-primary px-2 text-[10px] text-text-secondary outline-none disabled:opacity-50"
        bind:value={hierarchyScope}
        disabled={!isCurrentPlan()}
        title={isCurrentPlan() ? 'Hierarchy scope' : 'Current subtree is available for plan records'}
      >
        <option value="workspace">Full workspace</option>
        <option value="subtree">Current subtree</option>
      </select>
    {/if}
  </div>

  {#if graphNodes.length > 0}
    <svg
      class="h-full w-full"
      viewBox="0 0 {width} {height}"
      role="img"
      aria-label={mode === 'connected' ? 'Connected record graph' : 'Hierarchy record graph'}
      onpointermove={handlePointerMove}
      onpointerup={handlePointerUp}
      onpointerleave={handlePointerUp}
    >
      <defs>
        <marker id="graph-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--border-subtle)" />
        </marker>
      </defs>

      {#if mode === 'hierarchy'}
        <g class="layer-labels">
          {#each hierarchyLayerLabels() as layer (layer.layer)}
            <text x="14" y={layer.y ?? 0} dominant-baseline="middle" class="fill-text-tertiary text-[10px] uppercase tracking-wide">
              {layer.label}
            </text>
            <line x1="72" y1={layer.y ?? 0} x2={width - 18} y2={layer.y ?? 0} stroke="var(--border-subtle)" stroke-opacity="0.22" />
          {/each}
        </g>
      {/if}

      <g class="edges">
        {#each graphEdges as edge (`${typeof edge.source === 'string' ? edge.source : edge.source.id}-${typeof edge.target === 'string' ? edge.target : edge.target.id}-${edge.type}`)}
          {@const source = edgeNode(edge.source)}
          {@const target = edgeNode(edge.target)}
          {#if source && target}
            <line
              x1={source.x}
              y1={source.y}
              x2={target.x}
              y2={target.y}
              stroke={edge.type === 'depends_on' ? 'var(--accent-primary)' : 'var(--border-subtle)'}
              stroke-width={edge.type === 'depends_on' ? 1.4 : 1}
              stroke-opacity={edge.type === 'depends_on' ? 0.55 : 0.72}
              stroke-dasharray={edge.type === 'depends_on' ? '4 3' : undefined}
              marker-end="url(#graph-arrow)"
            />
          {/if}
        {/each}
      </g>

      <g class="nodes">
        {#each graphNodes as node (node.id)}
          <g
            transform="translate({node.x ?? width / 2},{node.y ?? height / 2})"
            class="graph-node cursor-pointer"
            role="button"
            tabindex="0"
            onpointerdown={(event) => handlePointerDown(event, node)}
            onmouseenter={() => hoveredNode = node}
            onmouseleave={() => hoveredNode = null}
            onclick={() => onNavigate?.(node.id)}
            onkeydown={(event) => {
              if (event.key === 'Enter' || event.key === ' ') onNavigate?.(node.id);
            }}
          >
            <circle
              r={node.isCurrent ? 10 : 7}
              fill={surfaceColor(node.surface)}
              fill-opacity={node.isCurrent ? 0.95 : 0.82}
              stroke={node.isCurrent ? 'var(--accent-primary)' : 'var(--border-default)'}
              stroke-width={node.isCurrent ? 2.5 : 1.2}
            />
            <text y={node.isCurrent ? 24 : 20} text-anchor="middle" class="pointer-events-none fill-text-secondary text-[10px]">
              {labelFor(node)}
            </text>
          </g>
        {/each}
      </g>
    </svg>

    {#if hoveredNode}
      <div class="pointer-events-none absolute left-3 top-14 max-w-xs rounded-md border border-border-default bg-bg-surface/95 px-3 py-2 text-[11px] shadow-lg">
        <div class="font-medium text-text-primary">{hoveredNode.label}</div>
        <div class="mt-1 text-text-tertiary">{hoveredNode.id}</div>
        {#if hoveredNode.status}
          <div class="mt-1 text-text-secondary">Status: {hoveredNode.status}</div>
        {/if}
      </div>
    {/if}

    <div class="absolute bottom-3 left-3 flex items-center gap-3 rounded-md border border-border-subtle bg-bg-surface/80 px-3 py-2 text-[10px] text-text-tertiary">
      <span>{graphNodes.length} records</span>
      <span>{graphEdges.length} links</span>
      <span>{mode === 'hierarchy' ? 'Solid = hierarchy' : 'Solid = references'}</span>
      <span class="text-accent-primary">Dashed = depends_on</span>
    </div>
  {:else if mode === 'hierarchy'}
    <div class="flex h-full items-center justify-center text-[12px] text-text-tertiary">
      No records found for the hierarchy graph.
    </div>
  {:else if documentId}
    <div class="flex h-full items-center justify-center text-[12px] text-text-tertiary">
      No matching record found for this graph.
    </div>
  {:else}
    <div class="flex h-full items-center justify-center text-[12px] text-text-tertiary">
      Select a record to view its connected graph.
    </div>
  {/if}
</div>
