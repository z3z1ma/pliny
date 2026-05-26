<script lang="ts">
  let { diff }: { diff: string } = $props();

  interface DiffLine {
    type: 'add' | 'remove' | 'context' | 'hunk' | 'header';
    content: string;
    oldLineNum: number | null;
    newLineNum: number | null;
  }

  interface DiffFile {
    oldPath: string;
    newPath: string;
    lines: DiffLine[];
    collapsed: boolean;
  }

  let files = $derived(() => {
    const parsedFiles: DiffFile[] = [];
    if (!diff) return parsedFiles;
    
    let currentFile: DiffFile | null = null;
    let oldLine = 0;
    let newLine = 0;

    const lines = diff.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (line.startsWith('diff --git ')) {
        if (currentFile) parsedFiles.push(currentFile);
        const match = line.match(/diff --git a\/(.+) b\/(.+)/);
        currentFile = {
          oldPath: match ? match[1] : '',
          newPath: match ? match[2] : '',
          lines: [],
          collapsed: false
        };
      } else if (line.startsWith('--- ')) {
        if (!currentFile) {
          currentFile = { oldPath: line.substring(4), newPath: '', lines: [], collapsed: false };
        } else {
          currentFile.oldPath = line.substring(4).replace(/^a\//, '');
        }
      } else if (line.startsWith('+++ ')) {
        if (currentFile) {
          currentFile.newPath = line.substring(4).replace(/^b\//, '');
        }
      } else if (line.startsWith('@@ ')) {
        if (currentFile) {
          const match = line.match(/@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@/);
          if (match) {
            oldLine = parseInt(match[1], 10);
            newLine = parseInt(match[2], 10);
          }
          currentFile.lines.push({ type: 'hunk', content: line, oldLineNum: null, newLineNum: null });
        }
      } else if (line.startsWith('+')) {
        if (currentFile) {
          currentFile.lines.push({ type: 'add', content: line, oldLineNum: null, newLineNum: newLine++ });
        }
      } else if (line.startsWith('-')) {
        if (currentFile) {
          currentFile.lines.push({ type: 'remove', content: line, oldLineNum: oldLine++, newLineNum: null });
        }
      } else if (line.startsWith(' ')) {
        if (currentFile) {
          currentFile.lines.push({ type: 'context', content: line, oldLineNum: oldLine++, newLineNum: newLine++ });
        }
      } else if (line === '\\ No newline at end of file') {
        if (currentFile) {
          currentFile.lines.push({ type: 'context', content: line, oldLineNum: null, newLineNum: null });
        }
      } else if (currentFile && currentFile.lines.length === 0 && !line.startsWith('index ') && !line.startsWith('new file ') && !line.startsWith('deleted file ')) {
        // Capture things like "Binary files differ" or other metadata
        currentFile.lines.push({ type: 'context', content: line, oldLineNum: null, newLineNum: null });
      }
    }
    if (currentFile) parsedFiles.push(currentFile);
    return parsedFiles;
  });

  function toggleCollapse(file: DiffFile) {
    file.collapsed = !file.collapsed;
  }
</script>

<div class="flex flex-col gap-4 font-mono text-xs">
  {#if !diff || diff.trim() === ''}
    <div class="p-4 text-center text-text-tertiary italic bg-bg-surface border border-border-default rounded">
      No changes
    </div>
  {:else}
    {#each files() as file}
      <div class="border border-border-default rounded overflow-hidden bg-bg-surface">
        <button 
          class="w-full flex items-center justify-between px-3 py-2 bg-bg-surface-elevated border-b border-border-default hover:bg-bg-surface-hover transition-colors"
          onclick={() => toggleCollapse(file)}
        >
          <span class="font-semibold text-text-primary">
            {file.newPath !== '/dev/null' ? file.newPath : file.oldPath}
          </span>
          <span class="text-text-tertiary">
            {file.collapsed ? 'Expand' : 'Collapse'}
          </span>
        </button>
        
        {#if !file.collapsed}
          <div class="overflow-x-auto">
            <table class="w-full border-collapse text-left whitespace-pre">
              <tbody>
                {#each file.lines as line}
                  <tr class="
                    {line.type === 'add' ? 'bg-status-success-bg text-status-success-text' : ''}
                    {line.type === 'remove' ? 'bg-status-error-bg text-status-error-text' : ''}
                    {line.type === 'hunk' ? 'bg-bg-surface-active text-accent-text' : ''}
                    {line.type === 'context' ? 'text-text-secondary' : ''}
                  ">
                    <td class="w-10 px-2 py-0.5 text-right text-text-tertiary select-none border-r border-border-subtle bg-bg-surface-elevated">
                      {line.oldLineNum ?? ''}
                    </td>
                    <td class="w-10 px-2 py-0.5 text-right text-text-tertiary select-none border-r border-border-subtle bg-bg-surface-elevated">
                      {line.newLineNum ?? ''}
                    </td>
                    <td class="px-3 py-0.5">
                      {line.content}
                    </td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        {/if}
      </div>
    {/each}
  {/if}
</div>
