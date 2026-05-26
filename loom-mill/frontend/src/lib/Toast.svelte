<script lang="ts">
  import { fly, fade } from 'svelte/transition';

  let toasts = $state<{id: number; message: string; type: 'info' | 'warning' | 'error'; duration: number}[]>([]);
  let nextId = 0;

  export function show(message: string, type: 'info' | 'warning' | 'error' = 'info', duration = 4000) {
    const id = nextId++;
    toasts = [...toasts, { id, message, type, duration }];
    if (toasts.length > 3) toasts = toasts.slice(-3);
    setTimeout(() => {
      toasts = toasts.filter(t => t.id !== id);
    }, duration);
  }
</script>

{#if toasts.length > 0}
  <div role="alert" aria-live="polite" class="fixed bottom-4 left-1/2 -translate-x-1/2 z-50 flex flex-col gap-2 items-center pointer-events-none">
    {#each toasts as toast (toast.id)}
      <div class="pointer-events-auto flex items-center gap-2 rounded-lg border px-4 py-2 shadow-lg
        text-[12px] font-medium backdrop-blur-sm
        {toast.type === 'error' ? 'border-red-500/30 bg-red-950/80 text-red-200' :
         toast.type === 'warning' ? 'border-amber-500/30 bg-amber-950/80 text-amber-200' :
         'border-border-default bg-bg-surface-elevated/90 text-text-primary'}
        animate-[slideUp_200ms_ease-out]">
        {toast.message}
      </div>
    {/each}
  </div>
{/if}
