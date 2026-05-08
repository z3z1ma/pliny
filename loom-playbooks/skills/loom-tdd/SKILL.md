---
name: loom-tdd
description: "Drive behavior changes with failing checks first. Use when implementing logic, fixing bugs, changing behavior, adding edge cases, writing tests, or needing red/green proof before a ticket can claim correctness."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-tdd

TDD is behavior proof before implementation confidence.

This playbook adapts red/green/refactor and the bug-fix prove-it pattern to
Loom: specs and tickets own the behavior claim, evidence owns observations, and
critique judges whether the proof is good enough.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- red/green/refactor execution for behavior changes
- regression-test-first bug fixes
- selection of unit, integration, browser, or end-to-end proof seams
- test-quality review before accepting green output
- evidence preservation for red and green states

## What This Workflow Does Not Own

- intended behavior; use specs or ticket-local acceptance
- live execution, blockers, acceptance, or closure; use tickets
- observed test output; use evidence
- review verdicts; use critique
- package or PR summaries; use `loom-ship`

## Use This Skill When

- implementing new logic or changing behavior
- fixing a bug that should never recur
- adding edge case handling
- modifying an existing contract where regressions matter
- a ticket, critique, or user asks for proof rather than assertion
- tests exist or can reasonably be added at a meaningful seam

## Do Not Use This Skill When

- the change is pure docs, record hygiene, static content, or metadata with no behavior
- the honest proof is runtime observation rather than an automated check; use
  observation-first evidence through core evidence/ticket guidance
- intended behavior is unclear; update the spec or ticket before writing tests
- there is no credible test seam and the next step is a spike or codemap pass

## Default Procedure

1. Identify the behavior claim and its owner: spec acceptance ID, ticket-local
   criterion, bug report, or current implementation contract.
2. Pick the smallest meaningful proof seam: unit for pure logic, integration for
   boundaries, browser/UI for visible behavior, end-to-end only for critical flows.
3. RED: write the check before the implementation, run it, and confirm it fails
   for the expected reason. A passing test at RED proves nothing.
4. GREEN: write the minimal implementation that makes the check pass. Do not
   bundle unrelated refactors or speculative abstractions.
5. REFACTOR: clean up while keeping the check and relevant existing checks green.
6. For bug fixes, prove the original symptom with a failing reproduction check
   before the fix when practical.
7. Preserve red and green output in evidence when the ticket needs citable support.
8. If the check is flaky, shape-based, over-mocked, or too indirect, improve the
   proof before claiming acceptance.
9. Route residual risk to critique or ticket disposition instead of hiding it in
   a green test summary.

## Test-Quality Rules

- Test outcomes and state, not incidental implementation details.
- Prefer real implementations, fakes, and stubs over interaction mocks unless the
  real dependency is slow, nondeterministic, external, or side-effectful.
- Keep tests descriptive even when they duplicate setup. DAMP tests are often more
  useful than over-DRY helpers.
- Name tests like behavior specifications.
- Do not skip, delete, or weaken tests to make the suite pass without ticket-owned
  rationale and critique when risk warrants it.

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "I'll write tests after the code works." | That is test-after. TDD requires RED before GREEN when this workflow applies. |
| "The test passes on first run, so good." | A test that never failed may not prove the intended behavior. Verify RED or state the limit. |
| "Manual testing is enough." | Manual observation can be evidence, but it does not create a reusable regression guard. |
| "Mocks make this easy." | Over-mocking can test your mock setup while production behavior is broken. |
| "The fix is tiny, so no repro test." | Tiny bug fixes still need a guard when recurrence matters. |

## Red Flags

- implementation code appears before a failing behavior check without rationale
- bug fix has no reproduction test or explicit reason one is impossible
- test asserts private calls, snapshots, or framework behavior instead of project behavior
- test names say `works`, `handles errors`, or other vague outcomes
- a skipped or weakened test is treated as success
- same test command is rerun without source changes just for reassurance

## Verification

- [ ] Behavior claim and owner are explicit.
- [ ] RED failed for the expected reason or the limitation is recorded.
- [ ] GREEN passed after the implementation change.
- [ ] Refactor, if any, kept relevant checks green.
- [ ] Test quality was checked for behavior focus, determinism, and over-mocking.
- [ ] Evidence links support ticket acceptance when needed.

## Done Means

- the behavior is owned by spec or ticket truth
- red and green observations exist or limitations are explicit
- implementation and tests stay inside the scoped ticket or packet
- evidence and critique disposition are sufficient for the claim being made

## Read In This Order

Read immediately for TDD work:

1. `references/red-green-behavior-proof.md` for test-seam selection, prove-it bug
   fixes, test quality, browser proof, and anti-patterns.
2. the core `loom-specs` and `loom-tickets` skills to identify the behavior claim
   and live acceptance owner.
3. the core `loom-evidence` skill when preserving red/green output.

Then read conditionally:

4. `skills/loom-debugging/SKILL.md` when the test is reproducing an unknown root cause.
5. `skills/loom-ui-browser/SKILL.md` when the behavior is browser-visible.
6. `skills/loom-code-review/SKILL.md` and the core `loom-critique` skill when proof
   quality or implementation risk needs review.
