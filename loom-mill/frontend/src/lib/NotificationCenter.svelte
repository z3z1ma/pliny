<script lang="ts">
  import { fade, fly } from 'svelte/transition';

  export type NotificationType = 'started' | 'completed' | 'stopped' | 'andon' | 'shipping_merged' | 'shipping_conflict' | 'connection';
  
  export interface Notification {
    id: string;
    type: NotificationType;
    message: string;
    timestamp: number;
    read: boolean;
  }

  let { 
    open, 
    onClose,
    notifications,
    onMarkAllRead
  }: { 
    open: boolean; 
    onClose: () => void;
    notifications: Notification[];
    onMarkAllRead: () => void;
  } = $props();

  function formatRelativeTime(ts: number) {
    const diff = Date.now() - ts;
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'Just now';
    if (mins < 60) return `${mins}m ago`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours}h ago`;
    return `${Math.floor(hours / 24)}d ago`;
  }

  function getIcon(type: NotificationType) {
    switch (type) {
      case 'started': return { icon: '▶', color: 'text-status-info-text' };
      case 'completed': return { icon: '✓', color: 'text-status-success-text' };
      case 'stopped': return { icon: '⛔', color: 'text-status-error-text' };
      case 'andon': return { icon: '⚠', color: 'text-status-warning-text' };
      case 'shipping_merged': return { icon: '🚀', color: 'text-accent-primary' };
      case 'shipping_conflict': return { icon: '🚀', color: 'text-status-error-text' };
      case 'connection': return { icon: '●', color: 'text-text-tertiary' };
      default: return { icon: '•', color: 'text-text-tertiary' };
    }
  }
</script>

{#if open}
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div class="fixed inset-0 z-40" onclick={onClose}></div>
  
  <div 
    transition:fly={{ y: -10, duration: 200 }}
    class="absolute top-10 right-4 z-50 w-[350px] max-h-[400px] flex flex-col bg-bg-surface border border-border-default rounded-lg shadow-xl overflow-hidden"
  >
    <div class="flex items-center justify-between px-3 py-2 border-b border-border-default shrink-0 bg-bg-surface-elevated">
      <h3 class="text-[12px] font-semibold text-text-primary">Notifications</h3>
      {#if notifications.some(n => !n.read)}
        <button 
          class="text-[10px] text-accent-primary hover:underline"
          onclick={onMarkAllRead}
        >
          Mark all read
        </button>
      {/if}
    </div>
    
    <div class="flex-1 overflow-y-auto">
      {#if notifications.length === 0}
        <div class="p-6 text-center text-[11px] text-text-tertiary">
          No notifications yet.
        </div>
      {:else}
        {#each notifications as n (n.id)}
          {@const { icon, color } = getIcon(n.type)}
          <div class="flex items-start gap-3 px-3 py-2.5 border-b border-border-subtle hover:bg-bg-surface-hover transition-colors {n.read ? 'opacity-70' : 'bg-bg-surface-active/30'}">
            <span class="mt-0.5 text-[12px] {color}">{icon}</span>
            <div class="flex-1 min-w-0">
              <p class="text-[11px] text-text-primary leading-snug break-words">{n.message}</p>
              <p class="text-[9px] text-text-tertiary mt-1">{formatRelativeTime(n.timestamp)}</p>
            </div>
            {#if !n.read}
              <span class="w-1.5 h-1.5 rounded-full bg-accent-primary shrink-0 mt-1.5"></span>
            {/if}
          </div>
        {/each}
      {/if}
    </div>
  </div>
{/if}