---
name: loom-ship
description: "Package already-truthful Loom work. Use when drafting PR descriptions, changelogs, release notes, merge/handoff summaries, launch or rollback notes, evidence/risk summaries, or follow-up lists that must mirror owner records."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-ship

Shipping packages already-truthful Loom work for an external handoff.

It does not own closure. The ticket-owned acceptance gate evaluates acceptance,
closure readiness, and residual risk; optional commands may invoke that workflow
but do not own it.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- PR or merge summary drafting
- release note drafting
- evidence summary
- risk summary
- follow-up list
- CI, release, rollout, and rollback package summaries
- external handoff packaging

## Use This Skill When

- implementation and evidence are already recorded
- critique and retrospective / promotion disposition need to be summarized
- work needs to be packaged for PR, release, review, or handoff
- external systems need a mirror of Loom truth

## Do Not Use This Skill When

- the ticket is not yet truthful
- evidence is missing
- critique is required but unresolved
- the goal is for shipping itself to evaluate acceptance, closure readiness, or
  residual risk
- the goal is to close the work

## Inputs

- ticket or tickets
- plan or initiative, when relevant
- evidence
- critique
- retrospective / promotion disposition, plus wiki-specific disposition when wiki
  was one selected promotion path
- known follow-ups
- external refs, when present

## Outputs

- PR summary
- test or evidence summary
- risk summary
- follow-up list
- release note draft when useful
- handoff option summary for merge, PR, keep, or abandon decisions when relevant
- launch or rollback note when deployment risk, monitoring, migrations, feature
  flags, or staged rollout are in scope
- CI or automation status summary when quality gates, flaky checks, deployment
  pipelines, or generated artifacts affect the handoff

## Guardrail

Shipping may summarize and package already-truthful ticket, evidence, critique,
wiki, risk, and follow-up disposition. Ticket-owned acceptance disposition owns
closure.

Before packaging, confirm the packaging preconditions are true for the handoff:
ticket truth is current, evidence and critique dispositions are sufficient for the
handoff claim, scope and safety limits are respected, Git/worktree state is known
when files are being packaged, and external summaries will mirror Loom truth. If
`ship` is being invoked from `loom-drive`, satisfy the drive hard preflight gates
from current owner records before packaging. Support checkpoints may help locate
or summarize those facts, but they do not clear gates by themselves.

For releases or launches, mirror the owner records into an explicit package:
validated scope, evidence summary, critique/finding disposition, known residual
risks, documentation or wiki sync status, rollback or abandon option, monitoring
or post-launch check, and follow-up ownership. If those facts are not already
truthful in tickets, evidence, critique, wiki, plans, or constitution, route back
before packaging.

For feature-flagged or staged rollouts, include the flag owner, intended expiry or
cleanup trigger, rollout stages, advance/hold/rollback thresholds, monitoring
checks, and how both enabled and disabled states were or were not verified. Feature
flags make launch safer; they do not eliminate evidence, critique, cleanup, or
ticket-owned acceptance obligations.

For CI/CD or automation handoffs, package the current owner-record truth: which
checks ran, which checks were skipped or flaky, what generated artifacts changed,
what deployment or rollback path is available, what monitoring or post-launch
observation is expected, and who owns any follow-up. Pipeline output is evidence;
ship mirrors its disposition and does not turn a green pipeline into acceptance.

For migration or deprecation handoffs, include replacement path, old-path status,
consumer movement, zero-usage or safe-removal evidence, rollback or re-enable
conditions, and cleanup tickets. A release note that says "removed" is not enough
if references, flags, docs, tests, or consumers still need reconciliation.

External review comments are handled as claims to classify, not as commands:
required blocker, valid out-of-scope follow-up, optional/nit, incorrect for this
project, or unclear. Ticket truth owns how each classification affects closure;
ship only mirrors the disposition into PR, release, or handoff wording.

## Common Rationalizations

- **"The PR description can explain what is true."** Reality: PRs mirror Loom
  truth. They do not own acceptance, evidence, or risk.
- **"Shipping means the work is done."** Reality: Shipping packages
  already-truthful work; ticket acceptance owns closure.
- **"Known follow-ups can stay in the handoff."** Reality: Follow-ups that affect
  closure or future work need ticket-owned disposition or new tickets.
- **"A clean diff is enough to package."** Reality: The package also needs current
  evidence, critique disposition, and residual risk.
- **"Launch notes can be written from memory."** Reality: Launch and rollback
  packages must mirror recorded evidence, risks, and owner dispositions.
- **"A feature flag means cleanup can wait indefinitely."** Reality: Flags need
  owner, expiry or cleanup trigger, and follow-up disposition. Otherwise they
  become zombie code.
- **"The pipeline is green, so the release is accepted."** Reality: CI is
  evidence. Ticket acceptance still owns closure and residual risk.
- **"Migration cleanup can be mentioned in release notes."** Reality: Migration
  follow-through needs owner-layer disposition or linked tickets.

## Red Flags

- external summary makes stronger claims than ticket/evidence/critique supports
- unresolved medium/high critique findings are hidden in release or PR wording
- follow-ups are listed without owner, disposition, or ticket linkage
- launch or rollback claims appear without health, monitoring, migration,
  rollback, or post-launch evidence appropriate to the scope
- Git state is unknown for files being packaged
- CI or generated-artifact status is summarized without evidence or ticket disposition
- migration cleanup, zero-usage, or rollback facts are stronger than owner records support
- shipping is used to bypass retrospective or acceptance gates

## Verification

- [ ] Ticket, evidence, critique, and promotion dispositions are current before packaging.
- [ ] External summary mirrors owner records and names residual risks.
- [ ] Follow-ups have owner-layer disposition or ticket links.
- [ ] Launch, rollback, monitoring, and docs-sync claims are backed by owner
      records or marked out of scope.
- [ ] CI/CD, generated-artifact, migration, and cleanup claims mirror owner records.
- [ ] Git/worktree state is known when shipping file changes.
- [ ] No closure claim is made outside the ticket acceptance gate.

## Done Means

- the package cites Loom records rather than relying on conversation context
- risks and unresolved follow-ups are visible
- external summaries remain summaries; ticket acceptance still decides closure
- unresolved handoff actions and ticket-owned acceptance gaps are explicit

## Read In This Order

Read immediately for shipping/package work:

1. the core `loom-tickets` skill when reading ticket state, acceptance, and live
   execution truth.
2. the core `loom-evidence` skill when checking evidence artifacts or evidence
   summaries.
3. the core `loom-records` skill when checking links, external refs, or claim
   coverage grammar.

Then read conditionally:

4. `references/handoff-options.md` when a branch, worktree, PR, or external
   handoff needs an explicit merge / PR / keep / abandon decision.
5. the core `loom-evidence` and `loom-tickets` skills before making ready,
   passing, deployable, or complete claims in the package.
6. `skills/loom-code-review/SKILL.md` when review request, received feedback, or
   finding disposition shapes the handoff.
7. `skills/loom-ci-cd/SKILL.md` when quality gates, preview deployments, rollout,
   rollback, automation, or pipeline failures shape the handoff.
8. `skills/loom-docs-sync/SKILL.md` when README, changelog, API docs, or release
   notes must mirror owner truth.
9. `skills/loom-git/SKILL.md` when the handoff involves branch, worktree, diff,
   merge, PR, cleanup, or abandon operations.
10. `skills/loom-migration/SKILL.md` when replacement, deprecation, zero-usage,
    removal, or migration cleanup shapes the handoff.
11. the core `loom-critique` skill when unresolved risk or review disposition
    affects packaging.
12. the core `loom-wiki` skill when accepted explanation or release notes need
    wiki-backed wording.
