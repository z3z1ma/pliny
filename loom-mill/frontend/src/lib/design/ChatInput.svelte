<script lang="ts">
  import VoiceIndicator from './VoiceIndicator.svelte';

  export let onSend: (text: string, context?: any) => void;
  export let disabled: boolean = false;
  export let attachedContext: any = null;
  export let onClearContext: () => void;

  let inputText = '';
  let textareaRef: HTMLTextAreaElement;

  let isRecording = false;
  let recognition: any = null;
  let baseText = '';

  function toggleVoice() {
    if (isRecording) {
      recognition?.stop();
      isRecording = false;
      return;
    }
    
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SR) {
      alert("Voice not supported in this browser");
      return;
    }
    
    recognition = new SR();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
    
    recognition.onresult = (event: any) => {
      let transcript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      inputText = baseText + (baseText && transcript ? ' ' : '') + transcript;
      handleInput();
    };
    
    recognition.onerror = () => { isRecording = false; };
    recognition.onend = () => { isRecording = false; };
    
    baseText = inputText;
    recognition.start();
    isRecording = true;
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }

  function send() {
    if (!inputText.trim() || disabled) return;
    if (isRecording) {
      recognition?.stop();
      isRecording = false;
    }
    onSend(inputText.trim(), attachedContext);
    inputText = '';
    baseText = '';
    onClearContext();
    
    // Reset height
    if (textareaRef) {
      textareaRef.style.height = 'auto';
    }
  }

  function handleInput() {
    if (textareaRef) {
      textareaRef.style.height = 'auto';
      textareaRef.style.height = Math.min(textareaRef.scrollHeight, 120) + 'px';
    }
  }
</script>

<div class="flex flex-col border-t border-border-default bg-bg-surface p-3 gap-2 relative">
  <VoiceIndicator {isRecording} />
  {#if attachedContext}
    <div class="flex items-center justify-between bg-bg-surface-hover border border-border-default rounded px-2 py-1 text-[11px] text-text-secondary">
      <div class="flex items-center gap-1 overflow-hidden">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
        <span class="truncate">{attachedContext.path} (lines {attachedContext.line_range[0]}-{attachedContext.line_range[1]})</span>
      </div>
      <button class="hover:text-text-primary p-0.5" on:click={onClearContext}>
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
      </button>
    </div>
  {/if}

  <div class="flex items-end gap-2 bg-bg-surface-hover border border-border-default rounded-lg p-1 focus-within:border-border-hover focus-within:ring-1 focus-within:ring-border-hover transition-all">
    <textarea
      bind:this={textareaRef}
      bind:value={inputText}
      on:keydown={handleKeydown}
      on:input={handleInput}
      {disabled}
      placeholder="Shape this record..."
      class="flex-1 bg-transparent border-none focus:ring-0 resize-none text-[13px] text-text-primary placeholder:text-text-tertiary p-2 min-h-[36px] max-h-[120px] overflow-y-auto"
      rows="1"
    ></textarea>
    
    <div class="flex items-center gap-1 p-1 shrink-0">
      <button 
        class="p-1.5 rounded transition-colors relative {isRecording ? 'text-status-error-text bg-status-error-bg' : 'text-text-tertiary hover:text-text-primary hover:bg-bg-surface'}"
        title="Voice input"
        on:click={toggleVoice}
        {disabled}
      >
        {#if isRecording}
          <div class="absolute inset-0 rounded-full animate-pulse-ring"></div>
        {/if}
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
      </button>
      <button 
        class="p-1.5 rounded transition-colors {inputText.trim() && !disabled ? 'text-text-inverse bg-bg-accent hover:bg-bg-accent-hover' : 'text-text-tertiary bg-bg-surface cursor-not-allowed'}"
        on:click={send}
        disabled={!inputText.trim() || disabled}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
      </button>
    </div>
  </div>
</div>
