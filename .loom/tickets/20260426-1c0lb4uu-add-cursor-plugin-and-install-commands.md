---
id: ticket:1c0lb4uu
kind: ticket
status: closed
change_class: release-packaging
risk_class: medium
created_at: 2026-04-26T07:47:49Z
updated_at: 2026-04-26T07:53:38Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:loom-install-experience
  plan:
    - plan:install-experience-harness-adapters
  decision:
    - decision:0006
  related:
    - ticket:jt2vy25y
    - ticket:lx9nnztk
  evidence:
    - evidence:cursor-plugin-install-validation
  critique:
    - critique:cursor-plugin-install-doc-review
depends_on: []
---

# Summary

Add Cursor's native plugin manifest for Loom's skills-only product surface and
make install docs expose one-line native install commands for supported harnesses.

# Context

`decision:0006` makes `skills/` the product surface. Cursor docs and Superpowers'
Cursor plugin both use `.cursor-plugin/plugin.json` with `skills: "./skills/"` for
plugin-packaged skills. Loom should provide the same native manifest without
reintroducing fallback installers or command-wrapper surfaces.

# Scope

- add `.cursor-plugin/plugin.json`
- document one-line native install commands or native install entries for Claude,
  OpenCode, Codex, and Cursor
- keep Codex and Cursor validation/listing caveats truthful
- update Cursor adapter fixture notes
- validate JSON, OpenCode smoke, Claude plugin validation, npm package dry-run, and
  diff whitespace

# Non-goals

- do not restore Makefile, shell installer, top-level `commands/`, or top-level
  `rules/`
- do not claim Cursor marketplace listing before it exists
- do not claim Codex installed plugin skill discovery before `ticket:lx9nnztk`
  validates it

# Acceptance Criteria

- Cursor plugin manifest exists and points at `skills/`
- Cursor plugin manifest does not auto-load Claude-specific root hooks
- install docs include concise one-line install paths for Claude, OpenCode, Codex,
  and Cursor
- docs distinguish accepted install paths from validation/listing targets
- validation passes

# Evidence

Expected:

- JSON validation for plugin manifests
- `node open-loom.mjs --smoke`
- `claude plugin validate /Users/alexanderbutler/code_projects/personal/agent-loom`
- `npm pack --dry-run`
- `git diff --check`

Observed:

- JSON validation passed for present manifests, including `.cursor-plugin/plugin.json`.
- `node open-loom.mjs --smoke` passed.
- `claude plugin validate /Users/alexanderbutler/code_projects/personal/agent-loom` passed.
- `npm pack --dry-run` passed.
- `git diff --check` passed.

# Critique Disposition

Critique policy: recommended

Rationale: release packaging docs and manifest changes can mislead users if they
overclaim native install support.

Disposition: completed in `critique:cursor-plugin-install-doc-review`; no blockers
remain after adding `hooks: {}` to prevent Cursor from auto-discovering Claude
hooks.

# Acceptance Decision

Accepted by: OpenCode agent implementing operator directive
Accepted at: 2026-04-26T07:53:38Z
Basis: `evidence:cursor-plugin-install-validation`,
`critique:cursor-plugin-install-doc-review`, Cursor docs lookup, Superpowers
manifest comparison, JSON validation, OpenCode smoke, Claude plugin validation,
npm dry run, and diff whitespace check.
Residual risks: Cursor runtime plugin loading and Marketplace listing are not
validated; Codex installed plugin skill discovery remains in `ticket:lx9nnztk`.

# Journal

- 2026-04-26: created for Cursor plugin manifest and native install command docs.
- 2026-04-26: closed after adding skills-only Cursor manifest, install commands,
  evidence, and critique disposition.
