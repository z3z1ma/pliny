---
id: ticket:q7xyjztn
kind: ticket
status: closed
created_at: 2026-04-18T02:58:42Z
updated_at: 2026-04-19T23:34:12Z
scope:
  kind: repository
  repositories:
    - repo:root
links: {}
depends_on: []
---

# Summary

Add a repository Makefile that installs and uninstalls Loom's rules, skills,
and commands into the global config locations used by OpenCode, Claude Code,
Codex, and Gemini CLI.

# Context

This repository ships a Markdown-first Loom bundle, but it does not yet expose
one thin install surface for copying the current `rules/`, `skills/`, and
`commands/` directories into the harness-specific global paths the operator is
already using.

The install surface needs to stay thin, prefer plain filesystem operations,
and adapt only where harnesses expect different instruction or command shapes.

# Why Now

The operator explicitly wants one `make install harness=...` flow that works
against the harnesses already in use on this machine, plus an uninstall path
that can cleanly reverse the Loom-specific install.

# Scope

- research the relevant global config locations and formats for OpenCode,
  Claude Code, Codex, and Gemini CLI
- add a root `Makefile` with phony `install` and `uninstall` targets
- support a `harness=` selector for individual harnesses and an aggregate mode
- keep the implementation shell-first, using inline Python only where small
  format adaptation or config merging is genuinely needed

# Non-goals

- do not introduce a build pipeline or helper runtime beyond the Makefile
- do not redesign Loom's rules, skills, or command corpus itself
- do not overwrite unrelated user configuration beyond the smallest necessary
  Loom-specific integration points

# Acceptance Criteria

- `make install harness=<name>` works for `opencode`, `claude`, `codex`,
  `gemini`, and an aggregate mode
- `make uninstall harness=<name>` removes only the Loom-specific installation
  for that harness
- the Makefile copies `rules/`, `skills/`, and `commands/` into harness-specific
  global locations, adapting formats only where the harness requires it
- harness-specific root instruction/config files are updated truthfully and with
  minimal collateral impact
- manual verification shows the generated paths and adapted files match the
  researched harness expectations

# Execution Notes

1. Inspect the current global harness directories on disk before choosing the
   install strategy.
2. Prefer direct copies for skills and commands where the harness accepts the
   current Markdown shape.
3. Use a small generated wrapper or inline conversion only where the harness
   expects a different root instruction or command format.
4. Verify the Makefile with dry-run-style installs into a temporary HOME.

# Evidence

Expected evidence for this ticket includes:

- cited harness path and format expectations from current docs or source
- the resulting `Makefile`
- manual install/uninstall checks in a temporary HOME

# Critique Disposition

Critique is recommended because this changes the operator-facing install flow
across multiple harnesses.

# Wiki Disposition

Wiki follow-through is optional unless the final install model becomes the
accepted long-term operator path that future agents will need to read.

# Dependencies

- current harness docs and local config directories
- current `rules/`, `skills/`, and `commands/` distribution surfaces in this
  repository

# Journal

- 2026-04-18: created `ticket:q7xyjztn` and marked it active for the Makefile-
  based multi-harness global install work.
- 2026-04-19: closed per user confirmation that this ticket is completed.
