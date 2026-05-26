<script lang="ts">
  import type { LoomRecord } from './types';

  let {
    record,
    badge = '',
    statusColor = 'bg-text-tertiary',
    onSelect = () => {}
  }: {
    record: LoomRecord;
    badge?: string;
    statusColor?: string;
    onSelect?: () => void;
  } = $props();

  let title = $derived(() => {
    if (record.headings.length > 0) {
      return record.headings[0][1];
    }
    return record.metadata.id || record.path;
  });
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="flex items-center gap-2 px-3 py-2 hover:bg-bg-surface-elevated transition-colors duration-150 cursor-pointer"
  onclick={onSelect}>
  <!-- Status dot -->
  <span class="w-2 h-2 rounded-full shrink-0 {statusColor}"></span>
  
  <!-- Title -->
  <span class="flex-1 truncate text-[12px] text-text-primary">{title()}</span>
  
  <!-- Badge (optional: "external", "blocked", etc.) -->
  {#if badge}
    <span class="rounded-full px-1.5 py-0.5 text-[9px] font-medium bg-bg-surface-active text-text-tertiary border border-border-subtle">
      {badge}
    </span>
  {/if}
</div>
