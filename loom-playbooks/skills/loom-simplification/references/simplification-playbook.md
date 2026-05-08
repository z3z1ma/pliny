# Simplification Playbook

Use this reference when a simplification pass needs more than the top-level
`SKILL.md` reminder. The goal is not fewer lines. The goal is code a new team
member or future agent can understand, modify, debug, and review faster while the
observable behavior stays the same.

## Non-Negotiable Test

Before accepting a simplification, ask:

- Would a new maintainer understand this faster than the original?
- Does every input produce the same output?
- Are side effects, ordering, error behavior, and edge cases unchanged?
- Do existing checks pass without modifying tests to accommodate new behavior?
- Did the diff become easier to review, not just shorter?

If any answer is unclear, the simplification is not yet safe. Route missing
behavior truth to specs, missing context to codemap/research, and missing proof to
evidence.

## Five Principles

### 1. Preserve Behavior Exactly

Simplification may change expression, not semantics. Preserve:

- inputs and outputs
- side effects and ordering
- error types, messages, status codes, and retry behavior when callers can observe them
- edge cases and null/empty handling
- timing or performance properties when they matter to users or contracts

Changing tests to pass after simplification is a warning sign. Test changes are
valid only when they remove implementation coupling while preserving the same
behavioral expectation.

### 2. Match Project Conventions

Simpler means more consistent with this codebase, not more aligned with the
agent's preferences. Check nearby code for:

- import and module style
- naming conventions
- error-handling patterns
- type annotation depth
- framework idioms already accepted by the project
- formatting and lint rules

If official docs and project conventions conflict, route the conflict through
codemap, research, spec, or ticket instead of silently rewriting local style.

### 3. Prefer Clarity Over Cleverness

Compact code is not automatically simpler. Prefer explicit control flow when a
dense expression requires a mental stack. Prefer a named intermediate when it
captures a real concept. Prefer direct loops when chained functional operations
hide mutation, ordering, or error behavior.

Good simplification reduces the number of concepts a reader must hold. Bad
simplification hides concepts behind clever syntax.

### 4. Maintain Balance

Over-simplification is a real failure mode:

- inlining a helper can remove a useful domain name
- merging two simple functions can create one complex function
- removing an abstraction can destroy a real seam or test surface
- optimizing for line count can make review harder
- deleting error handling can make happy-path code look cleaner while weakening behavior

The right question is whether comprehension, locality, and reviewability improved.

### 5. Scope To The Current Work

Default to simplifying recently touched or ticket-scoped code. Drive-by cleanup in
unrelated areas creates noisy diffs and regression risk. If nearby cleanup is
tempting, record it as a follow-up unless the ticket explicitly scopes it.

## Process

### Step 1: Understand Before Touching

Apply Chesterton's Fence before deletion, inlining, or renaming:

- What is this code's responsibility?
- What calls it, and what does it call?
- Which behavior is observable by users, API consumers, or tests?
- What edge cases and error paths exist?
- Are there tests, evidence, docs, or specs defining expected behavior?
- Is there historical context in recent commits, comments, or owner records?
- Was the complexity caused by performance, platform, compatibility, or rollout constraints?

If you cannot answer, do not simplify yet. Read more, map the code, or create a
research note for uncertainty.

### Step 2: Identify Concrete Opportunities

Do not hunt for vague smells. Use observable signals.

| Area | Signal | Typical simplification |
| --- | --- | --- |
| Deep nesting | Three or more nested levels make control flow hard to scan | Use guard clauses, early returns, or named predicates |
| Long function | Function mixes validation, IO, transformation, rendering, and side effects | Split by responsibility with names that match domain concepts |
| Nested ternaries | Reader must parse a decision tree inline | Use if/else, switch, lookup table, or named helper |
| Boolean flags | Calls look like `doThing(true, false)` | Use options object, enum, or separate named functions |
| Repeated conditionals | Same condition appears in several places | Extract a well-named predicate if it is a real concept |
| Generic names | `data`, `result`, `temp`, `item`, `val` hide meaning | Rename to the domain content, such as `validationErrors` |
| Abbreviations | `usr`, `cfg`, `btn`, `evt` slow comprehension | Use full words except universal forms like `id`, `url`, `api` |
| Misleading names | `getUser` also mutates state or logs analytics | Rename or split so names match effects |
| What-comments | Comment narrates obvious code | Delete the comment or make code clearer |
| Why-comments | Comment records intent, constraint, or failure mode | Keep or move to owner records if durable |
| Duplicated logic | Same behavior appears in multiple places | Extract only when the shared concept is real |
| Dead code | Unused imports, unreachable branches, commented blocks | Remove after confirming no references or consumers |
| Pass-through wrapper | Wrapper adds no validation, naming, policy, or seam | Inline and call the underlying function directly |
| Over-engineered pattern | Factory for one implementation, strategy with one strategy | Replace with direct code unless a real extension seam exists |
| Redundant type assertion | Type is already inferred or checked at the boundary | Remove if behavior and type safety remain clear |

### Step 3: Apply One Change At A Time

For each simplification:

1. State the behavior that must remain unchanged.
2. Make one logical change.
3. Run the smallest relevant check.
4. If it fails, revert or narrow the change.
5. Continue only from a working, reviewable state.

Separate feature and bug-fix work from simplification. Mixed diffs are harder to
review, revert, and explain in history.

### Step 4: Use Automation Above Manual Scale

If a refactor touches hundreds of lines or many repetitive sites, manual editing
becomes error-prone. Consider codemods, formatter-safe transforms, or AST-aware
tools, but keep them derivative. The ticket and evidence still own scope and proof.

Before bulk changes, record:

- exact pattern being transformed
- files in scope and out of scope
- dry-run or sample diff
- rollback plan or revert path
- validation command and evidence target

### Step 5: Compare Before And After

After the pass, evaluate the whole result:

- Is the final code easier to understand than the starting code?
- Did new helpers add more concepts than they removed?
- Did names become more specific and more project-aligned?
- Is the diff focused enough for review?
- Would a reviewer understand why this is behavior-preserving?

If the simplified version is harder to understand, revert. Not every cleanup idea
is worth keeping.

## Language And Framework Notes

### JavaScript / TypeScript

Good candidates:

- remove unnecessary `async` wrappers that only `return await` and do not need local error handling
- replace verbose boolean returns with the boolean expression
- replace manual array construction with `map`, `filter`, or `reduce` only when the intent stays clearer
- move stable constants out of render functions when referential identity matters
- remove redundant type assertions after boundary validation

Use caution:

- `||` is not equivalent to `??` for empty string, zero, or false
- `return await` changes stack traces and catch behavior in some contexts
- chained array methods can be slower or less debuggable on hot paths or large data
- callback extraction can hide closure dependencies

### React / JSX

Good candidates:

- separate data loading containers from presentation when it makes states clearer
- extract repeated UI states such as empty/error/loading only when they carry reusable semantics
- replace prop drilling through unused intermediates with composition or context only when the depth and reuse justify it
- keep conditional rendering readable; a small `if` can be clearer than a compact ternary

Use caution:

- do not add `useMemo`, `useCallback`, or `React.memo` as decoration; use them when profiling, referential identity, or project convention justifies them
- do not collapse accessibility labels, focus behavior, or error states for visual neatness
- do not abstract before there are enough real call sites

### Python

Good candidates:

- replace nested conditionals with guard clauses that preserve exception type and order
- use comprehensions when they remain readable and do not hide side effects
- extract named predicates for repeated domain checks

Use caution:

- comprehension order and laziness can affect side effects and performance
- changing exception timing or type is behavior change

## Evidence Expectations

Minimum evidence depends on risk:

- tiny local cleanup: relevant tests or diff review plus targeted search for removed references
- behavior-preserving refactor: test suite or focused checks through the public seam
- dead-code deletion: reference search plus tests or build/lint proof
- naming/API surface cleanup: typecheck/build plus downstream reference reconciliation
- large or bulk simplification: dry-run/sample, full relevant checks, and critique
- performance-sensitive simplification: before/after measurement or explicit measurement limits

Evidence should prove the exact claim: behavior preserved, references reconciled,
dead code removed, or readability improved by a named criterion. It should not say
"simpler" without explaining the observed basis.

## Escalation Routes

- If behavior changes, stop simplification and route to specs/tickets.
- If a seam, interface, or module boundary is the real issue, route to `loom-architecture`.
- If old paths have consumers or need staged removal, route to `loom-migration`.
- If source/version correctness matters, route through `loom-codemap` or research.
- If the diff becomes broad or high-risk, use a plan, Ralph packet, and critique.

## Review Questions

- What behavior is claimed unchanged?
- What evidence proves unchanged behavior through a meaningful seam?
- Did this remove concepts or just move them?
- Are names better because they match domain language, not personal taste?
- Was any error handling, validation, logging, or accessibility behavior weakened?
- Are feature work and cleanup separated enough for review?

## Common Failure Modes

- editing tests to match changed behavior
- inlining a helper that carried a useful domain name
- turning a shallow wrapper into a different shallow wrapper
- deleting "unused" code without checking dynamic references or external consumers
- replacing clear loops with dense functional chains
- broad cleanup outside ticket scope
- claiming behavior preservation from a clean-looking diff alone
