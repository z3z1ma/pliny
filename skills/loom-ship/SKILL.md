---
name: loom-ship
description: "Package already-truthful Loom work for merge, release, or handoff without closing tickets. Use when ticket, evidence, critique, and promotion disposition should become a PR summary, release note draft, risk summary, or follow-up list."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-ship

Shipping packages work for an external handoff.

It does not own closure. The ticket acceptance gate owns closure; optional
commands may invoke that workflow but do not own it.

## What This Workflow Coordinates

- PR or merge summary drafting
- release note drafting
- evidence summary
- risk summary
- follow-up list
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
- the goal is to close the work

## Inputs

- ticket or tickets
- plan or initiative, when relevant
- evidence
- critique
- retrospective / promotion disposition, plus route-specific wiki disposition when
  wiki was one selected promotion route
- known follow-ups
- external refs, when present

## Outputs

- PR summary
- test or evidence summary
- risk summary
- follow-up list
- release note draft when useful
- handoff option summary for merge, PR, keep, or abandon decisions when relevant

## Guardrail

Shipping may summarize and package. Ticket-owned acceptance disposition owns closure.

## Done Means

- the package cites Loom records rather than relying on conversation context
- risks and unresolved follow-ups are visible
- external summaries remain summaries; ticket acceptance still decides closure
- the next route is explicit, usually ticket acceptance review or critique

## Read In This Order

Read immediately for shipping/package work:

1. `skills/loom-tickets/SKILL.md` when reading ticket state, acceptance, and
   live execution truth.
2. `skills/loom-evidence/SKILL.md` when checking evidence artifacts or evidence
   summaries.
3. `skills/loom-records/SKILL.md` when checking links, external refs, or claim
   coverage grammar.

Then read conditionally:

4. `references/handoff-options.md` when a branch, worktree, PR, or external
   handoff needs an explicit merge / PR / keep / abandon decision.
5. `skills/loom-git/SKILL.md` when the handoff involves branch, worktree, diff,
   merge, PR, cleanup, or abandon operations.
6. `skills/loom-critique/SKILL.md` when unresolved risk or review disposition
   affects packaging.
7. `skills/loom-wiki/SKILL.md` when accepted explanation or release notes need
   wiki-backed wording.
