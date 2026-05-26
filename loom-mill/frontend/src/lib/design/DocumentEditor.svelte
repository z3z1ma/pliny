<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { EditorView, keymap, lineNumbers, highlightActiveLine } from '@codemirror/view';
  import { EditorState } from '@codemirror/state';
  import { markdown } from '@codemirror/lang-markdown';
  import { defaultKeymap, indentWithTab, history, historyKeymap } from '@codemirror/commands';
  import { searchKeymap, highlightSelectionMatches } from '@codemirror/search';
  import { millTheme, millHighlighting } from './editor-theme';
  import { recordLinks, recordLinksClick, loomAutocompletion, recordHoverPreview } from './editor-extensions';
  import { apiUrl } from '../api';
  import { store } from '../ws.svelte.ts';
  import SelectionAction from './SelectionAction.svelte';
  
  let { documentPath, onSave, onAttachContext, onNavigate }: { documentPath: string | null; onSave: (content: string) => void; onAttachContext?: (context: any) => void; onNavigate?: (id: string) => void } = $props();
  
  let view = $state<EditorView | null>(null);
  let modified = $state(false);
  let lastSavedContent = '';
  let lastKnownHash = $state('');
  let loading = $state(false);
  let conflict = $state(false);
  let conflictContent = $state<string | null>(null);
  let pollTimer: ReturnType<typeof setInterval> | undefined;
  let editorContainer: HTMLDivElement;

  let selectionAction = $state<{ top: number; left: number; text: string; lineRange: [number, number] } | null>(null);
  let selectionTimeout: ReturnType<typeof setTimeout>;

  let headings = $state<{ level: number; text: string; line: number }[]>([]);

  let documentTitle = $derived(headings.length > 0 ? headings[0].text : null);

  let showHeadings = $state(false);

  function updateHeadings(doc: string) {
    const lines = doc.split('\n');
    headings = lines
      .map((line, i) => {
        const match = line.match(/^(#{1,3})\s+(.+)/);
        if (match) return { level: match[1].length, text: match[2], line: i + 1 };
        return null;
      })
      .filter(Boolean) as { level: number; text: string; line: number }[];
  }

  function jumpToLine(lineNum: number) {
    if (view) {
      const line = view.state.doc.line(lineNum);
      view.dispatch({ selection: { anchor: line.from }, scrollIntoView: true });
      view.focus();
    }
    showHeadings = false;
  }

  // Fetch content when documentPath changes
  $effect(() => {
    if (documentPath) {
      fetchContent(documentPath);
    } else {
      if (view) view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: '' } });
      modified = false;
    }
  });

  // Poll the open document for content-only external changes.
  $effect(() => {
    if (documentPath) {
      clearInterval(pollTimer);
      pollTimer = setInterval(pollForChanges, 1000);
    } else {
      clearInterval(pollTimer);
      pollTimer = undefined;
    }

    return () => {
      clearInterval(pollTimer);
      pollTimer = undefined;
    };
  });

  // Keep record deletion handling separate from content synchronization.
  $effect(() => {
    if (documentPath) {
      const record = store.state.records.find(r => r.metadata.id === documentPath || r.path === documentPath);
      if (!record) {
        conflict = false;
        conflictContent = null;
      }
    }
  });

  async function fetchContent(path: string) {
    loading = true;
    try {
      const res = await fetch(apiUrl(`/records/${encodeURIComponent(path)}/content`));
      if (res.ok) {
        const data = await res.json();
        lastSavedContent = data.content;
        lastKnownHash = data.hash || '';
        setContent(data.content);
        modified = false;
        conflict = false;
        conflictContent = null;
      }
    } finally {
      loading = false;
    }
  }

  async function pollForChanges() {
    if (!documentPath || loading) return;

    try {
      const headers: Record<string, string> = {};
      if (lastKnownHash) {
        headers['If-None-Match'] = `"${lastKnownHash}"`;
      }

      const res = await fetch(apiUrl(`/records/${encodeURIComponent(documentPath)}/content`), { headers });

      if (res.status === 304) return;
      if (!res.ok) return;

      const data = await res.json();
      lastKnownHash = data.hash || '';

      if (data.content === lastSavedContent) return;

      if (!modified) {
        lastSavedContent = data.content;
        setContent(data.content, true);
        modified = false;
      } else {
        conflict = true;
        conflictContent = data.content;
      }
    } catch {
      // Network errors are transient; try again on the next poll tick.
    }
  }

  function setContent(content: string, preserveScroll = false) {
    if (view) {
      const scrollTop = view.scrollDOM.scrollTop;
      view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: content } });
      updateHeadings(content);
      setTimeout(() => {
        if (view) {
          view.scrollDOM.scrollTop = preserveScroll ? scrollTop : 0;
        }
      }, 0);
    }
  }

  function handleSave() {
    if (view && modified) {
      const content = view.state.doc.toString();
      onSave(content);
      lastSavedContent = content;
      lastKnownHash = '';
      modified = false;
      conflict = false;
      conflictContent = null;
    }
  }

  function acceptExternalChanges() {
    if (conflictContent !== null) {
      lastSavedContent = conflictContent;
      setContent(conflictContent, true);
      modified = false;
      conflict = false;
      conflictContent = null;
    }
  }

  function keepLocalChanges() {
    conflict = false;
    conflictContent = null;
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
          highlightSelectionMatches(),
          markdown(),
          millTheme,
          millHighlighting,
          ...(onNavigate ? [recordLinks(onNavigate), recordLinksClick(onNavigate)] : []),
          loomAutocompletion(() => store.state.records),
          recordHoverPreview(() => store.state.records),
          history(),
          EditorView.lineWrapping,
          keymap.of([...defaultKeymap, ...historyKeymap, ...searchKeymap, indentWithTab]),
          saveKeymap,
          EditorView.updateListener.of((update) => {
            if (update.docChanged) {
              const newContent = view!.state.doc.toString();
              updateHeadings(newContent);
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
  <div class="flex items-center h-8 px-4 border-b border-border-default bg-bg-surface text-[11px] shrink-0 relative">
    {#if documentPath}
      <button onclick={() => showHeadings = !showHeadings} class="text-[10px] text-text-tertiary hover:text-text-secondary mr-2">
        §
      </button>
      
      {#if showHeadings}
        <div class="absolute top-8 left-0 z-50 bg-bg-surface border border-border-default rounded shadow-lg max-h-64 overflow-y-auto w-64">
          {#each headings as h}
            <button onclick={() => jumpToLine(h.line)} class="block w-full text-left px-3 py-1.5 text-[11px] hover:bg-bg-surface-active"
              style="padding-left: {(h.level - 2) * 12 + 12}px">
              {h.text}
            </button>
          {/each}
        </div>
      {/if}

      <div class="flex items-center gap-1 text-[11px]">
        <span class="text-text-tertiary capitalize">{documentPath.split('/')[0]}</span>
        <span class="text-text-tertiary">/</span>
        <span class="text-text-secondary font-medium">{documentTitle || documentPath.split('/')[1] || documentPath}</span>
      </div>

      {#if modified}
        <span class="ml-2 w-2 h-2 rounded-full bg-accent-primary" title="Unsaved changes"></span>
      {/if}
      <div class="flex-1"></div>
      {#if onAttachContext}
        <button 
          class="text-text-tertiary hover:text-text-primary transition-colors flex items-center gap-1 mr-16"
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

  {#if conflict}
    <div class="flex items-center gap-2 px-3 py-2 bg-status-warning-bg/30 border-b border-status-warning-border text-[11px]">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-status-warning-text shrink-0">
        <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
        <path d="M12 9v4"/><path d="M12 17h.01"/>
      </svg>
      <span class="text-status-warning-text flex-1">File changed externally. You have unsaved edits.</span>
      <button
        onclick={acceptExternalChanges}
        class="px-2 py-0.5 rounded text-[10px] font-medium bg-accent-primary/10 text-accent-primary hover:bg-accent-primary/20 transition-colors"
      >
        Accept external
      </button>
      <button
        onclick={keepLocalChanges}
        class="px-2 py-0.5 rounded text-[10px] font-medium bg-bg-surface-active text-text-secondary hover:bg-bg-surface-hover transition-colors"
      >
        Keep mine
      </button>
    </div>
  {/if}

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
