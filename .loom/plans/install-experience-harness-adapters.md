---
id: plan:install-experience-harness-adapters
kind: plan
status: active
created_at: 2026-04-25T18:46:08Z
updated_at: 2026-04-26T07:23:57Z
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
    - research:codex-plugin-distribution-surfaces
  spec:
    - spec:opencode-plugin-install-contract
  wiki:
    - wiki:harness-adapter-package-pattern
  ticket:
    - ticket:3t93tsci
    - ticket:7ex8w32y
    - ticket:q7h1d05q
    - ticket:cldrel01
    - ticket:jt2vy25y
  decision:
    - decision:0005
    - decision:0006
  related:
    - ticket:lx9nnztk
    - ticket:6uy1rx20
    - ticket:us1brnsv
  evidence:
    - evidence:open-loom-smoke
    - evidence:cursor-harness-install-validation
    - evidence:claude-plugin-hybrid
    - evidence:claude-sessionstart-stdout-context
    - evidence:codex-sessionstart-stdout-context
  critique:
    - critique:codex-plugin-hook-config-review
---

# Purpose

Sequence the install-experience initiative into one bounded ticket per supported
harness so Loom uses harness-native skill or plugin package paths instead of a
cross-harness installer.

After `decision:0006`, this plan no longer preserves fallback installers. The
target is native exposure of the canonical `skills/` package, with optional
`loom-bootstrap` preload where a harness supports it cleanly.

# Strategy

Use the research recommendation as the route:

1. Treat `skills/` as the primary package surface, with `loom-bootstrap` as the
   mandatory entry skill.
2. Use harness prototypes to establish adapter-package conventions: bootstrap
   reference preloading when supported, source markers, fixture layout, validation
   evidence, and disable expectations.
3. Apply that adapter-package discipline to Claude Code, Codex, OpenCode, Gemini,
   and Cursor without making always-on adapter preload the only completeness path.
4. Keep optional always-on hooks or instruction files as boosts over the same
   `loom-bootstrap` references, not separate doctrine.
5. Reconcile `INSTALL.md` and adapter fixtures after the per-harness decisions are
   proven.

The plan should not swallow live execution truth. Each ticket owns its own
implementation state, evidence, critique disposition, and acceptance decision.

# Strategy Snapshot

Current strategic picture:

- `decision:0005` and `decision:0006` define the install strategy: Loom is a
  skills package with `loom-bootstrap` as the mandatory first skill, and `skills/`
  is the only product surface.
- Claude Code has an accepted automated boost adapter: `.claude-plugin/plugin.json`
  exposes canonical `skills/`, `.claude-plugin/marketplace.json`
  exposes marketplace `agent-loom`, and `claude-hooks/hooks.json` emits `loom-bootstrap`
  references as same-session, source-marked `SessionStart` stdout. Remaining
  Claude release risks are installed marketplace behavior, package/cache contents,
  Windows shell behavior, `clear|compact` runtime events, and installed skill
  invocation.
- Codex can now use the same skills-package story: `.codex-plugin/plugin.json`
  exposes `loom-bootstrap` and the subsystem skills, while `.codex/hooks.json`
  remains an optional trusted-project preload proof. The next Codex evidence need
  is installed plugin skill discovery, not plugin-owned hook support.
- OpenCode is the first accepted adapter-package result. `open-loom@0.1.0` uses
  the plugin `config(config)` hook to register bootstrap references through
  `config.instructions` and skills through `config.skills.paths`. The cold-cache
  npm-plugin first-run caveat is tracked separately by `ticket:us1brnsv`.
- Generic Agent Skills are now the main cross-harness package shape where a
  harness supports them.
- Adapter outputs must remain derivative from canonical `skills/`, especially
  `loom-bootstrap`.

# Workstreams

Complete package prototypes:

- `ticket:3t93tsci` - prototype Cursor plugin install package
- `ticket:7ex8w32y` - prototype Gemini CLI extension install package

Hybrid package prototypes:

- `ticket:q7h1d05q` - prototype Claude Code hybrid install path: plugin for
  skills plus hook-delivered bootstrap context
- `ticket:cldrel01` - proposed release-packaging hardening for Claude marketplace
  distribution beyond the accepted local/prototype integration
- `ticket:lx9nnztk` - blocked Codex remote plugin install investigation

Accepted OpenCode plugin-first package:

- `ticket:6uy1rx20` - closed after publishing and accepting the `open-loom`
  OpenCode plugin install path
- `ticket:us1brnsv` - follow-up investigation for OpenCode cold-cache npm-plugin
  first-run behavior

Shared follow-through inside the harness tickets:

- document why the chosen harness mechanism is native
- preserve source markers in generated adapter outputs
- validate install or package structure under a temporary home or fixture root
- keep uninstall, disable, or cleanup behavior explicit
- update `INSTALL.md` only when a harness decision is evidenced

# Milestones

1. Cursor plugin and Gemini extension prototypes produce a concrete adapter
   package shape that exposes `skills/` without direct user-rule mutation.
2. Claude and Codex tickets decide how plugin packaging exposes `loom-bootstrap`
   and whether optional hook preload should remain part of the adapter evidence.
3. OpenCode plugin-first ticket proves the ideal plugin-array install shape, using
   npm publication for normal users and local file/path plugins for cloned-repo
   installs, while documenting the cold-cache npm-plugin first-run caveat as
   follow-up work.
4. The public install docs distinguish user-global install, project-local
   adoption, and adapter-package development.
5. Removed fallback installer and command-wrapper assumptions stay removed from
   package docs and examples.

# Sequencing

Cursor and Gemini come first because their first-class package systems appear to
cover skills and optional context preload. They are the best proving ground for
native adapter package discipline.

Claude and Codex come next because they need the same packaging discipline with an
explicit split between plugin-delivered skills and optional hook- or
instruction-delivered bootstrap preload.

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
  scope: Cursor adapter package or fixture files, Cursor-related docs
  updates, and linked Loom ticket/evidence updates. It should not edit canonical
  `skills/` except to record a source bug in a follow-up.
- `ticket:7ex8w32y` - Gemini CLI extension install prototype. Expected child
  write scope: Gemini extension package or fixture files, Gemini-related
  installer/docs updates, and linked Loom ticket/evidence updates. It should not
  edit Cursor adapter files.

Wave 2:

- `ticket:q7h1d05q` - Claude Code hybrid install prototype. Expected child write
  scope: Claude adapter package or fixture files, Claude-specific install docs,
  and linked Loom ticket/evidence updates.
- `ticket:lx9nnztk` - Codex remote plugin install investigation. Expected child
  write scope: Codex plugin or marketplace fixture files, Codex hook config proof
  files, Codex-specific install docs, and linked Loom ticket/evidence updates. Do
  not present project-local hooks as the normal remote product path.

Wave 3:

- `ticket:6uy1rx20` - `open-loom` OpenCode plugin-first install validation.
  Expected child write scope: OpenCode plugin fixture/package files,
  OpenCode-specific docs, source-backed research updates, and this
  ticket/evidence records.

# Risks

- Plugin-first enthusiasm could hide the fact that agents still need to use
  `loom-bootstrap` first.
- Generated adapter outputs could become stale copies of canonical bootstrap
  references or skills.
- A shared `~/.agents/skills` destination could reduce duplication but create
  surprising precedence behavior in harnesses that also have native skill roots.
- Cursor and Claude both have hook/plugin features that could tempt overpowered
  runtime behavior instead of simple static instruction install.
- Codex and Gemini instruction-size or context-loading limits could make a naive
  aggregate rule file less reliable than source-marked per-rule hook output or
  direct ordered file references.
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
- source-marker spot-checks showing adapter files point back to canonical Loom
  source surfaces
- a package or fixture structure check when a plugin/extension package is added
- `git diff --check`
- explicit note of any harness CLI or UI validation that could not be run

Additional evidence for plugin or extension tickets:

- manifest fields match the official harness reference
- bootstrap/context files preserve ordered Loom bootstrap loading when preloaded
- skills remain directories with `SKILL.md` and supporting files intact
- local link/install/disable commands are run when the harness CLI is available,
  or explicitly marked unvalidated when unavailable
- for OpenCode specifically, validate the npm package path and local file/path
  plugin path; record Git URL plugin specs as unsupported unless new upstream
  behavior appears

# Exit Criteria

This plan can complete when:

- each supported harness has a linked ticket with accepted implementation or an
  explicit accepted decision not to implement a first-class package path
- `INSTALL.md` explains the chosen per-harness native path without fallback
  installer instructions
- adapter fixtures or package outputs exist where they are the chosen path
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

When this plan is completed, record which harness tickets closed, which native
install paths were accepted, and where any deferred validation or marketplace
publishing work moved. Live progress and final acceptance remain in the linked
tickets, not in this plan.
