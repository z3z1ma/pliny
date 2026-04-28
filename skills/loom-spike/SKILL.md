---
name: loom-spike
description: "Run bounded spike and sketch investigations as research variants. Use when an experiment, prototype, or UI/product sketch should produce evidence, conclusions, null results, and a downstream route without becoming a new layer."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-spike

Spikes and sketches are research-shaped workflows.

They are useful when the project needs bounded discovery before commitment.

## What This Workflow Coordinates

- spike experiment framing
- sketch variant framing
- throwaway write-scope discipline
- evidence and null-result capture
- downstream routing after discovery

## Use This Skill When

- a technical question needs a bounded experiment
- a design question needs a few concrete variants
- a throwaway prototype should inform a spec, plan, ticket, or wiki page
- rejected paths and null results should remain citable

## Do Not Use This Skill When

- the intended behavior is already clear enough for a normal ticket
- the work needs production-quality implementation
- the artifact should become accepted explanation without critique or evidence

## Spike Flow

`question -> experiment matrix -> bounded throwaway child write scope -> evidence -> conclusions/null results -> downstream route`

If the spike only reads, compares, sketches, or records observations, research
and evidence may be enough. If the spike writes throwaway code or mutates the
repository, create or tighten a ticket and use a Ralph packet with explicit
cleanup expectations.

Record:

- question
- method
- experiment matrix
- child write scope and cleanup expectation
- evidence gathered
- conclusions
- null results or rejected paths
- recommended downstream owner

## Sketch Flow

`design question -> 2-3 variants -> screenshots or artifacts -> critique -> accepted wiki/spec updates`

Sketches are the Loom adaptation of visual brainstorming. Use them when seeing a
mockup, diagram, state flow, layout comparison, or spatial relationship would
make a decision more honest than text alone.

Record:

- design question
- variants
- screenshots, prototypes, or other artifacts
- critique findings
- accepted behavior or explanation
- downstream spec, wiki, or ticket recommendation

If a harness or local tool helps produce visual artifacts, treat that tool as
transport. It does not become a Loom layer. Preserve durable outputs in evidence
and route accepted behavior or explanation to spec or wiki.

## Done Means

- research owns conclusions and null results
- evidence owns observed artifacts
- any accepted behavior is routed to spec
- any accepted explanation is routed to wiki
- throwaway code is removed or explicitly contained

## Read In This Order

Read immediately for spike or sketch work:

1. `skills/loom-research/SKILL.md` when recording experiment method,
   conclusions, rejected options, or null results.
2. `skills/loom-evidence/SKILL.md` when preserving screenshots, logs,
   artifacts, or observed outputs.

Then read conditionally:

3. `skills/loom-tickets/SKILL.md` and `skills/loom-ralph/SKILL.md` when the
   spike or sketch writes throwaway code or mutates repository files.
4. `skills/loom-critique/SKILL.md` when variants or experiment conclusions need
   adversarial review.
5. `skills/loom-specs/SKILL.md` when accepted behavior should become a contract.
6. `skills/loom-wiki/SKILL.md` when accepted explanation should become reusable.
