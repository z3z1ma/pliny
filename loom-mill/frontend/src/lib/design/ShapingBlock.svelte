<script lang="ts">
  import type { InteractionBlock } from '../types';
  import ProposalCard from './ProposalCard.svelte';

  let { block, sessionId, onRespond }: { block: InteractionBlock, sessionId: string, onRespond: (content: string) => void } = $props();

  let expanded = $state(false);
</script>

<div class="flex flex-col gap-2 w-full">
  {#if block.type === 'operator_input'}
    <div class="bg-bg-surface-active p-3 rounded text-[13px] text-text-primary font-mono whitespace-pre-wrap">
      {block.content.text}
    </div>
    
  {:else if block.type === 'agent_question'}
    <div class="bg-bg-surface border-l-2 border-accent-primary p-3 rounded shadow-sm flex flex-col gap-2">
      <div class="flex items-start gap-2">
        <span class="text-accent-primary mt-0.5">❓</span>
        <div class="text-[13px] text-text-primary whitespace-pre-wrap">{block.content.question}</div>
      </div>
      {#if block.content.options && block.content.options.length > 0}
        <div class="flex flex-wrap gap-2 mt-2 ml-6">
          {#each block.content.options as option}
            <button 
              class="px-3 py-1 text-[12px] rounded border border-border-default bg-bg-primary hover:bg-bg-surface-hover text-text-secondary transition-colors"
              onclick={() => onRespond(option)}
            >
              {option}
            </button>
          {/each}
        </div>
      {/if}
    </div>
    
  {:else if block.type === 'agent_observation'}
    <div class="bg-bg-surface border-l-2 border-status-success-text/50 p-3 rounded shadow-sm flex flex-col gap-2">
      <div class="flex items-start gap-2">
        <span class="text-status-success-text mt-0.5">👁️</span>
        <div class="text-[13px] text-text-primary whitespace-pre-wrap">{block.content.observation}</div>
      </div>
      {#if block.content.evidence}
        <div class="ml-6 mt-1">
          <button 
            class="text-[11px] text-text-tertiary hover:text-text-secondary flex items-center gap-1"
            onclick={() => expanded = !expanded}
          >
            <span class="transform transition-transform {expanded ? '' : '-rotate-90'}">▼</span>
            {expanded ? 'Hide evidence' : 'Show evidence'}
          </button>
          {#if expanded}
            <div class="mt-2 p-2 bg-bg-primary rounded border border-border-subtle text-[11px] font-mono text-text-secondary overflow-x-auto whitespace-pre-wrap">
              {block.content.evidence}
            </div>
          {/if}
        </div>
      {/if}
    </div>
    
  {:else if block.type === 'agent_proposal'}
    <ProposalCard proposal={block.content.proposal} {sessionId} />
    
  {:else if block.type === 'exploration_start'}
    <div class="text-[11px] text-text-tertiary flex items-center gap-2">
      <span>🔍</span> Exploring: {block.content.goal}
    </div>
    
  {:else if block.type === 'exploration_complete'}
    <div class="text-[11px] text-text-tertiary flex items-center gap-2">
      <span class="text-status-success-text">✓</span> Explored: {block.content.summary}
    </div>
    
  {:else if block.type === 'branch_point'}
    <div class="bg-status-warning-bg/10 border border-status-warning-border/30 rounded p-3 flex flex-col gap-2">
      <div class="text-[12px] font-medium text-status-warning-text flex items-center gap-2">
        <span>🔀</span> Branch Point
      </div>
      <div class="text-[12px] text-text-secondary">{block.content.description}</div>
      <div class="flex gap-2 mt-2">
        {#each block.content.branches as branch}
          <button 
            class="px-3 py-1 text-[12px] rounded bg-bg-surface hover:bg-bg-surface-hover border border-border-default text-text-primary transition-colors"
            onclick={() => onRespond(`Switch to branch: ${branch.name}`)}
          >
            {branch.name}
          </button>
        {/each}
      </div>
    </div>
    
  {:else if block.type === 'system'}
    <div class="text-[10px] text-text-tertiary italic">
      {block.content.message}
    </div>
    
  {:else}
    <div class="text-[12px] text-text-secondary">
      Unknown block type: {block.type}
    </div>
  {/if}
  
  <div class="text-[9px] text-text-tertiary text-right mt-1">
    {new Date(block.timestamp).toLocaleTimeString()}
  </div>
</div>
