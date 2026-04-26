---
id: ticket:lx9nnztk
kind: ticket
status: ready
change_class: release-packaging
risk_class: medium
created_at: 2026-04-25T18:46:08Z
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
    - research:harness-install-surfaces
    - research:codex-command-skill-installation
    - research:codex-plugin-distribution-surfaces
  related:
    - ticket:ffg8elkb
    - ticket:p9m4x2qt
external_refs:
  codex_docs:
    - https://developers.openai.com/codex/skills
    - https://developers.openai.com/codex/guides/agents-md
    - https://developers.openai.com/codex/plugins
    - https://developers.openai.com/codex/plugins/build
    - https://developers.openai.com/codex/cli/reference#codex-plugin-marketplace
    - https://developers.openai.com/codex/concepts/customization
    - https://developers.openai.com/codex/config-advanced
  codex_source:
    - https://github.com/openai/codex/blob/main/codex-rs/core-plugins/src/manifest.rs
    - https://github.com/openai/codex/blob/main/codex-rs/core-plugins/src/loader.rs
    - https://github.com/openai/codex/blob/main/codex-rs/plugin/src/plugin_namespace.rs
    - https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/plugin-creator/references/plugin-json-spec.md
    - https://github.com/openai/plugins
depends_on: []
---

# Summary

Prototype and decide a Codex hybrid Loom install path that uses Codex plugins or
skills for reusable workflows while keeping ordered always-on Loom rules in
Codex's actual `AGENTS.md` instruction surface.

# Context

Prior `research:codex-command-skill-installation` moved Codex command wrappers
from legacy prompt files into explicit-only `loom-command-*` adapter skills.
Focused `research:codex-plugin-distribution-surfaces` now shows that Codex
plugins are the first-class installable distribution unit for reusable skills,
apps, and MCP servers, with repo/user marketplace files and a `codex plugin
marketplace` CLI surface.

That same research does not find evidence that plugins own Codex's always-on
`AGENTS.md` instruction chain. The current installer copies skills into
`$HOME/.agents/skills`, generates explicit-only command adapter skills, and
mirrors ordered Loom rules into a managed block in `~/.codex/AGENTS.md`. This
ticket now tests the package-layout question: how to use a Codex plugin for
skills and generated command adapters while keeping ordered Loom rules in an
actual Codex instruction surface.

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
- compare whether the plugin root should be the repository root, a derivative
  `plugins/loom` package, or an `examples/adapters/` fixture before committing
  to a release package layout
- evaluate whether plugin packaging improves update, enable/disable, or
  marketplace behavior enough to justify changing the current direct skill copy
  path
- verify command adapter names avoid collisions with canonical Loom skill names
- record the tested Codex CLI version because docs and local runtime support are
  moving quickly
- update Codex install docs and shell fallback only after the hybrid path is
  evidenced

# Non-goals

- do not reinstall Loom commands as legacy Codex prompts
- do not use `~/.codex/rules/` for Loom Markdown rules
- do not make generated command adapter skills implicit triggers
- do not publish a Codex marketplace package
- do not change canonical Loom command names just to fit generated adapter names
- do not treat plugin cache files as canonical Loom source
- do not rely on plugin hooks, plugin commands, plugin agents, or plugin-managed
  `AGENTS.md` unless the target Codex runtime proves that support
- do not add generated command adapter skills to top-level `skills/` as if they
  were canonical Loom skills

# Acceptance Criteria

- the ticket records a clear Codex recommendation: keep direct skill generation,
  add a Codex plugin/marketplace package, or defer plugin packaging with rationale
- the prototype compares the viable plugin package layouts and identifies the
  preferred next implementation shape
- ordered Loom rules remain in a documented Codex instruction surface such as
  `AGENTS.md`
- canonical Loom skills remain valid `SKILL.md` directories
- generated command adapter skills remain explicit-only and non-colliding
- plugin manifest or marketplace fixture matches Codex docs if package fixtures
  are added
- the package layout does not turn generated command adapter skills into
  canonical top-level Loom skills
- validation shows generated adapters include expected `agents/openai.yaml`
  policy and metadata
- install/uninstall or package-link validation is run if available, or limitations
  are recorded honestly
- `INSTALL.md` reflects the chosen Codex path only after the prototype is
  evidenced

# Coverage

Covers:

- None - no spec-owned acceptance IDs exist. This ticket consumes
  `research:loom-install-distribution-methods#codex` and
  `research:codex-command-skill-installation` plus
  `research:codex-plugin-distribution-surfaces` while owning ticket-local
  acceptance criteria for the Codex install slice.

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| Codex plugins are first-class distribution units for reusable skills, apps, and MCP servers. | `research:codex-plugin-distribution-surfaces` | None | supported |
| Codex plugins do not currently own Loom's always-on rule surface. | `research:codex-plugin-distribution-surfaces` | None | supported pending runtime validation |
| Codex command wrappers should remain explicit-only `loom-command-*` adapter skills. | `research:codex-command-skill-installation`, `ticket:p9m4x2qt` | None | supported |
| The best next move is a package-layout spike, not broad release packaging. | `research:codex-plugin-distribution-surfaces` | None | supported |

# Execution Notes

Codex facts to preserve from research:

- Codex home defaults to `~/.codex` unless `CODEX_HOME` is set
- global instructions use `AGENTS.override.md` first, otherwise `AGENTS.md`
- `$HOME/.agents/skills` is the user skill location
- `allow_implicit_invocation` defaults to `true`; generated command adapter
  skills should set it to `false`
- Codex plugins install into a cache copy and are enabled/disabled through Codex
  plugin configuration
- plugins are now documented as the installable distribution unit for reusable
  skills, apps/connectors, MCP servers, and assets
- `codex plugin marketplace add` accepts local marketplace roots, GitHub
  shorthand, HTTP(S) Git URLs, and SSH URLs
- installed local `codex-cli 0.123.0` exposes marketplace add/upgrade/remove but
  not a simple documented non-interactive `codex plugin install` command
- plugin docs and inspected source package skills, MCP, apps/connectors, and
  assets, not always-on instructions
- inspected manifest source models `skills`, `mcpServers`, `apps`, and
  `interface`, but not `hooks`, `commands`, `agents`, or `AGENTS.md`
- OpenAI plugin examples and plugin-creator docs mention hooks or extra plugin
  surfaces inconsistently; do not rely on them for Loom until runtime-proven
- plugin skills appear to be namespaced by plugin manifest name, so a `loom`
  plugin should reduce collision risk, but explicit invocation shape still needs
  runtime validation
- Loom's current top-level rule corpus is about 45.6 KiB, so project-local
  `AGENTS.md` mirroring may collide with Codex's documented 32 KiB default
  project-doc budget

Candidate package layouts to compare:

- repository-root plugin: add `.codex-plugin/plugin.json` at repo root and use
  canonical `skills/`; this is smallest but does not solve packaging generated
  command adapter skills unless a second skill path or generated fixture is added
- derivative plugin fixture: create a plugin root such as `plugins/loom` or an
  `examples/adapters/codex-plugin-install` fixture with copied/generated skills;
  this can package command adapters but must stay clearly derivative from
  canonical `skills/` and `commands/`
- direct fallback only: keep `$HOME/.agents/skills` generation and managed
  `~/.codex/AGENTS.md`; this remains valid fallback but underuses Codex's native
  plugin UX

Likely implementation choices after the spike:

- keep the managed `AGENTS.md` rule block as the rule path
- use a Codex plugin or marketplace fixture for canonical skills plus generated
  explicit-only command adapter skills if layout and runtime validation are good
- preserve direct generation as fallback until plugin behavior is validated on
  the chosen minimum Codex CLI version

# Blockers

None.

# Next Move / Next Route

Ralph implementation packet for an observation-first Codex package-layout spike.
The packet should not attempt broad release packaging. It should create or
compare the smallest plugin/marketplace fixture that proves the right layout for
canonical skills, generated explicit-only command adapters, and separate
`AGENTS.md` rules.

# Ralph Readiness

Bounded iteration:
Prototype or structurally compare Codex plugin/marketplace layouts for Loom
skills and generated command adapters, then record the recommended Codex hybrid
path. Install guidance should change only if the prototype produces enough
evidence.

Write boundary:
Codex adapter package or fixture paths, generated command-adapter logic if needed,
`INSTALL.md` only if the path is evidenced, `examples/adapters/` or `plugins/`
if used for fixtures, `scripts/install-loom.sh` only for a small proven fallback
adjustment, and this ticket/evidence records. Read-only source inputs are
`rules/`, `skills/`, and `commands/`.

Likely verification posture:
Observation-first structural validation. Include temporary `CODEX_HOME` or
`HOME` checks only when the implementation changes direct Codex installer
behavior or can safely add a local marketplace without touching real user state.

Expected output contract:
Chosen Codex package-layout recommendation, changed files, generated adapter
summary, Codex CLI version tested, validation commands and results, limitations,
and ticket state recommendation.

# Evidence

Expected evidence:

- structural inspection of Codex plugin or marketplace fixture if created
- package-layout comparison covering repository-root plugin versus derivative
  plugin fixture, unless one option is explicitly rejected before implementation
- generated adapter skill inspection, including `agents/openai.yaml`
- collision check between canonical skill names and generated `loom-command-*`
  adapter names
- plugin skill namespace or selector behavior inspection when runtime validation
  is available
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
- 2026-04-26: expanded with focused Codex plugin research. The next move is now
  a package-layout spike that treats Codex plugins as first-class for skills and
  generated explicit-only command adapters while keeping ordered rules in
  `AGENTS.md`.
