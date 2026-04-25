---
id: ticket:6uy1rx20
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
  opencode_docs:
    - https://opencode.ai/docs/config/
    - https://opencode.ai/docs/plugins/
    - https://opencode.ai/docs/skills/
    - https://opencode.ai/docs/commands/
depends_on: []
---

# Summary

Finalize OpenCode's Loom install path as a direct config install, including the
decision about whether OpenCode should consume shared `~/.agents/skills` or keep
OpenCode-native skill copies under `~/.config/opencode/skills`.

# Context

`research:loom-install-distribution-methods` concludes that OpenCode should not
be forced into a plugin package. OpenCode plugins are JavaScript/TypeScript hook
modules and runtime extension points. Loom is a static Markdown protocol bundle,
and OpenCode already has direct config support for always-on instructions,
skills, and commands.

The current installer copies rules to `~/.config/opencode/loom/rules`, copies
skills to `~/.config/opencode/skills`, copies commands to
`~/.config/opencode/commands`, and updates `~/.config/opencode/opencode.json`
so the rule glob appears in `instructions`.

# Why Now

OpenCode is the harness where the correct answer may be to avoid a first-class
plugin package. The install initiative needs one ticket that makes that decision
explicit, hardens the direct path, and prevents future agents from re-opening an
OpenCode plugin design just for symmetry with Cursor or Gemini.

# Scope

- confirm the direct OpenCode install path remains the preferred path
- decide whether skills should stay under `~/.config/opencode/skills` or move to
  or additionally use generic `~/.agents/skills`
- keep ordered Loom rules loaded through `opencode.json` `instructions`
- keep optional commands as Markdown files under OpenCode's documented command
  directory
- document why OpenCode JS/TS plugins are rejected as the primary Loom install
  mechanism
- update `INSTALL.md`, adapter fixtures, and shell fallback behavior only where
  needed to reflect the direct-config decision
- validate install/uninstall behavior in a temporary `HOME` if installer behavior
  changes

# Non-goals

- do not create an OpenCode JS/TS plugin package for Loom's static Markdown
  surfaces
- do not add runtime hooks, custom tools, Bun dependencies, or node package
  behavior to Loom core
- do not remove OpenCode-native skill copies unless shared Agent Skills behavior
  is validated and documented
- do not change canonical Loom rules, skills, or commands for OpenCode
- do not let `opencode.json` become the source of Loom semantics

# Acceptance Criteria

- the ticket records a clear OpenCode recommendation: native skill directory,
  shared `~/.agents/skills`, both, or another documented direct-config shape
- OpenCode rules are loaded through the documented `instructions` array or an
  equally documented always-on instruction mechanism
- optional commands remain Markdown command files compatible with OpenCode's
  command surface
- OpenCode plugin rejection is documented with source-backed rationale
- install/uninstall validation passes in a temporary `HOME` if the shell fallback
  changes
- generated or copied OpenCode surfaces remain Loom-managed and reversible
- `INSTALL.md` reflects the accepted OpenCode path and its relationship to any
  shared Agent Skills destination

# Coverage

Covers:

- None - no spec-owned acceptance IDs exist. This ticket consumes
  `research:loom-install-distribution-methods#opencode` and owns ticket-local
  acceptance criteria for the OpenCode install slice.

# Claim Matrix

None - no evidence exists yet for the final OpenCode decision.

# Execution Notes

OpenCode facts to preserve from research:

- global config lives at `~/.config/opencode/opencode.json`
- `instructions` accepts paths and glob patterns for always-on instructions
- global commands live in `~/.config/opencode/commands/`
- global skills live in `~/.config/opencode/skills/<name>/SKILL.md`
- OpenCode also discovers compatible skills from `~/.agents/skills` and other
  agent-compatible locations
- OpenCode plugins are JS/TS modules for hooks, events, tools, environment, and
  TUI behavior, not documented static bundles of rules, skills, and commands

Likely implementation choices:

- keep direct `opencode.json` instruction wiring
- decide whether to preserve OpenCode-native skill copy for least surprise or use
  shared `~/.agents/skills` for cross-harness deduplication
- keep Markdown command copies as direct command adapters
- document OpenCode as the intentionally direct install outlier

# Blockers

None.

# Next Move / Next Route

Ralph implementation packet.

# Ralph Readiness

Bounded iteration:
Finalize and validate OpenCode's direct install recommendation, including the
shared Agent Skills decision and any needed documentation or fallback installer
adjustment.

Write boundary:
OpenCode-specific installer/docs/fixture paths, `INSTALL.md`, `examples/adapters/`
if used for fixtures, `scripts/install-loom.sh` only for a small proven fallback
adjustment, and this ticket/evidence records. Read-only source inputs are
`rules/`, `skills/`, and `commands/`.

Likely verification posture:
Observation-first structural validation plus temporary `HOME` install/uninstall
checks if installer behavior changes.

Expected output contract:
Chosen OpenCode recommendation, changed files, validation commands and results,
explicit plugin rejection rationale, limitations, and ticket state recommendation.

# Evidence

Expected evidence:

- `opencode.json` instruction-array inspection in a temporary `HOME` if changed
- installed rule, skill, and command path inspection
- shared `~/.agents/skills` precedence or compatibility note if selected
- `git diff --check`
- explicit limitation if OpenCode runtime discovery cannot be validated

# Critique Disposition

Risk class: medium

Critique policy: recommended

Policy rationale:
OpenCode's ticket may look simpler than the plugin tickets, but the shared skill
destination decision can affect multiple harnesses and operator expectations.

Required critique profiles:

- operator-clarity

Findings:

None - no critique yet.

Disposition status: pending

Deferral / not-required rationale:

None.

# Wiki Disposition

Wiki promotion is optional. Promote only if the direct-config-versus-plugin
decision becomes a reusable adapter-design principle.

# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:

# Dependencies

Uses `research:loom-install-distribution-methods` and prior direct OpenCode
install proof from `ticket:ffg8elkb`. No hard ticket prerequisite blocks starting
this work, though the plan recommends running it after Cursor/Gemini package
prototypes clarify shared skill handling.

# Journal

- 2026-04-25: created as the OpenCode harness ticket under
  `plan:install-experience-harness-adapters`.
