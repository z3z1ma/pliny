# Packet Contract

A Ralph packet is a contract, not a reminder note.

Use `skills/loom-records/references/packet-frontmatter.md` for shared packet
frontmatter fields and valid values. This reference owns Ralph-specific contract
guidance: how an implementation packet frames a child iteration, stop
conditions, evidence obligations, and parent reconciliation.

Use `skills/loom-records/references/route-vocabulary.md` for route tokens and
`skills/loom-records/references/status-lifecycle.md` for packet lifecycle status
boundaries. Ralph child outcomes are packet output vocabulary, not route tokens
or ticket states until the parent reconciles them.

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

Ralph-specific frontmatter must include `change_class`,
`verification_posture`, and `iteration`. Optional `risk_class` may repeat or
narrow ticket risk for the packet, but the ticket still owns critique disposition
and acceptance gates.

Use `packet:ralph-ticket-<token>-<UTC compact timestamp>` as the packet ID and
save the file as
`.loom/packets/ralph/<UTC compact timestamp>-ticket-<token>-iter-<NN>.md`, where
`iter-<NN>` matches frontmatter `iteration`.

## Parent launch checklist

Before launching a Ralph child, the parent should check:

- source freshness: governing records, resolved integration ref, working-tree
  status, and child-write-scope files still match the `source_fingerprint` closely
  enough to trust the packet
- child write scope overlap: `child_write_scope` records and paths are exact,
  narrow, non-overlapping with any parallel packet, and fail closed for canonical
  record writes unless exact record refs are granted
- parent merge scope: `parent_merge_scope` names the records and paths the parent
  must reconcile, especially ticket truth, evidence or critique disposition, and
  packet lifecycle notes when applicable
- Git and execution context: branch, worktree, isolation, network posture,
  destructive command policy, and shared Git metadata policy match the intended
  execution run
- verification posture: `verification_posture` fits the change class and states
  what red/green, before/after, or verification-neutral evidence the child must
  return
- stop conditions: freshness, scope, execution-context, and posture-specific stop
  conditions tell the child when to return `blocked` or `escalate`
- output contract: the required return fields are sufficient for parent-side
  reconciliation of ticket state, evidence, critique, and packet status

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

Every Ralph packet must make the compilation baseline inspectable using the
shared packet-frontmatter shape. For Ralph this is not optional shared metadata;
it is part of the launch-safety contract.

Required frontmatter:

```yaml
source_fingerprint:
  git_commit: <sha or unknown>
  integration_remote: <remote name|none|unknown>
  integration_ref: <ref, tag, commit, or unknown>
  integration_commit: <sha or unknown>
  git_status_summary: <clean|dirty|unknown>
  git_status_detail: <short status detail or unknown - rationale>
  compiled_from:
    - ticket:<token>
    - spec:<slug>
```

Before launch, the parent checks whether governing records, resolved integration
refs, or write-scope files changed materially since the packet was compiled. The
child should stop and report `blocked` or `escalate` if those surfaces appear
materially different at execution time and the packet did not explicitly account
for the difference. If yes, supersede the packet and compile a fresh one.

## Write And Merge Scope

Separate child mutation authority from parent reconciliation authority.

Ralph uses the shared `child_write_scope` and `parent_merge_scope` fields to
separate child mutation authority from parent reconciliation authority:

```yaml
child_write_scope:
  records:
    - "None - child returns output only unless parent grants exact narrow record refs"
  paths:
    - src/example/**
    - tests/example/**
parent_merge_scope:
  records:
    - ticket:<token>
  paths:
    - .loom/tickets/<ticket-file>.md
```

Children can recommend ticket, evidence, critique, or wiki updates. Ralph child
canonical-record writes fail closed by default: use `None - child returns output
only` unless the parent grants exact, narrow record refs. The parent commits
canonical reconciliation unless the packet explicitly grants the child
record-write authority.

Do not treat empty `child_write_scope.records` or `child_write_scope.paths` as a
launch-ready no-write declaration. Empty child write scope is ambiguous and
launch-blocking until the parent clarifies the child boundary with exact record
refs, paths, or globs, or explicit `None - <rationale>` entries for records and
paths.

Legacy packets may use `write_scope`. Treat that as child write scope unless the
packet says otherwise. New Ralph packets should use `child_write_scope` for the
child boundary; reserve `write_scope` references to explicit legacy compatibility
notes, not new packet grammar.

Do not confuse this with bounded support handoffs outside Ralph. For example, a
drive outer-loop handoff may use support-local `handoff_write_scope` to describe
proposal-time mutation permission, but that does not make the handoff a packet or
give it canonical truth ownership.

## Context Budget

Every Ralph packet must declare the expected source-reading posture using the
shared `context_budget` field.

Required frontmatter:

```yaml
context_budget:
  posture: normal
  max_source_files: 8
  max_excerpt_lines_per_file: 80
  avoid_full_file_reads: true
```

Current templates default to `normal` for bounded but realistic source reading.
Use `tight` for very narrow slices and `expansive` only when the parent
intentionally grants broader inspection. The budget is guidance, not a substitute
for judgment. A child may exceed it only when the packet or discovered evidence
makes that necessary, and should say so in its output.

## Execution Context

Ralph packets must declare the execution environment using the shared
`execution_context` field. For Git-backed work this includes branch, worktree,
isolation, network posture, destructive-command policy, and shared Git metadata
policy; unknown values require rationale and should be launch blockers when they
make the child boundary unsafe.

Required frontmatter:

```yaml
execution_context:
  branch: <name|unknown>
  push_remote: <remote name|same_as_integration|none|unknown>
  worktree: <path|none|unknown>
  isolation: none | branch | worktree | sandbox
  git_shared_metadata_mutations: forbidden | allowed | unknown
  destructive_commands: forbidden
  network: allowed | forbidden | unknown
```

This helps a future parent understand where the child worked and what tool
permissions were expected.

Use `skills/loom-git/SKILL.md` when choosing these values for Git-backed work.
For fork/upstream, stacked-diff, and multi-repo packets, name the primary
checkout in frontmatter and put per-repository integration remote, integration
ref, push/review remote, branch, and worktree details in the packet body.

## Packet Lifecycle

Use packet statuses deliberately:

Terminal packet statuses are `consumed`, `superseded`, and `abandoned`.
`compiled` is launch-ready or pending parent action, not terminal.

- `compiled -> consumed`: child output returned and parent merge notes were written
- `compiled -> superseded`: governing records, source fingerprint, scope, or
  child write scope changed before launch
- `compiled -> abandoned`: packet will not be launched and no successor is intended
- `consumed -> superseded`: rare; use only when a later packet or owner
  correction invalidates the result

After reconciliation, parent must update packet status away from `compiled`.

`consumed` only means output returned and parent merge notes exist. It does not
mean the work was accepted, successful, merged, closure-compatible, or promoted
into owner-layer truth; the ticket and other canonical owners decide those facts.

If a launched child result is unusable because it was rejected, corrupted,
materially stale, or outside scope, do not mark the work successful. Update the
packet status honestly, usually `consumed` when the child output was received and
parent merge notes explain rejection, or `superseded` when a fresh packet replaces
the unusable contract. Update ticket truth, preserve useful evidence or critique
findings where applicable, and compile a new packet only after the owner records
and write boundary are accurate.

For stale `compiled` packet recovery, first discover pending packets, then read
the packet before acting. Compare its target, governing records, source
fingerprint, child write scope, parent merge scope, and intended iteration against
current ticket truth and source files. If any launch-safety surface materially
changed before launch, do not ask the child to guess: set the old packet to
`superseded` when a corrected packet will replace it, or `abandoned` when the
work will not proceed. Keep the disposition in packet status and parent merge
notes, while ticket execution state, acceptance, evidence sufficiency, and next
route remain ticket-owned.

## Child Outcomes vs Routes

A Ralph child should return one child outcome: `continue`, `stop`, `blocked`, or
`escalate`. These words describe the bounded iteration result for the parent;
they do not directly set `next route:` and they do not change ticket state.

The parent reconciles the child outcome into ticket truth and then chooses the
next governed route, such as `ticket`, `research`, `critique`,
`acceptance_review`, `continue`, or `stop`. This is especially important for
`continue` and `stop`, which are also route tokens when they appear in a route
field.

## Verification Targets

When upstream specs or tickets use claim coverage IDs, the packet should list
the IDs this iteration targets in a `# Verification Targets` section.

## The important test

Read the packet as if you were the child.

If you would still need transcript archaeology to know what to do, the packet is not ready.
