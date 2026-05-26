<script lang="ts">
  import type { LoomRecord } from '../types';
  import TreeNodeComponent from './TreeNodeComponent.svelte';

  interface TreeNode {
    record: LoomRecord;
    children: TreeNode[];
    depth: number;
  }

  let { 
    node, 
    selectedId, 
    onSelect,
    allRecords
  }: { 
    node: TreeNode; 
    selectedId: string | null; 
    onSelect: (id: string) => void;
    allRecords: LoomRecord[];
  } = $props();

  let expanded = $state(true);

  let statusColor = $derived(() => {
    const status = node.record.metadata.status?.toLowerCase() || '';
    if (['closed', 'accepted', 'completed'].includes(status)) return 'bg-[#22c55e]';
    if (['active'].includes(status)) return 'bg-[#3b82f6]';
    if (['open', 'draft'].includes(status)) return 'bg-[#f59e0b]';
    if (['blocked'].includes(status)) return 'bg-[#ef4444]';
    if (['cancelled', 'retired', 'superseded'].includes(status)) return 'bg-[#6b7280]';
    return 'bg-border-strong'; // default
  });

  let title = $derived(() => {
    if (node.record.headings && node.record.headings.length > 0) {
      return node.record.headings[0][1];
    }
    if (node.record.metadata.id) {
      return node.record.metadata.id;
    }
    return node.record.path.split('/').pop() || node.record.path;
  });

  let isReady = $derived(() => {
    const record = node.record;
    if (record.surface !== 'tickets') return false;
    if (record.metadata.status?.toLowerCase() !== 'open') return false;
    
    // Check dependencies
    if (record.metadata.depends_on && record.metadata.depends_on.length > 0) {
      for (const depId of record.metadata.depends_on) {
        const depRecord = allRecords.find(r => r.metadata.id === depId);
        if (!depRecord || depRecord.metadata.status?.toLowerCase() !== 'closed') {
          return false;
        }
      }
    }

    // Check ACC-* labels
    if (!record.labeled_ids || !record.labeled_ids.some(id => id.startsWith('ACC-'))) {
      return false;
    }

    return true;
  });

  let isSelected = $derived(selectedId === node.record.path);
</script>

<div class="relative" style="padding-left: {node.depth * 16}px">
  <div 
    role="button"
    tabindex="0"
    onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') onSelect(node.record.path); }}
    onclick={() => onSelect(node.record.path)}
    class="flex items-center w-full py-1.5 pr-2 text-[11px] rounded transition-colors gap-1.5 cursor-pointer
      {isSelected ? 'bg-bg-surface-active text-text-primary ring-1 ring-border-strong' : 'hover:bg-bg-surface-hover text-text-secondary'}"
  >
    <!-- Expand chevron -->
    {#if node.children.length > 0}
      <button 
        onclick={(e) => { e.stopPropagation(); expanded = !expanded; }} 
        class="w-4 h-4 flex items-center justify-center text-[8px] text-text-tertiary hover:text-text-primary transition-colors shrink-0"
      >
        {expanded ? '▼' : '▶'}
      </button>
    {:else}
      <span class="w-4 shrink-0"></span>
    {/if}
    
    <!-- Status dot -->
    <span class="w-2 h-2 rounded-full shrink-0 {statusColor()}"></span>
    
    <!-- Title -->
    <span class="truncate flex-1 text-left">{title()}</span>
    
    <!-- Child count -->
    {#if node.children.length > 0}
      <span class="ml-auto text-[9px] text-text-tertiary px-1 bg-bg-surface-hover rounded">{node.children.length}</span>
    {/if}
    
    <!-- Ready indicator -->
    {#if isReady}
      <span class="text-[#22c55e] shrink-0 font-bold text-[10px]">✓</span>
    {/if}
  </div>

  <!-- Children -->
  {#if expanded && node.children.length > 0}
    <!-- Connector line -->
    <div class="absolute border-l border-border-subtle" style="left: {node.depth * 16 + 8}px; top: 24px; bottom: 0"></div>
    <div class="flex flex-col gap-0.5 mt-0.5">
      {#each node.children as child}
        <TreeNodeComponent node={child} {selectedId} {onSelect} {allRecords} />
      {/each}
    </div>
  {/if}
</div>