<script lang="ts">
  let { activeMode, onSwitch } = $props<{
    activeMode: 'design' | 'factory';
    onSwitch: (mode: 'design' | 'factory') => void;
  }>();
</script>

<div class="flex items-center gap-4 ml-4 h-full pt-1">
  <button
    class="flex items-center gap-1.5 h-full border-b-2 transition-colors {activeMode === 'design' ? 'border-accent-primary text-text-primary' : 'border-transparent text-text-tertiary hover:text-text-secondary'}"
    onclick={() => onSwitch('design')}
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
    <span class="text-[13px] font-medium">Design Room</span>
  </button>
  <button
    class="flex items-center gap-1.5 h-full border-b-2 transition-colors {activeMode === 'factory' ? 'border-accent-primary text-text-primary' : 'border-transparent text-text-tertiary hover:text-text-secondary'}"
    onclick={() => onSwitch('factory')}
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1"/><path d="M12 18h1"/><path d="M7 18h1"/></svg>
    <span class="text-[13px] font-medium">Factory Floor</span>
  </button>
</div>
