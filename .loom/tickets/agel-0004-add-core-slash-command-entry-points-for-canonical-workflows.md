---
{
  "created_at": "2026-04-04T23:57:49Z",
  "id": "ticket:0004",
  "kind": "ticket",
  "links": {
    "initiative": [
      "initiative:prove-core-loom-workflow"
    ],
    "plan": [
      "plan:bootstrap-core-workflow-backlog"
    ],
    "spec": [
      "spec:minimum-proven-core-workflow-surface"
    ],
    "ticket": [
      "ticket:0003"
    ]
  },
  "repository_scope": {
    "kind": "repository",
    "repository_id": "repo:root"
  },
  "schema_version": 1,
  "status": "proposed",
  "updated_at": "2026-04-04T23:58:09Z"
}
---

# Summary

Add the smallest useful set of slash-command entry points for canonical Loom
workflows so operators can create or advance core records and review flows
without discovering everything from skill surfaces alone.

# Context

The shipped product already includes skills and scripts for canonical record
work, critique, docs, and workspace operations, but `src/commands/` currently
contains only `loom-memory-reflect` and `loom-memory-housekeeping`.

This makes the most routine non-memory workflows harder to discover than they
need to be, especially for a repository whose product surface is meant to teach
the operator what to do next.

# Why This Work Matters Now

Once `ticket:0003` proves one real workflow slice, the next highest-leverage
improvement is to expose that path through a small, obvious command surface.
That improves operator usability without introducing a hidden runtime or a
monolithic CLI.

# Scope

- define a minimal command family for root canonical actions that the current
  product already supports, likely covering ticket work plus critique and docs
  follow-through, and any small supporting record action the proof slice shows
  is truly needed
- keep command files as pure Markdown prompt definitions under `src/commands/`
- route each command to the owning skill and package-local paths only
- commands should guide the agent to use standard tools for record population,
  content editing, and workflow orchestration; Python scripts should only be
  invoked for structural validation, link checks, and frontmatter scaffolding
- add or refresh references where command discoverability would otherwise remain
  weak

# Non-goals

- do not build runtime orchestration or shell-heavy wrappers
- do not create commands for every skill just for symmetry
- do not duplicate full skill manuals inside command files
- do not point operators at build-only or repo-root-only paths that would not
  ship with the bundle

# Acceptance Criteria

- `src/commands/` contains a small set of core workflow commands beyond the two
  current memory commands
- each new command has a clear trigger surface and routes to the correct owning
  skill
- command guidance stays consistent with skill docs and package-local script
  paths
- assembly and structural verification still pass after the additions

# Implementation Plan

1. Use the result of `ticket:0003` to choose the smallest stable command set.
2. Draft the new command files under `src/commands/`.
3. Update any affected references so the command surface is discoverable and not
   contradictory.
4. Run assembly and repository validation.
5. Reconcile the ticket with the accepted command set and any remaining follow-up
   scope.

# Dependencies

- `ticket:0003` should land first or at least narrow the minimal command set
- existing skill-local create, critique, docs, and validation scripts already
  distributed through the bundle
- the repository's current command-file style and package-local path rules

# Risks / Edge Cases

- command sprawl if the set is chosen before the proof slice teaches what is
  actually needed
- drift between command prompts and skill instructions over time
- overprescribing harness-specific behavior in what should remain portable prompt
  guidance

# Verification

Expected verification for this ticket includes:

- `python3 build/assemble-skills.py`
- `uvx ruff check build/ src/`
- manual comparison of the new command prompts against the owning skill docs and
  bundled script references

There is no separate command runner test harness in this repo, so consistency
with shipped docs and structure is the main quality bar.

# Documentation Disposition

The command files themselves are operator-facing documentation.

Additional canonical docs should only be created if this ticket reveals a wider
accepted workflow explanation that does not fit cleanly inside the commands and
skill references alone.

# Journal

- 2026-04-04: created `ticket:0004` as the proposed follow-up for turning the
  proved core workflow path into a discoverable command surface inside the
  shipped bundle.
- 2026-04-04: updated scope to reinforce that commands guide the agent to use
  standard tools for all record work; Python scripts are invoked only for
  structural validation, link checks, and frontmatter scaffolding.
