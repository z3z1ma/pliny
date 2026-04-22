# Parent / Child Handshake

## Child output vocabulary

The child should return:

- `continue`
- `stop`
- `blocked`
- `escalate`

And it should also return:

- files changed
- records changed
- evidence gathered
- blockers or risks
- ticket-state recommendation

## Parent responsibilities after return

The parent should ask:

1. did the child stay inside the write boundary
2. did the child stay inside scope
3. did the packet source fingerprint remain fresh enough for the work
4. did the child respect or explicitly justify exceeding the context budget
5. what evidence exists
6. what claims or acceptance IDs are now supported or challenged
7. what does the ticket now need to say
8. is critique next
9. is wiki next
10. is another Ralph iteration next
11. did the child reveal missing outer-loop work instead

## A child does not close the loop alone

The child's job is to complete the bounded step.
The parent's job is to decide what that means for durable truth.

## Parallel Ralph

Parallel Ralph is allowed only when the parent can prove static independence
from Loom records before launch.

For parallel Ralph, parent must verify:

- no `depends_on` conflict
- no `write_scope` overlap
- no shared migration, generated-file, lockfile, or stateful resource
  contention
- each child gets its own packet
- each packet has its own source fingerprint
- parent reconciles each result separately before merging wave truth

If any check is ambiguous, run the work sequentially or return to plan/ticket
refinement.
