<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { EditorView, keymap, lineNumbers, highlightActiveLine, drawSelection } from '@codemirror/view';
  import { EditorState } from '@codemirror/state';
  import { markdown } from '@codemirror/lang-markdown';
  import { defaultKeymap, indentWithTab } from '@codemirror/commands';
  import { searchKeymap, highlightSelectionMatches } from '@codemirror/search';
  import { millTheme, millHighlighting } from './editor-theme';
  import { apiUrl } from '../api';
  import { store } from '../ws.svelte';
  import SelectionAction from './SelectionAction.svelte';
  
  let { documentPath, onSave, onAttachContext }: { documentPath: string | null; onSave: (content: string) => void; onAttachContext?: (context: any) => void } = $props();
  
  let view: EditorView | null = null;
  let modified = $state(false);
  let lastSavedContent = '';
  let loading = $state(false);
  let conflict = $state(false);
  let editorContainer: HTMLDivElement;

  let selectionAction = $state<{ top: number; left: number; text: string; lineRange: [number, number] } | null>(null);
  let selectionTimeout: ReturnType<typeof setTimeout>;

  // Fetch content when documentPath changes
  $effect(() => {
    if (documentPath) {
      fetchContent(documentPath);
    } else {
      if (view) view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: '' } });
      modified = false;
    }
  });

  // Watch for external file changes
  $effect(() => {
    // When store records change and matches our document, check for external update
    const record = store.state.records.find(r => r.metadata.id === documentPath || r.path === documentPath);
    if (record && !modified && view) {
      // Re-fetch to see if content changed externally
      // (The RecordChanged event means the file was modified)
      // We only re-fetch if we don't have local modifications to avoid overwriting user's work
      fetchContent(documentPath!);
    } else if (record && modified && view) {
      // If we have local modifications and the file changed externally, it's a conflict
      conflict = true;
    }
  });

  async function fetchContent(path: string) {
    loading = true;
    try {
      const res = await fetch(apiUrl(`/records/${encodeURIComponent(path)}/content`));
      if (res.ok) {
        const data = await res.json();
        setContent(data.content);
        lastSavedContent = data.content;
        modified = false;
        conflict = false;
      }
    } finally {
      loading = false;
    }
  }

  function setContent(content: string) {
    if (view) {
      view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: content } });
    }
  }

  function handleSave() {
    if (view && modified) {
      const content = view.state.doc.toString();
      onSave(content);
      lastSavedContent = content;
      modified = false;
      conflict = false;
    }
  }

  function handleAttachContext() {
    if (!view || !documentPath || !onAttachContext) return;
    
    const selection = view.state.selection.main;
    if (selection.empty) return;
    
    const selectedText = view.state.sliceDoc(selection.from, selection.to);
    const startLine = view.state.doc.lineAt(selection.from).number;
    const endLine = view.state.doc.lineAt(selection.to).number;
    
    onAttachContext({
      path: documentPath,
      selected_text: selectedText,
      line_range: [startLine, endLine]
    });
  }

  function sendSelectionToChat() {
    if (selectionAction && documentPath && onAttachContext) {
      onAttachContext({
        path: documentPath,
        selected_text: selectionAction.text,
        line_range: selectionAction.lineRange
      });
      selectionAction = null;
    }
  }

  function initEditor(node: HTMLDivElement) {
    const saveKeymap = keymap.of([{ key: 'Mod-s', run: () => { handleSave(); return true; } }]);
    
    view = new EditorView({
      state: EditorState.create({
        doc: '',
        extensions: [
          lineNumbers(),
          highlightActiveLine(),
          drawSelection(),
          highlightSelectionMatches(),
          markdown(),
          millTheme,
          millHighlighting,
          keymap.of([...defaultKeymap, ...searchKeymap, indentWithTab]),
          saveKeymap,
          EditorView.updateListener.of((update) => {
            if (update.docChanged) {
              const newContent = view!.state.doc.toString();
              if (newContent !== lastSavedContent) {
                modified = true;
              } else {
                modified = false;
              }
            }
            
            if (update.selectionSet) {
              clearTimeout(selectionTimeout);
              const selection = update.state.selection.main;
              if (selection.from !== selection.to) {
                const text = update.state.doc.sliceString(selection.from, selection.to);
                if (text.length > 5) {
                  selectionTimeout = setTimeout(() => {
                    if (!view || !editorContainer) return;
                    const coords = view.coordsAtPos(selection.from);
                    if (coords) {
                      const fromLine = update.state.doc.lineAt(selection.from).number;
                      const toLine = update.state.doc.lineAt(selection.to).number;
                      const containerRect = editorContainer.getBoundingClientRect();
                      selectionAction = {
                        top: coords.top - containerRect.top + editorContainer.scrollTop,
                        left: coords.left - containerRect.left + editorContainer.scrollLeft,
                        text,
                        lineRange: [fromLine, toLine]
                      };
                    }
                  }, 200);
                }
              } else {
                selectionAction = null;
              }
            }
          }),
        ],
      }),
      parent: node,
    });

    if (documentPath) {
      fetchContent(documentPath);
    }

    return {
      destroy() {
        view?.destroy();
        view = null;
      }
    };
  }

  onDestroy(() => { view?.destroy(); });
</script>

<div class="flex flex-col h-full">
  <!-- Editor header -->
  <div class="flex items-center h-8 px-4 border-b border-border-default bg-bg-surface text-[11px] shrink-0">
    {#if documentPath}
      <span class="text-text-secondary truncate">{documentPath}</span>
      {#if modified}
        <span class="ml-2 w-2 h-2 rounded-full bg-accent-primary" title="Unsaved changes"></span>
      {/if}
      {#if conflict}
        <span class="ml-2 text-status-warning-text">File changed externally</span>
        <button class="ml-1 text-[10px] underline" onclick={() => fetchContent(documentPath!)}>Reload</button>
      {/if}
      <div class="flex-1"></div>
      {#if onAttachContext}
        <button 
          class="text-text-tertiary hover:text-text-primary transition-colors flex items-center gap-1"
          onclick={handleAttachContext}
          title="Select text and click to attach to chat"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
          Attach
        </button>
      {/if}
    {:else}
      <span class="text-text-tertiary">No document open</span>
    {/if}
  </div>
  
  <!-- Editor body -->
  <div bind:this={editorContainer} class="flex-1 min-h-0 overflow-auto relative {documentPath ? 'block' : 'hidden'}">
    {#if selectionAction}
      <SelectionAction 
        position={{ top: selectionAction.top, left: selectionAction.left }}
        onSendToChat={sendSelectionToChat}
      />
    {/if}
    <div class="h-full" use:initEditor></div>
  </div>
  {#if !documentPath}
    <div class="flex-1 flex items-center justify-center text-[12px] text-text-tertiary">
      Select a record from the graph to open it here.
    </div>
  {/if}
</div>
