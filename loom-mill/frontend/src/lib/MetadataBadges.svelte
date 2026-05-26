<script lang="ts">
  import type { RecordMetadata } from './types';

  let { metadata }: { metadata: RecordMetadata } = $props();

  function getStatusColor(status: string | null) {
    if (!status) return 'bg-status-neutral-bg text-status-neutral-text border-status-neutral-border';
    const s = status.toLowerCase();
    if (s === 'closed' || s === 'done' || s === 'completed') return 'bg-status-success-bg text-status-success-text border-status-success-border';
    if (s === 'active' || s === 'in progress') return 'bg-status-info-bg text-status-info-text border-status-info-border';
    if (s === 'open' || s === 'todo') return 'bg-status-warning-bg text-status-warning-text border-status-warning-border';
    if (s === 'blocked') return 'bg-status-error-bg text-status-error-text border-status-error-border';
    return 'bg-status-neutral-bg text-status-neutral-text border-status-neutral-border';
  }

  function getRiskColor(risk: string | null) {
    if (!risk) return '';
    const r = risk.toLowerCase();
    if (r === 'high') return 'bg-status-error-bg text-status-error-text border-status-error-border';
    if (r === 'medium') return 'bg-status-warning-bg text-status-warning-text border-status-warning-border';
    if (r === 'low') return 'bg-status-success-bg text-status-success-text border-status-success-border';
    return 'bg-status-neutral-bg text-status-neutral-text border-status-neutral-border';
  }

  function getPriorityColor(priority: string | null) {
    if (!priority) return '';
    const p = priority.toLowerCase();
    if (p === 'high' || p === 'p1') return 'bg-status-error-bg text-status-error-text border-status-error-border';
    if (p === 'medium' || p === 'p2') return 'bg-status-warning-bg text-status-warning-text border-status-warning-border';
    if (p === 'low' || p === 'p3') return 'bg-status-success-bg text-status-success-text border-status-success-border';
    return 'bg-status-neutral-bg text-status-neutral-text border-status-neutral-border';
  }
</script>

<div class="flex flex-wrap items-center gap-2">
  {#if metadata.status}
    <span class="badge border {getStatusColor(metadata.status)}">
      {metadata.status}
    </span>
  {/if}
  
  {#if metadata.risk}
    <span class="badge border {getRiskColor(metadata.risk)}">
      Risk: {metadata.risk}
    </span>
  {/if}

  {#if metadata.priority}
    <span class="badge border {getPriorityColor(metadata.priority)}">
      Priority: {metadata.priority}
    </span>
  {/if}

  <div class="ml-auto flex items-center gap-3 text-[10px] text-text-tertiary">
    {#if metadata.created}
      <span>Created: {metadata.created.split('T')[0]}</span>
    {/if}
    {#if metadata.updated}
      <span>Updated: {metadata.updated.split('T')[0]}</span>
    {/if}
  </div>
</div>
