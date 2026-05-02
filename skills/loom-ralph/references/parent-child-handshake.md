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
- self-review findings or concerns
- blockers or risks
- ticket-state recommendation

## Parent responsibilities after return

The parent should ask:

1. did the child stay inside the write boundary
2. did the child stay inside scope
3. did the packet source fingerprint remain fresh enough for the work
4. did the child respect or explicitly justify exceeding the context budget
5. what evidence exists
6. did the child's self-review concerns change risk, scope, or next route
7. what claims or acceptance IDs are now supported or challenged
8. what does the ticket now need to say
9. is critique next
10. is wiki next
11. is another Ralph iteration next
12. did the child reveal missing outer-loop work instead

## Rejected Or Unusable Child Results

If the child result is rejected, corrupted, stale against the packet source
fingerprint, or overscoped beyond the declared child write scope, the parent must
not smooth it into a success story.

Parent recovery steps:

1. classify the result honestly in the ticket and parent merge notes
2. preserve any useful observations as evidence or critique only if they remain
   inspectable and within their owning layer
3. revert or ignore out-of-scope mutations before dependent work relies on them
4. set the packet to a terminal status: usually `consumed` if output was received
   and rejected in parent merge notes, or `superseded` if a fresh packet replaces
   a stale or invalid contract
5. return to ticket refinement, critique, or a fresh Ralph packet instead of
   claiming the original iteration succeeded

Use `abandoned` for a packet that will not be launched and has no successor, not
for a launched child whose output merely failed review.

## A child does not close the loop alone

The child's job is to complete the bounded step.
The parent's job is to decide what that means for durable truth.

## Parallel Ralph

Parallel Ralph is allowed only when the parent can establish static independence
from Loom records before launch.

For parallel Ralph, parent must verify:

- no `depends_on` conflict
- no `child_write_scope` overlap
- no legacy `write_scope` overlap when reviewing older packet records
- no shared migration, generated-file, lockfile, or stateful resource
  contention
- each child gets its own packet
- each packet has its own source fingerprint
- each Git-backed child gets a distinct branch and, for concurrent mutation, a
  distinct worktree
- parent reconciles each result separately before merging wave truth

If any check is ambiguous, run the work sequentially or return to plan/ticket
refinement.
