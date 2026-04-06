---
name: loom-research
description: Maintain Loom research memory: durable evidence, experiments, investigations, comparisons, spikes, synthesis notes, and reusable findings. Use when evidence gathering, option analysis, technical investigation, experiments, or discovery work should inform later specs, plans, tickets, critique, or docs. Not for live execution tracking, behavior contracts, or final accepted documentation.
compatibility: Designed for this Markdown-first Loom repository.
metadata:
  author: agent-loom
  version: "0.1"
  loom-layer: evidence-memory
---

# loom-research

Research is the Loom evidence and discovery layer.

Use this skill to preserve reusable discovery before execution outruns understanding.

## Use This Skill When

- the team needs evidence before choosing a spec or plan direction
- an option comparison, experiment, or investigation result should be durable
- the work produces reusable findings that later artifacts should cite

## Do Not Use This Skill When

- you are tracking live task execution
- you are writing the final behavioral contract
- you are writing accepted explanation for operators or maintainers

## What This Skill Governs

- research records

## Research Posture

Research records should be written for reuse.

A future agent should be able to read the note and understand:

- what was being asked
- how it was investigated
- what evidence was gathered
- what conclusions are justified now
- what downstream work should do with the result

Do not let research collapse into a raw transcript dump. The durable value is curated synthesis.

## Before You Write

1. read existing research for overlap so you do not create competing notes for the same question
2. define the exact question and the decision that the research is meant to inform
3. decide the scope and non-goals up front so the note does not widen silently

## Execution Playbook

1. create a research note only if the question is not already owned elsewhere
2. if you create a note, populate the question, objective, scope, and methodology sections immediately
3. record evidence as evidence, not as vague impressions
4. separate experiments from conclusions so later readers can audit the reasoning chain
5. synthesize findings into explicit conclusions and recommendations
6. link the research to the specs, plans, tickets, initiatives, critique, or docs it informs
7. validate the note before relying on it downstream

## How To Use The Scripts

Read `references/scripts.md` for the bundled CLI surface, including argument meanings and example invocations.

- `scripts/research.py create`: use when a new question needs durable investigation space in `.loom/research/`
- `scripts/research.py create`: after running it, populate the body immediately; the command only creates the record shell
- `scripts/research.py link`: use after the note has meaningful conclusions so downstream consumers are explicit

## Neighboring Layer Boundaries

- research is not the execution ledger
- research is not the final explanatory docs layer
- research should feed specs, plans, tickets, critique, and docs with durable evidence and conclusions
- if the note starts reading like intended behavior, move that truth into a spec

## What Good Looks Like

- the question is crisp
- the investigation method is visible
- the evidence is concrete enough to audit later
- the conclusions are bounded by what the evidence actually supports
- downstream work knows what to do with the findings

## Validation Focus

- required sections present
- downstream links explicit where needed
- research remains scoped and reusable
- methodology and conclusions are visible enough to evaluate later

## Failure Conditions

- the note is mostly transcript with no synthesis
- conclusions overclaim beyond the evidence
- the question or scope remains vague
- downstream implications are implied but not stated
- a freshly created note remains mostly empty and still gets treated as authoritative

## Done Means

- the note preserves reusable findings rather than ephemeral chat
- evidence, conclusions, and recommendations are explicit
- downstream links are present where useful
- the scaffold and frontmatter are explicit enough for later workspace validation

## Read In This Order

1. `references/schema-research.md`
2. `references/scripts.md`
3. `references/examples.md`

## References

- `references/schema-research.md`
- `references/scripts.md`
- `references/examples.md`
