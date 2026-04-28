# Problem Shaping

Problem shaping is the divergent pre-planning posture for fuzzy requests.

It should make the request legible enough to route, without prematurely
creating initiatives, specs, plans, or tickets.

## Use When

- the request is fuzzy
- assumptions are hidden
- precedent may already answer the question
- the honest next move is questions rather than records

## Procedure

1. Orient without committing.
2. Restate the request in one or two sentences.
3. Name what is unclear.
4. Ask a small number of sharp clarifying questions.
5. Check constitution, decisions, wiki, and prior research for precedent.
6. Surface assumptions as accepted, to-be-confirmed, or contested.
7. When the work is creative or behavior-shaping, present two or three viable
   approaches with tradeoffs and a recommendation before narrowing.
8. Route to the next owner layer or workflow.

## Creative Shaping

Use creative shaping when the request could reasonably produce different valid
designs, behaviors, architectures, UI shapes, or rollout paths.

The goal is not to create a new design-doc ledger. The goal is to make the next
owner-layer mutation safe.

Do this:

- ask one question at a time when the operator needs to choose or clarify
- prefer multiple-choice questions when that lowers friction without hiding nuance
- name purpose, constraints, success criteria, and non-goals before proposing work
- propose two or three approaches with tradeoffs when alternatives matter
- separate accepted assumptions from contested or unconfirmed assumptions
- keep large multi-subsystem ideas decomposed before creating one oversized plan
- route accepted intended behavior to spec and sequencing to plan

For visual, spatial, or product-shape questions, a sketch route may be better
than more prose. Use `loom-spike` sketch flow when mockups, diagrams, screenshots,
or side-by-side variants would make the choice clearer. Evidence owns the
observed artifacts; specs and wiki own accepted behavior or explanation.

## Routes

- clear enough to sequence -> plan
- evidence missing -> research
- behavior unclear -> spec
- design alternatives need artifacts -> spike/sketch evidence, then spec or wiki
- durable choice needed -> constitution decision
- already answered -> cite the existing owner record
- still too fuzzy but worth preserving -> research with `status: deferred_questions`

## Guardrails

- Do not draft execution records from a still-fuzzy request.
- Do not answer with code.
- Do not silently choose between ambiguous readings.
- Do not bypass constitutional conflicts.
- Do not let an approved-sounding chat summary replace spec, plan, or ticket
  ownership when the decision needs to persist.
