---
id: ticket:3t93tsci
kind: ticket
status: closed
change_class: release-packaging
risk_class: medium
created_at: 2026-04-25T18:46:08Z
updated_at: 2026-04-28T18:50:38Z
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
  evidence:
    - evidence:cursor-harness-install-validation
  related:
    - ticket:rd48g1kg
external_refs:
  cursor_docs:
    - https://cursor.com/docs/rules
    - https://cursor.com/docs/skills
    - https://cursor.com/docs/plugins
    - https://cursor.com/docs/reference/plugins
depends_on: []
---

# Summary

Prototype a Cursor plugin install path for Loom that packages rules, skills, and
optional commands through Cursor's documented plugin system instead of relying on
direct Cursor User Rules database mutation as the strategic install path.

# Context

`research:loom-install-distribution-methods` identifies Cursor as one of the two
strongest first-class package candidates. Cursor plugins are Git-backed bundles
with `.cursor-plugin/plugin.json` and can package rules, skills, agents,
commands, MCP servers, and hooks. Cursor plugin component discovery includes
`rules/`, `skills/`, `commands/`, `hooks/hooks.json`, and `mcp.json` unless a
manifest path overrides the default.

The existing Cursor installer in `ticket:rd48g1kg` proved that Loom can install
rules into Cursor User Rules, copy skills to `~/.cursor/skills`, and generate
commands under `~/.cursor/commands`. That path is useful but brittle because it
mutates Cursor User Rules storage directly. This ticket tests the more native
plugin package route.

# Why Now

Cursor should be prototyped first because it can likely express all three Loom
surfaces in one documented package:

- rules as `.mdc` files under plugin `rules/`
- skills as `skills/<name>/SKILL.md`
- commands as Markdown-like command files under plugin `commands/`

If this works, Cursor becomes the model for replacing fragile direct config
mutation with a first-class adapter package where the harness supports it.

# Scope

- design a Cursor plugin package or fixture shape derived from canonical Loom
  `rules/`, `skills/`, and optional `commands/`
- create `.cursor-plugin/plugin.json` metadata if a package fixture is added
- generate or write Cursor rule files that preserve numeric Loom rule order and
  use `alwaysApply: true` where that is the correct Cursor rule frontmatter
- preserve skill directories with `SKILL.md`, `references/`, and `templates/`
- preserve optional command wrappers as explicit adapter commands, not protocol
  owners
- compare the plugin path against the current User Rules managed-block path
- update `INSTALL.md` or adapter examples only for the Cursor decision that this
  ticket proves
- record validation evidence in the ticket or a linked evidence record

# Non-goals

- do not change canonical `rules/`, `skills/`, or `commands/` semantics
- do not add Cursor hooks, MCP servers, or agents unless the ticket is explicitly
  revised to justify them
- do not publish a Cursor Marketplace package
- do not remove the existing Cursor shell fallback unless the plugin path is
  proven and replacement scope is explicitly accepted
- do not treat generated `.mdc` files as Loom's canonical rules

# Acceptance Criteria

- a Cursor plugin package or fixture exists, or the ticket records a supported
  reason why the plugin path cannot currently be used
- plugin manifest fields match Cursor's documented `.cursor-plugin/plugin.json`
  requirements
- Loom rules are represented as ordered always-on Cursor plugin rules, or a
  documented limitation explains why User Rules remain necessary
- Loom skills remain discoverable Agent Skill directories with `SKILL.md`
- optional Loom commands remain explicit command surfaces and carry source
  markers or clear provenance back to `commands/*.md`
- validation shows the plugin/package structure can be inspected with ordinary
  file tools
- if Cursor CLI/UI validation is unavailable, the ticket names that limitation
  instead of claiming runtime proof
- `INSTALL.md` and any adapter fixture documentation reflect the proven Cursor
  recommendation

# Coverage

Covers:

- None - no spec-owned acceptance IDs exist. This ticket consumes
  `research:loom-install-distribution-methods#cursor` and owns ticket-local
  acceptance criteria for the Cursor install slice.

# Claim Matrix

No new Cursor plugin prototype evidence was added to this ticket before closure.
Operator accepted no further action here; prior Cursor harness support remains
owned by `ticket:rd48g1kg` and `evidence:cursor-harness-install-validation`.

# Execution Notes

Cursor facts to preserve from research:

- User Rules apply globally across Agent Chat, but mutating their storage is a
  brittle fallback compared with documented plugin packaging.
- Project rules live in `.cursor/rules` and can use `.mdc` frontmatter such as
  `description`, `globs`, and `alwaysApply`.
- Cursor skills load from `.agents/skills`, `.cursor/skills`, `~/.agents/skills`,
  and `~/.cursor/skills`, and also from some Claude/Codex-compatible paths.
- Cursor plugins can package `rules/`, `skills/`, `commands/`, hooks, MCP, and
  agents.
- Cursor local plugin testing uses `~/.cursor/plugins/local`, including symlinked
  plugin repositories.

Likely implementation shape:

- create a non-canonical adapter package or fixture directory for Cursor
- copy or generate rules into plugin `rules/` as Cursor-compatible `.mdc` files
- copy canonical skill directories into plugin `skills/`
- generate command adapter files into plugin `commands/`
- keep every generated file marked as derived from Loom source
- leave canonical Loom behavior in top-level source files

# Blockers

None. Operator accepted closure without further Cursor plugin prototype work in
this ticket.

# Next Move / Next Route

Closed. If Cursor plugin packaging becomes the preferred supported install path,
open a fresh ticket with current Cursor docs/runtime evidence.

# Ralph Readiness

Bounded iteration:
Prototype and validate the Cursor plugin install package or fixture, then update
Cursor install documentation to reflect whether plugin packaging should replace
or supplement the current User Rules fallback.

Write boundary:
Cursor adapter package or fixture paths, `INSTALL.md`, `examples/adapters/` if
used for fixtures, `scripts/install-loom.sh` only if the proven path requires a
small fallback adjustment, and this ticket/evidence records. Read-only source
inputs are `rules/`, `skills/`, and `commands/`.

Likely verification posture:
Observation-first structural validation. Capture before/after generated package
structure and run any Cursor local plugin link/install check available on the
machine. If no Cursor CLI/UI validation is available, record that limitation.

Expected output contract:
Changed files, generated package or fixture summary, validation commands and
results, limitations, recommendation for Cursor install path, and ticket state
recommendation.

# Evidence

Expected evidence was not gathered in this ticket before operator closure:

- structural review of plugin manifest and component directories
- source-marker spot-check for generated rules and commands
- check that all canonical Loom skills copied into plugin package still contain
  `SKILL.md`
- `git diff --check`
- optional Cursor local plugin link/install validation if available
- explicit limitation if runtime Cursor validation cannot be run

# Critique Disposition

Risk class: medium

Critique policy: recommended

Policy rationale:
This is a meaningful install-surface change that could mislead operators if the
plugin package does not actually load ordered rules. It is release-packaging work,
not core protocol authority, so critique is recommended rather than mandatory.

Required critique profiles:

- operator-clarity

Findings:

None - no critique yet.

Disposition status: not_required by operator acceptance at closure

Deferral / not-required rationale:

No Cursor plugin package change is being accepted from this ticket; closure rests
on operator decision that no further prototype work is required here.

# Wiki Disposition

Wiki promotion is not required for this closure. If the Cursor plugin pattern
becomes accepted later, promote the general adapter-package pattern through a
fresh ticket or retrospective.

# Acceptance Decision

Accepted by: operator
Accepted at: 2026-04-28T18:50:38Z
Basis: Operator stated the remaining open adapter work was complete and accepted closing this Cursor plugin prototype with no further action. Existing Cursor support remains represented by the prior direct harness-install ticket and evidence.
Residual risks: This ticket did not create or validate a Cursor plugin package; future Cursor plugin packaging should be handled as new work with current docs/runtime validation.

# Dependencies

Uses `research:loom-install-distribution-methods`, prior Cursor installer proof
from `ticket:rd48g1kg`, and `evidence:cursor-harness-install-validation`. No hard
ticket prerequisite blocks starting this prototype.

# Journal

- 2026-04-25: created as the Cursor harness ticket under
  `plan:install-experience-harness-adapters`.
- 2026-04-28T18:50:38Z: Operator accepted closing the remaining Cursor plugin
  prototype work with no further action; future Cursor plugin packaging should
  start from a fresh ticket and current evidence.
