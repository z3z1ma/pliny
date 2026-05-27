<script lang="ts">
  import type { InteractionBlock } from '../types';
  import ShapingBlock from './ShapingBlock.svelte';
  import { onMount, tick } from 'svelte';

  let { 
    sessionId, 
    blocks, 
    activeExplorations, 
    onRespond 
  }: { 
    sessionId: string; 
    blocks: InteractionBlock[]; 
    activeExplorations: string[]; 
    onRespond: (content: string) => void;
  } = $props();

  let timelineContainer: HTMLDivElement;
  let autoScroll = $state(true);
  let operatorInput = $state('');

  // Auto-scroll logic
  $effect(() => {
    if (blocks.length && autoScroll && timelineContainer) {
      tick().then(() => {
        timelineContainer.scrollTop = timelineContainer.scrollHeight;
      });
    }
  });

  function handleScroll() {
    if (!timelineContainer) return;
    const { scrollTop, scrollHeight, clientHeight } = timelineContainer;
    const isAtBottom = scrollHeight - scrollTop - clientHeight < 10;
    autoScroll = isAtBottom;
  }

  function blockColor(type: string) {
    switch (type) {
      case 'operator_input': return 'bg-text-secondary';
      case 'agent_question': return 'bg-accent-primary';
      case 'agent_observation': return 'bg-status-success-text';
      case 'agent_proposal': return 'bg-accent-secondary';
      case 'exploration_start': return 'bg-text-tertiary';
      case 'exploration_complete': return 'bg-text-tertiary';
      case 'branch_point': return 'bg-status-warning-text';
      case 'system': return 'bg-text-tertiary/50';
      default: return 'bg-text-tertiary';
    }
  }

  async function submitResponse() {
    if (!operatorInput.trim()) return;
    onRespond(operatorInput);
    operatorInput = '';
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submitResponse();
    }
  }

  // Determine if we are awaiting input (last block is a question, or we just want to allow input)
  let awaitingInput = $derived(true); // For now, always allow input
</script>

<div class="flex flex-col h-full relative">
  <div 
    bind:this={timelineContainer}
    onscroll={handleScroll}
    class="flex-1 overflow-y-auto p-6 flex flex-col gap-0"
  >
    {#each blocks as block (block.id)}
      <div class="flex gap-3 py-3 border-b border-border-subtle/30 animate-in fade-in slide-in-from-bottom-2 duration-300">
        <!-- Timeline gutter -->
        <div class="w-6 flex flex-col items-center pt-1 shrink-0">
          <div class="w-2 h-2 rounded-full {blockColor(block.type)}"></div>
          <div class="flex-1 w-px bg-border-subtle mt-1"></div>
        </div>
        <!-- Block content -->
        <div class="flex-1 min-w-0">
          <ShapingBlock {block} {sessionId} {onRespond} />
        </div>
      </div>
    {/each}
    
    <!-- Active exploration indicators -->
    {#each activeExplorations as exp}
      <div class="flex gap-3 py-3 animate-pulse">
        <div class="w-6 flex items-center justify-center shrink-0">
          <div class="w-2 h-2 rounded-full bg-accent-primary animate-ping"></div>
        </div>
        <div class="text-[11px] text-text-tertiary">
          Exploring: {exp}
        </div>
      </div>
    {/each}
    
    <!-- Operator input area -->
    {#if awaitingInput}
      <div class="flex gap-3 py-3 mt-4">
        <div class="w-6 shrink-0"></div>
        <div class="flex-1 flex flex-col gap-2">
          <textarea 
            bind:value={operatorInput}
            onkeydown={handleKeydown}
            class="w-full min-h-[80px] p-3 rounded border border-border-default bg-bg-surface text-[13px] text-text-primary font-mono resize-y focus:outline-none focus:border-accent-primary"
            placeholder="Type your response... (Enter to send, Shift+Enter for new line)"
          ></textarea>
          <div class="flex justify-end">
            <button 
              onclick={submitResponse}
              disabled={!operatorInput.trim()}
              class="px-4 py-1.5 rounded bg-accent-primary text-white text-[12px] font-medium hover:bg-accent-primary/90 disabled:opacity-50 transition-colors"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>
