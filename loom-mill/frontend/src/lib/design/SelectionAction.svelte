<script lang="ts">
  let { position, onSendToChat }: { position: { top: number; left: number }; onSendToChat: () => void } = $props();
</script>

<div class="absolute z-50 bg-bg-surface border border-border-default rounded-md shadow-lg px-2 py-1 text-[10px] flex items-center gap-1.5"
  style="top: {position.top}px; left: {position.left}px; transform: translateY(-100%) translateY(-8px);">
  <button onclick={onSendToChat} class="flex items-center gap-1 text-accent-primary hover:text-accent-primary-hover font-medium">
    📎 Send to chat
  </button>
</div>
