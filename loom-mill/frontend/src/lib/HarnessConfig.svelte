<script lang="ts">
  import { onMount } from 'svelte';
  import type { HarnessConfig } from './types';

  let command = $state('');
  let argsText = $state('');
  let envText = $state('');
  let cwd = $state('');
  let saving = $state(false);
  let message = $state('');
  let testing = $state(false);
  let testResult = $state<{success: boolean, output?: string, error?: string} | null>(null);

  const apiBase = `${window.location.protocol}//${window.location.hostname}:8765`;

  function applyConfig(config: HarnessConfig) {
    command = config.command;
    argsText = config.args.join('\n');
    envText = Object.entries(config.env || {}).map(([key, value]) => `${key}=${value}`).join('\n');
    cwd = config.cwd || '';
  }

  function parseEnv(): Record<string, string> {
    const env: Record<string, string> = {};
    for (const line of envText.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      const separator = trimmed.indexOf('=');
      if (separator === -1) {
        env[trimmed] = '';
      } else {
        env[trimmed.slice(0, separator).trim()] = trimmed.slice(separator + 1);
      }
    }
    return env;
  }

  async function loadConfig() {
    const response = await fetch(`${apiBase}/api/config/harness`);
    if (response.ok) {
      applyConfig(await response.json());
    }
  }

  async function saveConfig() {
    saving = true;
    message = '';
    const response = await fetch(`${apiBase}/api/config/harness`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        command,
        args: argsText.split('\n').map(arg => arg.trim()).filter(Boolean),
        env: parseEnv(),
        cwd: cwd.trim() || null
      })
    });
    saving = false;
    if (response.ok) {
      applyConfig(await response.json());
      message = 'Saved harness config';
    } else {
      const data = await response.json();
      message = data.error || 'Failed to save harness config';
    }
  }

  async function testHarness() {
    testing = true;
    testResult = null;
    try {
      const response = await fetch(`${apiBase}/harness/test`, {
        method: 'POST'
      });
      testResult = await response.json();
    } catch (err) {
      testResult = { success: false, error: String(err) };
    } finally {
      testing = false;
    }
  }

  onMount(() => {
    loadConfig();
  });
</script>

<section class="space-y-3">
  <div>
    <h2 class="text-[11px] font-semibold uppercase tracking-wider text-text-secondary">Harness</h2>
    <p class="mt-1 text-[10px] text-text-tertiary">Command and flags used when starting a ticket workstation.</p>
  </div>

  <label class="block text-[11px] font-medium text-text-secondary">
    Command
    <input bind:value={command} class="mt-1 w-full rounded-md border border-border-default bg-bg-primary px-2.5 py-1.5 text-xs text-text-primary outline-none focus:border-accent-primary focus:ring-1 focus:ring-accent-primary transition-shadow" placeholder="opencode" />
  </label>

  <label class="block text-[11px] font-medium text-text-secondary">
    Arguments
    <textarea bind:value={argsText} rows="3" class="mt-1 w-full rounded-md border border-border-default bg-bg-primary px-2.5 py-1.5 font-mono text-[10px] text-text-primary outline-none focus:border-accent-primary focus:ring-1 focus:ring-accent-primary transition-shadow" placeholder="One argument per line. Use &#123;ticket_path&#125; for the ticket file."></textarea>
  </label>

  <label class="block text-[11px] font-medium text-text-secondary">
    Environment
    <textarea bind:value={envText} rows="2" class="mt-1 w-full rounded-md border border-border-default bg-bg-primary px-2.5 py-1.5 font-mono text-[10px] text-text-primary outline-none focus:border-accent-primary focus:ring-1 focus:ring-accent-primary transition-shadow" placeholder="KEY=value"></textarea>
  </label>

  <label class="block text-[11px] font-medium text-text-secondary">
    Working directory
    <input bind:value={cwd} class="mt-1 w-full rounded-md border border-border-default bg-bg-primary px-2.5 py-1.5 text-xs text-text-primary outline-none focus:border-accent-primary focus:ring-1 focus:ring-accent-primary transition-shadow" placeholder="Optional path inside worktree" />
  </label>

  <button type="button" onclick={saveConfig} disabled={saving || !command.trim()} class="w-full rounded-md bg-bg-surface-active px-3 py-1.5 text-[11px] font-medium text-text-primary ring-1 ring-border-default hover:bg-bg-surface-hover disabled:cursor-not-allowed disabled:opacity-50 transition-colors">
    {saving ? 'Saving...' : 'Save Harness'}
  </button>

  {#if message}
    <p class="text-[10px] {message.startsWith('Failed') ? 'text-status-error-text' : 'text-status-success-text'}">{message}</p>
  {/if}

  <div class="mt-3 pt-3 border-t border-border-subtle">
    <button 
      onclick={testHarness}
      disabled={testing}
      class="flex items-center gap-2 px-3 py-1.5 rounded text-[11px] font-medium
        bg-bg-surface-active border border-border-default text-text-secondary
        hover:bg-bg-surface-elevated hover:text-text-primary transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
      {#if testing}
        <span class="animate-spin">↻</span> Testing...
      {:else}
        ▶ Test Harness
      {/if}
    </button>
    
    {#if testResult}
      <div class="mt-2 rounded border p-2 font-mono text-[10px] leading-relaxed whitespace-pre-wrap
        {testResult.success ? 'border-status-success-border bg-status-success-bg text-status-success-text' : 
                             'border-status-error-border bg-status-error-bg text-status-error-text'}">
        {testResult.success ? '✓ ' : '✗ '}{testResult.output || testResult.error}
      </div>
    {/if}
  </div>
</section>
