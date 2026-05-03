# Handoff Options

Use this reference when implementation work is substantially complete and the
operator needs an explicit branch, PR, merge, keep, or abandon decision.

Shipping packages already-truthful Loom work. It does not close tickets.

Use `skills/loom-git/SKILL.md` for the Git mechanics behind branch, worktree,
diff, merge, PR, cleanup, or abandon operations. This reference only shapes the
handoff decision and package.

## Preconditions

Before presenting handoff options, check:

- ticket state, acceptance criteria, evidence, critique disposition,
  retrospective / promotion disposition, and route-specific wiki disposition when
  wiki was selected
- current Git branch/worktree, changed files, untracked files, and relevant diff
- verification evidence fresh enough for the handoff claim
- unresolved medium/high critique findings or required follow-ups

If required evidence or critique is missing, route there before presenting the
work as ready to merge or PR.

## Standard Options

Offer only options that are actually safe in the current repository state.

Common options:

1. merge locally into the integration branch
2. push and create or update a pull request
3. keep the branch or worktree for later
4. abandon the work

For each option, say what Loom truth will remain after the action:

- which ticket owns acceptance or remaining work
- which evidence supports the handoff
- which critique findings remain open, accepted, or resolved
- whether retrospective / promotion follow-through is complete or deferred,
  including route-specific wiki follow-through when wiki was selected

## Merge Or PR

Before merge or PR packaging:

- cite ticket, evidence, critique, and follow-up records in the summary
- rerun or cite integration validation when several child branches were combined
- keep external PR descriptions as mirrors of Loom truth, not the canonical ledger
- do not mark the ticket `closed` unless the ticket acceptance gate has actually
  closed it

## Keep Branch Or Worktree

If the operator chooses to keep the branch or worktree:

- record where it lives
- record what remains to be done
- keep the ticket in the truthful state (`active`, `blocked`,
  `review_required`, or `complete_pending_acceptance`)
- do not clean up files or worktrees that may contain useful evidence or work

## Abandon Work

Abandoning work is destructive if it deletes branches, commits, worktrees, or
untracked artifacts.

Before abandonment:

- preserve useful conclusions, rejected options, and validation output in
  research or evidence
- update the ticket with cancellation or follow-up truth
- ask for explicit confirmation before deleting local work
- inspect the branch/worktree state and name what would be lost

Never discard work merely because it failed. Failed attempts often belong in
research, evidence, critique, or a follow-up ticket before cleanup.
