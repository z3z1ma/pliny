---
name: loom-specs
description: "Define intended behavior and acceptance contracts. Use when building features, changing UX/API/domain behavior, requirements are fuzzy, a request needs grilling into a contract, acceptance is unclear, or future tickets need reusable behavior truth."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: owner-layer
  owns_layer: spec
---

# loom-specs

Specs own intended behavior.

They turn ambiguity into a durable contract.

## What This Skill Owns

- behavior contracts
- requirements
- scenarios
- acceptance criteria
- explicit constraints that shape downstream delivery
- spec grilling that turns fuzzy language, domain boundaries, and operator answers
  into intended behavior

## Acceptance Boundary

Specs own acceptance IDs, intended behavior, scenarios, and requirements.

Tickets decide which acceptance IDs are in scope for live work and whether the
evidence/critique dossier is sufficient for closure. Packets, evidence,
critique, and wiki pages may cite spec acceptance IDs; they must not redefine
them.

## Requirement And Scenario Discipline

Specs should make intended behavior easy to cite, test, review, and amend.

- give behavior-bearing requirements stable `REQ-*` IDs when downstream tickets,
  packets, evidence, or critique will need to cite them
- use normative language for real requirements: `MUST` or `SHALL` for required
  behavior, `SHOULD` only when exceptions are legitimate and named, and avoid
  vague verbs such as "works", "supports", or "handles" without observable detail
- keep each requirement focused on one behavior, invariant, interface guarantee,
  error semantic, or quality constraint
- pair each behavior-bearing requirement with at least one concrete scenario that
  could drive a test, smoke check, screenshot, trace, or manual observation
- write scenarios around observable state, trigger, and outcome; use GIVEN, WHEN,
  THEN, and AND steps when they make the scenario clearer
- include success, edge, failure, permission, compatibility, idempotency, and empty
  states when those states would change implementation or acceptance
- treat scenarios as evidence seeds: if no plausible evidence could prove the
  scenario, sharpen the scenario or remove the claim

Do not turn requirements into implementation plans. File names, helpers,
libraries, migrations, and step order belong in plans, tickets, or packets unless
the public/shared interface itself is the behavior being specified.

## Progressive Rigor

Use the lightest spec that still makes downstream work testable and reviewable.

For routine, local, low-risk behavior, a lite spec may be enough: problem,
desired behavior, focused requirements, representative scenarios, acceptance IDs,
and an evidence plan.

Increase rigor when ambiguity or cost is higher: public APIs, command surfaces,
cross-repository behavior, migrations, security/privacy boundaries,
compatibility/deprecation paths, user-facing UX/product quality, parallel-worker
contracts, or behavior likely to be reused by several tickets.

Lite never means vague. Full never means verbose theater. The spec should contain
the contract a future ticket, packet, evidence record, or critique pass actually
needs.

## Spec Amendment Discipline

When changing an existing spec, identify what kind of behavior mutation is being
made before editing:

- **Added**: new behavior, scenario, constraint, or acceptance that does not change
  an existing requirement
- **Modified**: changed behavior for an existing requirement; update the complete
  requirement, its affected scenarios, acceptance IDs, evidence plan, and decision
  points together
- **Removed**: behavior that is no longer intended; state the reason, successor,
  compatibility, migration, or removal boundary when any downstream work may care
- **Renamed**: terminology or heading changed while behavior is otherwise stable;
  preserve or reconcile IDs and search for inbound references
- **Superseded**: old IDs no longer own the active contract; point to successor IDs
  when behavior splits, narrows, or changes enough that reuse would mislead

Preserve stable IDs after downstream records cite them. If a requirement,
scenario, or acceptance unit splits, mark the old ID as superseded in prose and
introduce successor IDs instead of silently reusing the old one for a different
contract.

If the intent, beneficiary, or scope changes enough that the old spec would tell a
confusing story, route the change outward: create or reshape the right spec,
initiative, plan, or ticket instead of laundering a new objective into an old
behavior contract.

## Use This Skill When

- several solutions are plausible and the intended behavior matters
- acceptance criteria are vague
- a request, plan, domain term, or workflow idea needs grilling before tickets or
  packets depend on it
- a ticket or critique would otherwise keep redefining what "correct" means
- a workflow or capability needs one stable behavioral source

## Do Not Use This Skill When

- you are still only gathering evidence
- you only need execution sequencing
- you only need to decompose already-clear high-level work into ticket-ready units
- you are writing a user-facing explanation page

## Spec Creation Discipline

Creating a spec is an active grilling pass, not a form fill.

When the request is fuzzy enough that an answer could change behavior, UX, API,
workflow, acceptance, or risk:

- interview the operator relentlessly about every material branch of the behavior
  contract until the intended behavior, terms, boundaries, scenarios, and
  acceptance criteria are shared and precise
- ask one material question at a time, waiting for the answer before moving to the
  next dependent branch
- provide a recommended answer for each question, including the behavior, user,
  product, risk, or owner-record reason that makes the recommendation coherent
- challenge vague, overloaded, or conflicting terms immediately and propose a
  precise canonical term or concept
- invent concrete scenarios and edge cases that force boundaries between concepts,
  roles, states, errors, permissions, invariants, and non-goals
- keep walking the design tree until dependent decisions are resolved, routed, or
  explicitly blocking
- capture durable decisions in the right owner: spec for behavior, ticket for local
  assumptions, research for tradeoffs/null results, wiki for accepted explanation,
  and constitution decisions only when the choice is hard to reverse, surprising,
  and tradeoff-backed

## Good Spec Questions

A strong spec answers:

- what problem is being solved
- who or what exact user, operator, API, system, or maintenance surface benefits
- what current workaround, pain, baseline behavior, or evidence shows the problem
- what desired behavior is expected
- what the smallest valuable shape is, especially when the request arrived as a
  preferred solution
- which existing spec, requirement IDs, scenario IDs, or acceptance IDs this
  creates, changes, removes, or supersedes
- which domain, product, owner-record, or accepted-language facts shaped the contract
- which material decisions were resolved, routed, or left blocking
- what terminology conflicts or concrete scenarios shaped the contract
- what quality bar would make the result materially better
- what examples and non-examples make fuzzy requirements concrete
- what constraints matter
- what scenarios matter
- how acceptance should be judged
- what evidence would prove the behavior and quality bar
- what assumptions or decision points would materially change the contract

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "The requirement is obvious." | Obvious requirements still hide assumptions. Specs exist to surface them before delivery. |
| "The quality bar is subjective, so skip it." | Subjective does not mean unverifiable. Name observable probes, examples, non-examples, or before/after evidence. |
| "The ticket can define this later." | Tickets scope live work. Reusable intended behavior belongs in a spec before downstream work relies on it. |
| "A lite spec can skip scenarios." | Lite means small, not vague. Each behavior-bearing requirement still needs a concrete way to observe or test it. |
| "Implementation details make the spec clearer." | Delivery mechanics usually belong in plans, tickets, packets, or code. Specs own observable behavior and shared contracts. |

## Red Flags

- acceptance says "works" or "looks good" without observable criteria
- requirements lack stable IDs even though downstream work needs to cite them
- requirements lack scenarios, or scenarios are too abstract to test or observe
- the spec inherits a requested solution shape without checking the underlying
  problem, beneficiary, workaround, or smallest valuable form
- UX/product claims lack examples, non-examples, or evidence plan
- modifications to an existing spec quietly change behavior without naming what
  was added, modified, removed, renamed, or superseded
- open questions would materially change downstream work but are not marked blocking
- a ticket or critique keeps redefining correctness because the spec is too vague

## Verification

- [ ] Requirements and acceptance IDs are stable and citable.
- [ ] Behavior-bearing requirements use concrete normative language and avoid
      implementation-plan trivia.
- [ ] Each behavior-bearing requirement has at least one scenario that can be
      tested, observed, or explicitly validated.
- [ ] Any material spec grilling questions were answered, routed, or explicitly
      marked blocking before downstream work depends on the contract.
- [ ] New or changed behavior is classified as added, modified, removed, renamed,
      or superseded when an existing spec is amended.
- [ ] The quality bar names a baseline/current-state delta.
- [ ] Examples or non-examples make ambiguous behavior concrete, or absence is justified.
- [ ] Decision points say whether they block downstream work.
- [ ] Evidence plan can prove the behavior and quality bar.

## Done Means

- the behavior is explicit enough that tickets and critique can reference one contract
- the spec is precise without becoming delivery trivia

## Read In This Order

Read immediately for normal spec creation or review:

1. `references/spec-shape.md` when deciding what belongs in requirements,
   scenarios, constraints, and acceptance.
2. `templates/spec.md` only when creating or substantially reshaping a spec
   record.
