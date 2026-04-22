---
name: loom-ralph
description: "Run the inner implementation loop through bounded fresh-context packets. Use when one exact ticket is ready for one explicit iteration, when the write boundary and output contract should be declared up front, or when critique/wiki should be launched as packetized sibling variants."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  loom_layer: inner-loop
  protocol_version: "2.0"
---

# loom-ralph

Ralph is Loom's bounded execution loop.

This skill is for the parent agent that is preparing, launching, and reconciling one fresh-context iteration.

## What This Skill Owns

- Ralph packet creation
- packet style selection
- source fingerprint and freshness checks
- context budget declaration
- parent/child handshake
- iteration outcome vocabulary
- ticket reconciliation after return

## Use This Skill When

- one exact ticket is ready for one bounded iteration
- the work would benefit from fresh context
- the write boundary should be explicit
- the parent wants a durable packet contract
- critique or wiki passes need to be launched in the same packetized style

## Do Not Use This Skill When

- the work is still under-scoped
- the ticket is too vague
- the next move is obviously research, spec, plan, or ticket refinement
- the task is a tiny local edit that does not need a packet

## Parent Procedure

1. read the governing ticket and upstream chain
2. decide whether the next move is really Ralph
3. choose packet style
4. choose verification posture (`test-first`, `observation-first`, or `none`)
5. decide write scope
6. declare source fingerprint and context budget
7. compile the packet from the template
8. read it once as if you were the child
9. check whether sources or write-scope files changed materially before launch
10. launch the fresh worker through the available harness transport
11. inspect and reconcile the result back into the ticket
12. route to Ralph again, critique, wiki, or outer-loop refinement

## Strong Ralph Discipline

A strong packet should make all of these explicit:

- target ticket
- bounded goal for this iteration
- sources that matter
- write scope
- source fingerprint
- context budget
- verification targets when claim coverage exists
- verification posture and what counts as proof for this iteration
- stop conditions
- output contract
- what the parent will do after the child returns

## Verification Posture

Packet style governs how much context is carried. Verification posture governs how the child proves this iteration worked. The two are independent axes and both belong in the packet frontmatter.

Postures:

- `test-first` — the child must produce a failing check before any implementation change and drive it to green inside this iteration. This is Loom's native TDD shape.
- `observation-first` — the child must capture inspectable evidence of current behavior, change it, and capture inspectable evidence of the new behavior.
- `none` — no explicit verification beyond the normal output contract. Honest only for iterations that do not change behavior (record hygiene, reference reconciliation, documentation edits).

Choose per packet, not per ticket. A test-first ticket can still have a refactor-only iteration that is `none`.

See `references/verification-posture.md` for details.

## Done Means

- one packet exists as a durable contract
- the worker's outcome is classified honestly
- the ticket tells the truth afterward
- the next owner is explicit

## Read In This Order

1. `references/packet-contract.md`
2. `references/packet-styles.md`
3. `references/verification-posture.md`
4. `references/parent-child-handshake.md`
5. `references/harness-invocation.md`
6. `templates/ralph-packet.md`
