---
id: research:codex-plugin-distribution-surfaces
kind: research
status: active
created_at: 2026-04-26T01:43:51Z
updated_at: 2026-04-26T01:43:51Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:loom-install-experience
  plan:
    - plan:install-experience-harness-adapters
  research:
    - research:loom-install-distribution-methods
    - research:codex-command-skill-installation
  ticket:
    - ticket:lx9nnztk
    - ticket:p9m4x2qt
external_refs:
  codex_docs:
    - https://developers.openai.com/codex/plugins
    - https://developers.openai.com/codex/plugins/build
    - https://developers.openai.com/codex/skills
    - https://developers.openai.com/codex/guides/agents-md
    - https://developers.openai.com/codex/concepts/customization
    - https://developers.openai.com/codex/config-advanced
    - https://developers.openai.com/codex/cli/reference#codex-plugin-marketplace
    - https://developers.openai.com/codex/changelog
  codex_source:
    - https://github.com/openai/codex/blob/main/codex-rs/core-plugins/src/manifest.rs
    - https://github.com/openai/codex/blob/main/codex-rs/core-plugins/src/loader.rs
    - https://github.com/openai/codex/blob/main/codex-rs/plugin/src/plugin_namespace.rs
    - https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/plugin-creator/references/plugin-json-spec.md
    - https://github.com/openai/plugins
---

# Question

How should Loom use Codex's plugin system as a first-class distribution surface
without pretending that a Codex plugin can own Loom's ordered always-on rule
surface?

# Why This Matters

`ticket:lx9nnztk` was created when Codex plugin support looked incomplete and
thinly documented. Codex now has stronger plugin and marketplace docs, a CLI
marketplace command surface, and curated plugin examples. The ticket needs a
fresh source-backed next move before implementation so Loom does not either
underuse a native Codex package surface or overclaim plugin coverage for
always-on rules.

The decision also affects how Loom handles optional command wrappers in Codex.
Prior `research:codex-command-skill-installation` correctly moved Codex command
wrappers into explicit-only `loom-command-*` skills. A Codex plugin package could
be the distribution unit for those adapters, but only if the package layout does
not make generated adapter files the semantic owner of Loom commands.

# Scope

Covered:

- official Codex plugin, skill, `AGENTS.md`, customization, config, CLI, and
  changelog docs available on 2026-04-26
- OpenAI Codex source files that parse plugin manifests, load plugin components,
  and derive plugin namespaces for skills
- OpenAI's public plugin examples repository and built-in plugin-creator spec
- local Codex CLI command help for the installed `codex-cli 0.123.0`
- implications for `ticket:lx9nnztk`

Excluded:

- implementing a Codex plugin fixture
- installing or enabling a local Codex plugin in the user's real Codex config
- publishing a Codex marketplace package
- changing the existing direct Codex installer

# Method

- Read the existing Loom install initiative, plan, broad install research,
  Codex command-skill research, and Codex tickets.
- Fetched official Codex docs for plugins, plugin building, skills,
  `AGENTS.md`, customization, advanced config, CLI reference, and changelog.
- Inspected OpenAI Codex source for manifest parsing, plugin component loading,
  and plugin skill namespace derivation.
- Inspected OpenAI's public `openai/plugins` examples repository and the bundled
  `plugin-creator` spec.
- Ran local command help for `codex --version`, `codex plugin --help`,
  `codex plugin marketplace --help`, and `codex plugin marketplace add --help`.
- Measured the top-level Loom `rules/*.md` corpus at 45,588 bytes to evaluate
  the risk of stuffing ordered rules into project instruction surfaces.

# Sources

Repository sources:

- `initiative:loom-install-experience`
- `plan:install-experience-harness-adapters`
- `research:loom-install-distribution-methods`
- `research:codex-command-skill-installation`
- `ticket:lx9nnztk`
- `ticket:p9m4x2qt`
- `scripts/install-loom.sh`
- `INSTALL.md`
- `rules/*.md`, `skills/*/SKILL.md`, and `commands/*.md`

External sources are listed in frontmatter under `external_refs`.

Local observations:

- `codex --version` returned `codex-cli 0.123.0`.
- `codex plugin --help` exposes only the `marketplace` subcommand under
  `plugin` in the installed CLI.
- `codex plugin marketplace add --help` accepts GitHub shorthand, HTTP(S) Git
  URLs, SSH URLs, and local marketplace root directories.
- `wc -c rules/*.md` reported 45,588 bytes across the seven Loom rule files.

# Evidence

## Codex Plugin Model

Official Codex docs now describe plugins as the installable distribution unit
for reusable Codex workflows. They can bundle:

- skills
- app integrations or connectors
- MCP servers
- presentation assets and interface metadata

The docs explicitly say skills remain the authoring format, while plugins are
the installable distribution unit when a workflow should be shared beyond local
authoring.

This is a stronger first-class fit than the existing direct Codex installer for
Loom skills because Codex users can browse, install, enable, disable, and upgrade
plugins through Codex's plugin surfaces.

## Manifest Shape

The official plugin root shape is:

```text
my-plugin/
  .codex-plugin/plugin.json
  skills/
  .mcp.json
  .app.json
  assets/
```

The official minimal manifest is a JSON object with `name`, `version`,
`description`, and `skills`, for example:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Reusable greeting workflow",
  "skills": "./skills/"
}
```

OpenAI Codex source-backed manifest parsing currently models these component
paths:

- `skills`
- `mcpServers`
- `apps`

It also models `interface` presentation fields such as display names, default
prompts, icons, logos, screenshots, category, capabilities, and external URLs.

Manifest paths must be relative to the plugin root, start with `./`, avoid `..`,
and stay inside the plugin root. Invalid paths are ignored with warnings in the
source-level parser.

## Marketplace Shape

Codex can read marketplace files from:

- the official curated plugin directory
- `$REPO_ROOT/.agents/plugins/marketplace.json`
- `$REPO_ROOT/.claude-plugin/marketplace.json`
- `~/.agents/plugins/marketplace.json`

The official repo marketplace shape includes top-level `name`, optional
`interface.displayName`, and a `plugins` array. Each plugin entry points at a
local or Git-backed source and includes installation/authentication policy and a
category.

For a local repo marketplace, docs show plugin entries like:

```json
{
  "name": "local-example-plugins",
  "interface": {
    "displayName": "Local Example Plugins"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "source": {
        "source": "local",
        "path": "./plugins/my-plugin"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

Codex installs plugin artifacts into
`~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/`. For local
plugins, Codex loads the installed cache copy rather than the marketplace source
directly.

## CLI Surface

The current official CLI reference marks `codex plugin marketplace` as
experimental and documents:

```text
codex plugin marketplace add <source> [--ref REF] [--sparse PATH]
codex plugin marketplace upgrade [marketplace-name]
codex plugin marketplace remove <marketplace-name>
```

Supported marketplace sources include GitHub shorthand, HTTP(S) Git URLs, SSH
URLs, and local marketplace root directories. The installed local CLI version
`codex-cli 0.123.0` exposes the same marketplace add shape, but plugin
install/enable still appears to be driven through the interactive `/plugins`
browser or app-server/plugin APIs, not a simple documented `codex plugin install`
CLI command.

The 2026-04 Codex changelog shows rapid plugin movement: remote plugin list/read,
remote/cross-repo/local marketplace sources, app-server plugin install, and
marketplace upgrade support changed between CLI 0.122.0 and 0.125.0. A Codex
plugin implementation ticket should therefore record the tested CLI version and
not assume all documented behavior exists in older installed CLIs.

## Skills Loaded From Plugins

Official skill docs say Codex skills are directories with required `SKILL.md`
frontmatter `name` and `description`, optional `scripts/`, `references/`,
`assets/`, and optional `agents/openai.yaml` for UI metadata, invocation policy,
and dependencies.

Source-level loader behavior supports:

- default `skills/` under the plugin root
- an additional or configured manifest `skills` path
- loaded plugin skills with `SkillScope::User`
- product restriction filtering
- disabled skill path config

OpenAI source for plugin namespace derivation walks up from a skill path until
it finds a `.codex-plugin/plugin.json`. The manifest `name` becomes the plugin
namespace when present. That implies a Loom plugin named `loom` can expose
namespaced plugin skills such as `loom:<skill-name>` in Codex contexts.

Direct non-plugin skill duplicates are not merged according to official skills
docs; both may appear in selectors. Plugin namespacing lowers collision risk,
but `ticket:lx9nnztk` should still validate actual runtime selector and explicit
invocation behavior for `loom` plugin skills.

## Always-On Instruction Surface

Official Codex customization docs treat `AGENTS.md` as the durable project and
global instruction layer. Official `AGENTS.md` docs describe the discovery chain:

- global Codex home: `AGENTS.override.md` first, otherwise `AGENTS.md`
- project scope: root-to-current-directory `AGENTS.override.md`, then
  `AGENTS.md`, then configured fallback filenames
- project docs stop at `project_doc_max_bytes`, documented as 32 KiB by default

The plugin docs and source inspected here do not show a plugin manifest field
that installs or injects global/project `AGENTS.md` instructions. They also do
not show plugins as an always-on instruction source equivalent to `AGENTS.md`.

This preserves the current hybrid conclusion: Codex plugin packaging can own the
installable workflow surfaces, but ordered always-on Loom rules still need a
Codex instruction surface such as `~/.codex/AGENTS.md`, `AGENTS.override.md`, or
a project `AGENTS.md` strategy.

The current Loom rule corpus is 45,588 bytes. A project-local plugin strategy
that blindly mirrors all rules into project `AGENTS.md` risks colliding with the
documented 32 KiB default project-doc budget. A global `~/.codex/AGENTS.md`
managed block may still work differently, but the implementation ticket should
observe rather than assume full rule loading.

## Hooks, Commands, And Agents

The plugin surface has inconsistencies that matter for Loom:

- official plugin docs emphasize skills, apps, MCP, and assets
- the OpenAI `openai/plugins` README mentions optional plugin-level `agents/`,
  `commands/`, and `hooks.json`
- the built-in plugin-creator spec includes a `hooks` field in its sample
  manifest
- current OpenAI Codex source manifest parsing inspected here models `skills`,
  `mcpServers`, `apps`, and `interface`, but not `hooks`, `commands`, `agents`,
  or `AGENTS.md`

This means Loom should not depend on plugin hooks, plugin commands, or plugin
agents for the Codex first-class install path until the target Codex CLI/runtime
version proves those fields are loaded and supported. For now, Loom command
wrappers remain safest as explicit-only generated skill adapters.

# Rejected Options

## Pure Codex Plugin Install

Rejected for this ticket because official docs and inspected source do not show
plugins owning Codex's always-on `AGENTS.md` instruction chain. Loom needs
ordered always-on rules, so a pure plugin install would be an attractive but
incomplete product story.

## Plugin Hooks As Rule Sync

Rejected for the next iteration. Codex hooks are documented as config-layer
hooks under `~/.codex` and trusted project `.codex/` layers. Plugin-level hook
support is not consistently documented or source-verified through the inspected
manifest loader, so using hooks to mutate `AGENTS.md` would copy the riskiest
part of the Claude hybrid before Codex proves it supports that model.

## Plugin Commands As Loom Command Wrappers

Rejected for the next iteration. Codex's stable workflow command story in the
inspected docs is skills, not plugin command files. Prior research already
established explicit-only `loom-command-*` adapter skills as the safe command
wrapper translation.

## Unchanged Direct Skill Copy As The Final Product Path

Rejected as the strategic endpoint. Direct copying into `$HOME/.agents/skills`
still works and should remain a fallback, but Codex now positions plugins as the
distribution unit for reusable skills. Loom should test that path before
continuing to treat generated user skill directories as the preferred product
experience.

# Null Results

- No documented `codex plugin validate` command was found in official docs or in
  the installed local `codex-cli 0.123.0` help surface.
- No official or inspected source path showed `.codex-plugin/plugin.json` as an
  `AGENTS.md` or always-on instruction installer.
- No current repository Codex plugin fixture exists under `.codex-plugin/`,
  `.agents/plugins/`, or `examples/adapters/`.

# Conclusions

Codex has a real first-class plugin distribution surface for Loom's reusable
workflow skills. It is now strong enough to deserve a package-layout prototype,
not just direct skill generation.

Codex plugins are still not a complete Loom install by themselves. The
evidence-backed split is:

- plugin package: canonical Loom skills, generated explicit-only command adapter
  skills, optional future MCP/app metadata if a later ticket needs it
- Codex instruction surface: ordered always-on Loom rules through managed
  `AGENTS.md`, `AGENTS.override.md`, or a project instruction strategy
- fallback installer: direct skill generation and managed `~/.codex/AGENTS.md`
  until plugin install behavior is validated against a target Codex CLI version

The next implementation should not jump straight to release packaging. It should
run a bounded package-layout spike that compares the smallest viable plugin root
shape against the need to include generated command adapter skills without
polluting canonical `skills/`.

# Recommendations

1. Refine `ticket:lx9nnztk` so the next route is an observation-first Codex
   package-layout spike.
2. Prototype a repo-scoped local marketplace fixture before touching broad
   install docs or the current direct installer.
3. Compare at least two layout options in the ticket or evidence:
   repo-root plugin using canonical `skills/` only, and a derivative plugin
   fixture containing canonical skill copies plus generated `loom-command-*`
   adapter skills.
4. Keep ordered Loom rules outside the plugin for now and validate Codex rule
   loading through `AGENTS.md` separately.
5. Treat plugin hooks, commands, and agents as experimental or unverified for
   Loom until a target Codex runtime proves them.
6. Record the tested Codex CLI version because official docs are ahead of the
   local `codex-cli 0.123.0` installed in this workspace.
7. Require the implementation packet to produce structural evidence for
   manifest paths, marketplace paths, generated command adapter policy, skill
   collision behavior, and any CLI validation that could or could not be run.

# Open Questions

- Should Loom's first Codex plugin prototype use the repository root as the
  plugin root, or a derivative fixture under `examples/adapters/` or `plugins/`?
- If the repository root is the plugin root, where can generated command adapter
  skills live without turning top-level `skills/` into a mixed canonical and
  generated surface?
- Does the target Codex runtime expose plugin skills as `loom:<skill-name>` in
  explicit `$` invocation syntax, `@` plugin syntax, or both?
- Does installed-plugin skill discovery preserve `agents/openai.yaml` policy for
  generated command adapters exactly as direct `$HOME/.agents/skills` install
  does?
- What minimum Codex CLI version should Loom document once the package path is
  validated?
- Can global `~/.codex/AGENTS.md` safely exceed 32 KiB while project docs remain
  capped, or should Loom generate a shorter Codex-specific always-on summary?

# Linked Work

- `initiative:loom-install-experience`
- `plan:install-experience-harness-adapters`
- `research:loom-install-distribution-methods`
- `research:codex-command-skill-installation`
- `ticket:lx9nnztk`
- `ticket:p9m4x2qt`
