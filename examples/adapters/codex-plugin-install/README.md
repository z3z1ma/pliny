# Codex Remote Plugin Install Spike

## Transport Surface

- `.codex-plugin/plugin.json` makes the repository root loadable as a Codex plugin.
- `.agents/plugins/marketplace.json` makes the repository a Codex marketplace
  named `agent-loom` with one Git-backed root plugin named `loom`.
- the plugin exposes canonical `skills/` directly from the repository root.
- `.codex/config.toml` enables Codex hooks for trusted project-local use.
- `.codex/hooks.json` registers one project-local `SessionStart` hook group with
  matcher `startup|resume|clear|compact`.
- that hook group has one command per `loom-bootstrap` reference; each command
  prints a `===== LOOM_BOOTSTRAP_REFERENCE <filename> =====` source marker and
  cats exactly one `skills/loom-bootstrap/references/<filename>` file to stdout.
- the hook commands use small increasing sleep delays so numeric rule order is
  likely in practice, especially `01-core-identity.md` first, but Codex hook
  ordering should still be treated as best effort.

## Remote Install Target

The intended product target is remote install for normal Codex users, pending
installed plugin skill-discovery validation:

```bash
codex plugin marketplace add z3z1ma/agent-loom
```

After that validation, users should be able to install or enable `loom` from
Codex's `/plugins` browser and get the complete Loom skill package, including the
mandatory `loom-bootstrap` entry skill, without cloning this repository.

Current Codex evidence supports a skills-package target but does not yet prove
installed Git-backed plugin skill discovery for `loom-bootstrap`. Installed
plugins are not source-proven to own always-on hook or instruction loading, so the
hook remains an optional preload proof rather than the completeness boundary.

## Hook-Context Proof Shape

Use Codex plugin packaging for discoverable skills and optional Codex
`SessionStart` hook stdout for same-session bootstrap context.

This keeps the core split simple:

- plugins package `loom-bootstrap` and reusable subsystem skills
- hooks may preload `loom-bootstrap` references as an optimization

The final remote Codex adapter does not require plugin-owned hooks if
`loom-bootstrap` is discoverable and the harness or user instruction tells agents
to use it first.

## Expected Properties

- Codex can read the marketplace from `.agents/plugins/marketplace.json`.
- Codex can load the `loom` plugin's canonical skills from `skills/` after the
  Git-backed root plugin is installed.
- project-local `SessionStart` hooks emit all seven `loom-bootstrap` references as
  source-marked stdout outputs, one file per command.
- same-session startup probes can see hook stdout as model context.
- each current bootstrap reference remains below Codex's per-output practical
  probe size and Claude's documented 10,000-character hook-output context cap used
  by the sibling Claude adapter.
- ordering is treated as best effort; source markers, not strict order, are the
  stable attribution mechanism.

## Limitations

- A remote plugin install still needs a project/user instruction that says to use
  `loom-bootstrap` first unless the ordered doctrine is already loaded.
- Codex source and docs currently document hook loading from `hooks.json` files or
  inline `[hooks]` tables next to active config layers; plugin docs currently list
  plugins as skills, apps, MCP servers, and assets.
- Codex local marketplace entries must point at a non-empty plugin folder path
  such as `./plugins/my-plugin`. A repository-root plugin uses the documented
  Git-backed `source: "url"` shape instead of local `path: "./"`.
- Project-local hooks load only when the project `.codex/` layer is trusted.
- Runtime validation covers local project hooks and CLI `-c` hook overrides in
  `codex-cli 0.125.0`; installed Git-backed plugin skill loading and plugin
  manifest hook loading are not yet runtime-proven.
- Codex source and docs map current `SessionStart` sources to `startup`, `resume`,
  and `clear`; the matcher includes `compact` defensively, but no separate
  `compact` `SessionStart` source was found in the inspected source.
- Runtime installed plugin skill invocation remains outside this hook-loading
  proof.

## Common Wrong Behavior

- treating optional hook preload as more authoritative than `loom-bootstrap`
- assuming Codex plugins own always-on instructions when current docs/source route hooks
  through Codex config layers
- putting Loom bootstrap references under `~/.codex/rules/`, which is a shell
  execution policy surface rather than the Markdown instruction surface
- concatenating all Loom bootstrap references into one hook output without
  preserving source markers
- assuming source-marked per-rule hook output preserves strict numeric order
- copying dogfooding `.loom/` records into the plugin package
