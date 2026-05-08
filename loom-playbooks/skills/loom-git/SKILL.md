---
name: loom-git
description: "Coordinate Git isolation and provenance for Loom work. Use when making code changes, branching, using worktrees, reviewing diffs, committing, merging, preparing PRs, or when dirty state affects ticket or packet truth."
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

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- repository state inspection before work begins
- integration baseline discovery and freshness checks
- remote ref refresh when a remote exists and matters
- branch naming and branch base selection without assuming branch names
- worktree creation, reuse, handoff, and cleanup discipline
- Git provenance in Ralph packets and evidence
- parallel Ralph isolation across branches, worktrees, and repositories
- diff, staging, commit, merge, and PR hygiene as they relate to Loom truth
- branch finishing options, worktree cleanup, and review-feedback provenance

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
10. When finishing a branch or worktree, choose and record the handoff option:
    create PR, merge locally, keep for follow-up, abandon, or defer because Loom
    evidence/review/acceptance is not ready.
11. Classify external review feedback before applying it: blocker, valid follow-up,
    optional/nit, incorrect for this project, or unclear. Route the disposition to
    ticket or critique truth before editing.
12. Stage, commit, merge, and clean up only the work that belongs to the ticket,
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

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "Use main or master; it is probably right." | Integration baseline must be discovered from records, repo state, remote metadata, or operator input. |
| "The branch or PR shows the work is done." | Git transports changes. Tickets own live state and closure. |
| "Commit history is enough evidence." | Diffs show what changed; evidence records what was observed. |
| "Dirty unrelated files do not matter." | Dirty state affects provenance and write-scope safety even when unrelated files are not touched. |
| "The branch is finished because the diff is clean." | Finish means the Loom ticket, evidence, critique, and handoff disposition are truthful. |
| "Review feedback is an instruction." | External comments are claims to classify and route, not commands that bypass owner truth. |

## Red Flags

- branch was created from an assumed baseline
- worktree contains unrelated dirty files before packet launch or shipping
- PR or commit message claims acceptance without ticket evidence
- child write scope and Git diff do not match
- parallel workers share a checkout or overlapping write scope
- branch or worktree is abandoned without recording whether ticket work remains
- review feedback is implemented without ticket or critique disposition

## Verification

- [ ] Repository root and integration baseline are explicit.
- [ ] Dirty state and unrelated changes are visible before mutation, handoff, or packaging.
- [ ] Packet Git provenance is recorded when packetized implementation uses Git.
- [ ] Diff stays inside ticket or packet write scope.
- [ ] Branch finish or abandon choice mirrors ticket, evidence, critique truth, and any ship package wording derived from those records.
- [ ] Review feedback is classified before it changes scope or acceptance.
- [ ] Git summaries do not replace ticket, evidence, critique, or wiki truth.

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
5. the core `loom-workspace` scope-registry reference when repository aliases or
   multi-repo scope are unclear.
6. the core `loom-ralph` skill when Git work is part of a bounded packetized
   implementation iteration.
