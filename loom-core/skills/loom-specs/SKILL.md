---
name: loom-specs
description: "Use when behavior, interfaces, invariants, requirements, scenarios, or intended outcomes need a stable source before tickets, packets, evidence, or audit rely on them."
---

# loom-specs

Specs own intended behavior.

A spec says what a system, workflow, interface, product surface, command, data
shape, permission boundary, error state, or record shape should do.

It turns fuzzy intent into requirements, scenarios, boundaries, and quality bars
that downstream tickets, packets, evidence, and audit can cite. Specs are one of
the main places to preserve outer-loop design judgment when behavior, state shape,
data shape, interface boundaries, or design coherence would otherwise be inferred
during implementation.

The current spec set, meaning specs with `Status: active` or `Status: accepted`,
should define the current product surface well enough that a future agent could
reconstruct the intended behavior from scratch without relying on chat history or
the current implementation as the behavior source of truth.

Specs do not own live execution state, implementation progress, evidence
sufficiency, audit verdicts, or ticket closure. Tickets own scoped acceptance for
a work unit and may cite spec requirements and scenarios.

## Use This Skill When

Use this skill when:

- intended behavior is fuzzy, disputed, reusable, shared, or easy to misstate
- interface, API, workflow, UX, permission, error, compatibility, or invariant
  behavior needs a durable contract
- product direction, state shape, data shape, abstraction boundary, or design
  coherence needs a stable behavior-level source before execution
- a ticket, plan, audit, packet, or worker would otherwise redefine what correct
  means
- operator answers need to become behavior truth before execution
- requirements or scenarios need to be added, modified, removed, renamed,
  superseded, accepted, or retired
- evidence or audit needs a stable behavior claim to evaluate

Do not use specs for execution sequencing, investigation notes, observed evidence,
audit findings, implementation journals, or reusable explanation that does not own
intended behavior.

## Dispatch

If creating or reshaping a spec:

- read `references/spec-shape.md`
- inspect existing specs and related records before asking the operator to repeat
  facts
- inspect source reality when current behavior, interfaces, errors, or constraints
  matter
- choose one coherent product slice before writing requirements; split the work
  when materially different product surfaces would otherwise share one spec
- shape fuzzy behavior until requirements, scenarios, boundaries, and open
  questions are clear enough for downstream work
- use examples, non-examples, data shapes, and interface boundaries to prevent
  downstream agents from inventing design direction
- use `templates/spec.md`
- write the smallest citable spec

If updating a spec:

- read the whole spec
- search for inbound references to affected `REQ-*` and `SCN-*` IDs when behavior
  changes
- check whether the spec still represents the current product surface slice it
  claims; if not, narrow it, split it, supersede it, or retire it before relying on
  it
- classify the amendment as added, modified, removed, renamed, or superseded
- update requirements, scenarios, evidence expectations, and open questions
  together
- supersede old IDs when reuse would mislead downstream records

If superseding or retiring a spec:

- preserve the reason
- name the successor when one exists
- update `Status:`, `Updated:`, `Replaces:`, or `Superseded By:` as appropriate
- repair or flag inbound refs when downstream records would otherwise cite stale
  behavior

If only finding or summarizing specs:

- inspect `.loom/specs/`
- report status, relevant requirements, scenarios, boundaries, and open questions
- do not mutate records unless the operator asked for a change

## Finding Specs

Specs live under `.loom/specs/`.

Useful starting points:

```bash
find .loom/specs -maxdepth 1 -name '*.md' -print 2>/dev/null | sort
grep -R '^ID: spec:' .loom/specs 2>/dev/null || true
grep -R '^Type: Spec' .loom/specs 2>/dev/null || true
grep -R '^Status:' .loom/specs 2>/dev/null || true
grep -R 'REQ-[0-9][0-9][0-9]' .loom/specs 2>/dev/null || true
grep -R 'SCN-[0-9][0-9][0-9]' .loom/specs 2>/dev/null || true
```

Search by capability, domain term, interface name, user task, error state,
requirement ID, scenario ID, related record ID, source path, command, API, or data
shape.

## Spec IDs And Filenames

Use stable semantic IDs:

```text
spec:<slug>
```

Use matching filenames without the `spec:` prefix:

```text
.loom/specs/<slug>.md
```

Choose a slug future agents will search for.

Do not use date prefixes for ordinary spec filenames.

## Required Top Labels

Specs use plain body labels near the top:

```text
ID: spec:<slug>
Type: Spec
Status: draft
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
```

Add only when useful:

```text
Replaces: spec:<slug>
Superseded By: spec:<slug>
```

## Status Lifecycle

Use this lifecycle:

- `draft`: the contract is being shaped and downstream work should not rely on it
  unless the open risk is explicit
- `active`: current working behavior truth for the named product slice, usable by
  downstream work with named open questions and limits
- `accepted`: reviewed enough that downstream tickets, packets, evidence, and
  audit can rely on it as the current behavior contract for the named product
  slice
- `superseded`: replaced by a named successor
- `retired`: intentionally no longer used

Use `active` for current contracts that are useful but still evolving.

Use `accepted` when the contract is stable enough for downstream records to rely on.

An `active` or `accepted` spec must represent the current product surface slice it
claims. If the product surface changed enough that the spec would mislead a
ticket, packet, evidence plan, audit, or future agent, update the spec immediately
or change its status to `superseded` or `retired`.

Use `superseded` when a successor spec now owns the behavior. Use `retired` when
the product surface, workflow, interface, or behavior no longer exists or should no
longer guide work.

## Current Spec Set

Treat `active` and `accepted` specs as the current behavior map for the product
surface. Their collective job is regeneration-grade coverage: a future agent should
be able to rebuild the intended behaviors, interfaces, workflows, record shapes,
permission boundaries, error states, and quality contracts they cover without
mining chat history or guessing from implementation details.

This is a collective goal, not permission to make broad specs. When regeneration
would require unrelated behavior areas, create or update multiple coherent specs.
Use related records, plans, research, or knowledge to connect them, but keep the
behavior contracts sliced.

When you discover a current product surface area that no `active` or `accepted`
spec covers, create or shape the missing spec before downstream work depends on an
implicit behavior claim. When a current spec points at behavior that no longer
exists or no longer works that way, update it, supersede it, or retire it.

## Slicing Specs

A spec should cover one coherent product slice: a behavior, workflow, interface,
record shape, permission boundary, error semantic, or quality contract whose
requirements change together and whose scenarios can be reviewed together.

Do not create an all-encompassing spec for a whole product, package, application,
agent, UI, protocol, or broad product surface. Use related specs, plans, research,
or knowledge records to connect separate surfaces instead of hiding them inside one
umbrella contract.

Split a spec, or create separate specs from the start, when any of these are true:

- the requirements involve different primary actors, workflows, interfaces,
  commands, record types, permission domains, or user jobs
- the areas can ship, regress, be deprecated, or be validated independently
- downstream tickets would cite disjoint subsets and should not need the rest of
  the spec to understand their acceptance
- the evidence plan needs unrelated test types, screenshots, logs, review methods,
  environments, or audit questions
- one part may become stale, superseded, retired, or accepted while another remains
  current or draft
- the title, summary, or requirements need broad words such as `entire`, `all`,
  `platform`, `system`, `product`, or repeated `and` clauses to stay honest

If a broad spec already exists, do not keep expanding it. Extract coherent product
slices into successor specs, move cross-surface coordination to a plan or related
records list, and mark the old umbrella spec `superseded` or narrow it so its
status remains truthful.

## Requirements And Scenarios

Every spec should include at least one requirement and one scenario unless the
record is still an early `draft`.

Requirements use stable local IDs:

```text
REQ-001
```

A requirement states one intended behavior, invariant, interface guarantee, error
semantic, permission rule, compatibility promise, or quality constraint.

Scenarios use stable local IDs:

```text
SCN-001
```

A scenario is an observable probe of behavior. It should describe state, trigger,
and outcome clearly enough for tickets, evidence, and audit to use.

Ticket acceptance owns closure criteria for scoped work and can cite
`spec:<slug>#REQ-001` or `spec:<slug>#SCN-001` when useful.

## Shaping Posture

When operator input is needed:

- ask one material question at a time
- recommend an answer when the repository, records, risk, or product shape supports
  one path
- challenge vague or overloaded terms before they become requirements
- test proposed wording against concrete scenarios
- invent success, edge, failure, permission, empty-state, compatibility, and
  idempotency scenarios when they reveal boundaries
- route unresolved investigation to research, complex execution strategy to plans,
  live work to tickets, durable judgment to constitution, and reusable explanation
  to knowledge

Stop shaping when remaining questions no longer change intended behavior or can be
recorded as open questions with clear downstream limits.

## Spec Invariants

Every spec should preserve these invariants:

- the spec owns one coherent product slice, not the entire product surface
- `active` and `accepted` specs describe the current product surface slice; stale
  specs are updated, superseded, or retired
- the current spec set can regenerate intended product behavior without relying on
  chat history or implementation archaeology
- intended behavior is separated from implementation plan
- requirements and scenarios are stable, citable, and observable
- important boundaries, non-goals, constraints, and open questions are explicit
- evidence expectations are concrete enough to guide tickets and audit
- public or shared interfaces name inputs, outputs, errors, validation, and
  compatibility expectations when those details matter
- quality claims have examples, non-examples, probes, or evidence expectations when
  they affect downstream work
- cited `REQ-*` and `SCN-*` IDs are not silently reused for different behavior
- specs do not claim ticket closure, evidence sufficiency, audit verdict, or
  implementation progress

## Done Means

Spec work is done when:

- the spec has a truthful status
- the spec slice is narrow enough that materially different product surfaces are
  not collapsed into one contract
- gaps in the current spec set are visible when the work reveals product behavior
  needed for regeneration-grade coverage
- behavior-bearing requirements and scenarios are clear enough to cite
- open questions and downstream limits are visible
- related records that constrain the behavior are linked or named
- tickets can cite the spec without redefining intended behavior
