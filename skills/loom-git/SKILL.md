---
name: loom-git
description: "Use Git for Loom implementation isolation, diff review, and provenance. Use when discovering a repository's integration baseline, preparing branches or worktrees, coordinating parallel Ralph work, reviewing diffs, staging commits, merging, or recording Git context in packets and evidence."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-git

Git is Loom's implementation isolation and source-history surface.

Branches, commits, worktrees, remotes, patch stacks, and PRs preserve
implementation history and transport work. Use Loom records for the objective,
live state, evidence, review, and accepted explanation around that work.

The first Git question is not "what common branch name should I use?" The first
Git question is: what integration baseline owns this repository's next change?

That baseline may be a remote-tracking branch, a local branch, a release branch,
a fork upstream, a patch-stack parent, a tag, or a specific commit. If Loom
cannot identify it from records, repository policy, remote metadata, or operator
input, scope fails closed.

## What This Workflow Coordinates

- repository state inspection before work begins
- integration baseline discovery and freshness checks
- remote ref refresh when a remote exists and matters
- branch naming and branch base selection without assuming branch names
- worktree creation, reuse, handoff, and cleanup discipline
- Git provenance in Ralph packets and evidence
- parallel Ralph isolation across branches, worktrees, and repositories
- diff, staging, commit, merge, and PR hygiene as they relate to Loom truth

## What Git Does Not Own

- intended behavior, which belongs in specs and tickets
- live execution state, which belongs in tickets
- bounded child authority, which belongs in packets
- observed evidence claims, which belong in evidence
- review verdicts, which belong in critique
- accepted explanation, which belongs in wiki
- external shipping summaries, which belong in `loom-ship`
- acceptance or closure, which belongs in the ticket acceptance gate

## Use This Skill When

- a Ralph iteration will mutate files inside a Git repository
- you need a branch or worktree before starting a ticket slice
- you need to discover or refresh the integration baseline before branching
- parallel Ralph workers or multiple repositories need isolation
- packet `source_fingerprint` or `execution_context` needs Git provenance
- you are reviewing diffs, staging changes, committing, rebasing, merging, or
  preparing work for a PR
- a dirty worktree, stale branch, or ambiguous remote could make Loom claims
  untrustworthy

## Do Not Use This Skill When

- the workspace is not a Git repository and no Git boundary exists
- the real issue is unclear ownership, fuzzy behavior, missing evidence, or an
  unready ticket
- you are tempted to use a branch name, commit message, or PR description as the
  place where live work status is decided
- the work is a tiny Loom record edit that does not need branch or worktree
  isolation

## Default Procedure

1. Confirm the repository root and Loom scope before touching branches or
   worktrees.
2. Inspect current state with `git status --short`, `git branch --show-current`,
   and `git remote -v`.
3. Discover the integration baseline from Loom records, operator request,
   project policy, PR target, branch tracking config, remote metadata, or an
   explicit commit.
4. Fetch the relevant remote refs when a remote-backed baseline exists; do not
   invent a remote or branch name from habit.
5. Choose the lightest safe isolation: current clean branch for trivial local
   work, one ticket branch for normal work, or one worktree per parallel Ralph
   child.
6. Create new work from the resolved baseline, not from an assumed local branch.
7. Record `integration_ref`, `integration_commit`, `integration_remote`, current
   commit, branch, worktree path, push remote, and isolation mode in the Ralph
   packet when packetized work is involved.
8. Keep the child inside the packet's `child_write_scope`; Git isolation does not
   widen Loom write authority.
9. Review `git status --short` and `git diff` before handoff, evidence, commit,
   critique, or shipping.
10. Stage, commit, merge, and clean up only the work that belongs to the ticket,
    and leave the ticket/evidence/critique graph truthful afterward.

## Worktree Rule

Use a separate worktree when two agents or two tickets could otherwise touch the
same checkout at the same time.

For parallel Ralph, the normal shape is:

```text
one ticket slice -> one packet -> one branch -> one worktree -> one child
```

Parallel work is safe only when Loom write scopes and Git worktrees are both
independent.

## Git Truth Boundary

Git can answer:

- what changed in files
- which commit or branch a packet was compiled against
- which integration remote and ref were used when a remote-backed baseline exists
- whether a worktree was dirty
- whether a branch contains or diverges from a resolved integration baseline
- whether a diff matches the claimed write scope

Git cannot answer by itself:

- whether the intended behavior was correct
- whether acceptance criteria are satisfied
- whether evidence is sufficient
- whether critique is required or resolved
- whether a ticket may close

## Done Means

- the branch or worktree starts from an explicit integration baseline
- dirty state and unrelated changes are visible instead of hidden
- Ralph packets name the Git execution context when Git matters
- parallel workers have non-overlapping Loom write scopes and distinct Git
  isolation
- diffs, commits, PRs, and cleanup do not create a shadow ledger outside Loom
- ticket, evidence, critique, and retrospective / promotion disposition remain
  truthful

## Read In This Order

Read immediately for normal Git-backed Loom work:

1. `references/branch-and-remote-hygiene.md` when preparing a branch, checking
   freshness, or deciding what integration baseline the work should use.
2. `references/worktree-discipline.md` when creating, reusing, handing off, or
   removing Git worktrees.

Then read conditionally:

3. `references/parallel-ralph-with-git.md` when multiple Ralph workers, tickets,
   repositories, or worktrees may run at once.
4. `references/diff-commit-and-merge-hygiene.md` when reviewing, staging,
   committing, merging, rebasing, or packaging changes.
5. `skills/loom-workspace/references/scope-registry.md` when repository aliases
   or multi-repo scope are unclear.
6. `skills/loom-ralph/SKILL.md` when Git work is part of a bounded packetized
   implementation iteration.
