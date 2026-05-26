<script lang="ts">
  import { onMount } from 'svelte';

  let theme = $state('dark');

  onMount(() => {
    const stored = localStorage.getItem('theme');
    if (stored) {
      theme = stored;
    } else if (window.matchMedia('(prefers-color-scheme: light)').matches) {
      theme = 'light';
    }
    document.documentElement.setAttribute('data-theme', theme);
    
    const handleThemeChange = (e: Event) => {
      const customEvent = e as CustomEvent<string>;
      theme = customEvent.detail;
    };
    window.addEventListener('theme-changed', handleThemeChange);
    return () => window.removeEventListener('theme-changed', handleThemeChange);
  });

  function toggle() {
    theme = theme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    window.dispatchEvent(new CustomEvent('theme-changed', { detail: theme }));
  }
</script>

<button
  type="button"
  onclick={toggle}
  class="flex h-7 w-7 items-center justify-center rounded-md text-text-secondary hover:bg-bg-surface-hover hover:text-text-primary transition-colors"
  title="Toggle theme"
  aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
>
  {#if theme === 'dark'}
    <svg xmlns="http://www.w3.org/0000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
  {:else}
    <svg xmlns="http://www.w3.org/0000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
  {/if}
</button>
