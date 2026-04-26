---
id: ticket:7ex8w32y
kind: ticket
status: closed
change_class: release-packaging
risk_class: medium
created_at: 2026-04-25T18:46:08Z
updated_at: 2026-04-26T08:26:59Z
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
  evidence:
    - evidence:gemini-extension-validation
  critique:
    - critique:gemini-extension-review
external_refs:
  gemini_cli_docs:
    - https://geminicli.com/docs/extensions/
    - https://geminicli.com/docs/extensions/reference/
    - https://geminicli.com/docs/extensions/writing-extensions/
    - https://geminicli.com/docs/cli/gemini-md/
    - https://geminicli.com/docs/cli/skills/
depends_on: []
---

# Summary

Prototype a first-class Gemini CLI extension install path for Loom that exposes
canonical `skills/` and preloads the ordered `loom-bootstrap` references through
Gemini's native `contextFileName` mechanism.

# Context

`research:loom-install-distribution-methods` identifies Gemini CLI extensions as
a strong first-class package candidate. `decision:0006` removes fallback copy
installers and top-level command wrappers from the product surface, so this ticket
tests only the native extension shape: `gemini-extension.json`, bundled `skills/`,
and optional bootstrap preload via extension context.

# Why Now

Gemini is one of the best proving grounds for a first-class adapter package
because its extension format includes Loom's current install needs:

- context file for ordered bootstrap preload
- `skills/` for Agent Skills
- documented install, link, disable, enable, and update commands

# Scope

- design a Gemini extension package or fixture derived from canonical Loom
  `skills/`
- create `gemini-extension.json` with appropriate metadata and context file
  configuration
- write an extension context file that imports bootstrap references in numeric
  order
- rely on repository `skills/` as the extension-bundled skill directory
- preserve source provenance in context outputs by importing canonical references
- validate extension structure and, if available, local `gemini extensions link`
  or `gemini extensions install` behavior
- update install docs and adapter fixture notes for the Gemini decision

# Non-goals

- do not add MCP servers, hooks, themes, or sub-agents to the Loom extension
  unless this ticket is explicitly revised
- do not publish a Gemini extension gallery entry
- do not restore direct Gemini fallback installers or top-level command wrappers
- do not change canonical Loom skills to satisfy Gemini formatting
- do not treat extension context as canonical Loom behavior

# Acceptance Criteria

- a Gemini extension package exists, or the ticket records a supported reason why
  an extension cannot currently express Loom install needs
- `gemini-extension.json` matches the documented manifest shape
- extension context preserves ordered bootstrap preload through canonical reference
  imports
- skills remain Agent Skill directories with `SKILL.md` and supporting files
- validation demonstrates package structure and context imports are inspectable
- install/link/disable validation is run with Gemini CLI when available, or the
  ticket records why only structural validation was possible
- `INSTALL.md` or adapter examples reflect the proven Gemini recommendation

# Coverage

Covers:

- None - no spec-owned acceptance IDs exist. This ticket consumes
  `research:loom-install-distribution-methods#gemini-cli` and owns ticket-local
  acceptance criteria for the Gemini extension slice.

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| Gemini extension can expose canonical Loom skills. | `evidence:gemini-extension-validation` | `critique:gemini-extension-review` | supported |
| Gemini extension can preload ordered bootstrap references via `contextFileName`. | `evidence:gemini-extension-validation` | `critique:gemini-extension-review` | supported |

# Execution Notes

Gemini facts to preserve from research:

- extensions load from `<home>/.gemini/extensions`; installed extensions are
  copied, while linked local extensions are symlinked
- `gemini-extension.json` can name `contextFileName`; if omitted and `GEMINI.md`
  exists, `GEMINI.md` is loaded
- skills can live in extension `skills/` and are lower precedence than workspace
  and user skills

Likely implementation shape:

- add root `gemini-extension.json`
- add configured extension context file that imports ordered
  `skills/loom-bootstrap/references/*.md`
- rely on root `skills/` for extension-bundled skills

# Blockers

None.

# Next Move / Next Route

Closed after local edit, structural validation, temp-home link/list and disable
validation, and recommended critique.

# Ralph Readiness

Bounded iteration:
Prototype and validate a Gemini CLI extension package or fixture for Loom, then
update Gemini install guidance with the proven path and limitations.

Write boundary:
Gemini extension manifest/context files, `INSTALL.md`, `examples/adapters/`, and
this ticket/evidence records. Read-only source inputs are `skills/`, especially
`skills/loom-bootstrap/references/`.

Likely verification posture:
Observation-first structural validation plus Gemini CLI local extension link or
install validation when available.

Expected output contract:
Changed files, extension structure summary, bootstrap context import behavior,
validation commands and results, limitations, recommendation for Gemini install
path, and ticket state recommendation.

# Evidence

Expected evidence:

- structural check of `gemini-extension.json`
- inspection of extension context imports
- check that bundled skills retain `SKILL.md`, references, and templates
- `git diff --check`
- `gemini extensions validate` and `gemini extensions link` or equivalent if
  available
- explicit limitation if Gemini CLI runtime validation cannot be run

Observed evidence:

- `evidence:gemini-extension-validation`
- JSON validation for manifests
- `gemini extensions validate /Users/alexanderbutler/code_projects/personal/agent-loom`
- temp-home `gemini extensions link` and `gemini extensions list`
- temp-home `gemini extensions disable agent-loom` and `gemini extensions list`
- `node open-loom.mjs --smoke`
- `claude plugin validate /Users/alexanderbutler/code_projects/personal/agent-loom`
- `git diff --check`

# Critique Disposition

Risk class: medium

Critique policy: recommended

Policy rationale:
This is a meaningful install-path change. Incorrect extension context behavior
could make users believe Loom bootstrap doctrine is preloaded when it is not.

Required critique profiles:

- operator-clarity

Findings:

`critique:gemini-extension-review` found no remaining blockers after moving Claude
hooks out of root `hooks/` and simplifying `gemini-extension.json` to documented
Gemini fields.

Disposition status: completed

Deferral / not-required rationale:

None.

# Wiki Disposition

Wiki promotion is optional. If Gemini extension packaging becomes the first
accepted full adapter-package pattern, promote the reusable adapter-package
pattern through retrospective.

# Acceptance Decision

Accepted by: OpenCode agent implementing operator directive
Accepted at: 2026-04-26T08:26:59Z
Basis: `evidence:gemini-extension-validation`, `critique:gemini-extension-review`,
Gemini docs lookup, `gemini extensions validate`, temp-home link/list and disable
validation, JSON validation, OpenCode smoke, Claude plugin validation, and diff
whitespace check.
Residual risks: runtime model-context expansion of `gemini-bootstrap.md` imports
was not directly inspected; remote `gemini extensions install
https://github.com/z3z1ma/agent-loom` was not run because it depends on pushed
repository state.

# Dependencies

Uses `research:loom-install-distribution-methods` and prior direct Gemini install
proof from `ticket:ffg8elkb`. No hard ticket prerequisite blocks starting this
prototype.

# Journal

- 2026-04-25: created as the Gemini CLI harness ticket under
  `plan:install-experience-harness-adapters`.
- 2026-04-26: updated for `decision:0006`; scope is now native extension with
  `skills/` plus `contextFileName` bootstrap preload, not fallback installers or
  command conversion.
- 2026-04-26: closed after Gemini extension manifest/context implementation,
  root-hook collision fix, temp-home link/list and disable validation, and
  critique acceptance.
