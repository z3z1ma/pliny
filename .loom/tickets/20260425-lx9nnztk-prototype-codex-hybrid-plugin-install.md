---
id: ticket:lx9nnztk
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
    - research:codex-command-skill-installation
    - research:codex-plugin-distribution-surfaces
  evidence:
    - evidence:codex-sessionstart-stdout-context
  critique:
    - critique:codex-plugin-hook-config-review
  decision:
    - decision:0005
    - decision:0006
  related:
    - ticket:ffg8elkb
    - ticket:p9m4x2qt
external_refs:
  codex_docs:
    - https://developers.openai.com/codex/skills
    - https://developers.openai.com/codex/guides/agents-md
    - https://developers.openai.com/codex/plugins
    - https://developers.openai.com/codex/plugins/build
    - https://developers.openai.com/codex/hooks
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

Prototype and decide the Codex remote plugin install shape now that Loom's
mandatory doctrine is packaged as the `loom-bootstrap` skill.

# Context

Prior `research:codex-command-skill-installation` moved Codex command wrappers
from legacy prompt files into explicit-only `loom-command-*` adapter skills, but
`decision:0006` supersedes command-wrapper distribution as product surface.
Focused `research:codex-plugin-distribution-surfaces` now shows that Codex
plugins are the first-class installable distribution unit for reusable skills,
apps, and MCP servers, with repo/user marketplace files and a `codex plugin
marketplace` CLI surface.

Follow-up source inspection and runtime probing found a useful optional preload
surface: Codex config-layer `SessionStart` hooks accept plain stdout as additional
developer context. That proves a hook mechanism, but `decision:0005` means the
remote install no longer depends on plugin-owned hooks. The remote package should
install `loom-bootstrap` and the other Loom skills; hooks are an optional
trusted-project boost.

# Why Now

Codex users should not need to clone Loom or trust a project-local fixture to get
Loom. The intended product shape is a remote marketplace/plugin path that can be
added easily across many machines. A plugin prototype is useful only if it either
meets that bar or makes the platform gap explicit.

# Scope

- design a Codex plugin or marketplace fixture that packages canonical Loom
  skills from top-level `skills/`
- evaluate whether a remote Codex plugin install exposes `loom-bootstrap` and the
  other Loom skills well enough for normal users
- add a Codex `SessionStart` hook fixture that emits `loom-bootstrap` references
  as source-marked stdout, one reference per command, as an optional preload proof
- keep Loom bootstrap references out of `~/.codex/rules/`, which is a shell
  execution policy surface rather than a Markdown instruction surface
- document that current Codex evidence supports hook config loading from active
  config layers, not installed-plugin manifest hook loading
- keep command-wrapper folding out of this ticket unless later work promotes a
  workflow into a canonical Loom skill
- compare whether the plugin root should be the repository root or a derivative
  package before broad release packaging
- evaluate whether plugin packaging improves update, enable/disable, or
  marketplace behavior enough to justify changing the current direct skill copy
  path
- verify command adapter names avoid collisions with canonical Loom skill names
- record the tested Codex CLI version because docs and local runtime support are
  moving quickly
- update Codex install docs only after the native plugin path is evidenced

# Non-goals

- do not reinstall Loom commands as legacy Codex prompts
- do not use `~/.codex/rules/` for Loom Markdown bootstrap references
- do not make generated command adapter skills implicit triggers
- do not publish a Codex marketplace package
- do not call a remote plugin complete unless `loom-bootstrap` is discoverable and
  documented as the mandatory first skill
- do not treat repository `.codex/hooks.json` as the normal remote-user install
  path
- do not change canonical Loom command names just to fit generated adapter names
- do not treat plugin cache files as canonical Loom source
- do not claim installed-plugin hooks load from `.codex-plugin/plugin.json` unless
  the target Codex runtime proves that support
- do not fold commands into skills as part of this ticket
- do not add generated command adapter skills to top-level `skills/` as if they
  were canonical Loom skills

# Acceptance Criteria

- the ticket records a clear Codex recommendation for remote plugin packaging
- the prototype identifies the preferred next implementation shape and records
  what current Codex evidence does and does not prove
- `loom-bootstrap` and its ordered references are available through the remote
  plugin path
- canonical Loom skills remain valid `SKILL.md` directories
- no top-level command-wrapper or fallback installer path is introduced
- plugin manifest or marketplace fixture matches Codex docs if package fixtures
  are added
- the package layout does not turn generated command adapter skills into
  canonical top-level Loom skills
- validation shows bootstrap hook stdout reaches same-session context for the proof
  fixture, without overstating that this proves remote plugin install
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
| Codex plugins do not currently own Loom's always-on hook surface. | `research:codex-plugin-distribution-surfaces`, `evidence:codex-sessionstart-stdout-context` | `critique:codex-plugin-hook-config-review#FIND-002` | supported but no longer blocking after `decision:0005` |
| Codex `SessionStart` hook stdout can carry Loom bootstrap context from an active config layer. | `evidence:codex-sessionstart-stdout-context` | None | supported |
| Packaging mandatory doctrine as `loom-bootstrap` changes the Codex blocker from plugin-owned hooks to installed skill discovery. | `decision:0005` | Pending | open |
| Codex command wrappers are no longer a product install surface after `decision:0006`. | `decision:0006` | None | supported |

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
- installed local `codex-cli 0.125.0` exposes marketplace add/upgrade/remove but
  not a simple documented non-interactive `codex plugin install` command
- plugin docs and inspected source package skills, MCP, apps/connectors, and
  assets, not always-on instructions
- inspected manifest source models `skills`, `mcpServers`, `apps`, and
  `interface`, but not source-proven plugin-owned `hooks`, `commands`, `agents`,
  or `AGENTS.md`
- source inspection shows Codex plugin install persists only
  `[plugins.<marketplace/plugin>.enabled]`; installed plugin loading contributes
  skills, MCP servers, and apps, not hooks
- Codex hooks docs and source prove `hooks.json` and inline `[hooks]` config-layer
  hook loading; `SessionStart` plain stdout becomes extra developer context
- OpenAI plugin examples and plugin-creator docs mention hooks or extra plugin
  surfaces inconsistently; do not rely on plugin-owned hooks for Loom until
  runtime-proven
- plugin skills appear to be namespaced by plugin manifest name, so a `loom`
  plugin should reduce collision risk, but explicit invocation shape still needs
  runtime validation
- the former top-level rule corpus now lives in `loom-bootstrap` references, so
  Codex plugin install can package the doctrine as a skill rather than needing
  plugin-owned hooks

Candidate package layouts to compare:

- repository-root plugin: add `.codex-plugin/plugin.json` at repo root and use
  canonical `skills/`; this is smallest and matches the current command-folding
  discussion because generated command adapters are not part of this ticket
- derivative plugin fixture: create a plugin root such as `plugins/loom` or an
  `examples/adapters/codex-plugin-install` fixture with copied skills; this must
  stay clearly derivative from canonical `skills/`

Likely implementation choices after the spike:

- use repository-root Codex plugin metadata as the remote skills-package shape
- keep trusted project `.codex/hooks.json` as an optional preload proof fixture
- do not preserve direct generation or managed `AGENTS.md` as supported fallback;
  use native plugin skill discovery and optional hook preload only

# Blockers

None. Operator accepted closure without further Codex plugin validation in this
ticket; any future Codex install packaging change should open a fresh ticket with
current runtime evidence.

# Next Move / Next Route

Closed. Future Codex install packaging work should start from current Codex docs
and runtime evidence in a new ticket rather than reopening this prototype.

# Ralph Readiness

Bounded iteration:
Prototype Codex plugin and hook config surfaces for Loom skills and rule context,
then record whether they satisfy remote install. Broad install guidance should
change only where evidence supports it.

Write boundary:
Codex adapter package or fixture paths, `INSTALL.md` only if the path is
evidenced, `examples/adapters/` if used for fixtures, and this ticket/evidence
records. Read-only source inputs are `skills/loom-bootstrap/references/` and
`skills/`.

Likely verification posture:
Observation-first structural validation. Include temporary `CODEX_HOME` or
`HOME` checks only when the implementation changes direct Codex installer
behavior or can safely add a local marketplace without touching real user state.

Expected output contract:
Codex remote-install recommendation or blocker, changed files, Codex CLI version
tested, validation commands and results, limitations, and ticket state
recommendation.

# Evidence

Recorded evidence:

- `evidence:codex-sessionstart-stdout-context`
- `.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`
- `.codex/config.toml`
- `.codex/hooks.json`
- `examples/adapters/codex-plugin-install/README.md`
- `codex exec` startup probe saw all seven `LOOM_RULE_FILE` markers and quoted
  `A child assertion is not enough.` from `07-validation-and-honesty.md`
- `CODEX_HOME=/tmp/... codex plugin marketplace add` registered the local
  `agent-loom` marketplace without touching the real Codex home
- `critique:codex-plugin-hook-config-review` found that local `source.path: "./"`
  is invalid for a repository-root plugin; the marketplace now uses Codex's
  documented Git-backed root-plugin `source: "url"` shape
- `critique:codex-plugin-hook-config-review#FIND-002` found a release blocker
  under the prior model: project-local hook proof did not make plugin install
  deliver always-on rules. `decision:0005` resolves that as a model blocker by
  making `loom-bootstrap` the mandatory plugin-packaged entry skill.

Residual evidence not gathered before closure:

- installed Git-backed plugin skill discovery for `loom-bootstrap`
- a Codex startup probe after the hook path update to
  `skills/loom-bootstrap/references/`
- structural inspection of Codex plugin or marketplace fixture if changed
- package-layout comparison covering repository-root plugin versus derivative
  plugin fixture, unless one option is explicitly rejected before implementation
- generated adapter skill inspection, including `agents/openai.yaml`, only if a
  future release package includes command adapter skills
- collision check between canonical skill names and generated `loom-command-*`
  adapter names, only if a future release package includes command adapter skills
- plugin skill namespace or selector behavior inspection when runtime validation
  is available
- `SessionStart` hook stdout context inspection if changed
- `git diff --check`
- optional Codex plugin install/enable validation if available

# Critique Disposition

Risk class: medium

Critique policy: recommended

Policy rationale:
Codex plugin-plus-hook-config packaging affects operator installation behavior
and can mislead users if docs imply installed plugins own always-on hooks. Review
should focus on operator clarity, evidence fidelity, and adapter boundaries.

Required critique profiles:

- operator-clarity

Findings:

`critique:codex-plugin-hook-config-review#FIND-001` found one high-severity
marketplace source issue. It is resolved by changing `.agents/plugins/marketplace.json`
to a Git-backed root-plugin source.

`critique:codex-plugin-hook-config-review#FIND-002` found one high-severity
remote-install blocker under the prior top-level-rules model. `decision:0005`
changes the product model so installed plugin skills can carry the mandatory
bootstrap doctrine. Follow-up critique must verify the new model.

Disposition status: deferred by operator acceptance at closure

Deferral / not-required rationale:

Installed plugin skill invocation and `loom-bootstrap` discovery were not
revalidated in this ticket before closure. Operator accepted this as residual
release-packaging risk; future broad Codex packaging should revalidate from
current runtime behavior.

# Wiki Disposition

Wiki promotion is not required for this prototype closure. Future accepted Codex
packaging behavior should be promoted through the adapter-package explanation
surface if it becomes a supported install path.

# Acceptance Decision

Accepted by: operator
Accepted at: 2026-04-28T18:50:38Z
Basis: Operator stated the remaining open install-adapter work was completed and accepted closing this prototype with no further action in this ticket. The record preserves prior Codex evidence, model decisions, and deferred validation limits rather than claiming fresh runtime proof.
Residual risks: Installed Git-backed plugin skill discovery for `loom-bootstrap`, plugin namespace/selector behavior, updated hook-path startup probing, and broad-release package-layout validation were not revalidated in this closure pass.

# Dependencies

Uses `research:loom-install-distribution-methods`,
`research:codex-command-skill-installation`,
`research:codex-plugin-distribution-surfaces`,
`evidence:codex-sessionstart-stdout-context`, prior direct install work from
`ticket:ffg8elkb`, and generated adapter work from `ticket:p9m4x2qt`. No hard
ticket prerequisite blocks acceptance review.

# Journal

- 2026-04-25: created as the Codex harness ticket under
  `plan:install-experience-harness-adapters`.
- 2026-04-26: expanded with focused Codex plugin research. Initial research
  routed toward a package-layout spike with rules in `AGENTS.md`; later hook
  research superseded that route with plugin-plus-hook-config evidence.
- 2026-04-26: implemented repository-root Codex plugin metadata, local
  marketplace metadata, project `.codex/config.toml`, and per-rule
  `.codex/hooks.json`. Runtime `codex-cli 0.125.0` startup probe saw all seven
  Loom rule files through `SessionStart` hook stdout. The ticket is now in
  `review_required` pending operator-clarity critique.
- 2026-04-26: critique found local marketplace `source.path: "./"` invalid for a
  repository-root plugin. Fixed the marketplace to use Codex's documented
  Git-backed `source: "url"` shape for root plugins and revalidated marketplace
  registration in a temporary `CODEX_HOME`.
- 2026-04-26: clarified the product goal as remote plugin install for normal Codex
  users, not repository-local proof. Source inspection found installed plugins do
  not own always-on hook/instruction loading in current Codex, so the ticket moved
  to `blocked` until remote rule delivery is possible or a separate installer is
  explicitly accepted.
- 2026-04-26: `decision:0005` repackaged mandatory doctrine as
  `loom-bootstrap`, resolving the plugin-owned-hook requirement as a product-model
  blocker. Ticket returned to `active`; next evidence is installed plugin skill
  discovery and updated hook-path validation.
- 2026-04-26: `decision:0006` removed fallback installers and command-wrapper
  product surfaces. Codex work now targets native plugin skill discovery only,
  with `.codex/hooks.json` as optional trusted-project preload proof.
- 2026-04-28T18:50:38Z: Operator accepted closure of the remaining open Codex
  prototype work. Closed with residual validation risks recorded; future Codex
  packaging changes should use a fresh ticket and current runtime evidence.
