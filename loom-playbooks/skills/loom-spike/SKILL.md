---
name: loom-spike
description: "Run bounded spike or sketch investigations. Use when prototyping a data model, state machine, API shape, integration, performance idea, or several UI/product variants before committing to implementation."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-spike

Spikes and sketches are research-shaped workflows.

They are useful when the project needs bounded discovery before commitment.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- spike experiment framing
- sketch variant framing
- throwaway write-scope discipline
- product and UI variant discipline before commitment
- feasibility, performance, integration, and migration probe boundaries
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

Pick the branch before writing throwaway work:

- logic/state prototype when the question is about state transitions, data shape,
  API feel, or business rules;
- UI/product sketch when the question is about what a page, flow, affordance, or
  layout should feel like;
- technical experiment when the question is about feasibility, integration,
  performance, migration, or failure mode.

If the branch is ambiguous and the answer would change the artifact shape, ask a
focused question or record a reversible assumption before continuing.

If the spike only reads, compares, sketches, or records observations, research
and evidence may be enough. If the spike writes throwaway code, changes source
files, generates prototype artifacts, or makes other non-record repository
mutations, create or tighten a ticket and use a Ralph packet with explicit
cleanup expectations.

Ordinary Loom record updates that preserve research, evidence, spec, or wiki truth
are not throwaway prototype mutations by themselves; route them through their
owning skills. The ticket/Ralph branch is for throwaway code, source-tree changes,
generated prototype artifacts, or other non-record repository mutations.

Throwaway prototypes should answer one explicit question. Keep them obviously
temporary, runnable through one existing project command where practical, free of
production persistence by default, and instrumented enough to show the relevant
state after each action or variant switch. Skip polish, broad error handling, and
abstractions unless they are required to answer the question.

Record:

- question
- method
- experiment matrix
- child write scope and cleanup expectation
- run command or inspection method for throwaway artifacts when a prototype is
  created
- evidence gathered
- conclusions
- null results or rejected paths
- recommended downstream owner

Use a variant or experiment matrix when comparing options:

- Variant / hypothesis:
  Artifact or probe:
  Strength:
  Weakness:
  Decision:

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

UI/product variants should be structurally different: different layout,
information hierarchy, interaction model, or primary affordance. Variants that
only change color, copy, or spacing are tweaks, not sketch exploration.

Ask one visual or product question at a time when a choice would change the next
variant or downstream spec. Use realistic content when fake content would hide
layout, density, edge-case, or copy problems. Do not advance from sketch to
implementation until the accepted behavior or remaining uncertainty is routed to
spec, research, plan, ticket, or wiki.

Technical experiments should name the source version, dependency version, official
docs or project example inspected when correctness depends on it, and the exact
signal that would confirm or falsify the hypothesis. A performance spike needs a
baseline and a measurement method before optimization ideas are compared.

If a harness or local tool helps produce visual artifacts, treat that tool as
transport. It does not become a Loom layer. Preserve durable outputs in evidence
and route accepted behavior or explanation to spec or wiki.

## Common Rationalizations

- Rationalization: "I can just implement the first plausible idea."
  Reality: Spikes exist when the first plausible idea may be wrong; compare enough
  variants or hypotheses to learn.
- Rationalization: "This prototype is useful, so we should keep it."
  Reality: The answer is worth keeping. Throwaway scaffolding should be deleted,
  absorbed deliberately, or clearly contained.
- Rationalization: "Persistence makes the prototype more realistic."
  Reality: Persistence is usually the thing being tested; otherwise it creates
  cleanup risk and accidental dependency.
- Rationalization: "Three UI variants that share the same layout are enough."
  Reality: Sketch variants must disagree structurally or they will not reveal
  product direction.
- Rationalization: "No evidence is needed because it was exploratory."
  Reality: Exploration produces observations, rejected options, null results, and
  downstream recommendations worth preserving.
- Rationalization: "The prototype command worked once, so feasibility is proven."
  Reality: A spike proves only the named hypothesis under the observed source,
  version, and environment limits.

## Red Flags

- prototype branch does not match the question being answered
- throwaway code writes production data or becomes a hidden dependency
- prototype has no clear question, run path, visible state, or cleanup expectation
- variants differ only cosmetically
- technical experiment lacks source/version or measurement context
- conclusions live only in chat or screenshots with no research/evidence link
- cleanup or downstream route is unspecified

## Verification

- [ ] Question and chosen branch are explicit.
- [ ] Variant/experiment matrix records strengths, weaknesses, and decisions when options were compared.
- [ ] Evidence preserves artifacts or observations.
- [ ] Technical experiments name source/version context and the signal tested.
- [ ] Accepted behavior routes to spec; accepted explanation routes to wiki.
- [ ] Throwaway code is deleted, absorbed, or explicitly contained.
- [ ] Spikes that write throwaway code, source-tree changes, generated prototype
  artifacts, or other non-record repository mutations reconcile ticket state,
  evidence, critique disposition, and cleanup outcome before downstream work relies
  on the result.

## Done Means

- research owns conclusions and null results
- evidence owns observed artifacts
- any accepted behavior is routed to spec
- any accepted explanation is routed to wiki
- throwaway code is removed or explicitly contained
- if the spike wrote throwaway code, changed source files, generated prototype
  artifacts, or made other non-record repository mutations, the owning ticket
  tells the truth about state, evidence, review disposition, and cleanup

## Read In This Order

Read immediately for spike or sketch work:

1. the core `loom-research` skill when recording experiment method, conclusions,
   rejected options, or null results.
2. the core `loom-evidence` skill when preserving screenshots, logs, artifacts,
   or observed outputs.

Then read conditionally:

3. the core `loom-tickets` and `loom-ralph` skills when the spike or sketch
   writes throwaway code, changes source files, generates prototype artifacts, or
   makes other non-record repository mutations.
4. the core `loom-critique` skill when variants or experiment conclusions need
   adversarial review.
5. the core `loom-specs` skill when accepted behavior should become a contract.
6. the core `loom-wiki` skill when accepted explanation should become reusable.
