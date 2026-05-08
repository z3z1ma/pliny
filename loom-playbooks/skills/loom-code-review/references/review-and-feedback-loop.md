# Review And Feedback Loop

Use this reference when reviewing code or processing review feedback.

## Review Input Package

Before reviewing, collect:

- ticket, spec, plan, and relevant acceptance IDs
- base and head commits or current diff when Git matters
- changed files and claimed write scope
- evidence gathered so far
- known risks, skipped checks, and residual questions
- project conventions or nearby patterns

If the reviewer lacks this context, review quality drops and findings drift into
preferences.

## Five Axes

### Correctness

- matches spec and ticket acceptance
- handles edge, empty, null, boundary, and error cases
- avoids race, state, ordering, and idempotency bugs
- tests would catch likely regressions

### Readability and simplicity

- clear names and straightforward control flow
- abstractions earn their complexity
- comments explain why, not obvious what
- no dead AI scaffolding, no-op variables, commented-out code, or speculative helpers

### Architecture

- respects module boundaries and dependency direction
- introduces new patterns only with rationale
- keeps public or shared contracts stable or spec-owned
- makes important behavior testable at the right seam

### Security

- validates untrusted input at boundaries
- avoids secrets in code, logs, tests, and evidence
- preserves auth and authorization expectations
- avoids injection, XSS, unsafe CORS, weak cookie/session handling, and error leakage

### Performance

- avoids N+1 queries, unbounded loops, and fetch-all endpoints
- avoids unnecessary synchronous or hot-path work
- uses pagination, caching, or batching only where justified
- checks UI re-render, bundle, image, and Core Web Vitals risks when relevant

## Review Tests First

Tests expose the author's understanding. Check:

- behavior focus instead of implementation details
- red/green proof for bugs where possible
- edge/error cases
- deterministic timing and isolation
- realistic boundaries instead of over-mocking
- descriptive test names

If tests are missing or weak, implementation review is operating with less proof.

## Change Size And Splitting

Reviewability drops as concerns mix. Split when:

- feature and broad refactor are bundled
- config/dependency changes are mixed with behavior
- generated artifacts obscure hand edits
- one diff needs several unrelated reviewers
- the change is too large for a meaningful review pass

Accept large diffs only when they are mechanical, generated, or deletion-heavy and
the evidence/intent is clear.

## Finding Format

Good finding:

```text
Severity: medium
Location: src/path/file.ts:42
Claim: This bypasses the spec's authorization requirement for archived projects.
Evidence: route checks project membership but not archive visibility.
Required action: enforce `canViewArchivedProject` or revise spec acceptance.
```

Use core critique severity values in saved critique findings: `low`, `medium`, or
`high`. If a human review system uses labels such as `blocker`, `nit`, or
`suggestion`, map them into core severity and ticket-owned disposition before
closure.

Avoid vague findings such as `this feels risky` without evidence or route.

## Receiving Review Feedback

Treat feedback as claims, not orders.

1. Read all feedback before editing.
2. Clarify unclear items before partial implementation when items may interact.
3. Verify each claim against code, tests, specs, decisions, and project constraints.
4. Classify: blocker, valid required change, optional/nit, incorrect, out of scope,
   or needs owner decision.
5. Implement valid changes one at a time with verification.
6. Push back factually when feedback is wrong or conflicts with accepted truth.
7. Record ticket disposition for closure-relevant findings.

Do not use performative agreement as a substitute for technical evaluation.

## Dependency Review

Before adding or keeping a dependency, ask:

- does the existing stack or standard library solve this?
- is the dependency actively maintained?
- what is the bundle/runtime footprint?
- are there known vulnerabilities?
- is the license compatible?
- what transitive risk or supply-chain exposure is introduced?

Every dependency is a maintenance and security liability, even when convenient.

## Verification Story Review

Review the proof as a first-class artifact:

- exact commands run
- current source state
- failures, warnings, skips, and stale evidence
- browser screenshots or runtime logs when UI claims are made
- benchmark methodology when performance claims are made
- scans and reachability when security claims are made

If proof is partial, review can still pass with residual risks, but closure must
not imply more than evidence supports.

## Loom Routing

- durable findings and verdict -> critique
- finding disposition and closure -> ticket
- output artifacts -> evidence
- changed behavior contract -> spec
- broader architecture issue -> architecture/research/plan
- PR or release summary -> ship
