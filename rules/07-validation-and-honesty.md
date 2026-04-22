# Validation And Honesty

Loom is only useful if its records are truthful and its completion claims mean something.

## What "Done" Means

Work is done only when all relevant conditions are true:

- the owning ticket tells the truth
- acceptance criteria are satisfied or explicitly revised
- required evidence exists
- required critique has happened or is explicitly deferred
- wiki follow-through has happened or is explicitly deferred
- references are reconciled
- the result stayed within scope

A child assertion is not enough.
A green feeling is not enough.

## Minimum Validation

Before claiming a bounded step landed, perform the smallest validation that makes the claim honest.

That usually includes some mix of:

- record structure checks
- link/reference checks
- scope checks
- behavioral tests or observed outputs
- manual inspection of changed files
- comparison against acceptance criteria
- change-class-specific evidence expectations

## Structural Checklist

A record is structurally credible when:

- the frontmatter exists
- the `id`, `kind`, `status`, `created_at`, and `updated_at` fields exist
- the body has the expected major sections for that kind
- links point at valid targets or are explicitly marked stale/superseded
- filenames and IDs agree with the naming convention

## Ticket Closure Discipline

Use ticket states deliberately.

### `proposed`

The ticket exists, but readiness has not been earned.

### `ready`

The ticket is clear enough to begin.

### `active`

Execution is in progress.

### `blocked`

A real blocker is preventing progress.

### `review_required`

The implementation step landed but critique or acceptance review is clearly next.

### `complete_pending_acceptance`

The work and evidence are substantially complete, but final acceptance or follow-through remains.

### `closed`

The graph tells a complete and truthful story.

### `cancelled`

The work should not proceed, and the cancellation reason is recorded.

Do not jump to `closed` just because a child returned `stop`.

## Reference Reconciliation

When removing, renaming, or superseding anything:

1. search for its canonical ID
2. search for its path if paths are referenced
3. reconcile the references
4. perform the rename or removal
5. run a final spot-check

Broken graph edges are not harmless.
They make future agents slower and less trustworthy.

## Critique And Wiki Gates

Use these defaults unless the project says otherwise:

- meaningful workflow or behavior changes usually deserve critique
- meaningful code changes usually deserve critique
- accepted understanding that future agents will need should become wiki, not only ticket prose
- if critique found unresolved medium or high-severity issues, do not pretend the work is fully accepted

## Honesty Rules

Always:

- distinguish evidence from inference
- distinguish accepted truth from proposed truth
- distinguish current blockers from future possibilities
- distinguish what you inspected from what you assumed
- name residual risks instead of burying them

Never:

- claim completion because "it probably works"
- imply a critique happened when it did not
- let the wiki quietly overstate certainty
- let memory become a second ticket system
- hide a scope expansion inside a local optimization

## If You Cannot Fully Validate

Then say so clearly and leave the graph truthful.

The right response is:

- record what was validated
- record what was not validated
- record the remaining risk
- leave the ticket in the right state
- create follow-up work if needed

Honesty is not failure.
False completion is failure.
