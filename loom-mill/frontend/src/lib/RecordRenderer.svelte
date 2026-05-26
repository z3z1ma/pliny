<script lang="ts">
  let { content }: { content: string } = $props();

  type Token = 
    | { type: 'heading'; level: number; text: string }
    | { type: 'paragraph'; text: string }
    | { type: 'codeblock'; language: string; code: string }
    | { type: 'blockquote'; text: string }
    | { type: 'list'; ordered: boolean; items: { text: string; isAcc: boolean; accChecked: boolean }[] }
    | { type: 'table'; headers: string[]; rows: string[][] }
    | { type: 'hr' };

  let tokens = $derived(parseMarkdown(content));

  function parseMarkdown(md: string): Token[] {
    const lines = md.split('\n');
    const result: Token[] = [];
    let i = 0;

    while (i < lines.length) {
      const line = lines[i];
      
      // Empty lines
      if (line.trim() === '') {
        i++;
        continue;
      }

      // Code blocks
      if (line.startsWith('```')) {
        const language = line.slice(3).trim();
        let code = '';
        i++;
        while (i < lines.length && !lines[i].startsWith('```')) {
          code += lines[i] + '\n';
          i++;
        }
        result.push({ type: 'codeblock', language, code: code.trimEnd() });
        i++;
        continue;
      }

      // Headings
      const headingMatch = line.match(/^(#{1,6})\s+(.*)/);
      if (headingMatch) {
        result.push({ 
          type: 'heading', 
          level: headingMatch[1].length, 
          text: headingMatch[2] 
        });
        i++;
        continue;
      }

      // Horizontal rules
      if (line.match(/^---+$/) || line.match(/^\*\*\*+$/)) {
        result.push({ type: 'hr' });
        i++;
        continue;
      }

      // Blockquotes
      if (line.startsWith('>')) {
        let text = line.slice(1).trim();
        i++;
        while (i < lines.length && lines[i].startsWith('>')) {
          text += ' ' + lines[i].slice(1).trim();
          i++;
        }
        result.push({ type: 'blockquote', text });
        continue;
      }

      // Lists (bullet or numbered)
      const listMatch = line.match(/^(\s*)([-*]|\d+\.)\s+(.*)/);
      if (listMatch) {
        const isOrdered = /^\d+\./.test(listMatch[2]);
        const items = [];
        
        while (i < lines.length) {
          const itemMatch = lines[i].match(/^(\s*)([-*]|\d+\.)\s+(.*)/);
          if (!itemMatch) break;
          
          let itemText = itemMatch[3];
          let isAcc = false;
          let accChecked = false;
          
          // Check for acceptance criteria like "- [x] ACC-1" or "- [ ] ACC-1" or "- ACC-1"
          const accMatch = itemText.match(/^(\[[xX\s]\]\s+)?(ACC-\d+.*)/);
          if (accMatch) {
            isAcc = true;
            accChecked = accMatch[1] ? accMatch[1].toLowerCase().includes('x') : false;
            itemText = accMatch[2];
          } else if (itemText.startsWith('ACC-')) {
            isAcc = true;
            accChecked = false;
          }

          items.push({ text: itemText, isAcc, accChecked });
          i++;
        }
        result.push({ type: 'list', ordered: isOrdered, items });
        continue;
      }

      // Tables
      if (line.trim().startsWith('|') && i + 1 < lines.length && lines[i+1].trim().startsWith('|') && lines[i+1].includes('---')) {
        const headers = line.split('|').map(s => s.trim()).filter(s => s !== '');
        i += 2; // skip header and separator
        const rows = [];
        while (i < lines.length && lines[i].trim().startsWith('|')) {
          const row = lines[i].split('|').map(s => s.trim()).filter(s => s !== '');
          rows.push(row);
          i++;
        }
        result.push({ type: 'table', headers, rows });
        continue;
      }

      // Paragraphs
      let text = line;
      i++;
      while (i < lines.length && lines[i].trim() !== '' && !lines[i].match(/^(#{1,6}|```|>|[-*]|\d+\.|\||---)/)) {
        text += ' ' + lines[i].trim();
        i++;
      }
      result.push({ type: 'paragraph', text });
    }

    return result;
  }

  // Helper to render inline markdown (bold, italic, code, links)
  function renderInline(text: string): string {
    if (!text) return '';
    
    let html = text
      // Escape HTML
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      // Bold
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      // Italic
      .replace(/_(.*?)_/g, '<em>$1</em>')
      // Code
      .replace(/`(.*?)`/g, '<code class="px-1 py-0.5 rounded bg-bg-surface-active text-text-primary text-[11px] font-mono">$1</code>')
      // Links
      .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" class="text-accent-primary hover:underline" target="_blank" rel="noopener noreferrer">$1</a>');
      
    return html;
  }
</script>

<div class="markdown-body space-y-4 text-[13px] text-text-secondary leading-relaxed">
  {#each tokens as token}
    {#if token.type === 'heading'}
      {#if token.level === 1}
        <h1 class="text-xl font-semibold text-text-primary mt-6 mb-3">{@html renderInline(token.text)}</h1>
      {:else if token.level === 2}
        <h2 class="text-lg font-semibold text-text-primary mt-5 mb-2 border-b border-border-subtle pb-1">{@html renderInline(token.text)}</h2>
      {:else if token.level === 3}
        <h3 class="text-base font-medium text-text-primary mt-4 mb-2">{@html renderInline(token.text)}</h3>
      {:else}
        <h4 class="text-sm font-medium text-text-primary mt-3 mb-1">{@html renderInline(token.text)}</h4>
      {/if}
    {:else if token.type === 'paragraph'}
      <p>{@html renderInline(token.text)}</p>
    {:else if token.type === 'codeblock'}
      <div class="relative group rounded-md overflow-hidden bg-bg-surface-active border border-border-subtle my-3">
        {#if token.language}
          <div class="absolute top-0 right-0 px-2 py-1 text-[10px] text-text-tertiary uppercase font-medium bg-bg-surface-elevated rounded-bl-md border-b border-l border-border-subtle">
            {token.language}
          </div>
        {/if}
        <pre class="p-3 overflow-x-auto text-[12px] font-mono text-text-primary leading-normal"><code>{token.code}</code></pre>
      </div>
    {:else if token.type === 'blockquote'}
      <blockquote class="border-l-2 border-accent-primary pl-3 py-1 my-3 text-text-tertiary bg-bg-surface-active/50 rounded-r-md">
        {@html renderInline(token.text)}
      </blockquote>
    {:else if token.type === 'list'}
      {#if token.ordered}
        <ol class="list-decimal list-outside ml-5 space-y-1 my-2">
          {#each token.items as item}
            <li class="pl-1">{@html renderInline(item.text)}</li>
          {/each}
        </ol>
      {:else}
        <ul class="space-y-1.5 my-2">
          {#each token.items as item}
            <li class="flex items-start gap-2">
              {#if item.isAcc}
                <div class="mt-0.5 flex-shrink-0">
                  {#if item.accChecked}
                    <svg class="w-4 h-4 text-status-success-text" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                  {:else}
                    <svg class="w-4 h-4 text-text-tertiary" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle></svg>
                  {/if}
                </div>
                <span class={item.accChecked ? 'text-text-tertiary line-through' : 'text-text-primary font-medium'}>
                  {@html renderInline(item.text)}
                </span>
              {:else}
                <span class="mt-1.5 w-1.5 h-1.5 rounded-full bg-text-tertiary flex-shrink-0"></span>
                <span>{@html renderInline(item.text)}</span>
              {/if}
            </li>
          {/each}
        </ul>
      {/if}
    {:else if token.type === 'table'}
      <div class="overflow-x-auto my-4 rounded-md border border-border-subtle">
        <table class="w-full text-left border-collapse">
          <thead class="bg-bg-surface-active text-text-primary text-[12px]">
            <tr>
              {#each token.headers as header}
                <th class="px-3 py-2 font-medium border-b border-border-subtle">{@html renderInline(header)}</th>
              {/each}
            </tr>
          </thead>
          <tbody class="divide-y divide-border-subtle">
            {#each token.rows as row}
              <tr class="hover:bg-bg-surface-hover/50 transition-colors">
                {#each row as cell}
                  <td class="px-3 py-2">{@html renderInline(cell)}</td>
                {/each}
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {:else if token.type === 'hr'}
      <hr class="border-border-subtle my-6" />
    {/if}
  {/each}
</div>
