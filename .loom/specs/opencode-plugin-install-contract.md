---
id: spec:opencode-plugin-install-contract
kind: spec
status: active
created_at: 2026-04-25T22:14:57Z
updated_at: 2026-04-25T22:14:57Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:loom-install-experience
  plan:
    - plan:install-experience-harness-adapters
  ticket:
    - ticket:6uy1rx20
    - ticket:us1brnsv
  evidence:
    - evidence:open-loom-smoke
  critique:
    - critique:open-loom-config-hook-review
  research:
    - research:loom-install-distribution-methods
external_refs:
  opencode_docs:
    - https://opencode.ai/docs/plugins/
    - https://opencode.ai/docs/config/
    - https://opencode.ai/docs/skills/
    - https://opencode.ai/docs/commands/
---

# Summary

Define the accepted behavior contract for the OpenCode `open-loom` install path.

This contract applies to OpenCode `>=1.14.22 <2`, matching the published package
metadata for `open-loom@0.1.0`.

# Problem

OpenCode originally had a direct-copy install path: copy rules, skills, and
commands into OpenCode config roots and add instruction paths manually. The
accepted product direction is better when a normal user can add one OpenCode
plugin entry and let the package expose Loom's bundled Markdown surfaces without
creating a second semantic source of truth.

# Desired Behavior

A normal OpenCode user should be able to configure Loom by adding
`open-loom@0.1.0` or a compatible future `open-loom` package version to
OpenCode's `plugin` array.

When OpenCode loads the plugin, `open-loom` should expose the package's canonical
Markdown surfaces through OpenCode's documented config surfaces:

- ordered rule files through `config.instructions`
- bundled skills through `config.skills.paths`
- optional command wrappers through `config.command`

Users who clone the repository should be able to point OpenCode at a local file or
package-root plugin path instead of installing from npm.

# Constraints

- `rules/`, `skills/`, and optional `commands/` remain the source package
  surfaces; package metadata and plugin registration do not own Loom semantics.
- The plugin must read bundled files relative to the package or clone location,
  not from dogfooding `.opencode/` or `.loom/` paths.
- Git URL plugin specs are not a supported recommendation for OpenCode because
  current validation found them unsupported in practice.
- The published package must declare the OpenCode compatibility range it was
  validated against.
- Cold-cache first-run npm-plugin behavior is a known OpenCode `1.14.22`
  limitation until `ticket:us1brnsv` resolves it.

# Requirements

- REQ-001: The npm package entrypoint is `open-loom.mjs` and default-exports an
  OpenCode plugin object with `id: "open-loom"` and `server()`.
- REQ-002: The plugin registers ordered top-level `rules/*.md` files as absolute
  `config.instructions` paths.
- REQ-003: The plugin registers the bundled `skills/` root in
  `config.skills.paths` when bundled skills exist.
- REQ-004: The plugin registers bundled Markdown command wrappers in
  `config.command` when bundled commands exist.
- REQ-005: Missing optional `commands/` must not make bundle inspection or config
  registration fail.
- REQ-006: Local clone usage supports a `file://.../open-loom.mjs` or local
  package-root plugin entry.
- REQ-007: The package declares `engines.opencode: >=1.14.22 <2` unless newer
  evidence changes the compatibility contract.
- REQ-008: Install documentation rejects Git URL plugin specs as the normal
  OpenCode path unless future runtime evidence proves support.
- REQ-009: Published package contents include the plugin, rules, skills, optional
  commands, install docs, and adapter examples needed by the install guide.

# Scenarios

- Npm package user adds `"plugin": ["open-loom@0.1.0"]` to an OpenCode config
  file and OpenCode loads Loom rules, skills, and commands from its package cache.
- Repository clone user points OpenCode at `file:///path/to/agent-loom/open-loom.mjs`
  and OpenCode loads the same Loom surfaces from the clone.
- Contributor runs `node open-loom.mjs --smoke` to verify ordered rules, skill
  path registration, command registration, and dedupe behavior without making a
  model request.
- A package without optional commands still registers rules and skills without
  crashing.
- A first cold-cache npm-package run logs `NpmInstallFailedError`; the user runs
  OpenCode again and the cached package resolves. Further investigation belongs to
  `ticket:us1brnsv`.

# Acceptance

- ACC-001: `node open-loom.mjs --smoke` shows seven ordered rule files, a bundled
  skill path, and command registration including `loom-plan`.
- ACC-002: `opencode debug config` with a local plugin file or package-root entry
  shows ordered Loom rule paths in `instructions`, a Loom `skills.paths` entry,
  and Loom command wrappers in `command`.
- ACC-003: `opencode debug skill` discovers Loom skills from the registered
  OpenCode skill path.
- ACC-004: `npm run pack:check` confirms the package dry-run includes all
  published support surfaces used by the install docs.
- ACC-005: `npm view open-loom name version dist-tags engines license --json`
  confirms the published package metadata.
- ACC-006: The ticket acceptance gate records any known OpenCode runtime caveat
  as accepted risk or a linked follow-up before closing the OpenCode ticket.

# Open Questions

- Is the cold-cache first-run `NpmInstallFailedError` caused by OpenCode's npm
  installer, package metadata, config-file load timing, or another factor?
- Should future `open-loom` package versions keep examples in the published
  tarball or move adapter fixture details into external docs once package install
  stabilizes?
- Should `open-loom` eventually support additional OpenCode versions outside
  `>=1.14.22 <2`?
