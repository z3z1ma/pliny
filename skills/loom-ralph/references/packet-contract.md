# Packet Contract

A Ralph packet is a contract, not a reminder note.

## Minimum packet contents

- exact target
- iteration goal
- governing source records
- scope
- write scope
- mode and style
- source fingerprint
- context budget
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

## Verification Targets

When upstream specs or tickets use claim coverage IDs, the packet should list
the IDs this iteration targets in a `# Verification Targets` section.

## The important test

Read the packet as if you were the child.

If you would still need transcript archaeology to know what to do, the packet is not ready.
