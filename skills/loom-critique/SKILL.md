---
name: loom-critique
description: "Run adversarial review as a first-class Loom layer. Use when a result needs pressure-testing, when confidence should be challenged against evidence, when residual risk must be surfaced durably, or when acceptance should be informed by a governed verdict rather than optimistic self-review."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  loom_layer: critique
  protocol_version: "2.0"
---

# loom-critique

Critique is the adversarial review layer.

This skill exists so review has the same durability and rigor as execution.

## What This Skill Owns

- critique records
- critique packets
- findings and verdicts
- named critique profiles
- review severity and disposition
- follow-up pressure on tickets, specs, plans, and wiki pages

## Use This Skill When

- implementation claims need pressure-testing
- accepted-shape claims feel risky
- evidence may be weaker than the prose suggests
- the change class calls for review before acceptance
- a wiki page may be overstating certainty

## Do Not Use This Skill When

- the next move is clearly implementation
- you only need a tiny local sanity check
- you want to silently mutate the ticket instead of leaving a review record

## Critique Posture

Critique should be:

- skeptical but fair
- evidence-oriented
- explicit about severity and confidence
- durable enough for future agents to inspect

## Default Procedure

1. choose the review target
2. choose critique profiles proportional to the risk
3. compile a critique packet if fresh-context review is warranted
4. inspect the relevant records, evidence, and changed files
5. write findings with severity, confidence, and challenged claims when relevant
6. record the verdict and required follow-up
7. link the critique back to the target ticket and related artifacts

## Done Means

- the review target is explicit
- the verdict is explicit
- the major findings are explicit
- follow-up implications are explicit

## Read In This Order

1. `references/critique-lens.md`
2. `references/finding-format.md`
3. `templates/critique.md`
4. `templates/critique-packet.md`
