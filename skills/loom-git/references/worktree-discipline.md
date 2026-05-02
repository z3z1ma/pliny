# Worktree Discipline

Git worktrees let multiple agents work from one repository without sharing one
mutable checkout.

In Loom terms, worktrees are isolation support. They do not grant scope, own
truth, or replace packet write boundaries.

Linked worktrees isolate working directories and indexes, but they can still
share repository metadata such as refs, config, hooks, and object storage. Treat
fetching, pruning, remote edits, config edits, and garbage collection as shared
operations unless repository inspection shows otherwise.

## When To Use A Worktree

Use a worktree when:

- parallel Ralph workers may run at the same time
- the user may keep working in the primary checkout while the agent works
- a ticket spans enough time that sharing the primary checkout would be fragile
- a spike or risky change should be easy to abandon
- several repositories need coordinated but separate branches

You usually do not need a worktree for a tiny record edit, link fix, or local
read-only inspection.

## File-First Edit Safety

Before writing in a shared or possibly stale checkout, re-read the target files
you are about to change and inspect the current worktree state when repository
changes matter. Preserve unrelated edits whether they came from the user,
another agent, generated tooling, or an earlier ticket.

Fail closed instead of guessing when:

- the current file no longer matches the packet, ticket, or source snapshot you
  are relying on
- another edit overlaps your intended write scope
- dirty or untracked files make ownership ambiguous
- applying the change would require rewriting unrelated work

Route stale or contradictory records through the layer that owns the fact. Do
not treat the newest file, branch, PR text, generated context, or dashboard state
as automatically authoritative.

## Placement

Place worktrees outside the tracked repository root unless the project already
has an ignored worktree directory.

Common sibling shape:

```text
../<repo>-<ticket-token>-<short-slug>
```

Avoid placing worktrees under paths that could be accidentally committed,
validated as source, or swept up by broad file operations.

## Creation Flow

Inspect existing worktrees first:

```bash
git worktree list
```

Refresh a remote-backed baseline before creating the branch:

```bash
git fetch --prune <remote>
```

Skip the fetch when the resolved baseline is local-only, a tag or commit already
present locally, or another explicit non-remote source.

Create a ticket-scoped branch and worktree from the resolved baseline:

```bash
git worktree add -b loom/<ticket-token>/<short-slug> ../<repo>-<ticket-token>-<short-slug> <integration-ref-or-commit>
```

Then verify the new checkout:

```bash
git -C ../<repo>-<ticket-token>-<short-slug> status --short
git -C ../<repo>-<ticket-token>-<short-slug> branch --show-current
```

## Baseline Validation

After creating a worktree for code changes, establish the cleanest honest
baseline available before implementation starts.

Use the project-known setup or validation command when it is already documented
in the ticket, plan, README, package scripts, or local convention. If no command
is known, record that instead of guessing a toolchain.

Record one of:

- baseline command passed, with the command and relevant output summary
- baseline command failed, with failure summary and whether the ticket should
  proceed, debug, or block
- no baseline command known, with the source inspected

Do not auto-install dependencies, edit ignore files, or mutate project setup just
because a worktree exists. Those are separate changes that need owner scope and,
when they affect source or records, ticket truth.

If linked worktrees are unavailable, use a separate clone or harness sandbox as
the isolation unit. Keep the same Loom discipline: explicit baseline, explicit
branch or detached commit, explicit write scope, and explicit cleanup rules.

## One Branch, One Checked-Out Worktree

Git does not allow the same branch to be checked out in two linked worktrees.

Treat that as a helpful constraint. If two children need to work in parallel,
give them distinct branches and distinct worktrees.

## Packet Provenance

When a Ralph child receives a worktree, the packet should name:

- worktree path
- branch
- integration ref
- integration commit
- integration remote, when the baseline is remote-backed
- push remote, when it differs from the integration remote
- current commit
- dirty or clean status at compile time
- whether child fetch/prune/config mutations are allowed
- whether destructive commands are forbidden

For multi-repo packets, include a table in the packet body if the packet
frontmatter only names the primary repository.

## Handoff Rules

Before handoff to critique, merge, shipping, or another agent, inspect:

```bash
git -C <worktree> status --short
git -C <worktree> diff --stat
git -C <worktree> diff
```

If untracked files, generated files, lockfiles, or local-only changes matter,
record them in the ticket and evidence. Do not let them disappear into a vague
"worktree has changes" note.

## Cleanup Rules

Do not remove a worktree until you know whether it contains useful work.

Safe inspection before removal:

```bash
git worktree list
git -C <worktree> status --short
git -C <worktree> branch --show-current
git -C <worktree> log --oneline --decorate -n 5
```

Remove only when the work is merged, abandoned with permission, or preserved
elsewhere:

```bash
git worktree remove <worktree>
```

Use `git worktree prune` only after checking `git worktree list` and confirming
the missing paths are stale administrative records. Pruning is maintenance, not
evidence that ticket work is safe to discard.

## Dirty Worktrees

A dirty worktree is not automatically bad. Hidden dirty state is bad.

When dirty state exists:

- name whether it was pre-existing or produced by the current ticket
- keep unrelated user changes out of staging and commits
- record generated or untracked artifacts that affect evidence
- stop if the dirty state makes write-scope ownership ambiguous

## Abandoning Experimental Work

For spikes or failed attempts, prefer preserving conclusions in research and
evidence before cleanup.

Only delete the branch or worktree after the owner records say what was learned,
what was rejected, and whether any follow-up remains.
