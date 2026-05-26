<script lang="ts">
  let { isRecording = false }: { isRecording?: boolean } = $props();
</script>

{#if isRecording}
  <div class="absolute -top-8 left-3 flex items-center gap-2">
    <div class="w-2 h-2 rounded-full bg-status-error-text animate-pulse-ring"></div>
    <span class="text-[11px] text-text-secondary">Listening...</span>
  </div>
{/if}