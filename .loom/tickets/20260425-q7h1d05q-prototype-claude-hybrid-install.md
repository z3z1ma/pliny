---
id: ticket:q7h1d05q
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
  claude_code_docs:
    - https://code.claude.com/docs/en/plugins
    - https://code.claude.com/docs/en/settings
    - https://code.claude.com/docs/en/hooks
    - https://code.claude.com/docs/en/skills
    - https://code.claude.com/docs/en/memory
depends_on: []
---

# Summary

Prototype and decide a Claude Code hybrid Loom install path that uses Claude's
native skill/plugin surfaces where they fit while keeping ordered always-on Loom
rules in a real Claude instruction surface.

# Context

Claude Code has strong first-class extension support, but
`research:loom-install-distribution-methods` did not find plugin docs showing a
clean way for a plugin alone to install arbitrary always-on Loom rules. Claude's
documented static instruction surfaces are `CLAUDE.md` and user/project rules,
while plugin support is attractive for skills, commands, namespacing, and
marketplace distribution.

The current installer directly copies rules to `~/.claude/rules/loom`, skills to
`~/.claude/skills`, and commands to `~/.claude/commands`. This ticket should
decide whether that direct shape remains best, or whether a hybrid plugin plus
separate rule installation is better.

# Why Now

Claude plugin support is likely the most tempting first-class install surface,
but it must not be allowed to obscure Loom's always-on rule requirement. The
project needs a clear Claude-specific decision before changing the installer or
documenting plugin installation as the recommended path.

# Scope

- compare three Claude install shapes against current docs and local feasibility:
  direct `~/.claude/rules/loom` plus `~/.claude/skills` and `~/.claude/commands`,
  plugin for skills/commands plus direct user rules, and plugin for skills/commands
  plus a managed `~/.claude/CLAUDE.md` import
- prototype a Claude plugin or fixture only if it improves the direct install
  story without hiding rule loading
- preserve ordered always-on Loom rules through `CLAUDE.md` or user rules rather
  than hooks
- preserve skills as `SKILL.md` directories
- preserve commands as explicit invocation wrappers or plugin command equivalents
- document why hooks are rejected for static rule loading unless new docs change
  that conclusion
- update install docs and shell fallback only after the chosen hybrid or direct
  path is evidenced

# Non-goals

- do not use Claude hooks to inject static Loom rules
- do not set a plugin custom agent as a substitute for installing Loom's rule
  corpus unless the ticket is explicitly reframed with evidence
- do not publish a Claude plugin marketplace package
- do not require managed enterprise settings for normal user install
- do not change canonical Loom source files to fit Claude packaging

# Acceptance Criteria

- the ticket records a clear Claude recommendation: direct install, hybrid plugin
  plus user rules, hybrid plugin plus `CLAUDE.md` import, or a justified deferral
- the chosen path preserves ordered always-on Loom rules through a documented
  Claude static instruction surface
- if a plugin fixture is created, `.claude-plugin/plugin.json` and component
  paths match Claude plugin docs
- skills remain discoverable `SKILL.md` directories in the chosen path
- optional commands remain explicit invocation surfaces and do not become protocol
  owners
- hook-based loading is explicitly rejected or justified with updated official
  evidence
- validation uses a temporary `HOME` or package fixture and records what could
  not be validated in actual Claude Code runtime
- `INSTALL.md` describes the chosen Claude path and its limitations

# Coverage

Covers:

- None - no spec-owned acceptance IDs exist. This ticket consumes
  `research:loom-install-distribution-methods#claude-code` and owns ticket-local
  acceptance criteria for the Claude install slice.

# Claim Matrix

None - no evidence exists yet for this Claude hybrid decision.

# Execution Notes

Claude facts to preserve from research:

- `~/.claude/CLAUDE.md` is a user instruction file and can import additional
  files with `@path`
- user-level rules live in `~/.claude/rules/`
- personal skills live in `~/.claude/skills/<skill-name>/SKILL.md`
- Claude plugins can include `skills/`, `commands/`, agents, hooks, MCP/LSP,
  monitors, `bin/`, and limited default settings
- plugin `settings.json` supports only `agent` and `subagentStatusLine` in the
  fetched docs
- hook docs say static context should use `CLAUDE.md` instead of `SessionStart`
  hooks

Likely implementation choices:

- if direct install remains best, harden docs and maybe fixture expectations
- if hybrid is better, create plugin/fixture for skills and commands while using
  `CLAUDE.md` or user rules for ordered Loom rules
- preserve current direct fallback until the hybrid path is proven

# Blockers

None.

# Next Move / Next Route

Ralph implementation packet.

# Ralph Readiness

Bounded iteration:
Prototype or structurally compare Claude direct and hybrid install paths, choose
one recommendation, and update Claude install documentation or fixtures.

Write boundary:
Claude adapter package or fixture paths, `INSTALL.md`, `examples/adapters/` if
used for fixtures, `scripts/install-loom.sh` only for a small proven fallback
adjustment, and this ticket/evidence records. Read-only source inputs are
`rules/`, `skills/`, and `commands/`.

Likely verification posture:
Observation-first structural validation plus temporary `HOME` install/uninstall
checks if direct user config mutation changes.

Expected output contract:
Chosen Claude install recommendation, changed files, validation commands and
results, explicit hook rejection or revised evidence, limitations, and ticket
state recommendation.

# Evidence

Expected evidence:

- structural inspection of any plugin fixture or direct install output
- ordered rule-loading path inspection through `CLAUDE.md` or user rules
- skill directory checks for `SKILL.md`
- command wrapper or plugin command inspection
- `git diff --check`
- explicit limitation if Claude runtime validation cannot be run

# Critique Disposition

Risk class: medium

Critique policy: recommended

Policy rationale:
Claude has multiple powerful extension mechanisms. The main risk is operator
confusion from calling a plugin install complete when always-on rules are not
actually installed.

Required critique profiles:

- operator-clarity

Findings:

None - no critique yet.

Disposition status: pending

Deferral / not-required rationale:

None.

# Wiki Disposition

Wiki promotion is optional. Promote only if the Claude hybrid decision becomes a
reusable pattern for other incomplete plugin systems.

# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:

# Dependencies

Uses `research:loom-install-distribution-methods` and prior direct Claude install
proof from `ticket:ffg8elkb`. No hard ticket prerequisite blocks starting this
prototype.

# Journal

- 2026-04-25: created as the Claude Code harness ticket under
  `plan:install-experience-harness-adapters`.
