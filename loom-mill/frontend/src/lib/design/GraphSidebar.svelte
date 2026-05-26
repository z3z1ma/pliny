<script lang="ts">
  import type { LoomRecord } from '../types';
  import NewRecordDropdown from './NewRecordDropdown.svelte';
  import TreeNodeComponent from './TreeNodeComponent.svelte';

  let { 
    records, 
    selectedId, 
    onSelect, 
    onCreateRecord 
  }: { 
    records: LoomRecord[]; 
    selectedId: string | null; 
    onSelect: (id: string) => void; 
    onCreateRecord: (surface: string) => void;
  } = $props();

  let searchQuery = $state('');
  let expandedSections = $state<Set<string>>(new Set(['specs', 'plans', 'tickets', 'research', 'knowledge', 'evidence', 'audit', 'constitution']));

  function toggleSection(id: string) {
    const newSet = new Set(expandedSections);
    if (newSet.has(id)) {
      newSet.delete(id);
    } else {
      newSet.add(id);
    }
    expandedSections = newSet;
  }

  const surfaceLabels: Record<string, string> = {
    specs: 'Specs',
    plans: 'Plans', 
    tickets: 'Tickets',
    research: 'Research',
    knowledge: 'Knowledge',
    evidence: 'Evidence',
    audit: 'Audit',
    constitution: 'Constitution',
  };

  const surfaceIcons: Record<string, string> = {
    specs: '📐',
    plans: '📊',
    tickets: '🎫',
    research: '🔬',
    knowledge: '💡',
    evidence: '✓',
    audit: '🔍',
    constitution: '📋'
  };

  const surfaceOrder = ['specs', 'plans', 'tickets', 'research', 'knowledge', 'evidence', 'audit', 'constitution'];

  interface TreeNode {
    record: LoomRecord;
    children: TreeNode[];
    depth: number;
  }

  function getTitle(record: LoomRecord): string {
    if (record.headings && record.headings.length > 0) {
      return record.headings[0][1];
    }
    if (record.metadata.id) {
      return record.metadata.id;
    }
    return record.path.split('/').pop() || record.path;
  }

  let filteredRecords = $derived(() => {
    if (!searchQuery.trim()) return records;
    const query = searchQuery.toLowerCase();
    return records.filter(r => {
      const title = getTitle(r).toLowerCase();
      const id = (r.metadata.id || '').toLowerCase();
      const status = (r.metadata.status || '').toLowerCase();
      return title.includes(query) || id.includes(query) || status.includes(query);
    });
  });

  let treeData = $derived(() => {
    const currentRecords = filteredRecords();
    const surfaces = new Map<string, TreeNode[]>();
    
    for (const surface of surfaceOrder) {
      const surfaceRecords = currentRecords.filter(r => r.surface === surface);
      
      if (surface === 'plans') {
        const nodes: TreeNode[] = surfaceRecords.map(plan => {
          const planId = plan.metadata.id;
          const children = currentRecords
            .filter(r => r.surface === 'tickets' && r.metadata.depends_on?.some(d => d === planId))
            .map(r => ({ record: r, children: [], depth: 1 }));
          return { record: plan, children, depth: 0 };
        });
        surfaces.set(surface, nodes);
      } else if (surface === 'tickets') {
        const nestedTicketIds = new Set<string>();
        currentRecords.filter(r => r.surface === 'plans').forEach(plan => {
          currentRecords
            .filter(r => r.surface === 'tickets' && r.metadata.depends_on?.some(d => d === plan.metadata.id))
            .forEach(t => { if (t.metadata.id) nestedTicketIds.add(t.metadata.id); });
        });
        
        const orphans = surfaceRecords.filter(r => !nestedTicketIds.has(r.metadata.id || ''));
        surfaces.set(surface, orphans.map(r => ({ record: r, children: [], depth: 0 })));
      } else {
        surfaces.set(surface, surfaceRecords.map(r => ({ record: r, children: [], depth: 0 })));
      }
    }
    
    return surfaces;
  });
</script>

<div class="flex flex-col h-full">
  <div class="flex items-center justify-between p-3 border-b border-border-default shrink-0">
    <span class="font-medium text-text-secondary text-[11px] uppercase tracking-wider">Records</span>
    <NewRecordDropdown onSelect={onCreateRecord} />
  </div>

  <div class="px-3 py-2 border-b border-border-subtle shrink-0">
    <input 
      type="text" 
      placeholder="Search records..." 
      bind:value={searchQuery}
      class="w-full px-2 py-1.5 text-[11px] rounded border border-border-default bg-bg-primary text-text-primary placeholder:text-text-tertiary focus:outline-none focus:border-accent-primary transition-colors" 
    />
  </div>

  <div class="flex-1 overflow-y-auto p-2 space-y-4">
    {#each surfaceOrder as surface}
      {@const nodes = treeData().get(surface) || []}
      {#if nodes.length > 0}
        <div class="flex flex-col gap-1">
          <button 
            class="flex items-center justify-between w-full text-left px-2 py-1 text-[11px] text-text-tertiary hover:text-text-secondary transition-colors"
            onclick={() => toggleSection(surface)}
          >
            <div class="flex items-center gap-2">
              <span>{surfaceIcons[surface]}</span>
              <span class="font-medium uppercase tracking-wider">{surfaceLabels[surface]}</span>
            </div>
            <div class="flex items-center gap-2">
              <span>{nodes.length}</span>
              <span class="transform transition-transform {expandedSections.has(surface) ? '' : '-rotate-90'}">▼</span>
            </div>
          </button>
          
          {#if expandedSections.has(surface)}
            <div class="flex flex-col gap-0.5 pl-1">
              {#each nodes as node}
                <TreeNodeComponent {node} {selectedId} {onSelect} allRecords={records} />
              {/each}
            </div>
          {/if}
        </div>
      {/if}
    {/each}
  </div>
</div>