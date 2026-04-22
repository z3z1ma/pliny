---
name: loom-spike
description: "Run bounded spike and sketch investigations as research variants. Use when an experiment, prototype, or UI/product sketch should produce evidence, conclusions, null results, and a downstream route without becoming a new layer."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  loom_layer: workflow
---

# loom-spike

Spikes and sketches are research-shaped workflows.

They are useful when the project needs bounded discovery before commitment.

## What This Skill Owns

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

Record:

- design question
- variants
- screenshots, prototypes, or other artifacts
- critique findings
- accepted behavior or explanation
- downstream spec, wiki, or ticket recommendation

## Done Means

- research owns conclusions and null results
- evidence owns proof artifacts
- any accepted behavior is routed to spec
- any accepted explanation is routed to wiki
- throwaway code is removed or explicitly contained

## Read In This Order

Read immediately for spike or sketch work:

1. `skills/loom-research/SKILL.md` when recording experiment method,
   conclusions, rejected options, or null results.
2. `skills/loom-records/templates/evidence.md` when preserving screenshots,
   logs, artifacts, or observed outputs.

Then read conditionally:

3. `skills/loom-critique/SKILL.md` when variants or experiment conclusions need
   adversarial review.
4. `skills/loom-specs/SKILL.md` when accepted behavior should become a contract.
5. `skills/loom-wiki/SKILL.md` when accepted explanation should become reusable.
