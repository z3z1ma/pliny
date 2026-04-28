# Parallel Ralph With Git

Parallel Ralph requires two kinds of independence:

- Loom independence: tickets, dependencies, and child write scopes do not
  conflict.
- Git independence: branches, worktrees, generated files, lockfiles, and shared
  state do not conflict.

Both are required. One does not substitute for the other.

## Preconditions

Before launching a parallel wave, the parent must verify:

- failures or tasks have been grouped into independent problem domains rather
  than merely split by convenience
- every child has one packet
- every packet targets one ticket or one clearly bounded ticket slice
- no `depends_on` conflict makes the sequence invalid
- no `child_write_scope` overlaps another child
- no shared migration, lockfile, generated output, database, service state, or
  external environment creates hidden contention
- no child needs to mutate shared Git metadata such as remote-tracking refs,
  config, hooks, object storage, or worktree administration files
- every child has a distinct branch
- every child that mutates files has a distinct worktree
- every packet has its own source fingerprint
- each packet freezes the resolved `integration_commit`

If any point is ambiguous, run the work sequentially or return to planning.

## Parent Setup Table

For a parallel wave, write down a table before launch. Scratch parent notes are
acceptable while designing the wave, but once children are launched the setup
must live in the plan, ticket journal, or packet working notes.

Recommended columns:

| Child | Ticket | Repo | Integration remote | Integration ref | Integration commit | Push/review remote | Branch | Worktree | Child write scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ticket:<token> | repo:web | `<remote-or-none>` | `<integration-ref>` | `<sha>` | `<remote-or-none>` | loom/<token>/web-ui | ../web-<token>-ui | apps/web/** |

This table is not a new ledger. It is a launch checklist that makes collisions
visible before they happen.

## Multi-Repository Work

For multi-repo tickets:

- name every repository alias in the ticket scope
- resolve each repository's integration baseline independently
- fetch relevant remotes only where the baseline is remote-backed
- record integration remote, integration ref, integration commit, and push/review
  remote per repository
- create separate worktrees per repository when concurrent mutation is possible
- keep cross-repo sequencing in the plan or ticket, not in branch names alone

If one child must coordinate changes across multiple repositories, the packet
should name all affected repo aliases and write scopes. If several children
mutate several repositories in parallel, each child still needs a non-overlap
evidence per repository.

## Packet Requirements

Each packet in a parallel Git-backed wave should include:

- `child_write_scope` with path patterns narrow enough to compare
- `source_fingerprint.git_commit`
- `source_fingerprint.integration_remote`
- `source_fingerprint.integration_ref`
- `source_fingerprint.integration_commit`
- `source_fingerprint.git_status_summary`
- `execution_context.branch`
- `execution_context.push_remote`
- `execution_context.worktree`
- `execution_context.isolation: worktree`
- stop conditions for stale source fingerprint or write-scope drift
- stop conditions that forbid child fetch/prune/config mutations unless the
  packet explicitly allows them

For multi-repo packets, use the packet body to list per-repo Git context if the
frontmatter only captures the primary checkout.

## Launch Flow

1. Resolve the integration baseline in each repository.
2. Fetch remote-backed baselines where needed.
3. Record each integration remote, integration ref, and integration commit.
4. Create one branch and one worktree per child per mutating repository.
5. Compile packets with matching execution context.
6. Forbid child fetch/prune/config mutations unless explicitly required and
   isolated.
7. Launch fresh workers only after confirming write-scope and Git isolation are
   both non-overlapping.
8. Keep parent reconciliation separate for each child.

## Reconciliation Flow

After children return:

1. inspect each worktree's status and diff
2. check that each diff stayed inside child write scope
3. record evidence per ticket or per wave, as appropriate
4. update each ticket separately before summarizing the wave
5. integrate branches in dependency order
6. run validation in the integration checkout when combined behavior matters,
   especially when several children each reported local success
7. route unresolved conflicts or shared-state surprises back to plan or ticket
   refinement

Do not merge a whole parallel wave just because every child reported `stop`.
The parent still owns integration, evidence, critique routing, and ticket truth.

## Lockfiles And Generated Files

Lockfiles, generated clients, schema artifacts, snapshots, and build outputs are
common hidden contention points.

Use one of these strategies:

- assign the shared artifact to exactly one child
- serialize children that would touch it
- defer generation to a parent integration pass
- split the ticket so the shared artifact has its own owner

Never let two children independently regenerate the same shared artifact and
hope Git will reconcile it cleanly.

## Failure Handling

If one child blocks, keep the others truthful:

- record the blocker in that child's ticket
- do not merge that branch without evidence and parent acceptance
- continue independent children only if their inputs did not depend on the
  blocked output
- update the plan or ticket dependencies if the wave shape was wrong
