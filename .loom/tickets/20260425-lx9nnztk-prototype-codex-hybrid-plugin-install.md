---
id: ticket:lx9nnztk
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
    - research:codex-command-skill-installation
  related:
    - ticket:ffg8elkb
    - ticket:p9m4x2qt
external_refs:
  codex_docs:
    - https://developers.openai.com/codex/skills
    - https://developers.openai.com/codex/guides/agents-md
    - https://developers.openai.com/codex/plugins/build
depends_on: []
---

# Summary

Prototype and decide a Codex hybrid Loom install path that uses Codex plugins or
skills for reusable workflows while keeping ordered always-on Loom rules in
Codex's actual `AGENTS.md` instruction surface.

# Context

Prior `research:codex-command-skill-installation` moved Codex command wrappers
from legacy prompt files into explicit-only `loom-command-*` adapter skills.
Current `research:loom-install-distribution-methods` adds that Codex plugins can
package skills, MCP servers, apps/connectors, and assets through
`.codex-plugin/plugin.json`, but the fetched docs do not describe plugins as a
mechanism for always-on instructions.

The current installer copies skills into `$HOME/.agents/skills`, generates
explicit-only command adapter skills, and mirrors ordered Loom rules into a
managed block in `~/.codex/AGENTS.md`. This ticket tests whether a Codex plugin
or marketplace package should own the skills/command-adapter portion while
`AGENTS.md` continues to own the always-on rule surface.

# Why Now

Codex already has the most sophisticated generated command adapter path in the
current installer. A plugin prototype can decide whether that adapter family
should become a packaged Codex distribution unit instead of only being generated
into the user's global skill directory by the shell script.

# Scope

- design a Codex plugin or marketplace fixture that packages canonical Loom
  skills and generated explicit-only command adapter skills
- preserve `agents/openai.yaml` metadata for generated command adapters,
  including `policy.allow_implicit_invocation: false`
- keep ordered Loom rules in `~/.codex/AGENTS.md` or another documented Codex
  instruction surface, not in `~/.codex/rules/`
- evaluate whether plugin packaging improves update, enable/disable, or
  marketplace behavior enough to justify changing the current direct skill copy
  path
- verify command adapter names avoid collisions with canonical Loom skill names
- update Codex install docs and shell fallback only after the hybrid path is
  evidenced

# Non-goals

- do not reinstall Loom commands as legacy Codex prompts
- do not use `~/.codex/rules/` for Loom Markdown rules
- do not make generated command adapter skills implicit triggers
- do not publish a Codex marketplace package
- do not change canonical Loom command names just to fit generated adapter names
- do not treat plugin cache files as canonical Loom source

# Acceptance Criteria

- the ticket records a clear Codex recommendation: keep direct skill generation,
  add a Codex plugin/marketplace package, or defer plugin packaging with rationale
- ordered Loom rules remain in a documented Codex instruction surface such as
  `AGENTS.md`
- canonical Loom skills remain valid `SKILL.md` directories
- generated command adapter skills remain explicit-only and non-colliding
- plugin manifest or marketplace fixture matches Codex docs if package fixtures
  are added
- validation shows generated adapters include expected `agents/openai.yaml`
  policy and metadata
- install/uninstall or package-link validation is run if available, or limitations
  are recorded honestly
- `INSTALL.md` reflects the chosen Codex path

# Coverage

Covers:

- None - no spec-owned acceptance IDs exist. This ticket consumes
  `research:loom-install-distribution-methods#codex` and
  `research:codex-command-skill-installation` while owning ticket-local
  acceptance criteria for the Codex install slice.

# Claim Matrix

None - no evidence exists yet for this Codex hybrid plugin decision.

# Execution Notes

Codex facts to preserve from research:

- Codex home defaults to `~/.codex` unless `CODEX_HOME` is set
- global instructions use `AGENTS.override.md` first, otherwise `AGENTS.md`
- `$HOME/.agents/skills` is the user skill location
- `allow_implicit_invocation` defaults to `true`; generated command adapter
  skills should set it to `false`
- Codex plugins install into a cache copy and are enabled/disabled through Codex
  plugin configuration
- plugin docs package skills, MCP, apps/connectors, and assets, not always-on
  instructions

Likely implementation choices:

- keep the managed `AGENTS.md` rule block as the rule path
- package canonical skills plus generated command-adapter skills in a Codex
  plugin fixture if plugin packaging proves useful
- preserve direct generation as fallback until plugin behavior is validated

# Blockers

None.

# Next Move / Next Route

Ralph implementation packet.

# Ralph Readiness

Bounded iteration:
Prototype or structurally compare Codex plugin/marketplace packaging for Loom
skills and command adapters, then update Codex install guidance with the chosen
hybrid path.

Write boundary:
Codex adapter package or fixture paths, generated command-adapter logic if needed,
`INSTALL.md`, `examples/adapters/` if used for fixtures, `scripts/install-loom.sh`
only for a small proven fallback adjustment, and this ticket/evidence records.
Read-only source inputs are `rules/`, `skills/`, and `commands/`.

Likely verification posture:
Observation-first structural validation plus temporary `HOME` install/uninstall
checks if direct Codex installer behavior changes.

Expected output contract:
Chosen Codex recommendation, changed files, generated adapter summary, validation
commands and results, limitations, and ticket state recommendation.

# Evidence

Expected evidence:

- structural inspection of Codex plugin or marketplace fixture if created
- generated adapter skill inspection, including `agents/openai.yaml`
- collision check between canonical skill names and generated `loom-command-*`
  adapter names
- `AGENTS.md` managed-block or instruction-surface inspection if changed
- `git diff --check`
- optional Codex plugin install/enable validation if available

# Critique Disposition

Risk class: medium

Critique policy: recommended

Policy rationale:
Codex command adapters affect invocation behavior and can create confusing skill
collisions if generated incorrectly. Review should focus on operator clarity and
adapter fidelity.

Required critique profiles:

- operator-clarity

Findings:

None - no critique yet.

Disposition status: pending

Deferral / not-required rationale:

None.

# Wiki Disposition

Wiki promotion is optional. Promote only if the Codex explicit command-adapter
pattern becomes a reusable adapter design beyond Codex.

# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:

# Dependencies

Uses `research:loom-install-distribution-methods`,
`research:codex-command-skill-installation`, prior direct install work from
`ticket:ffg8elkb`, and generated adapter work from `ticket:p9m4x2qt`. No hard
ticket prerequisite blocks starting this prototype.

# Journal

- 2026-04-25: created as the Codex harness ticket under
  `plan:install-experience-harness-adapters`.
