---
id: evidence:command-route-wording-validation
kind: evidence
status: recorded
created_at: 2026-05-02T21:32:25Z
updated_at: 2026-05-02T21:37:28Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:cmdroute
  packet:
    - packet:ralph-ticket-cmdroute-20260502T213017Z
external_refs: {}
---

# Summary

Observation-first validation for `ticket:cmdroute`, checking product-surface
command/adaptor wording before and after replacing route-peer phrasing with owner
layer and workflow-route wording.

# Procedure

Observed during `packet:ralph-ticket-cmdroute-20260502T213017Z` on branch `main`.

Before edit commands:

```bash
rg -n "optional command|owner layer, workflow|workflow, or optional command" skills README.md
rg -n -i "(owner layers?.{0,80}(command|adapter|adaptor|mcp)|workflows?.{0,80}(command|adapter|adaptor|mcp)|(command|adapter|adaptor|mcp).{0,80}(owner layers?|workflow|route value|route token|route))" skills README.md
```

After edit commands:

```bash
rg -n "optional command|owner layer, workflow|workflow, or optional command" skills README.md
rg -n -i "(owner layers?.{0,80}(command|adapter|adaptor|mcp)|workflows?.{0,80}(command|adapter|adaptor|mcp)|(command|adapter|adaptor|mcp).{0,80}(owner layers?|workflow|route value|route token|route))" skills README.md
git diff --check
```

Parent follow-up command after adding intent-to-add entries for the new evidence
and packet records:

```bash
git add -N ".loom/evidence/20260502-command-route-wording-validation.md" ".loom/packets/ralph/20260502T213017Z-ticket-cmdroute-iter-01.md" && git diff --check
```

# Artifacts

## Before observations

Exact route-peer wording search:

```text
skills/loom-wiki/references/wiki-write.md:43:- recommended next owner layer, workflow, or optional command
skills/loom-wiki/references/wiki-audit.md:46:- recommended next owner layer, workflow, or optional command per finding
skills/loom-workspace/references/status-snapshot.md:24:6. Recommend the next owner layer, workflow, or optional command. When naming a
skills/loom-workspace/references/status-snapshot.md:137:- best next owner layer, workflow, or optional command and why
```

Broad command/adaptor route wording search:

```text
README.md:478:It is not a runtime, service, daemon, MCP server, product CLI, workflow engine, hidden database, or prompt dump.
skills/loom-ship/SKILL.md:14:commands may invoke that workflow but do not own it.
skills/loom-workspace/references/status-snapshot.md:24:6. Recommend the next owner layer, workflow, or optional command. When naming a
skills/loom-workspace/references/status-snapshot.md:118:  command/adapter names instead of route tokens
skills/loom-workspace/references/status-snapshot.md:137:- best next owner layer, workflow, or optional command and why
skills/loom-workspace/references/routing.md:59:Commands are optional invocation adapters for these routes. They are not owner
skills/loom-records/references/route-vocabulary.md:6:Route tokens are not a runtime enum, command router, or new owner layer. They are
skills/loom-records/references/route-vocabulary.md:17:skill name, command, or ticket status into a route token.
skills/loom-records/references/route-vocabulary.md:51:  package-specific invocation wrappers. Commands may transport a route, but the
skills/loom-wiki/templates/atlas-page.md:25:Files, commands, records, or workflows a future agent should inspect first.
skills/loom-wiki/references/wiki-write.md:43:- recommended next owner layer, workflow, or optional command
skills/loom-wiki/references/wiki-audit.md:46:- recommended next owner layer, workflow, or optional command per finding
```

## After observations

Exact route-peer wording search produced no output.

Broad command/adaptor route wording search after edits:

```text
README.md:478:It is not a runtime, service, daemon, MCP server, product CLI, workflow engine, hidden database, or prompt dump.
skills/loom-records/references/route-vocabulary.md:6:Route tokens are not a runtime enum, command router, or new owner layer. They are
skills/loom-records/references/route-vocabulary.md:17:skill name, command, or ticket status into a route token.
skills/loom-records/references/route-vocabulary.md:51:  package-specific invocation wrappers. Commands may transport a route, but the
skills/loom-wiki/templates/atlas-page.md:25:Files, commands, records, or workflows a future agent should inspect first.
skills/loom-ship/SKILL.md:14:commands may invoke that workflow but do not own it.
skills/loom-workspace/references/status-snapshot.md:118:  command/adapter names instead of route tokens
skills/loom-workspace/references/routing.md:59:Commands are optional invocation adapters for these routes. They are not owner
```

Remaining broad matches are framed as non-runtime doctrine, command/adaptor
non-route guidance, invocation transport, or ordinary atlas inspection examples;
none use optional commands as peers to owner layers or workflow route values.

`git diff --check` produced no output and exited successfully. Parent reran it
after `git add -N` for the new untracked evidence and packet records; that
follow-up also produced no output.

# Supports Claims

- `initiative:skills-corpus-council-precision-pass#OBJ-012`
- `ticket:cmdroute#ACC-001`
- `ticket:cmdroute#ACC-002`
- `ticket:cmdroute#ACC-003`
- `ticket:cmdroute#ACC-004`

# Challenges Claims

None.

# Environment

Commit: working tree after baseline `0458921db7377783651abd73a00159a6bbcf289d`
and before ticket commit.

Branch: `main`

Runtime: none; Markdown corpus structural validation.

OS: macOS Darwin.

Relevant config: none.

# Validity

Valid for: current working-tree diff for `ticket:cmdroute` before oracle critique
and commit.

Recheck when: command/adaptor route wording changes again, route vocabulary
changes, or the touched product guidance files are edited before acceptance.

# Limitations

These are structural text searches over `skills/` and `README.md`. They cover the
known route-peer wording patterns and related command/adaptor route terms, but do
not prove every possible future phrasing choice.

# Result

The known route-peer wording was removed from product guidance. Remaining broad
command/adaptor matches are framed as non-runtime doctrine, non-route guidance,
invocation transport, or ordinary inspection examples. `git diff --check` passed,
including a parent follow-up run that covered the new evidence and packet records
via intent-to-add entries.

# Interpretation

This evidence supports that `ticket:cmdroute` has structurally removed known
optional-command-as-route-peer wording and preserved legitimate command/adaptor
transport guidance. It does not by itself satisfy `ticket:cmdroute#ACC-005`,
which requires oracle critique.

# Related Records

- `ticket:cmdroute`
- `packet:ralph-ticket-cmdroute-20260502T213017Z`
