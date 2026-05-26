<script lang="ts">
  import { onMount } from 'svelte';
  import { store } from './lib/ws.svelte';
  import ThemeToggle from './lib/ThemeToggle.svelte';
  import SettingsDrawer from './lib/SettingsDrawer.svelte';
  import Toast from './lib/Toast.svelte';
  import NotificationCenter, { type Notification, type NotificationType } from './lib/NotificationCenter.svelte';
  import CommandPalette from './lib/CommandPalette.svelte';
  import { formatDuration } from './lib/utils';
  import ModeSwitch from './lib/ModeSwitch.svelte';
  import FactoryFloor from './lib/FactoryFloor.svelte';
  import DesignRoom from './lib/design/DesignRoom.svelte';

  let activeMode = $state<'design' | 'factory'>('factory');
  let selectedWorkstationId = $state<string | null>(null);
  let activeTab = $state<'logs' | 'iterations' | 'playback'>('logs');
  let settingsOpen = $state(false);
  let notificationsOpen = $state(false);
  let commandPaletteOpen = $state(false);
  let toastRef = $state<Toast>();

  let layoutMode = $state<'desktop' | 'laptop' | 'tablet' | 'mobile'>('desktop');
  let showSidebar = $state(true);

  let notifications = $state<Notification[]>([]);
  let unreadCount = $derived(notifications.filter(n => !n.read).length);

  function addNotification(type: NotificationType, message: string) {
    const newNotif: Notification = {
      id: crypto.randomUUID(),
      type,
      message,
      timestamp: Date.now(),
      read: false
    };
    notifications = [newNotif, ...notifications].slice(0, 100);
    try {
      localStorage.setItem('loom-mill-notifications', JSON.stringify(notifications));
    } catch (e) {}
  }

  function markAllRead() {
    notifications = notifications.map(n => ({ ...n, read: true }));
    try {
      localStorage.setItem('loom-mill-notifications', JSON.stringify(notifications));
    } catch (e) {}
  }

  function updateLayout() {
    const w = window.innerWidth;
    if (w < 768) { layoutMode = 'mobile'; showSidebar = false; }
    else if (w < 1024) { layoutMode = 'tablet'; showSidebar = false; }
    else if (w < 1280) { layoutMode = 'laptop'; showSidebar = true; }
    else { layoutMode = 'desktop'; showSidebar = true; }
    (window as any).layoutMode = layoutMode;
  }

  let prevWorkstations: Record<string, { status: string, andonCount: number }> = {};

  onMount(() => {
    try {
      const saved = localStorage.getItem('loom-mill-notifications');
      if (saved) {
        notifications = JSON.parse(saved);
      }
    } catch (e) {}

    store.connect();
    updateLayout();
    window.addEventListener('resize', updateLayout);
    
    const handleOpenPlayback = (e: Event) => {
      const customEvent = e as CustomEvent<{ workstationId: string, source?: string }>;
      if (customEvent.detail?.workstationId) {
        selectedWorkstationId = customEvent.detail.workstationId;
        if (customEvent.detail.source === 'andon') {
          activeTab = 'logs';
          settingsOpen = false;
        } else if (customEvent.detail.source === 'controls') {
          activeTab = 'iterations';
        } else {
          activeTab = 'iterations';
        }
      }
    };
    
    window.addEventListener('open-playback', handleOpenPlayback);
    
    const handleGlobalKeydown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        commandPaletteOpen = true;
      }
    };
    window.addEventListener('keydown', handleGlobalKeydown);
    
    return () => {
      window.removeEventListener('open-playback', handleOpenPlayback);
      window.removeEventListener('keydown', handleGlobalKeydown);
    };
  });

  $effect(() => {
    document.title = `Loom Mill - ${store.connected ? 'Connected' : 'Disconnected'}`;
  });

  $effect(() => {
    if (!toastRef) return;
    
    for (const [id, ws] of Object.entries(store.state.workstations)) {
      const prev = prevWorkstations[id];
      if (!prev) {
        if (ws.status === 'running') {
          const msg = `Started: ${ws.ticket_slug}`;
          toastRef.show(`▶ ${msg}`, 'info');
          addNotification('started', msg);
        }
      } else if (prev.status !== ws.status) {
        if (ws.status === 'completed') {
          const duration = ws.iteration_summary?.duration_seconds ? ` (${formatDuration(ws.iteration_summary.duration_seconds)})` : '';
          const msg = `Completed: ${ws.ticket_slug}${duration}`;
          toastRef.show(`✓ ${msg}`, 'info');
          addNotification('completed', msg);
        } else if (ws.status === 'stopped') {
          const msg = `Stopped: ${ws.ticket_slug}`;
          toastRef.show(`⛔ ${msg}`, 'error');
          addNotification('stopped', msg);
        }
      }
    }
    
    for (const [id, events] of Object.entries(store.state.andon_events)) {
      const prevCount = prevWorkstations[id]?.andonCount || 0;
      if (events.length > prevCount) {
        const latest = events[events.length - 1];
        const msg = `Alert on ${store.state.workstations[id]?.ticket_slug || id}: ${latest.reasoning}`;
        toastRef.show(`⚠ ${msg}`, 'warning');
        addNotification('andon', msg);
      }
    }

    prevWorkstations = {};
    for (const [id, ws] of Object.entries(store.state.workstations)) {
      prevWorkstations[id] = { status: ws.status, andonCount: store.state.andon_events[id]?.length || 0 };
    }
  });

  let prevShippingCount = $state(0);
  $effect(() => {
    if (store.state.shipping_events.length > prevShippingCount) {
      const newEvents = store.state.shipping_events.slice(0, store.state.shipping_events.length - prevShippingCount);
      for (const event of newEvents) {
        if (event.action === 'merged') {
          addNotification('shipping_merged', `Merged: ${event.ticket_slug}`);
        } else if (event.action === 'conflict') {
          addNotification('shipping_conflict', `Conflict: ${event.ticket_slug}`);
        }
      }
      prevShippingCount = store.state.shipping_events.length;
    }
  });

  let prevConnected = $state<boolean | null>(null);
  $effect(() => {
    if (prevConnected !== null && prevConnected !== store.connected) {
      addNotification('connection', store.connected ? 'Connected to backend' : 'Disconnected from backend');
    }
    prevConnected = store.connected;
  });

  let andonCount = $derived(() => {
    let count = 0;
    for (const events of Object.values(store.state.andon_events)) {
      count += events.length;
    }
    return count;
  });
</script>

<main class="flex h-screen flex-col bg-bg-primary text-text-primary overflow-hidden font-sans">
  <Toast bind:this={toastRef} />
  <!-- Header: 48px -->
  <!-- svelte-ignore a11y_no_redundant_roles -->
  <header role="banner" class="flex items-center justify-between h-12 border-b border-border-default bg-bg-surface px-4 shrink-0">
    <div class="flex items-center gap-2 h-full">
      {#if layoutMode === 'tablet' || (layoutMode === 'mobile' && selectedWorkstationId)}
        <button 
          onclick={() => showSidebar = !showSidebar}
          class="p-1 -ml-1 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary transition-colors"
          aria-label="Toggle sidebar">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </button>
      {/if}
      <h1 class="text-[13px] font-semibold text-text-primary">Loom Mill</h1>
      <ModeSwitch {activeMode} onSwitch={(mode) => activeMode = mode} />
    </div>
    
    <div class="flex items-center gap-3">
      <div class="flex items-center gap-2 text-[11px] font-medium">
        <span class="relative flex h-2 w-2">
          {#if store.connected}
            <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-status-success-text opacity-75"></span>
            <span class="relative inline-flex h-2 w-2 rounded-full bg-status-success-text"></span>
          {:else}
            <span class="relative inline-flex h-2 w-2 rounded-full bg-status-error-text"></span>
          {/if}
        </span>
      </div>
      <div class="h-4 w-[1px] bg-border-default"></div>
      <ThemeToggle />
      
      <div class="relative">
        <button 
          onclick={() => notificationsOpen = !notificationsOpen}
          class="relative p-1 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary transition-colors"
          title="Notifications">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
          {#if unreadCount > 0}
            <span class="absolute -top-0.5 -right-0.5 flex items-center justify-center min-w-[12px] h-[12px] px-0.5 rounded-full bg-status-error-text text-[8px] font-bold text-white">
              {unreadCount > 99 ? '99+' : unreadCount}
            </span>
          {/if}
        </button>
        <NotificationCenter 
          open={notificationsOpen} 
          onClose={() => notificationsOpen = false} 
          {notifications}
          onMarkAllRead={markAllRead}
        />
      </div>

      <button 
        onclick={() => settingsOpen = !settingsOpen}
        class="relative p-1 rounded hover:bg-bg-surface-active text-text-tertiary hover:text-text-primary transition-colors"
        title="Settings & Info">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
        {#if andonCount() > 0}
          <span class="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-status-error-text"></span>
        {/if}
      </button>
    </div>
  </header>

  {#if activeMode === 'design'}
    <DesignRoom />
  {:else}
    <FactoryFloor 
      {layoutMode} 
      bind:showSidebar 
      bind:selectedWorkstationId 
      bind:activeTab 
    />
  {/if}

  <SettingsDrawer open={settingsOpen} onClose={() => settingsOpen = false} />
  
  <CommandPalette 
    bind:open={commandPaletteOpen}
    records={store.state.records}
    workstations={store.state.workstations}
    onSelectTicket={(id) => selectedWorkstationId = id}
    onSelectWorkstation={(id) => selectedWorkstationId = id}
    onToggleSettings={() => settingsOpen = !settingsOpen}
    onToggleTheme={() => {
      const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('theme', theme);
      window.dispatchEvent(new CustomEvent('theme-changed', { detail: theme }));
    }}
  />
</main>
