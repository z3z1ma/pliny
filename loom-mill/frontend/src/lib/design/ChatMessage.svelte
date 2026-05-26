<script lang="ts">
  export let message: { role: string; content: string; context?: any; timestamp: string };
  export let streaming: boolean = false;
  export let onRetry: (() => void) | undefined = undefined;

  let showContext = false;
  let copied = false;

  function formatTime(isoString: string) {
    if (!isoString) return '';
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    if (diffMins < 1) return 'just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${Math.floor(diffHours / 24)}d ago`;
  }

  // Basic markdown formatting
  function formatContent(text: string) {
    if (!text) return '';
    
    // First extract code blocks to avoid formatting inside them
    const codeBlocks: string[] = [];
    let processed = text.replace(/```([\s\S]*?)```/g, (match, code) => {
      codeBlocks.push(code);
      return `__CODE_BLOCK_${codeBlocks.length - 1}__`;
    });

    processed = processed
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code class="bg-bg-surface-hover px-1 py-0.5 rounded text-[11px] border border-border-default">$1</code>')
      .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" class="text-text-accent hover:underline" target="_blank">$1</a>')
      .replace(/\n/g, '<br>');

    // Restore code blocks
    processed = processed.replace(/__CODE_BLOCK_(\d+)__/g, (match, index) => {
      const code = codeBlocks[parseInt(index)]
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
      return `<pre class="bg-bg-surface-hover p-2 rounded text-[11px] overflow-x-auto my-1 border border-border-default"><code>${code}</code></pre>`;
    });

    return processed;
  }

  function getErrorMessage(text: string) {
    if (text.includes('not found')) return "Command not found. Check that the harness is installed.";
    if (text.includes('exited with code')) return "Harness crashed. Check stderr output above.";
    if (text.includes('ENOENT')) return "Command not found in PATH.";
    return text;
  }

  async function copyToClipboard() {
    try {
      await navigator.clipboard.writeText(message.content);
      copied = true;
      setTimeout(() => copied = false, 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  }
</script>

<div class="flex flex-col w-full mb-4 group text-[13px]">
  {#if message.role === 'user'}
    <div class="self-end max-w-[85%] flex flex-col items-end">
      {#if message.context}
        <div class="mb-1 text-[11px] text-text-tertiary flex items-center gap-1 cursor-pointer hover:text-text-secondary" on:click={() => showContext = !showContext}>
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
          {message.context.path} (lines {message.context.line_range[0]}-{message.context.line_range[1]})
        </div>
        {#if showContext}
          <div class="mb-2 p-2 bg-bg-surface-hover rounded border border-border-default text-[11px] text-text-secondary max-w-full overflow-x-auto whitespace-pre font-mono">
            {message.context.selected_text}
          </div>
        {/if}
      {/if}
      <div class="bg-bg-accent/10 text-text-primary px-3 py-2 rounded-lg rounded-tr-sm border border-bg-accent/20" title={new Date(message.timestamp).toLocaleString()}>
        {@html formatContent(message.content)}
      </div>
      <div class="text-[10px] text-text-tertiary mt-1 opacity-0 group-hover:opacity-100 transition-opacity">
        {formatTime(message.timestamp)}
      </div>
    </div>
  {:else if message.role === 'system'}
    {#if message.content.startsWith('Error:')}
      <div class="self-center flex flex-col items-center my-2 max-w-[90%]">
        <div class="text-[11px] text-status-error-text bg-status-error-bg/10 px-3 py-2 rounded border border-status-error-bg/30 text-center">
          <div class="font-medium mb-1">Error</div>
          <div>{getErrorMessage(message.content)}</div>
        </div>
        {#if onRetry}
          <button on:click={onRetry} class="mt-2 px-3 py-1 bg-bg-surface-hover hover:bg-bg-surface-active border border-border-default rounded text-[11px] text-text-secondary transition-colors">
            Retry
          </button>
        {/if}
      </div>
    {:else}
      <div class="self-center text-[11px] text-text-tertiary bg-bg-surface-hover px-2 py-1 rounded border border-border-default my-2">
        {message.content}
      </div>
    {/if}
  {:else}
    <div class="self-start w-full flex flex-col relative">
      <div class="text-text-primary leading-relaxed pr-6">
        {@html formatContent(message.content)}
        {#if streaming}
          <span class="inline-block w-2 h-3 bg-text-primary ml-1 animate-pulse align-middle"></span>
        {/if}
      </div>
      
      {#if !streaming}
        <button 
          class="absolute top-0 right-0 p-1 text-text-tertiary hover:text-text-primary opacity-0 group-hover:opacity-100 transition-opacity rounded hover:bg-bg-surface-hover"
          on:click={copyToClipboard}
          title="Copy message"
        >
          {#if copied}
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-status-success-text"><polyline points="20 6 9 17 4 12"></polyline></svg>
          {:else}
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
          {/if}
        </button>
      {/if}

      <div class="text-[10px] text-text-tertiary mt-1 opacity-0 group-hover:opacity-100 transition-opacity">
        {formatTime(message.timestamp)}
      </div>
    </div>
  {/if}
</div>
