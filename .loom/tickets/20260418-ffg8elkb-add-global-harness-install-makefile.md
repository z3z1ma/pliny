---
id: ticket:ffg8elkb
kind: ticket
status: closed
created_at: 2026-04-18T03:03:47Z
updated_at: 2026-04-19T23:34:12Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  research:
    - research:harness-install-surfaces
  related:
    - ticket:p9m4x2qt
depends_on: []
---

# Summary

Add a repository Makefile that installs and uninstalls Loom's canonical
`rules/`, `skills/`, and `commands/` surfaces into the correct user-level
harness locations for OpenCode, Claude Code, Codex, and Gemini CLI.

# Context

The product surface to ship is the top-level protocol bundle, not dogfooded
`.loom/` records or `.opencode/` consumption state.

The harnesses do not expose identical configuration models, so the installer has
to map Loom into each harness honestly.

# Why Now

The repository already teaches a harness-agnostic installation model, but it
does not yet give operators one simple command to install the shipped bundle
globally across the harnesses the maintainer actively uses.

# Scope

- add a top-level `Makefile`
- implement `install` and `uninstall` as phony targets
- accept `harness=<name>` with at least `opencode`, `claude`, `codex`,
  `gemini`, and `all`
- copy canonical `rules/`, `skills/`, and optional `commands/` from the current
  repository into harness-specific user config locations
- perform the smallest required translation when a harness does not accept the
  Loom files verbatim

# Non-goals

- do not install dogfooding `.loom/` or `.opencode/` state
- do not redesign Loom's shipped directory structure to fit one harness better
- do not add a hidden helper script as the primary implementation surface
- do not claim semantic parity where a harness only supports an approximate
  mapping

# Acceptance Criteria

- `make install harness=<name>` installs Loom for each supported harness using
  the canonical top-level directories in the current working tree
- `make uninstall harness=<name>` removes only Loom-managed install content for
  that harness
- `Makefile` declares both `install` and `uninstall` as phony targets
- OpenCode, Claude Code, Codex, and Gemini CLI mappings are documented and the
  implementation matches the researched install surfaces
- any required format translation is small, inspectable, and kept inside the
  Makefile

# Execution Notes

1. Implement shared path variables from `$(CURDIR)` so the installer copies the
   current repository bundle.
2. Use direct copies where possible.
3. For OpenCode, ensure global config points at the installed Loom rules.
4. For Codex, map Loom rules into a Loom-marked `AGENTS.md` block and Loom
   commands into prompt files if that surface remains worth supporting.
5. For Gemini CLI, convert Markdown commands into TOML command definitions.
6. Update install docs if the new Makefile materially changes the recommended
   adoption path.

# Evidence

Evidence gathered:

- manual review of `Makefile`, `scripts/install-loom.sh`, and `INSTALL.md`
  against the researched harness docs
- `HOME=<tempdir> make install harness=all` completed successfully in a throwaway
  home directory
- `HOME=<tempdir> make uninstall harness=all` completed successfully in the same
  throwaway home directory
- spot-checks confirmed:
  - OpenCode wrote `~/.config/opencode/opencode.json` with Loom rules under
    `instructions`
  - Claude installed rules under `~/.claude/rules/loom/`
  - Codex originally installed prompts under `~/.codex/prompts/` and mirrored
    Loom rules into `~/.codex/AGENTS.md`; follow-up `ticket:p9m4x2qt`
    superseded the prompt portion with explicit-only command adapter skills
  - Gemini installed TOML commands under `~/.gemini/commands/` and mirrored
    Loom rules into `~/.gemini/GEMINI.md`

# Critique Disposition

Critique is optional. The change is meaningful but narrowly scoped to packaging
and harness compatibility rather than core Loom doctrine.

# Wiki Disposition

Wiki follow-through is not expected unless the Makefile introduces a new durable
cross-harness installation pattern worth preserving beyond `INSTALL.md`.

# Dependencies

- `research:harness-install-surfaces` for the real target locations and format
  differences

# Journal

- 2026-04-18: created `ticket:ffg8elkb` to add a harness-aware global install
  and uninstall Makefile for the canonical Loom bundle.
- 2026-04-18: added `Makefile`, added `scripts/install-loom.sh`, updated
  `INSTALL.md`, and validated install/uninstall across OpenCode, Claude Code,
  Codex, and Gemini CLI using a throwaway `HOME`.
- 2026-04-19: follow-up ticket `ticket:p9m4x2qt` superseded the original Codex
  prompt conversion with explicit-only Codex command adapter skills.
- 2026-04-19: closed per user confirmation that this ticket is completed.
