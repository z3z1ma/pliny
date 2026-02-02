---
name: cli-command-removal-contract-checklist
description: Use when removing an entire CLI command/module (deleting a src/agent_loom/<command>/* subtree) to keep wiring, docs, and tests consistent and deterministic.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-02-02T21:09:13.316Z"
  updated_at: "2026-02-02T21:09:13.316Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
## When to use

- You are deleting an entire command/module directory (for example `src/agent_loom/init/`).
- You are removing a subcommand surface or renaming it in a way that breaks imports/tests/docs.

## Goal

Remove the command cleanly without leaving dangling UX contracts, imports, or docs.

## Checklist

1. Remove the wiring
   - Delete the command router/registration and any imports from the top-level CLI (for example `src/agent_loom/cli.py`).
   - Remove package exports / module glue (for example `src/agent_loom/init/__init__.py`).

2. Remove UX contract tests
   - Delete or update any focused UX contract tests that assert the removed command output.
   - If the command name/flags moved, update the tests to assert the new surface.

3. Remove stale procedural memory
   - Search `.opencode/skills/` for references to deleted paths (for example `src/agent_loom/init/cli.py`).
   - Update any referenced skills to either:
     - point at the new surface, or
     - explicitly mark the workflow as deprecated.

4. Keep output deterministic
   - If help text / command listing changed, ensure ordering stays stable.

5. Verification gate
   - `uv run basedpyright`
   - `uv run ruff check .`
   - `uv run pytest <the smallest relevant module(s)>`

## Common failure modes

- Broken imports due to deleted modules still referenced by the CLI router.
- Contract tests still asserting help/output for a command that no longer exists.
- Skills/docs referencing deleted paths.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
