# Verification Posture

Packet style governs how much context the packet carries. Verification posture governs how the child proves the iteration actually did what it claimed.

These are two axes, not one. A `reference-first` packet can be `test-first`. A `hermetic` packet can be `none`. Choose each axis deliberately.

## Why this is a packet-level field

Posture belongs in the packet frontmatter, not in the ticket. A single ticket may include iterations of different postures — test-first for behavior changes, none for a pure refactor iteration that rides on the tests already green. Binding posture to the packet keeps each iteration's contract honest without forcing every iteration of a test-first ticket into test-first shape.

## Postures

### `test-first`

Loom's native TDD shape.

The child must:

1. produce a failing check that expresses the intended behavior — a failing test, a failing assertion, a failing executable observation — *before* any implementation change
2. drive that check to green inside this iteration
3. return evidence of both the red state and the green state in the output contract

The stop conditions on the packet must include "a failing check exists and has been driven to green." The child cannot satisfy the contract by writing tests after the implementation and calling them new.

Use `test-first` when:

- the spec or ticket names a behavioral outcome that can be exercised
- the change is a new feature, a bug fix with a reproducible failure, or a behavior change with observable effects
- the project benefits from a regression check that outlives this iteration

### `observation-first`

The same red-before-green discipline applied to behavior that is not yet testable in an automated sense.

The child must:

1. capture inspectable evidence of current behavior before the change — a logged output, a captured artifact, a recorded run, a screenshot, a diffable snapshot
2. make the change
3. capture inspectable evidence of the new behavior
4. return both in the output contract

Use `observation-first` when:

- the behavior is observable but automated testing is impractical or premature
- the iteration changes something whose correctness depends on comparison with a prior state
- the evidence itself is the point (exploratory work, migration verification, an experiment whose result matters even without a test harness)

### `none`

No explicit verification beyond the normal output contract.

Honest choices for `none`:

- record hygiene and reference reconciliation
- documentation edits that do not change behavior
- a packet compile or a template move
- a pure refactor that rides on an already-green test suite (in which case the output should cite the suite that stayed green)

Dishonest uses of `none`:

- "there was no good way to test this" — reach for `observation-first` instead
- "the change is small" — smallness is not the same as verification-neutrality
- "we'll add tests later" — then the posture is `test-first` and the tests are due now

## Choosing posture

- if the spec or ticket acceptance names a behavioral outcome, default to `test-first`
- if the behavior is real but not yet testable, default to `observation-first`
- if the iteration genuinely does not change behavior, `none` is the honest choice

Use `skills/loom-records/references/change-class.md` to confirm the default.
For `code-behavior`, start from `test-first` or `observation-first`; for
`record-hygiene`, `none` is often enough when structural checks cover the
claim.

When in doubt, prefer the stricter posture. The discipline compounds.

## What goes in the packet body

The packet's Verification Posture section should concretely state:

- for `test-first`: what failing check must exist, what counts as green, and where the check lives
- for `observation-first`: what must be observed before and after, and how the before/after evidence is captured
- for `none`: a one-line justification of why this iteration is verification-neutral

## Relationship to acceptance and critique

Posture is not a substitute for acceptance criteria on the ticket, and it is not a substitute for critique.

- the ticket owns what "acceptance" means across iterations
- the packet owns what "this iteration proved it worked" means
- critique pressure-tests whether the evidence actually supports the claim

Source code shows current implementation reality. Specs and tickets state
intended behavior. Evidence is the bridge between them.

A green test-first iteration is not the same as a closed ticket. Acceptance still decides.
