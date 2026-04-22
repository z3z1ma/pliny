# Packet Contract

A Ralph packet is a contract, not a reminder note.

## Minimum packet contents

- exact target
- iteration goal
- governing source records
- scope
- child write scope
- parent merge scope
- mode and style
- change class
- source fingerprint
- context budget
- execution context
- verification targets when claim coverage exists
- verification posture
- stop conditions
- output contract

## Strong packet body

A strong packet usually includes:

- Mission
- Bound Context
- Source Snapshot
- Task For This Iteration
- Stop Conditions
- Output Contract
- Working Notes
- Child Output
- Parent Merge Notes

## Source snapshot guidance

The packet does not need to duplicate every source file.

It does need to include enough excerpts, summaries, or references that the child knows where the real constraints live.

For code work, separate intended behavior from implementation reality. The
packet should tell the child what the project intends and where to inspect what
the code currently does.

## Source Fingerprint

Every packet should make the compilation baseline inspectable.

Recommended frontmatter:

```yaml
source_fingerprint:
  git_commit: <sha or unknown>
  git_status_summary: <clean|dirty|unknown>
  compiled_from:
    - ticket:<id>
    - spec:<id>
```

Before launch, the parent checks whether governing records or write-scope files
changed materially since the packet was compiled. If yes, supersede the packet
and compile a fresh one.

## Write And Merge Scope

Separate child mutation authority from parent reconciliation authority.

Recommended frontmatter:

```yaml
child_write_scope:
  records: []
  paths:
    - src/example/**
    - tests/example/**
parent_merge_scope:
  records:
    - ticket:<id>
    - evidence:<slug>
  paths: []
```

Children can recommend ticket, evidence, critique, or wiki updates. The parent
commits canonical reconciliation unless the packet explicitly grants the child
record-write authority.

Legacy packets may use `write_scope`. Treat that as child write scope unless the
packet says otherwise.

## Context Budget

Every packet should declare the expected source-reading posture.

Recommended frontmatter:

```yaml
context_budget:
  posture: tight
  max_source_files: 8
  max_excerpt_lines_per_file: 80
  avoid_full_file_reads: true
```

The budget is guidance, not a substitute for judgment. A child may exceed it
only when the packet or discovered evidence makes that necessary, and should
say so in its output.

## Execution Context

For code work, declare the execution environment.

Recommended frontmatter:

```yaml
execution_context:
  branch: <name|unknown>
  worktree: <path|none|unknown>
  isolation: none | branch | worktree | sandbox
  destructive_commands: forbidden
  network: allowed | forbidden | unknown
```

This helps a future parent understand where the child worked and what tool
permissions were expected.

## Packet Lifecycle

Use packet statuses deliberately:

- `compiled -> consumed`: child output returned and parent merge notes were written
- `compiled -> superseded`: governing records, source fingerprint, scope, or
  child write scope changed before launch
- `compiled -> abandoned`: packet will not be launched and no successor is intended
- `consumed -> superseded`: rare; use only when a later packet or owner
  correction invalidates the result

After reconciliation, parent must update packet status away from `compiled`.

## Verification Targets

When upstream specs or tickets use claim coverage IDs, the packet should list
the IDs this iteration targets in a `# Verification Targets` section.

## The important test

Read the packet as if you were the child.

If you would still need transcript archaeology to know what to do, the packet is not ready.
