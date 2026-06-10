<script lang="ts">
  import { Node, Anchor } from 'svelvet';
  import { causalEdgeColor } from './edge-style';

  let { node, position, connections = [], onRespond, disabled = false, usedOptions = [] } = $props();
  
  let responseText = $state('');
  
  function handleSubmit() {
    if (disabled) return;

    if (responseText.trim() && onRespond) {
      onRespond(responseText.trim());
      responseText = '';
    }
  }
  
  function handleKeydown(e: KeyboardEvent) {
    if (disabled) return;

    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  function respondToOption(option: string) {
    if (disabled || usedOptions.includes(option) || !onRespond) return;

    onRespond(option, option);
  }
</script>

<Node id={node.id} {position} let:selected>
  <div class="bg-bg-surface border rounded-lg p-3 min-w-[250px] max-w-[350px] shadow-sm
    {selected ? 'ring-2 ring-accent-primary/50' : ''}
    {node.status === 'active' ? 'border-l-4 border-l-purple-500 border-border-default opacity-100' : ''}
    {node.status === 'dead' ? 'border-l-4 border-l-red-500/50 border-border-subtle opacity-40 grayscale' : ''}
    {node.status === 'stale' ? 'border-l-4 border-l-purple-500/50 border-dashed border-border-subtle opacity-60 animate-pulse' : ''}
  ">
    <div class="text-[11px] font-semibold text-purple-400 mb-1 uppercase tracking-wider">Question</div>
    <div class="text-[13px] text-text-primary whitespace-pre-wrap break-words mb-3">
      {node.content.question}
    </div>
    
    {#if node.status === 'active'}
      {#if node.content.options && node.content.options.length > 0}
        <div class="flex flex-wrap gap-2">
          {#each node.content.options as option}
            {@const optionUsed = usedOptions.includes(option)}
            <button 
              class="px-3 py-1.5 text-[12px] border rounded-md transition-colors text-left
                {disabled || optionUsed
                  ? 'bg-bg-surface border-border-subtle text-text-tertiary cursor-not-allowed opacity-60'
                  : 'bg-bg-surface-hover border-border-default hover:border-purple-400 hover:text-purple-300'}"
              disabled={disabled || optionUsed}
              aria-label={optionUsed ? `${option} already branched` : option}
              title={optionUsed ? 'Already branched' : undefined}
              onclick={() => respondToOption(option)}
            >
              {option}
            </button>
          {/each}
        </div>
      {:else}
        <div class="flex flex-col gap-2">
          <textarea 
            bind:value={responseText}
            onkeydown={handleKeydown}
            placeholder="Type your answer..."
            class="w-full bg-bg-primary border border-border-default rounded p-2 text-[12px] text-text-primary resize-none focus:outline-none focus:border-purple-400 disabled:cursor-not-allowed disabled:opacity-60 disabled:text-text-tertiary"
            rows="2"
            {disabled}
          ></textarea>
          <button 
            class="self-end px-3 py-1 text-[11px] bg-purple-500/20 text-purple-300 border border-purple-500/30 rounded hover:bg-purple-500/30 transition-colors disabled:opacity-50"
            disabled={disabled || !responseText.trim()}
            onclick={handleSubmit}
          >
            Submit
          </button>
        </div>
      {/if}
    {/if}
  </div>

  <div slot="anchorNorth">
    <Anchor id="{node.id}-in" input />
  </div>

  <div slot="anchorSouth">
    {#if connections && connections.length > 0}
      <Anchor id="{node.id}-out" output {connections} edgeColor={causalEdgeColor} />
    {:else}
      <Anchor id="{node.id}-out" output edgeColor={causalEdgeColor} />
    {/if}
  </div>
</Node>
