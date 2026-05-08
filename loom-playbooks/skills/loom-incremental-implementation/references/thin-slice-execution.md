# Thin Slice Execution

Use this reference when a ticket can be implemented in several safe increments.

## Increment Loop

```text
choose slice -> implement -> test/observe -> verify -> evidence -> reassess -> next slice
```

Do not start the next slice until the current one has a known state.

## Slicing Strategies

### Vertical slices

Build one complete path through the stack, even if narrow. A vertical slice proves
integration and user value earlier than completing one technical layer at a time.

### Contract-first slices

Define the API, type, schema, event, or module seam first, then implement sides
against that contract. Use when independent workers or teams will build caller and
callee in parallel.

### Risk-first slices

Tackle the riskiest unknown first: external integration, performance budget,
browser capability, migration shape, or compatibility concern. Do not save the
uncertain piece for the end.

### Behavior-preserving cleanup slices

When cleanup is needed before feature work, give it its own slice with explicit
behavior-preservation evidence. Do not bury cleanup inside feature implementation.

## Simplicity First

Before writing code, ask:

- what is the simplest thing that can satisfy the current acceptance claim?
- is this abstraction earned by current use cases?
- does this helper reduce concepts or add one?
- am I solving the current ticket or a hypothetical future requirement?

Prefer boring code until evidence shows complexity is needed.

## Scope Discipline

Do not touch code just because it is nearby:

- unrelated imports, formatting, or style churn
- comments you do not fully understand
- old code whose consumers were not inspected
- adjacent bugs not in scope
- modernization outside the ticket boundary

Record noticed issues in the ticket journal, ticket-owned accepted-risk rationale,
or follow-up ticket when they matter.

## Safe Defaults

New behavior should default to conservative, compatible, or disabled states unless
the spec says otherwise. Examples:

- optional behavior disabled unless explicitly enabled
- bounded pagination rather than fetch-all
- no notification or side effect unless requested
- validation rejects unsafe input rather than trying to repair silently

Security-sensitive defaults should route through `loom-security`.

## Feature Flags

Use feature flags to separate deployment from release, not to avoid finishing work.

Every flag needs:

- owner
- creation reason
- enabled and disabled behavior expectations
- cleanup trigger or expiry
- evidence for states in scope
- ticket or plan disposition for removal

Nested, permanent, or unowned flags are migration debt.

## Rollback-Friendly Increments

An increment is rollback-friendly when:

- it is additive where possible
- it avoids broad rewrites
- data migrations are reversible or idempotent where risk requires it
- deletion happens after replacement and usage evidence
- generated artifacts and lockfiles are intentional

Use `loom-migration` for old/new coexistence, consumer movement, or removal.

## Per-Slice Verification

After each slice, choose the smallest honest check:

- targeted test for behavior
- typecheck or build for structural integration
- browser observation for UI state
- scan or grep for reference reconciliation
- benchmark or measurement for performance
- security scan plus critique for security-sensitive changes

Preserve evidence when downstream acceptance, critique, shipping, or future agents
will need it.

## Reassessment Questions

Before the next slice:

- did the spec remain true?
- did implementation reveal a better or safer architecture seam?
- did migration, security, performance, or UI risk increase?
- is the next slice still independent?
- should the ticket move to review, blocked, or complete pending acceptance?

If the answer changes the owner truth, route to that owner before continuing.

## Anti-Patterns

- **horizontal-only layers**
  - Result: integration surprises late.
  - Correction: add vertical proof early.
- **large unverified batches**
  - Result: root cause hard to find.
  - Correction: verify after each slice.
- **mixed refactor and feature**
  - Result: review cannot see behavior change.
  - Correction: split into separate tickets/slices.
- **flag with no cleanup**
  - Result: zombie paths.
  - Correction: add owner and deletion trigger.
- **repeated command without edits**
  - Result: no new information.
  - Correction: run after relevant changes only.

## Loom Routing

- slice scope and live state -> ticket
- child implementation scope -> Ralph packet
- red/green or before/after output -> evidence
- changed intended behavior -> spec
- changed sequence or rollout -> plan
- broader seam -> architecture
- old/new coexistence -> migration
- release and PR summary -> ship
