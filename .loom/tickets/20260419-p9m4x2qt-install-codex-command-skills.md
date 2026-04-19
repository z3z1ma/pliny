---
id: ticket:p9m4x2qt
kind: ticket
status: closed
created_at: 2026-04-19T21:59:26Z
updated_at: 2026-04-19T23:34:12Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  research:
    - research:codex-command-skill-installation
  related:
    - ticket:ffg8elkb
depends_on: []
---

# Summary

Update the Codex harness installer so Loom commands are installed as
explicit-only Codex skills instead of deprecated prompt files.

# Context

The existing global installer copies canonical Loom skills into
`$HOME/.agents/skills` and converts top-level commands into
`~/.codex/prompts/*.md`.

Codex's current extension surface is skills. The command layer still matters,
but it should be represented as user-invoked command adapter skills rather than
legacy prompt files.

# Why Now

The operator identified that Codex custom prompts have been deprecated in favor
of skills and requested research before changing the installer.

# Scope

- update `scripts/install-loom.sh` Codex install/uninstall behavior
- generate command adapter skills from `commands/*.md`
- disable implicit invocation for generated Codex command adapter skills
- remove Loom-managed legacy prompt files during install and uninstall
- update install documentation and research records

# Non-goals

- do not remove top-level `commands/`, because other harnesses still use them
- do not rename canonical lower-level Loom skills
- do not make command adapter skills implicit behavior triggers
- do not change OpenCode, Claude Code, or Gemini behavior beyond shared wording

# Acceptance Criteria

- `make install harness=codex` installs canonical skills and generated
  `loom-command-*` adapter skills under `$HOME/.agents/skills`
- each generated adapter includes `agents/openai.yaml` with
  `policy.allow_implicit_invocation: false`
- `make install harness=codex` removes old Loom-managed prompt files from
  `~/.codex/prompts`
- `make uninstall harness=codex` removes generated adapter skills and old
  Loom-managed prompt files
- installer documentation no longer claims Codex commands install as
  `~/.codex/prompts/*.md`

# Execution Notes

- Generate non-colliding adapter names such as `loom-command-research` because
  `loom-research` and `loom-wiki` already exist as canonical lower-level skills.
- Preserve the original command name in generated metadata and Codex interface
  display metadata.

# Evidence

Evidence gathered:

- official Codex skills docs reviewed
- `bash -n scripts/install-loom.sh` passed
- `HOME=<tempdir> make install harness=codex` completed successfully
- 11 command source files produced 11 generated `loom-command-*` adapter skills
- spot-check confirmed canonical `loom-research` and generated
  `loom-command-research` both exist without collision
- spot-check confirmed generated `agents/openai.yaml` includes
  `policy.allow_implicit_invocation: false`
- spot-check confirmed install left no `~/.codex/prompts` directory in the temp
  home
- `HOME=<tempdir> make uninstall harness=codex` completed successfully
- post-uninstall checks confirmed no remaining temp-home `~/.codex/AGENTS.md`,
  `~/.agents/skills`, or `~/.codex/prompts`

# Critique Disposition

Critique is recommended but not mandatory. This is a meaningful installer
behavior change, but the scope is narrow and validation can inspect generated
artifacts directly.

# Wiki Disposition

Wiki follow-through is optional unless this command-adapter pattern becomes a
durable concept beyond the installer documentation.

# Dependencies

- `research:codex-command-skill-installation`
- `research:harness-install-surfaces`

# Journal

- 2026-04-19: created the ticket and focused Codex skills research record after
  reviewing current OpenAI Codex skills guidance.
- 2026-04-19: updated the installer to generate explicit-only Codex command
  adapter skills and remove Loom-managed legacy Codex prompt files.
- 2026-04-19: validated Codex install and uninstall behavior with a throwaway
  `HOME` and moved the ticket to `complete_pending_acceptance`.
- 2026-04-19: closed per user confirmation that this ticket is completed.
