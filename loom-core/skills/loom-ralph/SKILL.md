---
name: loom-ralph
description: "Run Ralph implementation packets. Use for larger feature, refactor, test, migration, or cleanup slices when a Ralph-ready ticket needs fresh context, explicit write scope, fingerprint, verification, and output contract."
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
- the ticket data shows that the missing work is research, spec shaping, plan or
  ticket refinement, debugging, spike, codemap, shipping, acceptance review, or
  another non-implementation workflow; Ralph is only for bounded implementation
  packets
- the next move is critique or wiki; use that domain skill first
- the task is tiny local execution that does not need a packet

## Parent Procedure

1. read the governing ticket and upstream chain
2. decide whether the next move is really Ralph
3. choose packet style
4. choose verification posture (`test-first`, `observation-first`, or `none`)
5. decide write scope
6. for Git-backed file changes, use an installed `loom-git` support coordinator or
   project Git practice to choose branch/worktree isolation and refresh the
   integration baseline
7. declare source fingerprint, execution context, and context budget
8. compile the packet from the template
9. read it once as if you were the child
10. check whether sources or write-scope files changed materially before launch
11. launch the fresh worker through the available harness transport
12. inspect and reconcile the result back into the ticket
13. decide from the reconciled ticket data whether another packet, critique,
    wiki, research, spec, plan, ticket update, debugging, spike, codemap, ship,
    or acceptance review is needed; `ship` is packaging or handoff only and does
    not close the ticket

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
- assumptions and decision triggers that could block the child
- quality delta for user-facing, operator-facing, or behavior-changing work
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

## Common Rationalizations

- **"The packet is detailed, so the ticket can be vague."**
  - Reality: Ralph starts from a Ralph-ready ticket. Packets cannot outrank or repair ticket truth by themselves.
- **"The child can decide the missing product direction."**
  - Reality: Material assumptions belong in owner records or user decisions before launch.
- **"Verification posture `none` is fine because this is Markdown."**
  - Reality: Protocol, acceptance, routing, and operator guidance changes can alter behavior and usually need evidence plus critique.
- **"The child returned `stop`, so the ticket is done."**
  - Reality: Child outcome vocabulary is not ticket closure. The parent reconciles evidence, critique, and acceptance first.

## Red Flags

- child write scope is broad, empty, or only implied by prose
- source fingerprint is stale or says `unknown` without launch-safe rationale
- the packet lacks quality delta for user-facing or operator-facing work
- stop conditions do not tell the child when to fail closed
- child output is treated as final truth before parent reconciliation

## Verification

- [ ] Ticket is Ralph-ready and matches the packet scope.
- [ ] Source fingerprint and write-scope files are fresh enough.
- [ ] Verification posture is justified and evidence expectations are concrete.
- [ ] Assumptions and quality delta are explicit when material.
- [ ] Parent merge scope names ticket and supporting reconciliation targets.

## Done Means

- a packet exists as a durable contract when the work is only packet compilation
- launched work has returned child output when an iteration was run
- the worker's outcome is classified honestly
- packet status moved away from non-terminal `compiled` after reconciliation;
  terminal packet statuses are `consumed`, `superseded`, and `abandoned`
- the ticket tells the truth afterward
- the ticket and packet parent merge notes make the post-iteration state legible

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
5. `loom-git`, when installed, or project Git practice when the iteration mutates
   repository files, needs branch/worktree isolation, or participates in parallel
   Ralph.
6. `references/parent-child-handshake.md` when launching or reconciling a child
   worker, especially parallel Ralph.
7. `skills/loom-critique/SKILL.md` or `skills/loom-wiki/SKILL.md` when the next
   packetized pass is review or synthesis rather than implementation.
8. `skills/loom-records/references/route-vocabulary.md` when distinguishing
   packet child outcomes from ticket states, support cues, commands, or workflow
   choices.
9. `references/harness-invocation.md` only when transport mechanics need to be
   documented or chosen.
10. `templates/ralph-packet.md` only when creating the packet.
