---
id: ticket:7ex8w32y
kind: ticket
status: ready
change_class: release-packaging
risk_class: medium
created_at: 2026-04-25T18:46:08Z
updated_at: 2026-04-25T18:46:08Z
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
external_refs:
  gemini_cli_docs:
    - https://geminicli.com/docs/extensions/
    - https://geminicli.com/docs/extensions/reference/
    - https://geminicli.com/docs/cli/skills/
    - https://geminicli.com/docs/cli/custom-commands/
depends_on: []
---

# Summary

Prototype a Gemini CLI extension install path for Loom that packages ordered
rules, Agent Skills, and optional TOML command adapters through Gemini's
documented extension system.

# Context

`research:loom-install-distribution-methods` identifies Gemini CLI extensions as
a strong first-class package candidate. Gemini extensions distribute prompts,
MCP servers, custom commands, themes, hooks, sub-agents, and agent skills. Each
extension root has `gemini-extension.json`, can load a configured context file or
default `GEMINI.md`, can package skills under `skills/`, and can package custom
commands as TOML files under `commands/`.

The existing shell fallback mirrors Loom rules into `~/.gemini/GEMINI.md`, copies
skills to `~/.gemini/skills`, and converts commands into
`~/.gemini/commands/*.toml`. This ticket tests whether a Gemini extension can
replace or supplement that direct mutation path.

# Why Now

Gemini is one of the best proving grounds for a first-class adapter package
because its extension format appears to include all Loom install needs:

- context file for ordered always-on rules
- `skills/` for Agent Skills
- `commands/*.toml` for slash-command wrappers
- documented install, link, disable, enable, and update commands

# Scope

- design a Gemini extension package or fixture derived from canonical Loom
  `rules/`, `skills/`, and optional `commands/`
- create `gemini-extension.json` with appropriate metadata and context file
  configuration
- generate or write an extension context file that loads Loom rules in numeric
  order
- copy canonical skill directories into extension `skills/`
- convert optional Loom command Markdown into Gemini TOML command files
- preserve source markers or provenance in generated command/context outputs
- validate extension structure and, if available, local `gemini extensions link`
  or `gemini extensions install` behavior
- update install docs and adapter fixture notes for the Gemini decision

# Non-goals

- do not add MCP servers, hooks, themes, or sub-agents to the Loom extension
  unless this ticket is explicitly revised
- do not publish a Gemini extension gallery entry
- do not remove the existing direct Gemini fallback until the extension path is
  proven and replacement scope is accepted
- do not change canonical Loom rules, skills, or commands to satisfy Gemini
  formatting
- do not treat generated TOML commands or extension context as canonical Loom
  behavior

# Acceptance Criteria

- a Gemini extension package or fixture exists, or the ticket records a supported
  reason why an extension cannot currently express Loom install needs
- `gemini-extension.json` matches the documented manifest shape
- extension context preserves ordered always-on Loom rules
- skills remain Agent Skill directories with `SKILL.md` and supporting files
- generated TOML commands preserve optional command wrapper intent and argument
  handling using Gemini-compatible syntax
- validation demonstrates package structure and generated files are inspectable
  and source-marked
- install/link/disable validation is run with Gemini CLI when available, or the
  ticket records why only structural validation was possible
- `INSTALL.md` or adapter examples reflect the proven Gemini recommendation

# Coverage

Covers:

- None - no spec-owned acceptance IDs exist. This ticket consumes
  `research:loom-install-distribution-methods#gemini-cli` and owns ticket-local
  acceptance criteria for the Gemini extension slice.

# Claim Matrix

None - no evidence exists yet for this extension prototype.

# Execution Notes

Gemini facts to preserve from research:

- extensions load from `<home>/.gemini/extensions`; installed extensions are
  copied, while linked local extensions are symlinked
- `gemini-extension.json` can name `contextFileName`; if omitted and `GEMINI.md`
  exists, `GEMINI.md` is loaded
- custom commands are TOML files under `commands/`
- `{{args}}` injects command arguments in Gemini commands
- skills can live in extension `skills/` and are lower precedence than workspace
  and user skills

Likely implementation shape:

- create a non-canonical Gemini extension fixture or package directory
- generate extension `GEMINI.md` or a configured context file from ordered Loom
  rules
- copy `skills/*` into extension `skills/`
- convert `commands/*.md` into `commands/*.toml`
- keep the current direct install path available until extension behavior is
  validated

# Blockers

None.

# Next Move / Next Route

Ralph implementation packet.

# Ralph Readiness

Bounded iteration:
Prototype and validate a Gemini CLI extension package or fixture for Loom, then
update Gemini install guidance with the proven path and limitations.

Write boundary:
Gemini adapter package or fixture paths, `INSTALL.md`, `examples/adapters/` if
used for fixtures, `scripts/install-loom.sh` only if a small fallback adjustment
is justified, and this ticket/evidence records. Read-only source inputs are
`rules/`, `skills/`, and `commands/`.

Likely verification posture:
Observation-first structural validation plus Gemini CLI local extension link or
install validation when available.

Expected output contract:
Changed files, extension structure summary, generated context/command behavior,
validation commands and results, limitations, recommendation for Gemini install
path, and ticket state recommendation.

# Evidence

Expected evidence:

- structural check of `gemini-extension.json`
- inspection of generated extension context and TOML commands
- check that copied skills retain `SKILL.md`, references, and templates
- `git diff --check`
- `gemini extensions link` or equivalent if available
- explicit limitation if Gemini CLI runtime validation cannot be run

# Critique Disposition

Risk class: medium

Critique policy: recommended

Policy rationale:
This is a meaningful install-path change. Incorrect extension context behavior
could make users believe Loom rules are always-on when they are not.

Required critique profiles:

- operator-clarity

Findings:

None - no critique yet.

Disposition status: pending

Deferral / not-required rationale:

None.

# Wiki Disposition

Wiki promotion is optional. If Gemini extension packaging becomes the first
accepted full adapter-package pattern, promote the reusable adapter-package
pattern through retrospective.

# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:

# Dependencies

Uses `research:loom-install-distribution-methods` and prior direct Gemini install
proof from `ticket:ffg8elkb`. No hard ticket prerequisite blocks starting this
prototype.

# Journal

- 2026-04-25: created as the Gemini CLI harness ticket under
  `plan:install-experience-harness-adapters`.
