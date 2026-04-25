---
id: plan:install-experience-harness-adapters
kind: plan
status: active
created_at: 2026-04-25T18:46:08Z
updated_at: 2026-04-25T22:14:57Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:loom-install-experience
  research:
    - research:loom-install-distribution-methods
    - research:harness-install-surfaces
    - research:codex-command-skill-installation
  spec:
    - spec:opencode-plugin-install-contract
  wiki:
    - wiki:harness-adapter-package-pattern
  ticket:
    - ticket:3t93tsci
    - ticket:7ex8w32y
    - ticket:q7h1d05q
    - ticket:lx9nnztk
    - ticket:6uy1rx20
    - ticket:us1brnsv
  evidence:
    - evidence:open-loom-smoke
    - evidence:cursor-harness-install-validation
---

# Purpose

Sequence the install-experience initiative into one bounded ticket per supported
harness so Loom can move from a working proof installer toward harness-native,
first-class, reversible install paths.

This plan exists because the research outcome is explicitly not "keep making the
shell script longer." The current `Makefile` and `scripts/install-loom.sh` remain
useful proof and fallback surfaces, but the next work should test the best native
install class for each harness and record why each adapter shape is accepted or
rejected.

# Strategy

Use the research recommendation as the route:

1. Start with the two harnesses whose plugin or extension systems appear to cover
   all Loom surfaces: Cursor and Gemini CLI.
2. Use those prototypes to establish adapter-package conventions: generated rule
   files, generated command files, source markers, fixture layout, validation
   evidence, and uninstall or disable expectations.
3. Apply that adapter-package discipline to hybrid harnesses: Claude Code and
   Codex, where plugins are useful but always-on Loom rules still need a separate
   instruction surface.
4. Re-open OpenCode as a plugin-first investigation: the ideal user experience is
   a single `plugin` array entry, but the ticket must prove which plugin APIs can
   actually inject or register Loom rules, skills, and commands.
5. Reconcile `INSTALL.md`, adapter fixtures, and shell fallback behavior after
   the per-harness decisions are proven.

The plan should not swallow live execution truth. Each ticket owns its own
implementation state, evidence, critique disposition, and acceptance decision.

# Strategy Snapshot

Current strategic picture:

- Cursor plugins and Gemini CLI extensions are the strongest first-class package
  candidates because their docs show package support for rules or context,
  skills, and commands.
- Claude Code and Codex are likely hybrid installs because their plugin systems
  do not cleanly own always-on Loom rules in the fetched docs.
- OpenCode is the first accepted adapter-package result. `open-loom@0.1.0` is
  published and uses the plugin `config(config)` hook to register rules through
  `config.instructions`, skills through `config.skills.paths`, and commands
  through `config.command`. The cold-cache npm-plugin first-run caveat is tracked
  separately by `ticket:us1brnsv`.
- Generic Agent Skills may reduce duplicated skill installs for OpenCode, Codex,
  Gemini CLI, and Cursor, but they cannot replace ordered always-on rules.
- Adapter outputs must remain derivative from canonical `rules/`, `skills/`, and
  optional `commands/`.

# Workstreams

Complete package prototypes:

- `ticket:3t93tsci` - prototype Cursor plugin install package
- `ticket:7ex8w32y` - prototype Gemini CLI extension install package

Hybrid package prototypes:

- `ticket:q7h1d05q` - prototype Claude Code hybrid install path
- `ticket:lx9nnztk` - prototype Codex hybrid plugin install path

Accepted OpenCode plugin-first package:

- `ticket:6uy1rx20` - closed after publishing and accepting the `open-loom`
  OpenCode plugin install path
- `ticket:us1brnsv` - follow-up investigation for OpenCode cold-cache npm-plugin
  first-run behavior

Shared follow-through inside the harness tickets:

- document why the chosen harness mechanism is first-class or fallback
- preserve source markers in generated adapter outputs
- validate install or package structure under a temporary home or fixture root
- keep uninstall, disable, or cleanup behavior explicit
- update `INSTALL.md` only when a harness decision is evidenced

# Milestones

1. Cursor plugin and Gemini extension prototypes produce a concrete adapter
   package shape that preserves Loom's three surfaces without direct user-rule
   mutation.
2. Claude and Codex hybrid tickets decide how plugin packaging combines with
   always-on rule installation and explicit command adapters.
3. OpenCode plugin-first ticket proves the ideal plugin-array install shape, using
   npm publication for normal users and local file/path plugins for cloned-repo
   installs, while documenting the cold-cache npm-plugin first-run caveat as
   follow-up work.
4. The public install docs distinguish user-global install, project-local
   adoption, and adapter-package development.
5. The current shell installer is either simplified into a fallback/prototype
   helper or left clearly documented as a local adapter rather than the semantic
   center.

# Sequencing

Cursor and Gemini come first because their first-class package systems appear to
cover rules/context, skills, and commands. They are the best proving ground for
generated adapter package discipline.

Claude and Codex come next because they need the same packaging discipline but
with an explicit split between plugin-delivered skills/commands and separately
installed always-on rules.

OpenCode can proceed as soon as the plugin-first investigation is useful. It may
need narrower validation before the shared skill-location decision, because the
ideal outcome is not a copied skill directory but a plugin that registers or
exposes bundled Loom surfaces through OpenCode APIs.

This order is recommended, not a hidden hard dependency. If a harness changes
docs or a user need makes one ticket urgent, the ticket can move independently as
long as its own scope and evidence remain truthful.

# Execution Waves

Wave 1:

- `ticket:3t93tsci` - Cursor plugin install prototype. Expected child write
  scope: Cursor adapter package or fixture files, Cursor-related installer/docs
  updates, and linked Loom ticket/evidence updates. It should not edit canonical
  `rules/`, `skills/`, or `commands/` except to record a source bug in a follow-up.
- `ticket:7ex8w32y` - Gemini CLI extension install prototype. Expected child
  write scope: Gemini extension package or fixture files, Gemini-related
  installer/docs updates, and linked Loom ticket/evidence updates. It should not
  edit Cursor adapter files.

Wave 2:

- `ticket:q7h1d05q` - Claude Code hybrid install prototype. Expected child write
  scope: Claude adapter package or fixture files, Claude-specific install docs,
  shell fallback changes only if needed, and linked Loom ticket/evidence updates.
- `ticket:lx9nnztk` - Codex hybrid plugin install prototype. Expected child write
  scope: Codex plugin or marketplace fixture files, generated command-adapter
  skill logic if needed, Codex-specific install docs, and linked Loom
  ticket/evidence updates.

Wave 3:

- `ticket:6uy1rx20` - `open-loom` OpenCode plugin-first install validation.
  Expected child write scope: OpenCode plugin fixture/package files,
  OpenCode-specific docs, source-backed research updates, and this
  ticket/evidence records. Fallback direct installer changes should wait until
  the plugin API limits are proven.

# Risks

- Plugin-first enthusiasm could hide the fact that a harness plugin does not load
  ordered always-on Loom rules.
- Generated adapter outputs could become stale copies of canonical rules, skills,
  or commands.
- A shared `~/.agents/skills` destination could reduce duplication but create
  surprising precedence behavior in harnesses that also have native skill roots.
- Cursor and Claude both have hook/plugin features that could tempt overpowered
  runtime behavior instead of simple static instruction install.
- Codex and Gemini instruction-size or context-loading limits could make a naive
  aggregate rule file less reliable than direct ordered file references.
- Marketplace package work could expand into release engineering before local
  package fixtures prove the adapter shape.
- OpenCode's npm-plugin install cache can log a first-run `NpmInstallFailedError`
  before resolving the cached package on a second run; `ticket:us1brnsv` owns that
  residual risk.
- OpenCode does not currently support Git URL plugin installs, so the user-facing
  plugin distribution path must be an npm package; local clone users can point
  `plugin` at a file or local path.

# Evidence Strategy

Each harness ticket should produce evidence appropriate to its install class.

Minimum evidence for all tickets:

- structural diff review for changed adapter files and docs
- source-marker spot-checks showing generated files point back to canonical Loom
  source surfaces
- a temporary `HOME` install/uninstall check when `scripts/install-loom.sh` or
  direct user config mutation changes
- a package or fixture structure check when a plugin/extension package is added
- `git diff --check`
- explicit note of any harness CLI or UI validation that could not be run

Additional evidence for plugin or extension tickets:

- manifest fields match the official harness reference
- rule/context files preserve ordered always-on Loom rule loading
- skills remain directories with `SKILL.md` and supporting files intact
- command adapters remain explicit invocation surfaces
- local link/install/disable commands are run when the harness CLI is available,
  or explicitly marked unvalidated when unavailable
- for OpenCode specifically, validate the npm package path and local file/path
  plugin path; record Git URL plugin specs as unsupported unless new upstream
  behavior appears

# Exit Criteria

This plan can complete when:

- each supported harness has a linked ticket with accepted implementation or an
  explicit accepted decision not to implement a first-class package path
- `INSTALL.md` explains the chosen per-harness path without making the shell
  script the only source of install truth
- adapter fixtures or package outputs exist where they are the chosen path
- direct fallback behavior remains reversible and clearly marked as Loom-managed
- ticket evidence records or ticket evidence sections support the claims made for
  each harness
- recommended critique has been completed, deferred with rationale, or marked not
  required by each ticket's acceptance gate
- no generated adapter output is treated as canonical Loom semantics

# Retrospective Notes

- `open-loom@0.1.0` established the first accepted package-adapter pattern in
  this plan.
- Future Cursor, Gemini, Claude, and Codex work should reuse the validation
  lessons captured in `wiki:harness-adapter-package-pattern` without assuming
  their harness APIs match OpenCode.
- `spec:opencode-plugin-install-contract` owns the accepted OpenCode behavior
  contract; do not keep redefining it in ticket prose.

# Completion Basis

When this plan is completed, record which harness tickets closed, which install
paths were accepted, which package or fallback surfaces remain, and where any
deferred validation or marketplace publishing work moved. Live progress and final
acceptance remain in the linked tickets, not in this plan.
