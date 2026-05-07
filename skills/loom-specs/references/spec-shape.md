# Spec Shape

## Core sections

- Summary
- Rigor Level
- Problem
- Problem Pressure Check
- Desired Behavior
- Quality Bar
- Options Considered
- Not Doing
- Boundary Tiers when operator or delivery authority matters
- Interface / API Contract when the behavior exposes a public or shared surface
- Examples / Non-Examples
- Constraints
- Requirements
- Scenarios
- Acceptance
- Evidence Plan
- Amendment Notes when changing an existing spec
- Contract Review
- Assumptions / Decision Points
- Open Questions

## Progressive Rigor

The template is broad so it can support high-risk contracts, but a saved spec
should be only as detailed as the risk and coordination need justify.

A **lite spec** is appropriate for local, low-risk behavior when a future ticket
can act safely from concise requirements, concrete scenarios, acceptance IDs, and
an evidence plan. It may write `None - reason` for options, boundary tiers,
interface contract, examples, or amendment notes when those sections add no real
clarity.

A **full spec** is appropriate when the behavior crosses public APIs, command
surfaces, shared module contracts, migrations, security/privacy boundaries,
compatibility promises, multiple repositories, product/UX quality bars, or several
downstream tickets. Full specs should spell out interfaces, errors,
deprecations, edge cases, non-goals, evidence expectations, and decision points.

Do not confuse rigor with length. A spec is strong when it prevents downstream
guessing and makes evidence/review possible, not when it fills every section with
ambient prose.

## Quality Bar

The quality bar prevents "it exists" from becoming "it is good." It names what
would make the result materially better than the current or baseline state.

For UI, UX, product, workflow, or operator-facing behavior, include observable
quality probes such as primary user task clarity, discoverability, affordance
quality, density, before/after comparison, or examples and non-examples.

## Requirement And Scenario Grammar

Requirements are the durable behavior claims. Scenarios are concrete probes that
make those claims testable, reviewable, and hard to hand-wave.

Requirement guidance:

- use stable local IDs such as `REQ-001` when the requirement may be cited later
- state one behavior, invariant, interface guarantee, error semantic, or quality
  constraint per requirement
- prefer normative verbs for hard contracts: `MUST` or `SHALL` for required
  behavior, `SHOULD` only when a named exception may be acceptable
- name the actor or surface, trigger or condition, observable outcome, and any
  important limit
- keep implementation mechanics out unless the interface or command shape is the
  behavior contract itself

Scenario guidance:

- give scenarios stable local IDs such as `SCN-001` when evidence or critique may
  need to cite them directly
- link each scenario to the requirement and acceptance IDs it exercises
- use GIVEN, WHEN, THEN, and AND steps when that structure clarifies state,
  trigger, and outcome
- include the smallest happy path plus material edge, failure, permission,
  compatibility, empty-state, and idempotency cases
- remove or sharpen scenarios that cannot plausibly be tested, observed, or
  explicitly validated

Acceptance guidance:

- use stable `ACC-*` IDs for acceptance units downstream tickets may cite
- write acceptance as the pass/fail contract, not as an implementation task
- map acceptance to requirements and scenarios when the relationship is not
  obvious

## Spec Ownership And Boundaries

Before creating or reshaping a spec, decide which behavior surface owns the
contract. The right boundary is usually a durable capability, workflow, API,
domain concept, user task, or operator surface that can evolve independently.

Avoid omnibus specs that gather unrelated behaviors only because one ticket will
touch them. Also avoid one-spec-per-implementation-step fragmentation. Split when
terms, acceptance, consumers, evidence, or compatibility can change independently;
merge when separating them would make future tickets chase artificial boundaries.

## Options Considered And Not Doing

Use `# Options Considered` when several behaviors, APIs, UX flows, architecture
shapes, or workflow designs would satisfy the same rough request. Keep it compact:
two or three materially different directions, their tradeoffs, and why the chosen
direction best fits the problem pressure check.

Use `# Not Doing` when scope focus matters. A good non-goal says which attractive
idea was deliberately excluded and why excluding it keeps the contract sharper.
Do not bury product tradeoffs in prose enthusiasm.

If options remain evidence-light, route to research or spike. If one option would
change durable policy, route to constitution. If an assumption is unresolved and
material, keep it as a decision point instead of silently choosing.

## Examples And Non-Examples

Use examples to make fuzzy quality concrete. Sources can include screenshots,
comparable workflow pages, accepted patterns, anti-patterns, or short prose
examples. Non-examples are especially useful for preventing safe-but-generic agent
output.

## Problem Pressure Check

Use this section when product, UX, workflow, API, or behavior direction could be
invented by the agent. It keeps a spec from laundering an untested solution shape
into a behavior contract.

Check only the gaps that matter for the scope:

- evidence: what observed pain, workaround, request, failure, or baseline proves
  this problem exists?
- specificity: which user, operator, system, API consumer, or maintenance surface
  is affected?
- counterfactual: what happens today if nothing changes?
- attachment: what is the smallest valuable shape, and what larger solution shape
  is intentionally out of scope?
- durability: what predictable change would make this contract wrong or stale?

If an answer would materially change behavior, UX, architecture, acceptance, risk,
or scope, record it as a decision point. Do not hide it in prose confidence.

## Spec Grilling Procedure

Use this when creating or reshaping a spec from a fuzzy request, overloaded domain
language, a proposed solution, a disputed behavior, or a plan that would otherwise
make tickets guess.

The grilling pass is the behavior-contract equivalent of walking the design tree:
resolve one material branch at a time until the intended behavior is stable enough
for planning, ticketing, evidence, and critique.

Procedure:

- read relevant specs, wiki pages, research, decisions, and prior tickets when
  those owner records already carry behavior, domain language, constraints, or
  tradeoffs that shape the contract
- ask one material question at a time when operator input is needed; wait for the
  answer before moving to dependent branches
- provide a recommended answer for each material question, including the behavior,
  user, API, risk, or owner-record signal that makes that answer plausible
- challenge terminology conflicts immediately: if accepted language says one thing
  and the request appears to mean another, ask which term or concept should win
- sharpen fuzzy terms into canonical concepts, roles, states, and boundaries; do
  not let overloaded language become acceptance criteria
- invent concrete scenarios, including edge and failure scenarios, that force
  boundaries between concepts and reveal whether the proposed contract is too broad
  or too narrow
- capture resolved truth in the owner that can maintain it: spec for intended
  behavior, wiki for accepted shared language, research for rejected options or
  null results, plan for execution decomposition, ticket for live local assumptions,
  and constitution decision records only for choices that are hard to reverse,
  surprising without context, and tradeoff-backed

Do not import a project-specific glossary file layout as Loom ontology. The Loom
equivalent is owner-layer routing: wiki for accepted language, specs for behavior,
constitution decisions for durable precedent, and tickets for live execution truth.

If a grilling question blocks the contract, leave it as a blocking decision point.
If it merely shapes execution order after behavior is settled, route it to the plan.

## Decision Points

Surface assumptions whose answer would materially change behavior, UX,
architecture, acceptance, risk, or scope. Low-risk reversible assumptions may be
recorded as accepted. Material or irreversible assumptions should block execution
until the user or the owning record resolves them.

## Amendment Discipline

When updating an existing behavior contract, classify the mutation before editing:

- **Added behavior**: introduce a new `REQ-*`, `SCN-*`, or `ACC-*` when the
  contract grows without changing an existing claim
- **Modified behavior**: update the full affected requirement, its scenarios,
  acceptance units, evidence plan, and decision points together
- **Removed behavior**: state what is no longer intended, why, and whether a
  successor, migration path, compatibility promise, or deprecation boundary exists
- **Renamed behavior**: preserve semantics while reconciling terminology,
  headings, IDs, and inbound references
- **Superseded behavior**: mark the old ID as superseded and point to the new ID
  when a claim splits, narrows, or changes enough that reuse would mislead

Do not silently rewrite cited IDs. Search for inbound references before renaming,
removing, or superseding stable IDs. Downstream tickets, packets, evidence,
critique, wiki, and plans may depend on those references for recovery.

If the amendment would change the problem, beneficiary, strategic objective, or
execution route more than the behavior contract itself, route that truth to the
initiative, plan, ticket, research, or constitution layer instead of expanding the
spec beyond its owner boundary.

## Boundary Tiers

Use boundary tiers when the spec constrains what agents, builders, or users may do
around the behavior:

- **Always**: required invariants, validation, checks, compatibility, or safety
  behavior.
- **Ask first**: changes that need operator, product, security, data, or
  architecture approval before downstream work.
- **Never**: forbidden actions such as weakening security, deleting user data,
  disabling checks, or widening scope outside the accepted contract.

These tiers are behavior and authority boundaries for this spec. They do not
replace ticket state, critique disposition, or external approval workflows.

## Interface / API Contracts

For public APIs, module interfaces, component props, command surfaces, data
schemas, or cross-worker contracts, specify the observable contract before
downstream work depends on it:

- inputs, outputs, generated fields, side effects, ordering, and idempotency
- error semantics and status/result shapes
- validation boundary and trust assumptions for external data
- compatibility expectations, deprecation path, and additive vs breaking changes
- examples and non-examples that make misuse visible

## Contract Review

Before downstream tickets rely on a spec, review the contract through three
lenses:

- **Completeness**: material desired behavior, edge states, non-goals,
  constraints, acceptance IDs, and evidence expectations are covered or explicitly
  out of scope
- **Correctness**: requirements reflect intended behavior and owner-record truth,
  not merely the current implementation or an attractive solution shape
- **Coherence**: requirements, scenarios, acceptance, interface details, and
  decision points do not contradict one another and use stable terminology

This review is a spec-quality pass. It does not replace ticket acceptance,
evidence sufficiency, or critique verdicts.

## Anti-patterns

Avoid:

- delivery journals
- strategic roadmap language
- research dumps with no contract
- hand-wavy acceptance language
- behavior-bearing requirements with no scenarios
- scenarios that cannot be tested, observed, or explicitly validated
- requirements that mix several behaviors under one ID because splitting feels
  inconvenient
- public or shared interfaces with missing error, validation, compatibility, or
  deprecation semantics
- stable IDs reused for different behavior after downstream records may have cited
  the old meaning
- solution attachment accepted as intended behavior before the problem is checked
- spec creation that records a pressure-check table but skips the active grilling
  loop needed to resolve fuzzy terms, contract conflicts, or concrete scenarios
- quality claims without examples, non-examples, or evidence plan
- silently accepted product or UX assumptions that would change the result
- one-path specs for fuzzy product or workflow requests where divergent options
  were never considered
- specs with no explicit `Not Doing` boundary when delivery could easily grow
  beyond the smallest valuable shape

## Good linking

Specs commonly link to:

- initiative
- research
- plan
- ticket
- critique
- wiki
