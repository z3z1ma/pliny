# Critique Lens

A good critique asks questions like:

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

## Profile Selection

- low risk: usually `operator-clarity` or no required profile
- medium risk: choose the one or two profiles matching the change class
- high risk: require the profile matching the domain plus `operator-clarity`

If the risk class is unclear, treat it as medium and explain the uncertainty.
