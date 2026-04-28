# Critique Lens

A good critique asks questions like:

- what could break in the changed code
- what claim here is weaker than it sounds
- what assumption is hidden
- what evidence is missing
- what scenario would break this
- where did the implementation or page overfit the happy path
- what did the author forget to update
- what future reader could misunderstand

## Common lenses

- correctness
- scope discipline
- evidence sufficiency
- operator clarity
- failure modes
- maintenance burden
- trust-boundary integrity

## Target Types

Critique can target:

- code diffs, branches, commits, or pull requests
- behavior changes after a Ralph iteration
- tickets, specs, plans, research, packets, evidence, and wiki pages
- release or handoff packages
- external summaries that mirror Loom work

The target type changes the evidence reviewed. It does not change the owner
model: critique owns findings and verdicts, while tickets own live execution
state.

## Packet Expectation

Use a critique packet for implementation/code review when a fresh reviewer
needs the ticket, parent plan or initiative, spec, research, evidence, prior
packet output, and git diff in one bounded review contract.

Do not compile a packet just to critique a Loom artifact by default. A ticket,
plan, spec, or wiki page can be reviewed directly as an artifact. Use a packet
only when the review is broad, high risk, or needs fresh-context isolation.

## Named Profiles

Use named profiles when a ticket or parent packet declares the review risk.
Profiles are lenses, not permanent agents or new layers.

### `protocol-change`

- authority drift
- layer ownership conflicts
- packet/ticket truth mismatch
- repair and retrospective implications

### `api-contract`

- backwards compatibility
- error semantics
- versioning
- client impact

### `code-change`

- correctness against the ticket and spec
- unintended side effects
- error handling
- edge cases
- integration boundaries
- maintainability of the changed code

### `test-coverage`

- missing regression coverage
- weak assertions
- untested edge cases
- mismatch between acceptance criteria and tests
- evidence gaps when automated tests are not practical

### `data-migration`

- schema drift
- rollback
- idempotency
- data loss
- migration evidence

### `security`

- secrets
- authentication and authorization
- injection
- dependency risk
- unsafe tool permissions

### `performance`

- asymptotic behavior
- hot path changes
- cache invalidation
- measurement evidence

### `operator-clarity`

- whether the next agent will know what to do
- explicit stop conditions
- honest ticket, evidence, and wiki disposition
- whether explanatory pages overstate certainty

### `workflow-boundary`

- whether the workflow routes through existing owner layers instead of creating a
  hidden ledger
- whether plans, packets, critique, ship summaries, or external systems are
  accidentally owning ticket truth
- whether stop conditions and loopbacks prevent forced execution through
  ambiguity
- whether parallel or delegated work has non-overlapping write scopes and parent
  reconciliation

### `operator-surface`

- whether the project's user-facing instructions, Loom skills, templates,
  examples, adapters, or support docs tell the same story
- whether a change adds a required support surface outside the declared Loom
  owner graph without an explicit owner-layer reason
- whether harness-specific convenience is being mistaken for canonical project
  truth or protocol behavior
- whether skill descriptions and read order make activation discoverable without
  duplicating workflow truth

## Profile Selection

- low risk: usually `operator-clarity` or no required profile
- medium risk: choose the one or two profiles matching the change class
- high risk: require the profile matching the domain plus `operator-clarity`

If the risk class is unclear, treat it as medium and explain the uncertainty.

Use `skills/loom-records/references/change-class.md` when the review target
declares a `change_class` or when profile selection would otherwise be
ambiguous.
