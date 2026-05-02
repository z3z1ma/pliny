---
name: loom-ralph
description: "Run the inner implementation loop through bounded fresh-context packets. Use when one exact ticket is Ralph-ready for one explicit implementation iteration and the write boundary, verification posture, source fingerprint, and output contract should be declared up front. For critique or wiki packets, activate the domain skill first and reuse packet discipline there."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: inner-loop
---

# loom-ralph

Ralph is Loom's bounded execution loop.

This skill is for the parent agent that is preparing, launching, and reconciling one fresh-context iteration.

## What This Skill Owns

- Ralph packet creation
- packet style selection
- source fingerprint and freshness checks
- context budget declaration
- Git execution context binding for packetized implementation work
- parent/child handshake
- iteration outcome vocabulary
- ticket reconciliation after return

Ralph owns packetized implementation. Critique and wiki may reuse packet
discipline, but their domain skills own critique packets and wiki packets.
Ralph packets use `kind: packet`, `packet_kind: ralph`, and the
`.loom/packets/ralph/` path. Critique packets use `packet_kind: critique` under
`.loom/packets/critique/`; wiki packets use `packet_kind: wiki` under
`.loom/packets/wiki/`.

## Use This Skill When

- one exact ticket is Ralph-ready for one bounded implementation iteration
- the work would benefit from fresh context
- the write boundary should be explicit
- the parent wants a durable packet contract

## Do Not Use This Skill When

- the work is still under-scoped
- the ticket is too vague
- the next move is obviously research, spec, plan, or ticket refinement
- the next move is critique or wiki; use that domain skill first
- the task is a tiny local edit that does not need a packet

## Parent Procedure

1. read the governing ticket and upstream chain
2. decide whether the next move is really Ralph
3. choose packet style
4. choose verification posture (`test-first`, `observation-first`, or `none`)
5. decide write scope
6. for Git-backed file changes, use `loom-git` to choose branch/worktree
   isolation and refresh the integration baseline
7. declare source fingerprint, execution context, and context budget
8. compile the packet from the template
9. read it once as if you were the child
10. check whether sources or write-scope files changed materially before launch
11. launch the fresh worker through the available harness transport
12. inspect and reconcile the result back into the ticket
13. route to Ralph again, critique, wiki, or outer-loop refinement

## Strong Ralph Discipline

A strong packet should make all of these explicit:

- target ticket
- bounded goal for this iteration
- sources that matter
- write scope
- source fingerprint
- Git integration ref, branch, worktree, and isolation mode when repository
  files will change
- context budget
- verification targets when claim coverage exists
- verification posture and what counts as evidence for this iteration
- stop conditions
- output contract
- what the parent will do after the child returns

## Verification Posture

Packet style governs how much context is carried. Verification posture governs how the child evidences this iteration. The two are independent axes and both belong in the packet frontmatter.

This `verification_posture` field is Ralph packet grammar. Critique and wiki
packets rely on their domain-specific review or synthesis evidence expectations
unless their owning skill later defines its own posture field.

Postures:

- `test-first` — the child must produce a failing check before any implementation change and drive it to green inside this iteration. This is Loom's native TDD shape.
- `observation-first` — the child must capture inspectable evidence of current behavior, change it, and capture inspectable evidence of the new behavior.
- `none` — no explicit verification beyond the normal output contract. Honest only for verification-neutral iterations such as non-semantic record hygiene, reference reconciliation, or packet compilation.

Choose per packet, not per ticket. A test-first ticket can still have a refactor-only iteration that is `none`.

See `references/verification-posture.md` for details.

Do not choose `none` just because the file is Markdown. Protocol authority,
operator guidance, acceptance, or behavior-contract edits can change how Loom
behaves and usually need structural evidence plus critique.

## Done Means

- a packet exists as a durable contract when the work is only packet compilation
- launched work has returned child output when an iteration was run
- the worker's outcome is classified honestly
- packet status moved away from non-terminal `compiled` after reconciliation;
  terminal packet statuses are `consumed`, `superseded`, and `abandoned`
- the ticket tells the truth afterward
- the next route is explicit

## Read In This Order

Read immediately before compiling or launching a Ralph packet:

1. `references/work-driver.md` when driving a ticket through execution and
   parent reconciliation.
2. `references/packet-contract.md` when compiling or reviewing the packet's
   required fields and boundaries.

Then read conditionally:

3. `references/packet-styles.md` when choosing reference-first,
   snapshot-first, or hermetic packet posture.
4. `references/verification-posture.md` when deciding test-first,
   observation-first, or verification-neutral execution.
5. `skills/loom-git/SKILL.md` when the iteration mutates repository files,
   needs branch/worktree isolation, or participates in parallel Ralph.
6. `references/parent-child-handshake.md` when launching or reconciling a child
   worker, especially parallel Ralph.
7. `skills/loom-critique/SKILL.md` or `skills/loom-wiki/SKILL.md` when the next
   packetized pass is review or synthesis rather than implementation.
8. `references/harness-invocation.md` only when transport mechanics need to be
   documented or chosen.
9. `templates/ralph-packet.md` only when creating the packet.
