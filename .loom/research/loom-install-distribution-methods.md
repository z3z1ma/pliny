---
id: research:loom-install-distribution-methods
kind: research
status: active
created_at: 2026-04-25T18:25:20Z
updated_at: 2026-04-26T05:15:49Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:loom-install-experience
  plan:
    - plan:install-experience-harness-adapters
  spec:
    - spec:opencode-plugin-install-contract
  wiki:
    - wiki:harness-adapter-package-pattern
  research:
    - research:harness-install-surfaces
    - research:codex-command-skill-installation
    - research:codex-plugin-distribution-surfaces
  ticket:
    - ticket:6uy1rx20
    - ticket:us1brnsv
    - ticket:q7h1d05q
    - ticket:cldrel01
    - ticket:lx9nnztk
    - ticket:7ex8w32y
    - ticket:3t93tsci
    - ticket:ffg8elkb
    - ticket:p9m4x2qt
    - ticket:rd48g1kg
  evidence:
    - evidence:open-loom-smoke
    - evidence:cursor-harness-install-validation
    - evidence:claude-plugin-hybrid
    - evidence:claude-sessionstart-stdout-context
external_refs:
  claude_code:
    - https://code.claude.com/docs/en/plugins
    - https://code.claude.com/docs/en/plugins-reference
    - https://code.claude.com/docs/en/settings
    - https://code.claude.com/docs/en/hooks
    - https://code.claude.com/docs/en/skills
    - https://code.claude.com/docs/en/memory
    - https://code.claude.com/docs/en/plugin-marketplaces
    - https://github.com/obra/superpowers
  codex:
    - https://developers.openai.com/codex/plugins
    - https://developers.openai.com/codex/skills
    - https://developers.openai.com/codex/guides/agents-md
    - https://developers.openai.com/codex/plugins/build
    - https://developers.openai.com/codex/cli/reference#codex-plugin-marketplace
    - https://developers.openai.com/codex/concepts/customization
    - https://developers.openai.com/codex/config-advanced
    - https://developers.openai.com/codex/changelog
  opencode:
    - https://opencode.ai/docs/config/
    - https://opencode.ai/docs/plugins/
    - https://opencode.ai/docs/skills/
    - https://opencode.ai/docs/commands/
  opencode_source:
    - https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/plugin/src/index.ts
    - https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/opencode/src/plugin/shared.ts
    - https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/opencode/src/plugin/loader.ts
    - https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/opencode/src/config/plugin.ts
    - https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/opencode/test/plugin/shared.test.ts
    - https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/opencode/test/plugin/trigger.test.ts
  gemini_cli:
    - https://geminicli.com/docs/extensions/
    - https://geminicli.com/docs/extensions/reference/
    - https://geminicli.com/docs/cli/skills/
    - https://geminicli.com/docs/cli/custom-commands/
  cursor:
    - https://cursor.com/docs/rules
    - https://cursor.com/docs/skills
    - https://cursor.com/docs/plugins
    - https://cursor.com/docs/reference/plugins
  agent_skills:
    - https://agentskills.io/specification
  installer_precedents:
    - https://brew.sh/
    - https://rust-lang.org/tools/install/
    - https://docs.astral.sh/uv/getting-started/installation/
    - https://ohmyz.sh/
    - https://ui.shadcn.com/docs/installation
    - https://code.visualstudio.com/api/working-with-extensions/publishing-extension
---

# Question

What installation and distribution model should Loom use so OpenCode, Claude
Code, Codex, Gemini CLI, and Cursor users get a first-class install experience
without turning Loom into a runtime, hidden helper system, or harness-specific
ontology?

# Why This Matters

Loom's current installer proves that global installation is possible, but it does
not prove that the current shape is the right product experience.

The repository now supports `make install harness=opencode|claude|codex|gemini|cursor|all`
through `scripts/install-loom.sh`. That script copies canonical top-level
`rules/`, `skills/`, and optional `commands/`, then translates or mirrors files
where a harness does not accept the Loom source format directly.

That is useful, but fragile:

- the script is the only place where several install decisions are fully encoded
- generated blocks and adapters are easy to inspect but can drift from harness
  product behavior
- first-class plugin and extension systems now exist in several harnesses and
  may provide better discovery, update, marketplace, and trust behavior
- some plugin systems still do not express Loom's ordered always-on rule
  requirement cleanly
- the installer can become a shadow product surface if maintainers start treating
  its generated outputs as more real than the canonical Markdown bundle

This research is meant to preserve the broad install reasoning before changing
implementation. It intentionally treats the current `Makefile` and shell script
as proof and fallback surfaces, not as the final design.

# Scope

Covered:

- Loom's current product and installer constraints from `constitution:main`,
  `README.md`, `PROTOCOL.md`, `ARCHITECTURE.md`, `INSTALL.md`, `Makefile`, and
  `scripts/install-loom.sh`
- existing Loom install records: `research:harness-install-surfaces`,
  `research:codex-command-skill-installation`, `ticket:ffg8elkb`,
  `ticket:p9m4x2qt`, `ticket:rd48g1kg`, and
  `evidence:cursor-harness-install-validation`
- first-party/current install and extension docs for OpenCode, Claude Code,
  Codex, Gemini CLI, Cursor, and the Agent Skills specification
- popular install precedent categories: plugin marketplaces, package managers,
  `curl | sh` installers, standalone tool installers, project scaffolders,
  extension packages, and manual clone/link workflows

Excluded:

- implementation changes to the current installer
- choosing final file paths for future adapter packages
- runtime UI validation inside every harness
- adding support for unsupported harnesses
- publishing any marketplace package
- treating external package registries as Loom truth owners

# Method

Repository inspection:

- read `constitution:main` and the public product framing docs
- read `Makefile`, `scripts/install-loom.sh`, and `INSTALL.md`
- read prior install research and tickets
- inspected supported harness values and per-harness installer branches in the
  current shell script

External source inspection:

- fetched official docs for Claude Code plugins, settings, hooks, skills, and
  memory/instruction loading
- fetched official Codex docs for Agent Skills, `AGENTS.md`, and plugins
- fetched OpenCode docs for config, plugins, skills, and commands
- fetched Gemini CLI docs for extensions, extension reference, skills, and custom
  commands
- fetched Cursor docs for rules, skills, plugins, and plugin reference
- fetched the Agent Skills specification
- fetched official or project docs for installer precedents including Homebrew,
  Rust/rustup, uv, Oh My Zsh, shadcn/ui, and VS Code extension publishing

Source quality notes:

- official product docs are treated as primary evidence for current surfaces
- prior Loom tickets and evidence are treated as repository-local evidence for
  what has already been implemented and validated
- docs that returned `404`, redirects, or incomplete extracted content are noted
  as null results rather than silently treated as evidence
- product docs for these harnesses are changing quickly, so implementation work
  should recheck the exact docs before mutating adapter behavior

# Sources

Repository sources:

- `constitution:main`
- `README.md`
- `PROTOCOL.md`
- `ARCHITECTURE.md`
- `INSTALL.md`
- `Makefile`
- `scripts/install-loom.sh`
- `research:harness-install-surfaces`
- `research:codex-command-skill-installation`
- `research:codex-plugin-distribution-surfaces`
- `ticket:ffg8elkb`
- `ticket:p9m4x2qt`
- `ticket:rd48g1kg`
- `evidence:cursor-harness-install-validation`

External sources are listed in `external_refs` frontmatter and cited by section
below.

# Evidence

## Loom Product Constraints

`constitution:main`, `README.md`, `PROTOCOL.md`, and `ARCHITECTURE.md` establish
these relevant constraints:

- Loom is a Markdown-native control plane, not a runtime, daemon, MCP bundle,
  dashboard, model router, or product CLI.
- The protocol core is top-level `rules/`, `skills/`, templates, references, and
  canonical examples. Optional `commands/` wrappers are transport/adoption
  surfaces, not protocol core.
- Record creation, packet compilation, validation, and graph inspection are
  visible protocol behaviors taught through Markdown guidance and ordinary file
  tools, not hidden helper behavior.
- Harness adapters may install, translate, wrap, or invoke Loom, but they must
  not define Loom truth.
- Deleting `commands/` must not delete a Loom capability.
- A valid install model must preserve ordered always-on rules and discoverable
  on-demand skills without requiring a central Loom runtime.

These constraints rule out install strategies that make a CLI, plugin runtime,
marketplace package, generated aggregate file, or helper database the semantic
owner of Loom.

## Current Installer Baseline

Current local implementation facts from `Makefile`, `scripts/install-loom.sh`,
and `INSTALL.md`:

| Harness | Current installer behavior | Translation used | Prior validation |
| --- | --- | --- | --- |
| OpenCode | Copies rules to `~/.config/opencode/loom/rules`, skills to `~/.config/opencode/skills`, commands to `~/.config/opencode/commands`, and updates `~/.config/opencode/opencode.json` `instructions`. | JSON/JSONC config mutation for `instructions`. | `ticket:ffg8elkb` throwaway `HOME` install/uninstall. |
| Claude Code | Copies rules to `~/.claude/rules/loom`, skills to `~/.claude/skills`, and commands to `~/.claude/commands`. | Direct copies. | `ticket:ffg8elkb` throwaway `HOME` install/uninstall. |
| Codex | Copies rules to `~/.codex/loom/rules`, skills to `~/.agents/skills`, converts commands into explicit-only `loom-command-*` skills, removes legacy prompts, and mirrors rules into `~/.codex/AGENTS.md`. | Managed `AGENTS.md` block plus generated command adapter skills with `agents/openai.yaml`. | `ticket:p9m4x2qt` throwaway `HOME` install/uninstall. |
| Gemini CLI | Copies rules to `~/.gemini/loom/rules`, skills to `~/.gemini/skills`, converts commands to `~/.gemini/commands/*.toml`, and mirrors rules into `~/.gemini/GEMINI.md`. | Managed `GEMINI.md` block plus Markdown-to-TOML command conversion. | `ticket:ffg8elkb` throwaway `HOME` install/uninstall. |
| Cursor | Copies rules to `~/.cursor/loom/rules`, skills to `~/.cursor/skills`, converts commands to `~/.cursor/commands/*.md`, writes `~/.cursor/loom/cursor-user-rules.md`, and mutates Cursor User Rules storage with a managed block. | Managed User Rules block plus generated command Markdown. | `evidence:cursor-harness-install-validation`. |

The installer is reversible in the validated throwaway-home cases and uses
Loom-managed markers for single-file instruction surfaces. It is still a fragile
adapter because it directly encodes per-harness knowledge, generated file formats,
and storage assumptions in one long shell script.

## Common Loom Surfaces To Preserve

Any install strategy must map these source surfaces honestly:

| Loom source surface | Required install property | Notes |
| --- | --- | --- |
| `rules/*.md` | Always-on, ordered, mandatory when Loom is present. | Numeric filenames preserve order. A skill-only install is insufficient. |
| `skills/*/SKILL.md` | Discoverable by name and description, full content hydrated only when relevant. | This maps well to Agent Skills style surfaces. |
| `skills/*/references/` and `skills/*/templates/` | Readable on demand relative to each skill root. | A packaging format must preserve directories, not flatten skills into prose. |
| `commands/*.md` | Optional explicit workflow wrappers. | Commands are adapter prompts, not the owner of Loom workflows. |
| `optional-utilities/` | Not default protocol install. | May be installed manually or by explicit local choice. |
| `.loom/` dogfooding records | Not product install. | Canonical records in this repo are project truth for this repo only. |
| `.opencode/` dogfooding surface | Not product install. | It is a consumption surface, not source protocol corpus. |

## Agent Skills As A Portable Skill Plane

The Agent Skills specification and harness docs show strong convergence around a
directory with `SKILL.md`, YAML frontmatter, and optional supporting directories.

Doc-backed facts:

- Agent Skills require a skill directory containing `SKILL.md` with YAML
  frontmatter and Markdown body.
- Required common fields in the Agent Skills specification are `name` and
  `description`; `name` must match the parent directory and be lowercase
  alphanumeric with hyphens.
- Optional directories such as `scripts/`, `references/`, and `assets/` are
  expected by the spec and by several harness docs.
- Progressive disclosure is central: metadata is visible initially, full
  `SKILL.md` loads on activation, and resources load only when needed.
- Codex, OpenCode, Gemini CLI, and Cursor all document support for
  `~/.agents/skills` or project `.agents/skills` in some form.
- Claude Code documents `~/.claude/skills` and plugin/project skill paths, but
  the fetched Claude docs do not identify `~/.agents/skills` as a Claude skill
  discovery path.

Implication for Loom:

- Loom skills already fit the broad `SKILL.md` shape.
- A generic `~/.agents/skills` install can reduce duplicated skill copies across
  Codex, Gemini CLI, Cursor, and OpenCode.
- A generic Agent Skills install does not solve Loom's always-on ordered rules or
  optional command wrappers by itself.
- Claude Code still needs a Claude-native skill destination unless future Claude
  docs add generic `.agents/skills` support.

## Claude Code

Doc-backed install surfaces:

- User settings live in `~/.claude/settings.json`; some global config lives in
  `~/.claude.json` instead.
- Managed settings exist at OS-level managed paths and have highest precedence.
- User instructions can live in `~/.claude/CLAUDE.md`.
- Claude Code loads `CLAUDE.md` files and supports imports with `@path` up to a
  documented recursion limit.
- Claude Code reads `CLAUDE.md`, not `AGENTS.md`, though a `CLAUDE.md` can import
  `@AGENTS.md`.
- User-level rules live in `~/.claude/rules/`; project rules live in
  `.claude/rules/` and can be unconditional or path-scoped.
- Personal skills live in `~/.claude/skills/<skill-name>/SKILL.md`.
- Project skills live in `.claude/skills/<skill-name>/SKILL.md`.
- Plugin skills live at `<plugin>/skills/<skill-name>/SKILL.md` and are
  namespaced by plugin.
- Claude Code plugins are directories with `.claude-plugin/plugin.json` and may
  include `skills/`, `commands/`, `agents/`, `hooks/hooks.json`, MCP/LSP config,
  monitors, `bin/`, and limited default settings.
- Claude plugin manifests can point component paths at existing plugin-root
  directories such as `./skills/` and `./commands/`; custom component paths replace
  defaults unless the defaults are included explicitly.
- Claude auto-loads the standard plugin `hooks/hooks.json` path. Local marketplace
  install showed a plugin manifest should not also declare `"hooks":
  "./hooks/hooks.json"`, because that duplicate declaration produces a hook-load
  error after install even though schema validation passes.
- Claude plugin hooks can run command hooks on `SessionStart` and
  `UserPromptSubmit`; plugin docs show hooks may use `${CLAUDE_PLUGIN_ROOT}` and
  `${CLAUDE_PLUGIN_DATA}`. `UserPromptSubmit` can block prompt processing with a
  user-visible reason.
- `${CLAUDE_PLUGIN_ROOT}` is the plugin installation directory, not the user or
  project `.claude` settings directory. For marketplace installs, docs say
  plugins are copied into `~/.claude/plugins/cache`; local `claude plugin list
  --json` showed project-scoped plugins with `installPath` under that cache and a
  separate `projectPath`.
- Claude plugin `settings.json` supports only `agent` and `subagentStatusLine` in
  the fetched docs; unknown keys are ignored.
- Claude plugins can be installed from marketplaces and tested locally with
  `claude --plugin-dir`.
- Claude marketplaces use `.claude-plugin/marketplace.json`; relative plugin
  sources such as `./` resolve from the marketplace root, not from
  `.claude-plugin/`.

Always-on rule fit:

- Claude's clean always-on instruction surfaces are `CLAUDE.md` and
  `.claude/rules/*.md` / `~/.claude/rules/*.md`.
- Claude docs state user-level rules load at launch, but the fetched docs do not
  specify a deterministic filename ordering contract for multiple rule files.
- The fetched plugin docs do not state that the `claude plugin install` command
  runs arbitrary setup code, adds always-on rules, or appends to `CLAUDE.md`.
- A plugin can include a custom agent and set it as the main thread through
  plugin settings, but that is not equivalent to installing Loom's always-on
  rule corpus as reusable harness-agnostic instructions. It changes the agent
  selection/system prompt rather than exposing a simple ordered rule bundle.
- Hook docs say static context should use `CLAUDE.md` when no script is needed,
  but they also state that `SessionStart` stdout is added as Claude context.
  `evidence:claude-sessionstart-stdout-context` observed a local plugin hook that
  cats a bundled rule file from `${CLAUDE_PLUGIN_ROOT}/rules/*.md` and has the
  marker visible to Claude in the same startup session.
- `obra/superpowers` uses a similar `SessionStart` matcher shape
  (`startup|clear|compact`) and emits Claude context from a plugin hook, though it
  uses structured `hookSpecificOutput.additionalContext` rather than raw `cat`.

Assessment:

- Claude plugins are attractive for packaging Loom skills and possibly commands,
  namespacing, versioning, and marketplace distribution.
- Claude plugins do not currently appear to be a complete manifest-only Loom
  install surface because Loom rules must be always-on and ordered.
- The accepted Claude adapter direction is automated hybrid: a Claude plugin
  exposes canonical `skills` and optional `commands`, and a plugin `SessionStart`
  hook emits canonical top-level rules as same-session, source-marked per-rule
  stdout context.
- The current direct copy to `~/.claude/rules/loom`, `~/.claude/skills`, and
  `~/.claude/commands` remains a fallback/proof path until plugin runtime timing
  and uninstall/disable behavior are proven.
- Runtime probes showed per-rule hook stdout made all seven rule files visible in
  same-session startup context.
- The per-rule design relies on source markers and best-effort sleep staggering.
  `01-core-identity.md` appeared first in repeated probes, but strict order after
  that is not guaranteed because Claude runs matching hooks concurrently.
- Disabling or uninstalling the plugin follows Claude's plugin manager UX because
  the active rule delivery path is plugin hook context emitted at session start.
- Local marketplace install validates `loom@agent-loom` can install without
  hook-load errors after relying on standard hook auto-loading instead of a
  duplicate manifest `hooks` field.
- Hook-context loading is accepted for the Claude adapter only in the per-rule raw
  stdout form implemented by `ticket:cldrel01`. Monolithic full-rule raw stdout and
  structured additional context were previewed/truncated. Plugin-root `CLAUDE.md`
  and `.claude/rules/loom.md` did not load under local `--plugin-dir`. Arbitrary
  26-command chunking worked once but was rejected as too brittle.

## Codex

Doc-backed install surfaces:

- Codex home defaults to `~/.codex` unless `CODEX_HOME` is set.
- Global instructions use `AGENTS.override.md` first if present, otherwise
  `AGENTS.md`; only the first non-empty global file is used.
- Project instructions are loaded by walking from project root to current working
  directory and concatenating one instruction file per directory.
- Combined project docs stop once `project_doc_max_bytes` is reached; the default
  documented value is `32 KiB`.
- Codex skills are directories with required `SKILL.md` frontmatter `name` and
  `description`.
- User skills live under `$HOME/.agents/skills`; repo/project and admin/system
  tiers also exist.
- Codex supports explicit `$skill` invocation and implicit invocation based on
  description.
- Optional `agents/openai.yaml` can set UI metadata and
  `policy.allow_implicit_invocation`.
- `allow_implicit_invocation` defaults to `true`; setting it to `false` preserves
  explicit invocation while preventing automatic selection.
- Codex plugins use `.codex-plugin/plugin.json` and can package `skills/`, MCP
  servers, apps/connectors, and assets.
- Codex plugin marketplaces are JSON catalogs under repo or user `.agents/plugins`
  paths, and plugins install into a Codex plugin cache.
- `codex plugin marketplace add` can add local, GitHub shorthand, HTTP(S) Git,
  and SSH marketplace sources.
- The official CLI reference marks `codex plugin marketplace` experimental.
- Installed local `codex-cli 0.123.0` exposes marketplace add/upgrade/remove but
  not a simple non-interactive `codex plugin install` command.
- OpenAI source inspected in `research:codex-plugin-distribution-surfaces` models
  plugin manifest paths for `skills`, `mcpServers`, `apps`, and `interface`, not
  `AGENTS.md`, `commands`, `agents`, or consistently supported plugin hooks.
- Plugin skill paths are namespaced from the plugin manifest name in inspected
  source, which should reduce collision risk for a `loom` plugin but still needs
  runtime validation.

Always-on rule fit:

- Codex's clean always-on user instruction surface is `~/.codex/AGENTS.md` or
  `AGENTS.override.md`.
- The fetched Codex plugin docs do not describe plugins as a mechanism for
  always-on instructions.
- Prior research already found that `~/.codex/rules/` is not a Markdown rules
  instruction surface for Loom; it should not receive Loom rules.

Assessment:

- Codex plugins are a good candidate for distributing Loom skills and generated
  explicit-only command adapter skills, but not a complete Loom install by
  themselves.
- The current generated command adapter skill pattern is aligned with Codex's
  skills-first extension surface because command wrappers become explicit-only
  skills with `allow_implicit_invocation: false`.
- A future Codex plugin package could contain canonical Loom skills and generated
  command adapter skills, but a managed `AGENTS.md` block or project `AGENTS.md`
  still appears necessary for ordered always-on rules.
- The `AGENTS.md` size budget matters: mirroring every rule into one global file
  can consume a meaningful chunk of the documented default project-doc budget if
  project instructions are also large.
- Current focused recommendation: run a package-layout spike before implementation
  chooses between a repository-root plugin, a derivative plugin fixture, or
  fallback-only direct skill generation. See
  `research:codex-plugin-distribution-surfaces` and `ticket:lx9nnztk`.

## OpenCode

Doc-backed install surfaces:

- Global config lives at `~/.config/opencode/opencode.json`.
- The `instructions` field accepts an array of paths and glob patterns for
  always-on/model instructions.
- Global commands live in `~/.config/opencode/commands/`; project commands live
  in `.opencode/commands/`.
- OpenCode custom commands can be Markdown files, with filename as command name
  and `$ARGUMENTS` / positional variables for arguments.
- Global skills can live in `~/.config/opencode/skills/<name>/SKILL.md`.
- OpenCode also discovers compatible skills from `~/.claude/skills`,
  `~/.agents/skills`, and project equivalents.
- OpenCode plugins are JavaScript/TypeScript modules exporting plugin functions
  and hooks. They can be local files or npm packages listed in config. Npm
  plugins are installed automatically with Bun and cached under
  `~/.cache/opencode/node_modules/`.
- The fetched OpenCode plugin docs describe hooks, events, custom tools,
  environment injection, and TUI behavior, but do not state that plugins package
  rules, skills, or commands as static resources.
- Official plugin docs show `plugin` array examples with npm package names only;
  they do not document GitHub repository shorthands as supported plugin specs.
- Source-level config handling accepts `plugin` entries as a string or
  `[string, options]`, with arbitrary options records.
- Source-level path handling treats specs starting with `file://`, `.`, or an
  absolute path as file plugins; other specs are treated as npm-style specs and
  passed to `Npm.add` after bare package names are normalized to `@latest`.
- Source-level `parsePluginSpecifier` tests cover bare npm packages, scoped
  packages, `npm:` protocol specs, aliases, and Git URLs such as
  `git+https://github.com/opencode/acme.git` and
  `git+ssh://git@github.com/opencode/acme.git`.
- The operator checked current OpenCode plugin loading and reported that Git URL
  plugin installs are not supported in practice. Treat npm publication and local
  file/path plugins as the viable distribution paths unless future runtime
  evidence contradicts this.
- The deeper source inspection did not find first-class `skill` or `command`
  registration fields on the plugin `Hooks` interface.
- The plugin `Hooks` interface does include `experimental.chat.system.transform`,
  which can mutate the system prompt array, but the better OpenCode route for
  Loom rules is now `config(config)` mutating the documented `instructions`
  config surface.
- The plugin `Hooks` interface includes `command.execute.before`, but source
  inspection shows that hook runs only after an existing command is resolved; it
  does not prove slash-command registration.
- `evidence:open-loom-smoke` validated `open-loom`, which reads ordered top-level
  `rules/*.md`, default-exports an OpenCode-shaped object with `id: "open-loom"`
  and `server()`, and uses the plugin `config(config)` hook to register ordered
  rule files through `config.instructions`, bundled skills through
  `config.skills.paths`, and bundled command wrappers through `config.command`.
  OpenCode CLI `1.14.22` validated the resolved config and skill discovery in an
  isolated temporary environment. Follow-up validation also proved local
  package-root plugin resolution, clean-project skill loading with 20 skills, and
  package dry-run contents. The package now declares `engines.opencode:
  >=1.14.22 <2`.
- `open-loom@0.1.0` is published on npm. A normal repo-root `opencode.json` with
  `plugin: ["open-loom@0.1.0"]` can load the package from OpenCode's package
  cache and expose Loom rules, skills, and commands. In isolated cold-cache
  validation, OpenCode `1.14.22` can log `NpmInstallFailedError` on the first
  config-file run while still caching the package; a second run in the same cache
  succeeds.

Always-on rule fit:

- OpenCode has a direct, clean always-on route: put installed Loom rules in a
  stable directory and add a glob to `opencode.json` `instructions`.
- OpenCode can also receive Loom's ordered rules from `open-loom` through the
  plugin `config(config)` hook, which appends the package's absolute rule-file
  paths to `config.instructions`.

Assessment:

- The ideal OpenCode user experience is a plugin-first install: the user adds one
  entry to the `plugin` array in `opencode.json`, and the plugin exposes bundled
  Loom rules, skills, and commands.
- That ideal is now accepted for `open-loom@0.1.0` on OpenCode `>=1.14.22 <2`,
  with the cold-cache first-run installer caveat tracked by `ticket:us1brnsv`.
  Official docs did not state this full static-resource registration shape; it is
  supported by source inspection and runtime evidence.
- A plugin can read its own bundled files using normal JavaScript module
  techniques such as `import.meta.url` in the repository/package-root `open-loom`.
- Separate first-class plugin registration fields for skills and slash commands
  were not found, but `config.skills.paths` and `config.command` are sufficient
  for current OpenCode `1.14.22` validation.
- GitHub-based plugin installation should not be recommended for OpenCode. The
  viable plugin distribution paths are an npm package for normal users and a
  cloned repo plus file/local path plugin entry for users who want to consume the
  repository directly.
- The preferred plugin design should consume or expose Loom's existing Markdown
  files from the package or cloned repository where practical, rather than
  generating a second plugin-owned Markdown corpus.

## Gemini CLI

Doc-backed install surfaces:

- Gemini CLI extensions distribute prompts, MCP servers, custom commands,
  themes, hooks, sub-agents, and agent skills.
- Extensions are installed with commands such as
  `gemini extensions install <source>` from GitHub repositories or local paths.
- Extensions load from `<home>/.gemini/extensions`; installing creates a copy,
  while linking local extensions uses a symlink for immediate testing.
- Each extension root must contain `gemini-extension.json`.
- `gemini-extension.json` supports fields including `name`, `version`,
  `description`, `mcpServers`, `contextFileName`, `excludeTools`, `plan`,
  `settings`, and `themes`.
- `contextFileName` names a context file loaded from the extension directory;
  if omitted and `GEMINI.md` exists, `GEMINI.md` is loaded.
- Extensions can package agent skills under `skills/<name>/SKILL.md`.
- Gemini skills are based on the Agent Skills open standard and may live in
  `.gemini/skills`, `.agents/skills`, `~/.gemini/skills`, `~/.agents/skills`, or
  inside extensions.
- Skill precedence is Workspace > User > Extension; within user/workspace tiers,
  `.agents/skills` overrides `.gemini/skills`.
- Gemini custom commands are TOML files under `~/.gemini/commands/` or project
  `.gemini/commands/`; subdirectories produce namespaced commands such as
  `/git:commit`.
- Gemini custom commands require a `prompt` string and optional `description`.
  Markdown command wrappers must be converted to TOML.

Always-on rule fit:

- Gemini extensions can load a context file from the extension directory,
  defaulting to `GEMINI.md` when present.
- This is a stronger first-class fit than Codex or Claude plugins because the
  extension format itself includes a context-file route plus skills and commands.

Assessment:

- Gemini CLI extensions are a strong candidate for a first-class Loom install
  package.
- A Gemini extension could package ordered Loom rules through an extension
  `GEMINI.md` or configured context file, canonical skills under `skills/`, and
  generated TOML commands under `commands/`.
- The current direct install is serviceable, but a Gemini extension may better
  support install/update/disable/link workflows and avoids hand-editing global
  `GEMINI.md`.
- Implementation should verify whether extension context is loaded with the
  right priority and whether a large ordered rules corpus remains visible in
  actual sessions.

## Cursor

Doc-backed install surfaces:

- Cursor User Rules are global preferences in Cursor Settings -> Rules and apply
  across Agent Chat.
- Cursor Project Rules live in `.cursor/rules`; `.mdc` frontmatter supports
  fields such as `description`, `globs`, and `alwaysApply`.
- Rule application shapes include always-apply, intelligent/relevance-based,
  file-specific, and manual `@` mention.
- Cursor also supports `AGENTS.md` in project roots or subdirectories, with
  nested files applying to descendants.
- Cursor skills are Agent Skills directories with `SKILL.md`; user/global paths
  include `~/.agents/skills` and `~/.cursor/skills`.
- Cursor also loads compatible skill paths from Claude and Codex locations.
- `disable-model-invocation: true` can make a skill explicit-only.
- Cursor plugins are Git-backed bundles with `.cursor-plugin/plugin.json`.
- Cursor plugins can package rules, skills, agents, commands, MCP servers, and
  hooks.
- Cursor plugin component discovery includes `rules/`, `skills/`, `agents/`,
  `commands/`, `hooks/hooks.json`, and `mcp.json` unless manifest paths override.
- Cursor plugin rules are generally `.mdc` files in `rules/` with YAML
  frontmatter.
- Cursor plugin commands can be `.md`, `.mdc`, `.markdown`, or `.txt` files with
  optional `name` and `description` frontmatter.
- Cursor plugins can be installed from the marketplace at project or user level;
  team marketplaces can make plugins required or optional.
- Local plugin testing uses `~/.cursor/plugins/local`, including symlinked plugin
  repositories.

Always-on rule fit:

- Cursor plugin rules appear to be a clean first-class way to package Loom rules
  if generated rule files can set `alwaysApply: true` and preserve order.
- This may be better than directly mutating Cursor User Rules storage, which the
  current installer does through a SQLite-backed state path on macOS.

Assessment:

- Cursor plugins are a strong candidate for first-class Loom distribution because
  they can package all three Loom surfaces: rules, skills, and commands.
- The current Cursor installer is useful proof, but User Rules database mutation
  is more brittle than a documented plugin package path.
- A Cursor plugin adapter may need generated `.mdc` rule frontmatter and perhaps
  generated command frontmatter, but those generated files would be packaging
  outputs, not semantic owners.
- Implementation should verify actual Cursor behavior for plugin rule ordering,
  `alwaysApply`, user-level install scope, and local plugin reload/discovery.

## Cross-Harness Plugin And Extension Fit

| Harness | First-class package surface | Covers rules? | Covers skills? | Covers commands? | Current fit |
| --- | --- | --- | --- | --- | --- |
| Claude Code | `.claude-plugin/plugin.json` plugins plus `.claude-plugin/marketplace.json` | Not manifest-only; prototype uses a plugin `SessionStart` hook to generate `loom.md` into user or project `.claude/rules/loom/`. | Yes. | Yes, but plugin skills are recommended for new plugins. | Automated hybrid plugin. |
| Codex | `.codex-plugin/plugin.json` plugins and marketplaces | Not in fetched plugin docs; use `~/.codex/AGENTS.md`. | Yes. | Not as native command docs here; adapter skills are viable. | Hybrid. |
| OpenCode | JS/TS plugins via npm package or local file/path specs | Yes, via plugin `config(config)` adding ordered files to `config.instructions`. | Yes, via `config.skills.paths`. | Yes, via `config.command`. | `open-loom` npm/local distribution. |
| Gemini CLI | `gemini-extension.json` extensions | Yes, via extension context file / `GEMINI.md` in fetched docs. | Yes. | Yes, as TOML command files. | Strong plugin/extension candidate. |
| Cursor | `.cursor-plugin/plugin.json` plugins | Yes, plugin rules. | Yes. | Yes. | Strong plugin candidate. |

The strongest already-documented full package candidates are Gemini CLI
extensions and Cursor plugins. Claude Code and Codex plugins are useful but
incomplete unless paired with explicit always-on instruction installation.
OpenCode's plugin system is attractive for UX and current `open-loom` validation
covers rules, skills, and commands through config mutation. Distribution should
assume `open-loom` npm publication for normal users and a local file/path plugin
entry for cloned-repo use, not Git URL plugin specs.

## Existing Install Surfaces Compared

| Surface | Strengths | Weaknesses | Loom use |
| --- | --- | --- | --- |
| Direct user config copy | Transparent, no marketplace dependency, easy to inspect, works today. | Requires per-harness mutation logic and careful uninstall. | Good fallback and local developer install. |
| Managed single-file block | Preserves existing user content when marker logic is correct. | Harder to validate in UI; conflicts possible; size and precedence concerns. | Necessary for Codex and maybe Claude/OpenCode unless native config points at files. |
| Generic `~/.agents/skills` | Portable for Codex, Gemini, Cursor, OpenCode; reduces duplicated skills. | Does not solve rules or commands; Claude support not shown in fetched docs. | Good shared skill target for supported harnesses. |
| Native plugin/extension package | Better install/update/disable/marketplace UX; documents package boundaries. | Harness-specific package files; may not cover all Loom surfaces. | Preferred where it covers ordered rules, skills, and commands. |
| Project-local install | Version-controlled and team-visible. | Not a global user install; can pollute projects if used casually. | Good for teams adopting Loom per repository. |
| Manual clone/link | Maximum transparency and low tooling. | Poor uninstall/update UX; user must know harness paths. | Useful developer/testing path, not best default. |

## Installer Precedent Comparison

Popular installer patterns provide useful product lessons but do not transfer
directly to Loom.

### Package Managers

Homebrew precedent:

- one-line shell installer bootstraps the package manager itself
- packages install into Homebrew-owned directories and symlink into a prefix
- Homebrew avoids installing files outside its prefix
- formulae/casks provide update and distribution conventions

VS Code extension marketplace precedent:

- extensions can be packaged as `.vsix` files for private/off-market install
- marketplace publishing provides discovery, versioning, publisher identity, and
  install analytics
- compatibility is declared through metadata such as `engines.vscode`

Loom implication:

- Package managers are good at installing a bundle or binary, but they do not
  solve per-harness instruction registration.
- A Homebrew formula for Loom could fetch the repo or install adapter packages,
  but it would still need post-install guidance or a separate adapter step to
  mutate harness config.
- A plugin marketplace is closer to the UX Loom wants when the harness's plugin
  system can express all needed surfaces.

### Standalone Shell Installers

uv precedent:

- supports `curl | sh`, PowerShell, package managers, Docker, Cargo, GitHub
  releases, and self-update for standalone installs
- lets users inspect installer scripts before execution
- documents update and uninstall differences by install method
- uses an opt-out environment variable for PATH mutation

rustup precedent:

- manages toolchains across channels and platforms
- installs binaries under a user-owned tool directory
- documents update and uninstall commands
- PATH setup is explicitly documented as a common source of post-install issues

Loom implication:

- A standalone installer script can be acceptable as a bootstrap/fallback, but it
  must make mutations explicit and reversible.
- Loom does not install a binary toolchain, so PATH management is not the main
  issue. The analogous risk is hidden mutation of harness config.
- If Loom keeps shell install, it should document update and uninstall clearly
  per method and support a dry-run or inspection posture before mutation.

### Dotfile And Framework Installers

Oh My Zsh precedent:

- the fetched homepage confirms a community-driven Zsh configuration framework
  with plugins and themes, but the extracted content did not provide detailed
  installer behavior.

Loom implication:

- Dotfile installers are an intuitive comparison because Loom installs into user
  config directories, but Loom must be stricter about not overwriting or owning
  unrelated user config.

### Project Scaffolders And Source-Copy Tools

shadcn/ui precedent:

- uses a CLI/init model for project setup across supported frameworks
- framework-specific guides distinguish new-project and existing-project setup

Loom implication:

- Project bootstrap could be a valid separate workflow for repositories that want
  Loom checked in as part of a project.
- Source-copy/project-scaffold patterns are less ideal for global user-level
  harness install because Loom's active surfaces live in harness config roots,
  not only in the target project.

## Option Comparison For Loom

| Option | Description | Pros | Cons | Research judgment |
| --- | --- | --- | --- | --- |
| Keep current Makefile/script as-is | Continue one shell adapter for all harnesses. | Works today, simple entrypoint, validated in temp homes. | Fragile, script-owned knowledge, weak first-class UX. | Keep as fallback/proof, not final design. |
| One monolithic `loom install` CLI | Build a real Loom installer command. | Could centralize validation and UX. | Conflicts with constitutional no-product-CLI direction and risks hidden ontology. | Reject for core. |
| Harness-native plugin/extension packages | Build per-harness packages for Cursor/Gemini and maybe Claude/Codex. | Better install/update/disable/marketplace fit. | Surface coverage differs; generated adapters must not own semantics. | Preferred where complete; hybrid where incomplete. |
| Generic Agent Skills install | Install skills once under `~/.agents/skills`. | Portable and reduces duplication. | Rules and commands still need harness-specific handling. | Use as shared skill plane where docs support it. |
| Project-local Loom bootstrap | Copy rules/skills into repo harness dirs or `.agents/skills`. | Version-controlled team adoption. | Different from global install; can mix product and project state. | Useful separate path, not replacement. |
| Package manager formula | Homebrew/Nix/etc installs Loom bundle. | Familiar install/update. | Does not register with harnesses alone. | Optional distribution wrapper only. |
| `curl | sh` remote installer | One-line install from GitHub. | Easy onboarding. | Trust and mutation risk; hard to review if script changes remotely. | Only if script is inspectable, version-pinned, and non-authoritative. |
| Manual clone/link | User clones repo and symlinks/copies surfaces. | Transparent and hackable. | High friction, poor uninstall/update. | Developer path, not default UX. |

# Rejected Options

## Plugin-Only Install For Every Harness

Rejected because plugin coverage is uneven.

- Claude plugins do not cleanly install arbitrary always-on Loom rules in the
  fetched docs.
- Codex plugins package skills/apps/MCP/assets but not always-on instructions in
  the fetched docs.
- OpenCode plugins are not yet proven as full static bundles of rules, skills,
  and commands. They should be prototyped rather than universally assumed.
- Gemini and Cursor have much stronger package fit, but making the lowest-common
  plugin model the universal strategy would either underuse them or overclaim
  support in other harnesses.

## Always-On Rules As Skills

Rejected because skills are on-demand expertise surfaces. Loom rules are mandatory
always-on doctrine. Installing rules as skills would hide core protocol behavior
behind relevance selection and would contradict Loom's operating sequence.

## Claude Hook Hack For Loading Rules

Rejected unless future docs explicitly bless it. Claude hook docs say static
context should use `CLAUDE.md` rather than `SessionStart` hooks, and the
`InstructionsLoaded` hook is for observability rather than modifying loaded
instructions.

This rejection targets hook-delivered context. It does not reject using a plugin
hook as an installer that writes files into Claude's documented static user-rule
surface, provided evidence records the first-session timing and cleanup limits.

## Codex `~/.codex/rules/` For Loom Markdown Rules

Rejected by prior research because that surface is not equivalent to Loom
Markdown instructions. Loom rules should live in `AGENTS.md` or another actual
instruction surface for Codex.

## Cursor User Rules Database Mutation As The Strategic Endpoint

Rejected as the long-term ideal, though it remains useful proof. The current
installer can mutate Cursor User Rules with a managed block, but Cursor plugins
now provide a documented way to package rules, skills, and commands. A plugin
package should be evaluated before doubling down on direct state database writes.

## Package Manager As The Sole Install Story

Rejected because package managers can install the bundle but cannot by themselves
make each harness load ordered rules, discover skills, or expose commands.

## Generated Aggregates As Canonical Truth

Rejected because generated `AGENTS.md`, `GEMINI.md`, `cursor-user-rules.md`, TOML
commands, and command adapter skills are adapter outputs. Canonical behavior stays
in top-level `rules/`, `skills/`, optional `commands/`, templates, and references.

# Null Results

- Exa web search hit its free MCP rate limit during earlier broad discovery, so
  this record relies on direct official-doc fetches and repository inspection
  rather than additional web search result expansion.
- `https://cursor.com/docs/commands` returned `404` during direct fetch. Cursor
  command facts in this record come from Cursor plugin reference docs and prior
  repository research rather than that URL.
- `https://docs.anthropic.com/en/docs/claude-code/plugins` redirected to
  `https://code.claude.com/docs/en/plugins`; the redirect was blocked by the
  fetch tool, so the canonical `code.claude.com` URL was used directly.
- The fetched Oh My Zsh homepage did not expose detailed install, backup, update,
  or uninstall behavior in the extracted content, so it is not used as strong
  evidence beyond the broad dotfile-framework analogy.
- The fetched shadcn/ui installation page did not expose enough detail about the
  source-copy `add` model or registry update philosophy to use it as strong
  evidence beyond project scaffold/init comparison.

# Conclusions

1. Loom needs a per-harness install strategy, not a single universal adapter
   model.

2. The best install mechanism is the most native mechanism that can express all
   three Loom surfaces without changing Loom's source of truth: ordered
   always-on rules, on-demand skills, and optional explicit commands.

3. Cursor plugins and Gemini CLI extensions are currently the strongest
   first-class package candidates because their docs show support for rules or
   context plus skills plus commands.

4. Claude Code plugins and Codex plugins are useful but incomplete for Loom as
   standalone installs because the fetched docs do not show a clean plugin-owned
   always-on rule mechanism. They likely need a hybrid with `CLAUDE.md` / user
   rules or `AGENTS.md` for rules.

5. OpenCode should continue through `open-loom` plugin-first validation. The
   ideal UX is a single `plugin` array entry in `opencode.json`. Current evidence
   validates local file plugin loading and `config(config)` registration for
   ordered rules, bundled skills, and bundled command wrappers. Operator
   validation indicates Git URL plugin specs are not supported, so npm publication
   and local file/path entries are the viable distribution paths.

6. Portable Agent Skills are a strong common denominator for the `skills/` part
   of Loom, especially across Codex, Gemini CLI, Cursor, and OpenCode, but they
   are not a complete Loom install surface.

7. The current `Makefile` and `scripts/install-loom.sh` should remain available
   as a proof/fallback adapter while the repository designs first-class packages
   and safer managed config fallbacks. They should not become the long-term
   semantic center.

8. A good future install architecture probably has two layers:

- canonical product source: unchanged top-level `rules/`, `skills/`, optional
  `commands/`, templates, references, and examples
- generated or packaged adapter outputs: per-harness plugin/extension packages,
  managed blocks, converted command files, and fixture expectations derived from
  the canonical source

9. Adapter outputs need validation fixtures and uninstall expectations, but they
   must remain derivative. The project should be able to regenerate or replace
   them without changing Loom's protocol truth.

# Recommendations

## Strategic Recommendation

Adopt a hybrid install strategy:

- use first-class plugin/extension packages where they cleanly cover Loom rules,
  skills, and commands
- use direct managed config installs where plugin systems do not cover ordered
  always-on rules
- use generic Agent Skills paths where they reduce duplicate skill copies without
  weakening per-harness behavior
- keep the current Makefile/script as a local bootstrap and validation fallback
  until the new strategy is proven

## Per-Harness Recommendation

| Harness | Recommended next strategy | Rationale |
| --- | --- | --- |
| OpenCode | Accepted plugin-first install via `open-loom@0.1.0`; investigate cold-cache first-run caveat separately. | Ideal UX is one `plugin` entry; npm package distribution and local file/path entries are validated. `ticket:us1brnsv` owns the remaining first-run installer behavior. |
| Claude Code | Keep direct or hybrid install; evaluate plugin for skills/commands only if rules are installed separately through `CLAUDE.md` or user rules. | Plugins are first-class but not a complete always-on rules surface in fetched docs. |
| Codex | Keep hybrid install; evaluate Codex plugin for canonical skills and generated explicit-only command adapter skills, paired with managed `AGENTS.md` rules. | Plugins package skills, but rules still need AGENTS. |
| Gemini CLI | Prototype a Gemini extension adapter. | Extension docs support context file, skills, and commands. |
| Cursor | Prototype a Cursor plugin adapter before investing further in User Rules DB mutation. | Plugin docs support rules, skills, and commands. |

## Implementation Sequencing Recommendation

1. Do not refactor `scripts/install-loom.sh` first. First create a small plan or
   tickets for adapter-package prototypes.
2. Prototype Cursor plugin packaging because Cursor appears to cover all Loom
   surfaces and would replace the most brittle current behavior.
3. Prototype Gemini extension packaging because Gemini appears to cover all Loom
   surfaces and has explicit extension install/link/update commands.
4. Use the accepted OpenCode package as the first concrete adapter-package
   precedent, but do not assume other harnesses expose equivalent APIs.
5. Re-evaluate Claude and Codex hybrid shapes after Cursor/Gemini prove the
   generated-adapter discipline.
6. Decide whether shared `~/.agents/skills` should become the default skill
   destination for Codex/Gemini/Cursor/OpenCode global installs only after plugin
   skill exposure limits are known.
7. Update `INSTALL.md` only after the preferred path is implemented or at least
   captured in a ready ticket.

## Validation Recommendation

For any future install implementation ticket, require evidence for:

- installed files and generated adapter files under a temporary `HOME`
- uninstall removing only Loom-managed files or marked blocks
- ordered rule loading surface exists and points at the canonical installed rule
  corpus or generated ordered aggregate
- skills are discoverable by name/description without eagerly loading full skill
  references/templates
- optional commands remain explicit invocation surfaces
- generated adapter outputs identify their Loom source files
- plugin or extension packages can be installed, disabled, or linked through the
  harness's documented commands where applicable

## Documentation Recommendation

Split future install docs into three conceptual modes:

- user-global install: install Loom into a developer's harness config roots
- project-local adoption: commit Loom-compatible instructions/skills into a
  repository's harness directories or `.agents/skills`
- adapter/package development: generate and validate harness-specific plugin or
  extension packages from canonical Loom source

# Open Questions

- Should Loom keep one top-level `make install` entrypoint after first-class
  Cursor/Gemini packages exist, or should it become a developer-only adapter
  fixture runner?
- Should generic `~/.agents/skills` become the default global skill target for
  Codex, Gemini CLI, Cursor, and OpenCode to avoid four separate skill copies?
- Should the Claude marketplace continue using source `./` for local/Git testing,
  or should a narrower release-packaged Claude plugin artifact be introduced
  before broad distribution?
- Can Cursor plugin rules set `alwaysApply: true` and preserve numeric rule order
  well enough to replace User Rules mutation?
- Does Gemini extension context loading preserve the mandatory ordered Loom rule
  behavior in real sessions?
- Should generated adapter packages live in the repository as committed fixtures,
  be generated only during release, or remain examples under `examples/`?
- What is the root cause of OpenCode `1.14.22` logging `NpmInstallFailedError` on
  the first cold-cache npm-package config-file run before succeeding on a second
  run?
- How should versioning work for adapter packages if Loom itself is source-only
  Markdown?
- Should install docs recommend marketplace installs for users and direct clone
  installs for contributors?
- How much dry-run or diff output should a shell fallback provide before mutating
  user config?
- Which install validations belong as evidence records versus non-normative
  adapter fixtures?

# Linked Work

- Initiative: `initiative:loom-install-experience`
- Plan: `plan:install-experience-harness-adapters`
- Harness ticket: `ticket:6uy1rx20` - OpenCode plugin-first install path
- Follow-up ticket: `ticket:us1brnsv` - OpenCode cold-cache npm-plugin first-run
  behavior
- Spec: `spec:opencode-plugin-install-contract`
- Wiki: `wiki:harness-adapter-package-pattern`
- Harness ticket: `ticket:q7h1d05q` - Claude Code hybrid install path
- Claude hybrid evidence: `evidence:claude-plugin-hybrid`
- Harness ticket: `ticket:lx9nnztk` - Codex hybrid plugin install path
- Harness ticket: `ticket:7ex8w32y` - Gemini CLI extension install path
- Harness ticket: `ticket:3t93tsci` - Cursor plugin install path
- Prior path-mapping research: `research:harness-install-surfaces`
- Prior Codex command adapter research: `research:codex-command-skill-installation`
- Focused Codex plugin research: `research:codex-plugin-distribution-surfaces`
- Prior installer ticket: `ticket:ffg8elkb`
- Prior Codex adapter ticket: `ticket:p9m4x2qt`
- Prior Cursor installer ticket: `ticket:rd48g1kg`
- Prior Cursor validation evidence: `evidence:cursor-harness-install-validation`

Downstream work should create bounded tickets before changing installer code or
adding generated adapter package directories.
