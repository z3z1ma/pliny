<script lang="ts">
  import { apiUrl } from '../../api';
  import { store } from '../../ws.svelte.ts';
  
  let { sessionId, onAdvance }: {
    sessionId: string;
    onAdvance: () => void;
  } = $props();
  
  let inputText = $state('');
  let submitting = $state(false);
  
  let sessionState = $derived(store.shapingSession?.advanceState ?? 'idle');
  let advanceError = $derived(store.shapingSession?.advanceError ?? null);
  
  let elapsed = $state(0);
  let timer: ReturnType<typeof setInterval> | null = null;

  $effect(() => {
    if (sessionState === 'thinking') {
      if (!timer) {
        elapsed = 0;
        timer = setInterval(() => { elapsed++; }, 1000);
      }
    } else {
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
    }
  });
  
  async function submit() {
    if (!inputText.trim() || submitting || sessionState === 'thinking') return;
    submitting = true;
    try {
      await fetch(apiUrl(`/shaping/sessions/${sessionId}/input`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText })
      });
      inputText = '';
      onAdvance();
    } catch (err) {
      console.error('Failed to send input:', err);
    } finally {
      submitting = false;
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }
</script>

<div class="w-full bg-bg-surface border-t border-border-default p-4 flex flex-col gap-2 shrink-0">
  <div class="flex items-center gap-2 text-sm">
    {#if sessionState === 'idle'}
      <div class="w-2 h-2 rounded-full bg-status-success-text"></div>
      <span class="text-text-secondary">Ready — type to continue or ask a follow-up</span>
    {:else if sessionState === 'thinking'}
      <div class="w-2 h-2 rounded-full bg-accent-primary animate-ping"></div>
      <span class="text-text-secondary">Processing... {elapsed}s</span>
    {:else if sessionState === 'error'}
      <div class="w-2 h-2 rounded-full bg-status-error-text"></div>
      <span class="text-status-error-text">Error: {advanceError}</span>
      <button class="px-2 py-0.5 bg-bg-secondary hover:bg-bg-tertiary rounded text-text-primary text-xs" onclick={onAdvance}>
        Retry
      </button>
    {/if}
  </div>
  
  <div class="flex gap-2">
    <textarea
      bind:value={inputText}
      onkeydown={handleKeydown}
      disabled={sessionState === 'thinking' || submitting}
      placeholder="What's next?"
      class="flex-1 bg-bg-primary border border-border-default rounded p-2 text-text-primary focus:outline-none focus:ring-1 focus:ring-brand-primary resize-none min-h-[40px] max-h-[120px] disabled:opacity-50"
      rows="1"
    ></textarea>
    <button
      onclick={submit}
      disabled={!inputText.trim() || sessionState === 'thinking' || submitting}
      class="px-4 py-2 bg-brand-primary hover:bg-brand-secondary text-white rounded font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
    >
      Send
    </button>
  </div>
</div>
