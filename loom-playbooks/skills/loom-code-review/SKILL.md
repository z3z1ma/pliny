---
name: loom-code-review
description: "Run multi-axis implementation review through Loom critique. Use before merge, after feature or bug-fix implementation, when receiving review feedback, when reviewing AI/human code, or when correctness, readability, architecture, security, performance, tests, or evidence need pressure-testing."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-code-review

Code review is adversarial evidence and implementation judgment, not politeness or rubber-stamping.

This playbook adapts peer code-review request and reception workflows into Loom's
critique, ticket, evidence, and ship layers.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- five-axis review: correctness, readability, architecture, security, performance
- test and evidence review before acceptance
- review packet/context preparation for humans or agents
- external review feedback classification and response
- ticket-owned finding disposition and follow-up routing

## What This Workflow Does Not Own

- critique verdict records; use core critique
- ticket acceptance, finding disposition, or closure; use tickets
- evidence artifacts; use evidence
- Git provenance; use `loom-git`
- PR or release wording; use `loom-ship`

## Use This Skill When

- reviewing a diff before merge or acceptance
- an AI agent or human produced code that needs independent scrutiny
- a bug fix needs both implementation and regression-test review
- receiving review comments that may be correct, unclear, optional, or wrong
- a change is large enough that tests passing is not sufficient evidence

## Do Not Use This Skill When

- the request is only to read current code and explain it; use codemap or research
- no implementation or reviewable artifact exists yet
- the target is a Loom record rather than code; use core critique directly
- the next step is only packaging already-reviewed work; use `loom-ship`

## Default Procedure

1. Understand intent before diff details: spec, ticket, acceptance IDs, plan,
   evidence, risk class, and claimed behavior.
2. Review tests first. Ask whether they prove behavior, cover edge/error cases, and
   would fail for the likely regression.
3. Review implementation across correctness, readability, architecture, security,
   and performance.
4. Check change size and concern mixing. Ask for split work when reviewability is poor.
5. Verify the verification story: commands, browser evidence, scans, screenshots,
   benchmarks, skipped checks, and stale outputs.
6. Record durable findings in critique when they should persist. Classify severity,
   confidence, evidence reviewed, residual risk, and required follow-up.
7. Route every open medium/high finding to ticket-owned disposition before closure.
8. When receiving feedback, evaluate it technically before implementing. Clarify
   unclear items, push back on incorrect or out-of-scope requests, and implement
   valid fixes one at a time with verification.
9. Use `loom-ship` only after review disposition and evidence are truthful.

## Finding Severity And Disposition

Use core critique severity in saved critique findings: `low`, `medium`, or
`high`. Put action semantics in the finding title, impact, or required follow-up;
do not replace core severity with peer labels such as `Critical`, `Important`,
`Suggestion`, `Nit`, or `FYI`.

- `high`: likely blocks acceptance unless the ticket records `resolved`,
  `accepted_risk`, `superseded`, or `converted_to_follow_up` disposition.
- `medium`: material risk or quality gap that needs ticket-owned disposition
  before closure.
- `low`: useful concern or polish issue; record it when it should persist, but it
  does not block closure by default.

For open medium/high findings, use only the ticket-owned finding dispositions
from core: `resolved`, `accepted_risk`, `superseded`, or
`converted_to_follow_up`.

## Common Rationalizations

- **Rationalization:** "Tests pass, so review can be quick."
  **Reality:** Tests do not cover architecture, security, readability, performance, or evidence sufficiency.
- **Rationalization:** "It's AI-generated but looks plausible."
  **Reality:** AI code needs more scrutiny because it can be confidently wrong.
- **Rationalization:** "Reviewer feedback is an order."
  **Reality:** Feedback is a claim to evaluate against codebase truth, scope, and owner records.
- **Rationalization:** "We can clean it up later."
  **Reality:** Deferred cleanup needs ticket disposition; otherwise it usually disappears.

## Red Flags

- `LGTM` without evidence of axes reviewed
- no review of tests or evidence
- required and optional comments are indistinguishable
- large mixed feature/refactor/config changes reviewed as one blob
- security-sensitive diff lacks security review
- external feedback implemented before verification or clarification
- medium/high findings lack ticket disposition

## Verification

- [ ] Review target, base/head or changed files, and intent are explicit.
- [ ] Tests and evidence were reviewed before implementation details.
- [ ] Five axes were considered or scoped out with rationale.
- [ ] Findings have severity, confidence, evidence, and required action.
- [ ] Ticket-owned disposition exists for closure-relevant findings.
- [ ] External feedback was classified before implementation.

## Done Means

- critique and ticket records tell the truth about review outcome
- evidence supports or limits the acceptance claim
- required findings are `resolved`, `accepted_risk`, `superseded`, or
  `converted_to_follow_up`
- optional feedback is not treated as hidden mandatory scope
- shipping summaries can mirror owner truth without inventing it

## Read In This Order

Read immediately for code review:

1. `references/review-and-feedback-loop.md` for five-axis review, review packet
   context, core severity/disposition usage, external feedback handling, and
   dependency review.
2. the core `loom-critique` skill for durable findings and verdicts.
3. the core `loom-tickets` skill for finding disposition and closure gate.
4. the core `loom-evidence` skill for verification story checks.

Then read conditionally:

5. `skills/loom-security/SKILL.md` or `skills/loom-performance/SKILL.md` for specialized risk.
6. `skills/loom-git/SKILL.md` when base/head, diff, branch, or PR provenance matters.
7. `skills/loom-ship/SKILL.md` when packaging review outcome for PR or release.
