---
id: ticket:6uy1rx20
kind: ticket
status: complete_pending_acceptance
change_class: release-packaging
risk_class: medium
created_at: 2026-04-25T18:46:08Z
updated_at: 2026-04-25T22:07:56Z
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
    - research:harness-install-surfaces
  related:
    - ticket:ffg8elkb
  packet:
    - packet:ralph-ticket-6uy1rx20-20260425T195559Z
    - packet:critique-ticket-6uy1rx20-open-loom-20260425T201112Z
  evidence:
    - evidence:open-loom-smoke
  critique:
    - critique:open-loom-review
    - critique:open-loom-config-hook-review
external_refs:
  opencode_docs:
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
depends_on: []
---

# Summary

Build and validate the `open-loom` OpenCode install path where the ideal user
experience is adding one `open-loom` plugin entry to `opencode.json` and having
the plugin expose bundled Loom rules, skills, and optional commands through
OpenCode's first-class plugin APIs.

# Context

The original OpenCode ticket assumed direct config install was the correct path:
copy rules under `~/.config/opencode/loom/rules`, copy skills under
`~/.config/opencode/skills`, copy commands under `~/.config/opencode/commands`,
and add the rule glob to `opencode.json` `instructions`.

The operator clarified a better target UX: OpenCode should ideally work like a
first-class JavaScript/TypeScript plugin. A user should add a plugin entry to the
`plugin` array in `opencode.json`, and the plugin should read or register its
bundled Loom surfaces without a separate install step.

Deeper evidence now says this is plausible enough to validate, but not proven:

- official OpenCode docs show npm package plugin entries and local plugin files
- official docs do not document GitHub repo plugin specs
- source-level config accepts plugin entries as strings or `[string, options]`
- source-level path handling accepts `file://`, relative, and absolute path specs
- source-level tests cover Git URL plugin specs such as `git+https://...` and
  `git+ssh://...`, but not `github:owner/repo` shorthand
- operator validation found current OpenCode does not support Git URL plugin
  installs in practice
- normal-user distribution should therefore be an npm package; local/manual users
  can clone the repo and reference the plugin through a file or local path entry
- the plugin `Hooks` interface includes `config(config)`, and runtime validation
  shows it can mutate `instructions`, `skills.paths`, and `command` in the
  resolved OpenCode config before skill and command discovery
- the plugin `Hooks` interface does not currently show separate first-class
  `skill` or `command` registration fields in the inspected source
- `command.execute.before` runs only after an existing command is resolved, so it
  does not by itself prove slash-command menu registration

# Why Now

OpenCode's ideal install surface may be better than the direct-copy fallback. If
a Loom plugin can register or inject all three surfaces, OpenCode becomes one of
the most attractive user installs: a single `plugin` entry, no shell copy step,
and no managed block edits.

The project should validate that ideal before hardening direct config fallback or
documenting OpenCode as the intentional direct-install outlier.

# Scope

- validate the minimal `open-loom` OpenCode plugin package or fixture
- target two supported distribution paths: an npm package entry for normal users
  and a file/local path plugin entry for users who clone the repository
- treat Git URL plugin specs as unsupported unless new upstream behavior appears
- test whether the plugin can read bundled Loom files from its package location,
  ideally through normal JavaScript module-relative file reads
- prefer consuming or exposing Loom's existing Markdown files from the package or
  cloned repository rather than generating a second plugin-owned copy
- test whether ordered Loom rules can be registered through the plugin API and
  OpenCode's supported instruction config surface
- test whether bundled Loom skills can be exposed through the plugin API and
  OpenCode's supported skill config surface
- test whether optional Loom commands can be registered through the plugin API and
  OpenCode's supported command config surface
- compare plugin-first install against current direct config install
- update `INSTALL.md`, adapter fixtures, and shell fallback only after the plugin
  API limits are evidenced

# Non-goals

- do not assume OpenCode plugins can register skills or commands until proven
- do not depend on Git URL plugin specs for OpenCode distribution
- do not publish an npm package without explicit operator approval and credentials;
  preparing a package that can be published is in scope
- do not add runtime behavior that makes the plugin the owner of Loom semantics
- do not change canonical `rules/`, `skills/`, or `commands/` to fit OpenCode
- do not remove the current direct fallback until plugin-first behavior is proven
- do not rely on undocumented third-party plugin syntax without source or runtime
  validation

# Acceptance Criteria

- the ticket records whether plugin-first OpenCode install is accepted, partially
  accepted with fallbacks, or rejected with source-backed rationale
- plugin spec validation distinguishes official-doc support from source-level or
  runtime-observed support
- the ticket documents npm package publication as the normal user install path
  and local file/path plugin entries as the clone-from-repo path
- Git URL plugin specs are recorded as unsupported for current OpenCode, not as a
  recommended install option
- `open-loom` can read bundled Loom files, or the ticket records why bundled
  file reads are not viable
- the npm/local plugin shape keeps canonical Loom Markdown consumable directly
  from the package or cloned repo where practical
- ordered always-on Loom rules are injected or registered by plugin API, or the
  ticket records why `opencode.json` `instructions` remains necessary
- skills are exposed through plugin API, or the ticket records why direct skill
  directory install remains necessary
- optional commands are exposed through plugin API, or the ticket records why
  Markdown command files or config-defined commands remain necessary
- no generated plugin output is treated as canonical Loom semantics
- `INSTALL.md` reflects the proven OpenCode recommendation and any fallback steps

# Coverage

Covers:

- None - no spec-owned acceptance IDs exist. This ticket consumes
  `research:loom-install-distribution-methods#opencode` and owns ticket-local
  acceptance criteria for the OpenCode plugin-first install slice.

# Claim Matrix

- Bundled file reads: supported by `evidence:open-loom-smoke`; `node
  open-loom.mjs --smoke` read 7 ordered top-level rule files from the
  package/clone layout.
- Ordered rules: supported by `evidence:open-loom-smoke`; `open-loom` registers
  each ordered rule file as an absolute `config.instructions` entry through
  OpenCode's plugin `config(config)` hook, and `opencode debug config` shows the
  resolved ordered instruction paths.
- Skills: supported by `evidence:open-loom-smoke`; `open-loom` registers the
  bundled `skills/` root through `config.skills.paths`, and `opencode debug skill`
  discovers Loom skills from that path.
- Commands: supported by `evidence:open-loom-smoke`; `open-loom` converts bundled
  command Markdown wrappers into `config.command` entries, and `opencode debug
  config` shows the resolved command config.
- Npm/local distribution: documented as package entry plus explicit local
  `file://` plugin entry for cloned repos. Local package-root validation now
  proves OpenCode can resolve the repository root through `package.json`.
- Npm package readiness: `package.json` now uses name `open-loom`, version
  `0.1.0`, author `z3z1ma`, repository metadata, `engines.opencode:
  >=1.14.22 <2`, `license: UNLICENSED`, `examples/` in the npm file list, and
  local release helper scripts. `npm view` showed both `open-loom` and
  `@z3z1ma/open-loom` were unpublished at check time. `npm run pack:check`
  succeeds after the metadata fixes.
- Npm pre-publish readiness: `npm whoami` returns `z3z1ma`; `npm publish
  --dry-run --access public` succeeds; `npm view open-loom name version --json`
  returns `E404`, confirming the package name remains available immediately
  before real publication.
- Npm publication: `open-loom@0.1.0` is published on npm; `latest` points at
  `0.1.0`, with `engines.opencode: >=1.14.22 <2` and `license: UNLICENSED`.
- Normal OpenCode package config: repo-root `opencode.json` with
  `plugin: ["open-loom@0.1.0"]` loads the published package from OpenCode's
  package cache and exposes package commands and skills.
- Cold-cache caveat: isolated first-run config-file validation can log
  `NpmInstallFailedError` and omit Loom surfaces; a second run in the same
  OpenCode cache succeeds and exposes instructions, skills, and commands. Treat
  this as an OpenCode npm-plugin installer quirk unless further investigation
  proves a package-side fix.
- Git URL specs: recorded as unsupported for current OpenCode practice and not a
  recommended install path.
- Runtime OpenCode loading: validated for local `file://` plugin loading through
  `OPENCODE_CONFIG_CONTENT`, resolved config mutation, and skill discovery with
  OpenCode CLI `1.14.22`. A paid model request or interactive TUI session has not
  been run.

# Execution Notes

OpenCode facts to preserve from research:

- global config lives at `~/.config/opencode/opencode.json`
- official docs show plugin array examples with npm package strings such as
  `opencode-helicone-session` and `@my-org/custom-plugin`
- official docs load local JS/TS plugins from `.opencode/plugins/` and
  `~/.config/opencode/plugins/`
- source-level config plugin entries may be a string or `[string, options]`
- source-level path plugins include `file://`, relative paths, and absolute paths
- source-level non-path plugin specs are passed through npm-style resolution
- source-level tests cover Git URL parsing, but operator validation found current
  OpenCode does not support Git URL plugin installs in practice
- viable distribution paths are npm publication and local file/path plugin entries
- `experimental.chat.system.transform` can mutate system prompt strings, but the
  corrected `open-loom` route uses the documented `instructions` config surface
  through the plugin `config(config)` hook instead
- no first-class plugin `skill` or `command` registration field was found in the
  inspected `Hooks` interface; `open-loom` uses `config.skills.paths` and
  `config.command` instead

Open validation questions:

- Can a plugin package ship `rules/`, `skills/`, and `commands/` directories and
  read them relative to `import.meta.url`?
- Can `Hooks.config` mutate in-memory `instructions`, `command`, or skill-related
  config in a supported way, and is that hook actually invoked in the right phase?
  Answer from current evidence: yes for OpenCode `1.14.22`.
- Is there any OpenCode API for plugin-bundled skills, or is upstream feature work
  required? Current route: `config.skills.paths`.
- Is there any OpenCode API for plugin-bundled commands, or must commands remain
  config/file based? Current route: `config.command`.
- What npm package layout keeps Loom's Markdown files bundled and readable without
  making package-generated files the canonical source?
- What exact local-path plugin entry should a user use after cloning this repo?

# Blockers

No implementation blocker. Residual acceptance risk: OpenCode `1.14.22` can log
`NpmInstallFailedError` on the first cold-cache npm-plugin config-file run, then
load the cached package correctly on the second run.

# Next Move / Next Route

Decide whether to accept the cold-cache first-run OpenCode npm-plugin quirk as a
documented residual risk or create a follow-up investigation/fix ticket. If
accepted, this ticket is close-ready.

# Ralph Readiness

Bounded iteration:
Build the smallest `open-loom` fixture that reads bundled files and attempts to
expose rules, skills, and commands through plugin APIs. Validate npm package and
local file/path plugin entry shapes, and record which parts need fallback direct
config install.

Write boundary:
OpenCode plugin fixture/package paths, `INSTALL.md` only if a proven doc update is
small and truthful, `examples/adapters/` if used for fixtures, this ticket, and
research/evidence records. `scripts/install-loom.sh` should remain unchanged
unless validation proves a small fallback adjustment is required.

Likely verification posture:
Observation-first. Use a temporary config directory or temporary `HOME`, run
OpenCode plugin loading if available, and inspect plugin-visible behavior. If
runtime OpenCode validation cannot be run, record structural evidence and the
remaining runtime risk.

Expected output contract:
Changed files, plugin fixture summary, plugin spec validation results,
rule/skill/command API findings, direct fallback requirements, limitations, and
ticket state recommendation.

# Evidence

Expected evidence:

- source-backed API summary for plugin `Hooks` and plugin spec parsing
- structural inspection of any plugin fixture/package
- runtime or structural validation that bundled files are readable
- runtime or structural validation for OpenCode plugin `config(config)` mutation
- explicit result for skill exposure: first-class API, fallback, or upstream gap
- explicit result for command exposure: first-class API, fallback, or upstream gap
- explicit npm package layout and local file/path plugin entry recommendation
- explicit note that Git URL plugin specs are unsupported for current OpenCode
- `git diff --check`
- OpenCode runtime limitation if validation cannot exercise a real model request

Observed evidence:

- `evidence:open-loom-smoke` records OpenCode `v1.14.22` source inspection,
  local smoke checks, import-based config-hook validation, isolated `opencode
  debug config`, isolated `opencode debug skill`, package-root plugin validation,
  `npm run pack:check`, `git diff --check`, `npm whoami`, `npm publish --dry-run`,
  and `npm view open-loom`. The evidence supports
  module-relative reads, ordered `config.instructions`, `config.skills.paths`,
  `config.command`, local `file://` plugin loading, local package-root plugin
  loading, package dry-run contents, npm auth as `z3z1ma`, and the package name
  being published as `open-loom@0.1.0`. It also records the cold-cache first-run
  `NpmInstallFailedError` caveat and second-run success.

# Critique Disposition

Risk class: medium

Critique policy: recommended

Policy rationale:
This ticket may change the OpenCode install strategy from transparent direct file
copying to plugin-driven behavior. Review should focus on operator clarity,
whether experimental hooks are acceptable, and whether fallback requirements are
communicated honestly.

Required critique profiles:

- operator-clarity

Findings:

Open findings:

None.

Resolved findings:

- `critique:open-loom-review#FIND-002` - Optional command surface
  was treated as present by helper discovery. Resolved by making bundle
  inspection tolerate missing `commands/` and `skills/` directories and validating
  a temporary no-commands bundle returns `commandCount: 0`.
- `critique:open-loom-config-hook-review#FIND-001` - OpenCode compatibility range
  was missing. Resolved with `engines.opencode: >=1.14.22 <2` and docs updates.
- `critique:open-loom-config-hook-review#FIND-002` - Package-root validation was
  missing from evidence. Resolved by recording local package-root `opencode debug
  config` validation.
- `critique:open-loom-config-hook-review#FIND-003` - Published docs pointed at
  omitted examples. Resolved by adding `examples/` to the npm package file list.
- `critique:open-loom-config-hook-review#FIND-004` - Install docs still said
  package metadata was private. Resolved by replacing that wording.
- `critique:open-loom-config-hook-review#FIND-005` - License metadata was absent.
  Resolved conservatively with `license: UNLICENSED`.

Disposition status: prior findings resolved; complete pending acceptance

Deferral / not-required rationale:

None.

# Wiki Disposition

Wiki promotion is optional. Promote only if OpenCode establishes a reusable
plugin-first adapter pattern or an important null result about plugin API limits.

# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks: OpenCode `1.14.22` cold-cache npm-plugin config-file run may log
`NpmInstallFailedError` before a second run loads the cached package correctly.

# Dependencies

Uses `research:loom-install-distribution-methods` and prior direct OpenCode
install proof from `ticket:ffg8elkb`. No hard ticket prerequisite blocks starting
this work.

# Journal

- 2026-04-25: created as the OpenCode harness ticket under
  `plan:install-experience-harness-adapters`.
- 2026-04-25: reframed from direct-config hardening to plugin-first investigation
  after operator clarified the ideal OpenCode UX and source-level research showed
  plugin APIs worth validating but not yet proven for bundled skills/commands.
- 2026-04-25: operator checked current OpenCode Git URL behavior and found it is
  not supported. Updated the ticket to treat npm publication as the normal plugin
  distribution path and local file/path entries from a cloned repo as the manual
  path.
- 2026-04-25: moved to active and compiled Ralph packet
  `packet:ralph-ticket-6uy1rx20-20260425T195559Z` for the first OpenCode plugin
  validation iteration.
- 2026-04-25: consumed `packet:ralph-ticket-6uy1rx20-20260425T195559Z`. Added a
  private root package plugin, `open-loom.mjs`, fixture notes, and `INSTALL.md`
  guidance. Parent corrected the plugin to match
  OpenCode's default-object `server()` and `output.system` mutation shape,
  recorded `evidence:open-loom-smoke`, and moved the ticket to
  `review_required` for recommended operator-clarity critique.
- 2026-04-25: ran `opencode plugin file://... --global` under a temporary `HOME`
  with OpenCode CLI `1.14.22`; OpenCode detected `open-loom` as a server target
  and wrote the expected local plugin entry. Chat/TUI hook invocation remains
  unvalidated.
- 2026-04-25: completed recommended critique
  `critique:open-loom-review`. Medium finding
  `critique:open-loom-review#FIND-001` remains open and blocks final acceptance.
  Low finding `critique:open-loom-review#FIND-002`
  was resolved by making helper discovery tolerate missing optional command
  surfaces. Ticket moved back to `active` for runtime validation or wording
  softening.
- 2026-04-25: renamed the OpenCode plugin artifact and package identity to
  `open-loom`; entrypoint is now `open-loom.mjs`, package/plugin id is
  `open-loom`, fixture docs moved to `examples/adapters/open-loom-install/`, and
  evidence/critique references were reconciled to the new names.
- 2026-04-25: prepared `open-loom@0.1.0` package metadata for npm publication
  under author `z3z1ma`, added local release helper scripts, ignored project-local
  `.npmrc`, verified `open-loom` and `@z3z1ma/open-loom` were unpublished, and ran
  `npm run pack:check`. Publishing remains blocked until local `npm login`
  succeeds; the pasted token was treated as exposed and was not persisted.
- 2026-04-25: after operator review found the chat-transform-only implementation
  was not acceptable, inspected OpenCode `v1.14.22` source and docs, replaced
  `open-loom` with a `config(config)` implementation that registers rules through
  `config.instructions`, skills through `config.skills.paths`, and commands
  through `config.command`, and recorded updated validation in
  `evidence:open-loom-smoke`.
- 2026-04-25: completed focused config-hook/package readiness review in
  `critique:open-loom-config-hook-review`. Resolved findings by adding
  `engines.opencode: >=1.14.22 <2`, documenting the minimum OpenCode range,
  adding `examples/` to the npm file list, replacing stale private-package
  wording, adding `license: UNLICENSED`, recording package-root OpenCode
  validation, and rerunning `node open-loom.mjs --smoke`, package-root
  `opencode debug config`, clean-project `opencode debug skill`,
  `npm run pack:check`, and `git diff --check`.
- 2026-04-25: ran final non-publishing npm checks: `npm whoami` returned
  `z3z1ma`, `npm publish --dry-run --access public` succeeded, and `npm view
  open-loom name version --json` returned `E404` because the package is still
  unpublished. Real publication is pending explicit operator approval.
- 2026-04-25: operator chose not to publish yet. Ticket moved to
  `complete_pending_acceptance`: implementation, evidence, critique, and
  pre-publish checks are complete; real npm publication remains paused.
- 2026-04-25: operator attempted real publication. Npm returned `E403` because
  two-factor authentication or a granular bypass-2FA token is required to publish.
  Ticket moved to `blocked`; implementation remains ready, but publication needs
  a valid OTP or token path.
- 2026-04-25: operator reported successful publication after satisfying npm's
  security requirement. Verified `open-loom@0.1.0` on npm, validated repo-root
  `opencode.json` package loading from OpenCode's package cache, and recorded the
  isolated cold-cache first-run npm-plugin installer caveat. Ticket moved to
  `complete_pending_acceptance` pending accepted-risk or follow-up disposition.
