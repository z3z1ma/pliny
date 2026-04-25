---
id: initiative:loom-install-experience
kind: initiative
status: active
created_at: 2026-04-25T18:25:20Z
updated_at: 2026-04-25T22:14:57Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  plan:
    - plan:install-experience-harness-adapters
  research:
    - research:loom-install-distribution-methods
    - research:harness-install-surfaces
    - research:codex-command-skill-installation
  spec:
    - spec:opencode-plugin-install-contract
  wiki:
    - wiki:harness-adapter-package-pattern
  ticket:
    - ticket:6uy1rx20
    - ticket:us1brnsv
    - ticket:q7h1d05q
    - ticket:lx9nnztk
    - ticket:7ex8w32y
    - ticket:3t93tsci
    - ticket:ffg8elkb
    - ticket:p9m4x2qt
    - ticket:rd48g1kg
  evidence:
    - evidence:open-loom-smoke
    - evidence:cursor-harness-install-validation
---

# Objective

Make Loom installation feel first-class in every supported harness while keeping
the product itself a Markdown-native protocol bundle rather than a runtime,
daemon, MCP, dashboard, or monolithic product CLI.

The outcome is not merely a nicer shell script. The desired result is a clear,
maintainable install strategy that maps Loom's canonical `rules/`, `skills/`,
and optional `commands/` surfaces into each harness through the most honest
native mechanism available.

# Why Now

The current `Makefile` and `scripts/install-loom.sh` proved that a user-level
global install is possible across OpenCode, Claude Code, Codex, Gemini CLI, and
Cursor. That proof is valuable, but it is also visibly a means-to-an-end:

- it encodes harness knowledge in one long shell script
- it mutates several single-file instruction surfaces with generated managed
  blocks
- it has to generate command adapters where harness command formats differ
- it relies on implementation details such as Cursor User Rules storage
- it does not distinguish first-class plugin or extension systems from direct
  config-copy fallbacks

Meanwhile, several harnesses now expose richer first-class distribution systems:
Claude Code plugins, Codex plugins, Gemini CLI extensions, Cursor plugins, and
portable Agent Skills. Loom needs to decide which of those should become the
preferred install surface, where direct managed config remains necessary, and
how to keep the protocol source of truth independent from adapter convenience.

# In Scope

- compare supported harness install surfaces for OpenCode, Claude Code, Codex,
  Gemini CLI, and Cursor
- evaluate first-class plugin, extension, marketplace, and Agent Skills surfaces
  where they exist
- evaluate direct user-level config installs, project-local installs, and generic
  `~/.agents/skills` installs
- compare popular installer precedents such as package managers, standalone
  shell installers, project scaffolders, extension marketplaces, and manual Git
  clone/link workflows
- define the qualities of a better Loom install experience without committing to
  an implementation prematurely
- keep current installer behavior available as prior evidence and a fallback
  adapter, not as the strategic endpoint

# Out Of Scope

- creating a required `loom` CLI
- adding a daemon, service, model router, MCP server, dashboard, or hidden
  installer runtime as protocol core
- changing Loom's canonical shipped product surfaces to fit one harness better
- making optional commands part of Loom core
- treating plugin manifests, generated adapter files, or package-manager recipes
  as owners of Loom semantics
- installing dogfooding `.loom/` records or `.opencode/` consumption state into
  downstream users

# Success Metrics

- a future maintainer can explain the recommended install path for each supported
  harness without rereading `scripts/install-loom.sh`
- each supported harness has a documented preferred install mechanism and a
  fallback mechanism when the preferred mechanism cannot express all Loom
  surfaces
- first-class plugin or extension systems are used where they cleanly cover Loom
  rules, skills, and command wrappers, and explicitly rejected where they do not
- always-on Loom rules remain always-on after install and preserve numeric rule
  order
- skill discovery preserves portable Agent Skills semantics and keeps full skill
  content on-demand
- optional command wrappers remain explicit adapter surfaces rather than a second
  protocol owner
- install and uninstall mutate only Loom-managed files or marked blocks
- adapter outputs are easy to inspect with ordinary filesystem tools
- no install strategy makes the shell script, a generated file, or a marketplace
  package the authority for Loom behavior

# Milestones

1. Preserve broad install-method research that compares native harness surfaces,
   plugin systems, and installer precedents.
2. Decide the preferred install class for each supported harness: plugin or
   extension package, direct config install, generic Agent Skills install, or a
   hybrid.
3. Define adapter fixture expectations for each chosen path so install behavior
   can be reviewed without relying on transcript context.
4. Refactor or replace the current Makefile/script only after the preferred
   per-harness strategy is explicit.
5. Update `INSTALL.md`, adapter examples, and any wrapper guidance to reflect the
   chosen strategy.

# Dependencies

- `constitution:main`, especially the constraints against a monolithic Loom CLI,
  hidden runtime, and helper-owned ontology
- `research:loom-install-distribution-methods` for broad install-surface and
  installer-precedent analysis
- `research:harness-install-surfaces` for the earlier concrete path mapping
- `research:codex-command-skill-installation` for the Codex command adapter
  decision
- `ticket:ffg8elkb`, `ticket:p9m4x2qt`, and `ticket:rd48g1kg` for prior
  implementation and validation history
- current official harness docs, because plugin and skill surfaces are changing
  quickly

# Risks

- overcorrecting from a fragile script into a hidden runtime or product CLI that
  violates Loom's constitutional boundary
- choosing plugin packaging because it feels more first-class even when it does
  not provide a clean always-on instruction surface
- letting generated adapter packages drift from canonical `rules/`, `skills/`,
  and `commands/`
- losing uninstall safety when a harness stores user rules in a non-file config
  database or managed settings surface
- treating generic Agent Skills as sufficient for Loom install even though Loom
  also requires ordered always-on rules
- expanding install support faster than the project can maintain evidence for
  each harness

# Linked Work

- Plan: `plan:install-experience-harness-adapters`
- Research: `research:loom-install-distribution-methods`
- Prior research: `research:harness-install-surfaces`
- Prior research: `research:codex-command-skill-installation`
- Harness ticket: `ticket:6uy1rx20` - validate `open-loom` OpenCode plugin-first install
- Follow-up ticket: `ticket:us1brnsv` - investigate OpenCode cold-cache
  npm-plugin first-run behavior
- Spec: `spec:opencode-plugin-install-contract`
- Wiki: `wiki:harness-adapter-package-pattern`
- Harness ticket: `ticket:q7h1d05q` - prototype Claude Code hybrid install
- Harness ticket: `ticket:lx9nnztk` - prototype Codex hybrid plugin install
- Harness ticket: `ticket:7ex8w32y` - prototype Gemini CLI extension install
- Harness ticket: `ticket:3t93tsci` - prototype Cursor plugin install
- Prior ticket: `ticket:ffg8elkb` - add global harness install Makefile
- Prior ticket: `ticket:p9m4x2qt` - install Codex command adapters as skills
- Prior ticket: `ticket:rd48g1kg` - add Cursor harness install support
- Prior evidence: `evidence:cursor-harness-install-validation`

# Status Summary

This initiative is active. The repository has a working proof installer and a
new execution plan for harness-specific install work. The OpenCode slice has
landed the first accepted package-adapter result: `open-loom@0.1.0` is published
and validates a plugin-array install for OpenCode `>=1.14.22 <2`. The remaining
OpenCode cold-cache first-run installer caveat is tracked by `ticket:us1brnsv`.

# Completion Basis

When this initiative is completed, the graph should show a researched,
per-harness install strategy and any resulting implementation tickets should
have evidence that install and uninstall are reversible, harness-appropriate,
and still subordinate to Loom's Markdown protocol corpus.
