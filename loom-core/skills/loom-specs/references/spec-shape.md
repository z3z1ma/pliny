# Spec Shape

A spec is a durable behavior contract.

It should be as small as the behavior allows and as precise as downstream work
needs.

A spec is not a product-wide constitution. It should describe one coherent product
slice, and its status must stay truthful for the current product surface area it
claims to cover.

The current spec set, meaning `active` and `accepted` specs together, should be
complete enough to regenerate the intended product behavior from scratch without
depending on chat history or treating the current implementation as the behavior
contract.

## Required Shape

A useful spec says:

- what behavior or interface it defines
- what product slice it owns and where that slice stops
- what problem, ambiguity, or shared contract requires a spec
- what the desired behavior is
- what is out of scope
- what domain model, data shape, state shape, interface boundary, or abstraction
  should guide downstream work when relevant
- which requirements must hold
- which scenarios exercise those requirements
- what evidence could show the behavior works
- what questions or assumptions remain

Use optional sections when they clarify downstream work: quality bar, interface
contract, examples and non-examples, constraints, amendment notes, or related
records.

## Product Slice

Choose the slice before writing requirements.

A good spec slice is one behavior, workflow, interface, record shape, permission
boundary, error semantic, or quality contract whose requirements change together
and whose scenarios can be reviewed together.

Do not write one all-encompassing spec for a whole product, package, application,
agent, UI, protocol, or broad product surface. Separate product surfaces should be
separate specs connected through `## Related Records`, a plan, research synthesis,
or knowledge when broader orientation is useful.

Use these split heuristics:

- split by actor or job when different users, agents, operators, maintainers, or
  systems need different outcomes
- split by workflow when behaviors can be started, completed, blocked, retried, or
  accepted independently
- split by interface when APIs, commands, records, components, packets, files, or
  data shapes have different callers or compatibility promises
- split by risk or permission boundary when one area has different authorization,
  privacy, safety, migration, or rollback concerns
- split by evidence when one evidence plan cannot honestly validate the whole
  contract without unrelated checks
- split by lifecycle when one area may become `active`, `accepted`, `superseded`,
  or `retired` independently of another

Broad wording is a smell. If the title or summary needs `entire`, `all`,
`platform`, `system`, `product`, or several unrelated `and` clauses, narrow the
slice or create multiple specs.

When a broad spec already exists, do not keep adding unrelated requirements. Extract
coherent product slices into successor specs, keep only the cross-links needed for
navigation, and mark the umbrella record `superseded` or narrow its scope until its
status is truthful.

## Spec Set Coverage

The current spec set should act like a rebuildable behavior map. If all
implementation disappeared, the `active` and `accepted` specs should describe the
observable product surface well enough for downstream agents to recreate intended
behaviors, interfaces, workflows, record shapes, permission boundaries, error
states, quality bars, and compatibility expectations.

Use that goal to find missing specs, not to enlarge individual specs. When a
surface area is missing from the current set, add or shape a focused spec for that
area. When a surface area is too broad for one coherent contract, create several
specs and connect them through `## Related Records`, a plan, research synthesis, or
knowledge.

Coverage does not mean every implementation detail belongs in specs. Specs should
define intended behavior, externally meaningful interfaces, scenarios, constraints,
and evidence expectations. Tickets, code, evidence, audit, research, plans, and
knowledge keep their own responsibilities.

## Requirements

Requirements are durable behavior claims.

Use `REQ-*` IDs, starting at `REQ-001`.

Good requirements:

- state one behavior, invariant, interface guarantee, error semantic, permission
  rule, compatibility promise, or quality constraint
- name the actor, system, API, workflow, or record surface when it matters
- name the condition or trigger when it matters
- name the observable outcome
- avoid implementation steps unless the interface, command, or file shape is the
  behavior being specified

Prefer precise language. Use `MUST` for hard requirements and `SHOULD` only when
exceptions are legitimate and named.

Do not reuse a requirement ID for different behavior. If meaning changes enough to
mislead existing references, supersede the old ID and create a new one.

## Scenarios

Scenarios are concrete probes for requirements.

Use `SCN-*` IDs, starting at `SCN-001`.

Each scenario should cite the requirements it exercises.

Use GIVEN, WHEN, THEN, and AND steps when that structure clarifies state, trigger,
and outcome.

Include the smallest happy path plus material edge, failure, permission,
compatibility, empty-state, and idempotency cases when they affect behavior.

Remove or sharpen scenarios that cannot plausibly be tested, observed, or reviewed.

## Evidence Plan

The evidence plan says how downstream work could prove the requirements and
scenarios.

Evidence can be tests, command output, screenshots, logs, manual observations,
diff review, trace output, generated artifacts, or another durable observation.

Specs define expected evidence. Evidence records store observed artifacts.

Good evidence expectations are claim-scoped. They say which requirement or scenario
the evidence should support and what observation would be sufficient.

## Quality Bar

Use a quality bar when the intended behavior includes quality beyond existence.

For UI, UX, product, operator workflow, API ergonomics, developer experience,
agent workflow, or record quality, name observable probes such as:

- task clarity
- before/after comparison
- discoverability
- error clarity
- density
- affordance quality
- compatibility
- examples and non-examples
- reduced ambiguity for downstream agents

Quality bars should be observable enough for tickets and audit to evaluate.

## Interface Contract

Use an interface contract for public APIs, module interfaces, component props,
commands, data shapes, file formats, packets, records, or cross-worker contracts.

Name inputs, outputs, side effects, ordering, idempotency, error semantics,
validation boundary, compatibility, and deprecation expectations when they matter.

When the interface is versioned or compatibility-sensitive, state which versions,
callers, files, or consumers are in scope.

## Examples And Non-Examples

Examples make fuzzy quality concrete.

Use examples, non-examples, screenshots, comparable flows, short prose examples,
or anti-patterns when they prevent generic or ambiguous implementation.

Good examples show the boundary of the behavior. Good non-examples prevent nearby
wrong implementations.

## Boundaries And Non-Goals

A spec should make scope boundaries visible.

Useful boundaries include:

- behaviors intentionally excluded
- interfaces or callers not covered
- environments, versions, or data shapes not covered
- quality claims not being made
- compatibility promises not being extended
- implementation choices intentionally left to tickets

Use non-goals to prevent likely scope creep or downstream misinterpretation.

## Current Surface And Status

An `active` or `accepted` spec must describe the current product surface slice it
claims to own. A stale active spec is worse than no spec because downstream tickets,
packets, evidence, and audit will treat it as behavior truth.

Before relying on a spec, and whenever product behavior changes, check source
reality and related records enough to decide whether the spec still matches the
current surface.

If it does not match:

- update it in place only when the same product slice and same cited IDs still own
  the behavior without misleading existing references
- split it when independent product surfaces were collapsed into one record
- mark it `superseded` and name the successor when a new spec owns the behavior
- mark it `retired` when the product surface or behavior no longer exists and has
  no successor

Do not leave a stale spec as `active` or `accepted` for historical context. History
belongs in amendment notes, related records, research, or the superseded/retired
record itself.

## Shaping Behavior

Before writing or accepting a spec, shape the behavior until these things are true:

- behavior question: the spec names the behavior, interface, invariant, workflow,
  or record shape being defined
- bounded scope: the spec can say what is covered, what is excluded, and where the
  contract stops
- design model: important domain model, data shape, state shape, interface
  boundary, or abstraction choices are explicit enough not to be invented
  downstream
- coherent slice: materially different product surfaces have been split or
  explicitly kept out of scope
- observable scenarios: the behavior can be probed through concrete scenarios,
  examples, commands, UI states, API calls, records, or review checks
- downstream use: tickets, packets, evidence, audit, or future agents can cite the
  requirements and scenarios without redefining them
- spec-set coverage: the work either improves regeneration-grade coverage of the
  current product surface or explicitly marks the remaining behavior gap

Inspect existing specs, tickets, plans, research, constitution, evidence,
knowledge, and source files that already constrain the behavior.

When operator input is needed:

- ask one material question at a time
- recommend an answer when the repository, records, risk, or product shape supports
  one path
- challenge vague or overloaded terms before they become requirements
- test proposed wording against concrete scenarios
- surface assumptions whose answer would change behavior, UX, system shape,
  evidence expectations, risk, or scope

Good shaping questions include:

- What smallest valuable behavior should exist?
- What is explicitly not being done?
- What domain model, data shape, state shape, or interface boundary should guide the work?
- What would make this design incoherent even if the scenarios pass?
- What current behavior, workaround, failure, or baseline matters?
- Which actor, workflow, API, command, record, or interface is affected?
- Which success, edge, failure, permission, empty-state, compatibility, or
  idempotency scenario would reveal the boundary?
- What evidence would show the behavior works?

Record settled answers in the spec. Route unsettled questions to the surface that
can answer them.

Stop shaping when remaining questions no longer change intended behavior or can be
recorded as open questions with clear downstream limits.

## Amending A Spec

Classify meaningful changes before editing:

- added: new behavior or scenario that does not change an existing claim
- modified: changed behavior for an existing requirement or scenario
- removed: behavior is no longer intended
- renamed: terminology changed while behavior remains stable
- superseded: old IDs no longer describe the active contract and have named
  successors

Search for inbound references before changing cited IDs.

If a requirement or scenario splits, narrows, or changes enough that reuse would
mislead, mark the old ID as superseded in prose and add successor IDs.

When amending, update related requirements, scenarios, evidence expectations, open
questions, and status together so the spec remains coherent.

If an amendment reveals that the spec covers significantly different product
surfaces, stop treating the record as one contract. Split or supersede it before
adding more requirements.

## Routing

Route truth to the owning surface:

- execution sequencing or complex multi-ticket strategy to plans
- live scoped work, blockers, acceptance, and closure to tickets
- investigation, tradeoffs, source synthesis, rejected paths, or null results to
  research
- durable judgment, policy, principles, or architectural precedent to constitution
- observations, logs, screenshots, reproductions, or validation outputs to evidence
- Ralph-backed adversarial review to audit
- accepted reusable explanation to knowledge

## Contract Review

Before downstream work relies on a spec, check:

- completeness: material behavior, edge states, non-goals, constraints, scenarios,
  and evidence expectations are covered or explicitly out of scope
- correctness: requirements describe intended behavior, not only current
  implementation or a preferred solution shape
- currency: `active` and `accepted` specs still represent the current product
  surface slice they claim to own
- slice: the spec does not collapse materially different product surfaces into one
  umbrella contract
- coverage: the current spec set does not force downstream work to infer intended
  behavior from chat history or implementation archaeology
- coherence: requirements, scenarios, examples, constraints, and open questions do
  not contradict one another
- citability: `REQ-*` and `SCN-*` IDs can be cited without requiring chat history

This is a spec-quality pass. Audit is the Ralph-backed challenge when a claim needs
adversarial review.
