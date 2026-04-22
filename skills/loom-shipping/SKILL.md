---
name: loom-shipping
description: "Package already-truthful Loom work for merge, release, or handoff without closing tickets. Use when ticket, evidence, critique, and wiki disposition should become a PR summary, release note draft, risk summary, or follow-up list."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  loom_layer: workflow
  protocol_version: "2.0"
---

# loom-shipping

Shipping packages work for an external handoff.

It does not own closure. `/loom-accept` owns ticket closure.

## What This Skill Owns

- PR or merge summary drafting
- release note drafting
- evidence summary
- risk summary
- follow-up list
- external handoff packaging

## Use This Skill When

- implementation and evidence are already recorded
- critique and wiki disposition need to be summarized
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
- wiki disposition
- known follow-ups
- external refs, when present

## Outputs

- PR summary
- test or evidence summary
- risk summary
- follow-up list
- release note draft when useful

## Guardrail

Shipping may summarize and package. Acceptance owns closure.

## Done Means

- the package cites Loom records rather than transcript memory
- risks and unresolved follow-ups are visible
- external summaries do not become a competing execution ledger
- the next command is explicit, usually `/loom-accept` or `/loom-review`

## Read In This Order

1. `skills/loom-records/SKILL.md`
2. `skills/loom-tickets/SKILL.md`
3. `skills/loom-critique/SKILL.md`
4. `skills/loom-wiki/SKILL.md`
