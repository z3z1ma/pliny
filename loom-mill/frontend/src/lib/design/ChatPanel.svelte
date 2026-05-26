<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { store } from '../ws.svelte.ts';
  import { apiUrl } from '../api';
  import ChatMessage from './ChatMessage.svelte';
  import ChatInput from './ChatInput.svelte';

  let { documentPath = null, attachedContext = null, onClearContext }: { documentPath?: string | null, attachedContext?: any, onClearContext: () => void } = $props();

  let messagesContainer: HTMLDivElement;
  let isCreatingSession = $state(false);
  let harnessCommand = $state('echo');
  let testStatus: 'idle' | 'testing' | 'success' | 'error' = $state('idle');
  let lastUserMessage: { text: string, context?: any } | null = $state(null);

  onMount(() => {
    harnessCommand = localStorage.getItem('mill-harness-command') || 'echo';
    if (!store.chatSession.id) {
      createSession();
    }
  });

  function saveHarnessConfig() {
    localStorage.setItem('mill-harness-command', harnessCommand);
  }

  async function testConnection() {
    testStatus = 'testing';
    try {
      // Create a temporary session
      const sessionRes = await fetch(apiUrl('/chat/sessions'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ harness_command: harnessCommand })
      });
      if (!sessionRes.ok) throw new Error('Failed to create session');
      const sessionData = await sessionRes.json();
      const sessionId = sessionData.session_id;

      // Send a ping message
      const msgRes = await fetch(apiUrl(`/chat/sessions/${sessionId}/messages`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: 'ping' })
      });

      if (msgRes.ok) {
        testStatus = 'success';
      } else {
        testStatus = 'error';
      }

      // Clean up session
      await fetch(apiUrl(`/chat/sessions/${sessionId}`), { method: 'DELETE' });

      setTimeout(() => testStatus = 'idle', 3000);
    } catch (err) {
      testStatus = 'error';
      setTimeout(() => testStatus = 'idle', 3000);
    }
  }

  // Auto-scroll when messages change
  $effect(() => {
    if (store.chatSession.messages.length || store.chatSession.streamingContent) {
      scrollToBottom();
    }
  });

  async function scrollToBottom() {
    await tick();
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  }

  async function createSession() {
    if (isCreatingSession) return;
    isCreatingSession = true;
    
    try {
      const response = await fetch(apiUrl('/chat/sessions'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          document_path: documentPath,
          harness_command: harnessCommand
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        store.chatSession = {
          id: data.session_id,
          messages: [],
          streaming: false,
          streamingContent: ''
        };
      } else {
        console.error('Failed to create chat session:', await response.text());
        store.chatSession = {
          ...store.chatSession,
          messages: [...store.chatSession.messages, {
            role: 'system',
            content: 'Failed to create chat session. Is the harness running?',
            timestamp: new Date().toISOString()
          }]
        };
      }
    } catch (err) {
      console.error('Error creating chat session:', err);
      store.chatSession = {
        ...store.chatSession,
        messages: [...store.chatSession.messages, {
          role: 'system',
          content: 'Error connecting to chat backend.',
          timestamp: new Date().toISOString()
        }]
      };
    } finally {
      isCreatingSession = false;
    }
  }

  async function handleSend(text: string, context?: any) {
    if (!store.chatSession.id) {
      await createSession();
      if (!store.chatSession.id) return; // Failed to create
    }

    lastUserMessage = { text, context };

    // Optimistic update
    const userMessage = {
      role: 'user',
      content: text,
      context,
      timestamp: new Date().toISOString()
    };
    
    store.chatSession = {
      ...store.chatSession,
      messages: [...store.chatSession.messages, userMessage],
      streaming: true,
      streamingContent: ''
    };

    try {
      const response = await fetch(apiUrl(`/chat/sessions/${store.chatSession.id}/messages`), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          content: text,
          context
        })
      });

      if (!response.ok) {
        console.error('Failed to send message:', await response.text());
        store.chatSession = {
          ...store.chatSession,
          streaming: false,
          messages: [...store.chatSession.messages, {
            role: 'system',
            content: 'Failed to send message.',
            timestamp: new Date().toISOString()
          }]
        };
      } else {
        const data = await response.json();
        // If WebSocket didn't deliver the response, use the HTTP response
        if (store.chatSession.streaming) {
          if (data.message && !store.chatSession.messages.some(m => m.content === data.message.content)) {
            store.chatSession = {
              ...store.chatSession,
              streaming: false,
              streamingContent: '',
              messages: [...store.chatSession.messages, data.message]
            };
          } else {
            store.chatSession = {
              ...store.chatSession,
              streaming: false,
              streamingContent: ''
            };
          }
        }
      }
    } catch (err) {
      console.error('Error sending message:', err);
      store.chatSession = {
        ...store.chatSession,
        streaming: false,
        messages: [...store.chatSession.messages, {
          role: 'system',
          content: 'Error: Network error sending message.',
          timestamp: new Date().toISOString()
        }]
      };
    }
  }

  function handleRetry() {
    if (!lastUserMessage) return;
    let newMessages = [...store.chatSession.messages];
    // Remove the last system error message
    const lastMsg = newMessages[newMessages.length - 1];
    if (lastMsg && lastMsg.role === 'system' && lastMsg.content.startsWith('Error:')) {
      newMessages = newMessages.slice(0, -1);
    }
    // Remove the optimistic user message so it doesn't duplicate
    const lastUserMsgIdx = newMessages.map(m => m.role).lastIndexOf('user');
    if (lastUserMsgIdx !== -1) {
      newMessages = newMessages.slice(0, lastUserMsgIdx);
    }
    store.chatSession = {
      ...store.chatSession,
      messages: newMessages
    };
    handleSend(lastUserMessage.text, lastUserMessage.context);
  }

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
</script>

<div class="flex flex-col h-full w-full bg-bg-surface">
  <!-- Header -->
  <div class="flex items-center justify-between h-10 px-4 border-b border-border-default shrink-0">
    <div class="flex flex-col">
      <div class="flex items-center gap-1.5 text-[11px] font-medium text-text-secondary">
        <span>Chat</span>
        <span class="text-text-tertiary">·</span>
        <select bind:value={harnessCommand} on:change={saveHarnessConfig}
          class="max-w-24 bg-transparent text-text-secondary text-[10px] focus:outline-none focus:text-text-primary">
          <option value="echo">echo</option>
          <option value="opencode run">opencode run</option>
          <option value="claude -p">claude -p</option>
          <option value="codex exec">codex exec</option>
        </select>
        <span class="text-text-tertiary">·</span>
        <button on:click={testConnection} class="text-[9px] text-text-tertiary hover:text-accent-primary transition-colors">
          {#if testStatus === 'testing'}
            Testing...
          {:else if testStatus === 'success'}
            <span class="text-status-success-text">Connected</span>
          {:else if testStatus === 'error'}
            <span class="text-status-error-text">Failed</span>
          {:else}
            Test
          {/if}
        </button>
      </div>
      {#if store.chatSession.id}
        <div class="text-[9px] text-text-tertiary">
          Session · {store.chatSession.messages.length} messages
          {#if store.chatSession.messages.length > 0}
            · {formatTime(store.chatSession.messages[store.chatSession.messages.length - 1].timestamp)}
          {/if}
        </div>
      {/if}
    </div>
    <button 
      class="text-[10px] text-text-tertiary hover:text-text-primary transition-colors"
      on:click={createSession}
      disabled={isCreatingSession || store.chatSession.streaming}
    >
      New
    </button>
  </div>

  <!-- Messages Area -->
  <div 
    bind:this={messagesContainer}
    class="flex-1 overflow-y-auto p-4 flex flex-col gap-2"
  >
    {#if store.chatSession.messages.length === 0 && !store.chatSession.streaming}
      <div class="flex-1 flex flex-col items-center justify-center text-center text-text-tertiary p-4">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mb-2 opacity-50"><path d="M14 9a2 2 0 0 1-2 2H6l-4 4V4c0-1.1.9-2 2-2h8a2 2 0 0 1 2 2v5Z"/><path d="M18 9h2a2 2 0 0 1 2 2v11l-4-4h-6a2 2 0 0 1-2-2v-1"/></svg>
        <p class="text-[12px]">Shape work with the AI harness.</p>
        <p class="text-[11px] mt-1 opacity-70">Select text in the editor to attach context.</p>
      </div>
    {:else}
      {#each store.chatSession.messages as message}
        <ChatMessage {message} onRetry={handleRetry} />
      {/each}
      
      {#if store.chatSession.streamingContent}
        <ChatMessage 
          message={{ role: 'assistant', content: store.chatSession.streamingContent, timestamp: new Date().toISOString() }} 
          streaming={true} 
        />
      {/if}

      {#if store.chatSession.streaming && !store.chatSession.streamingContent}
        <div class="flex items-center gap-2 py-3 text-[11px] text-text-tertiary">
          <span class="flex gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-accent-primary animate-bounce" style="animation-delay: 0ms"></span>
            <span class="w-1.5 h-1.5 rounded-full bg-accent-primary animate-bounce" style="animation-delay: 150ms"></span>
            <span class="w-1.5 h-1.5 rounded-full bg-accent-primary animate-bounce" style="animation-delay: 300ms"></span>
          </span>
          <span>Generating response...</span>
        </div>
      {/if}
    {/if}
  </div>

  <!-- Input Area -->
  <ChatInput 
    onSend={handleSend} 
    disabled={store.chatSession.streaming || isCreatingSession} 
    {attachedContext}
    {onClearContext}
  />
</div>
