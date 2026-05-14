---
name: loom-prototype-and-spike
description: "Use when the next step is building a disposable prototype/spike to answer a specific design, state-model, UI, interface, or integration question before committing production implementation."
---

# loom-prototype-and-spike

Prototype and spike is an exploration playbook.

It builds the smallest disposable artifact that answers a question, records the
answer, and then deletes, absorbs, or routes the result.

## Loom Routing

Common routes use these Loom skills for durable records or follow-up workflow:
`loom-research`, `loom-evidence`, `loom-specs`, `loom-constitution`,
`loom-knowledge`, `loom-tickets`, and `loom-audit`.

Ensure the `using-loom` skill is loaded before applying this workflow.

When routing to any named Loom skill, follow that skill's procedure and guidance
completely. This playbook adds workflow pressure; it does not shorten the target
skill's requirements.

Prototype code is not production work unless a later ticket deliberately absorbs
it.

A prototype is not a substitute for shaping the direction. Use it only after the
question is specific enough to answer without deciding the whole product,
system shape, data model, state model, or design direction by accident.

## Use This Playbook When

Use this playbook when:

- the operator asks to prototype, spike, sanity-check, or try options
- a state machine, data model, or information model is hard to reason about on paper
- UI direction needs visible alternatives before implementation
- interface shape is uncertain and examples would clarify it
- an integration assumption needs fast proof before planning
- a design decision would be expensive to reverse after full implementation

Skip it when existing source, specs, or tests can answer the question cheaply.

## Route

Use this route:

```text
question -> branch -> build throwaway -> observe -> decide -> preserve answer -> delete or absorb
```

## Question

Name the question before building.

Good prototype questions are specific:

- Does this state model produce understandable transitions?
- Which UI direction communicates the workflow best?
- Can this API shape express the common case simply?
- Does this library support the required integration path?

If the question is broad or vague, route to `loom-idea-refine`,
`loom-domain-language-and-decisions`, or `loom-research` first.

Do not build a prototype to avoid asking the operator what problem, boundary, data
model, state model, or design decision the prototype is supposed to clarify.

## Branch

Choose the prototype shape that answers the question.

Common branches:

- logic prototype: tiny runnable CLI, script, fixture, reducer, or state-machine
  harness for behavior and data questions
- UI prototype: several visibly different variants, reachable from one temporary
  route or switcher, for layout and interaction questions
- interface prototype: sample caller code and type shape for contract questions
- integration spike: minimal request, adapter, or fixture for source compatibility

State assumptions in the prototype header and/or linked research or evidence
record, clearly marked temporary, when the operator is not available to choose.

## Build Throwaway

Keep the artifact disposable from the start.

Rules:

- mark prototype files clearly as temporary
- place them near the relevant area only when that improves context
- provide one command or route to run it
- avoid persistence unless persistence is the question
- skip polish, broad error handling, and reusable abstractions
- surface state after each action or variant switch
- do not add production tests unless the prototype is being absorbed deliberately

Keep the prototype out of ticket scope unless the ticket explicitly asks for a
prototype.

## Observe

Capture the observation that answers the question.

Useful evidence:

- command output
- screenshot or browser observation
- state transition transcript
- variant comparison
- source behavior or compatibility note
- operator verdict

Use `loom-evidence` when the observation supports a later spec, decision, ticket,
or audit claim.

## Decide

Turn the observation into a route:

- update a spec when intended behavior or interface becomes clear
- update research when the answer is exploratory or source-grounded
- create a constitution decision when the result is hard to reverse and precedent
  setting
- create or update knowledge when the learning should be reused
- create a ticket when the prototype should be absorbed into production work
- abandon when the prototype invalidated the idea

## Delete Or Absorb

Do not leave prototype code rotting.

Choose one:

- delete after the answer is recorded
- absorb through a scoped ticket with production-quality tests and review
- keep temporarily with a ticketed expiration or cleanup owner

If absorption happens, treat it as implementation work and move still-relevant
assumptions into specs, research, or tickets. Prototype code does not get
grandfathered into production quality.

## Done Means

The prototype pass is done when:

- the question was explicit
- the artifact was scoped and marked as disposable
- the observation or operator verdict was captured
- durable learning moved to the right Loom record
- prototype code was deleted, absorbed through a ticket, or given an explicit
  cleanup route
