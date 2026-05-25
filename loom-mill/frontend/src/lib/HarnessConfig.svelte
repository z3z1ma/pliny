<script lang="ts">
  import { onMount } from 'svelte';
  import type { HarnessConfig } from './types';

  let command = $state('');
  let argsText = $state('');
  let envText = $state('');
  let cwd = $state('');
  let saving = $state(false);
  let message = $state('');

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

  onMount(() => {
    loadConfig();
  });
</script>

<section class="space-y-3">
  <div>
    <h2 class="text-sm font-semibold uppercase tracking-wider text-cyan-100">Harness</h2>
    <p class="mt-1 text-xs text-slate-500">Command and flags used when starting a ticket workstation.</p>
  </div>

  <label class="block text-xs font-medium text-slate-400">
    Command
    <input bind:value={command} class="mt-1 w-full rounded border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none focus:border-cyan-500" placeholder="opencode" />
  </label>

  <label class="block text-xs font-medium text-slate-400">
    Arguments
    <textarea bind:value={argsText} rows="5" class="mt-1 w-full rounded border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-xs text-slate-100 outline-none focus:border-cyan-500" placeholder="One argument per line. Use {ticket_path} for the ticket file."></textarea>
  </label>

  <label class="block text-xs font-medium text-slate-400">
    Environment
    <textarea bind:value={envText} rows="4" class="mt-1 w-full rounded border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-xs text-slate-100 outline-none focus:border-cyan-500" placeholder="KEY=value"></textarea>
  </label>

  <label class="block text-xs font-medium text-slate-400">
    Working directory
    <input bind:value={cwd} class="mt-1 w-full rounded border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none focus:border-cyan-500" placeholder="Optional path inside worktree" />
  </label>

  <button type="button" onclick={saveConfig} disabled={saving || !command.trim()} class="w-full rounded bg-cyan-500 px-3 py-2 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-400">
    {saving ? 'Saving...' : 'Save Harness'}
  </button>

  {#if message}
    <p class="text-xs {message.startsWith('Failed') ? 'text-rose-400' : 'text-emerald-400'}">{message}</p>
  {/if}
</section>
