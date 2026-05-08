---
name: loom-debugging
description: "Run reproduce-first debugging. Use when tests fail, builds break, behavior regresses, errors occur, flaky behavior appears, performance drops unexpectedly, root cause is unknown, or a fix needs red/green evidence."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow
---

# loom-debugging

Debugging routes reproduction, root-cause work, fixes, evidence, and prevention
follow-through into the Loom records that own those facts.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## What This Workflow Coordinates

- reproduce-first bug workflow
- root-cause routing
- fix evidence expectations
- performance-regression measurement loops
- CI/build failure triage as a feedback source
- prevention handoff into retrospective

## Use This Skill When

- there is a failing behavior or incident
- the root cause is unknown
- intended behavior is ambiguous
- a fix needs regression evidence before acceptance

## Do Not Use This Skill When

- the work is a normal feature with clear acceptance
- the failure cannot be reproduced or observed yet and the only need is intake
- the next step is already a narrow ready ticket with evidence

## Default Procedure

Follow:

`orient -> feedback loop -> reproduce -> localize -> hypothesize -> fix -> evidence -> prevent`

1. orient in the relevant domain language, code paths, decisions, and accepted
   behavior before treating the symptom as the root cause
2. build or improve a fast feedback loop that can show the failure
3. capture reproduction steps or current failing behavior as evidence
4. investigate root cause before proposing a fix; create or update research if
   the root cause is not known
5. generate ranked, falsifiable hypotheses when cause is unclear
6. update or create a spec if intended behavior is ambiguous
7. create or tighten a ticket for the bounded fix
8. for performance regressions, capture a baseline, name the budget or user-facing
   threshold when one exists, and measure after the fix instead of relying on a
   subjective speed impression
9. for CI/build failures, distinguish project behavior from environment, cache,
   dependency, or flaky-test signals before changing source code
10. choose local execution for a tiny, local, safe fix, or compile a Ralph packet when
    the fix needs fresh context, explicit child write scope, or packetized
    isolation; Ralph packets normally use `verification_posture: test-first`
11. preserve red and green evidence
12. run critique when risk warrants
13. run retrospective if the lesson should prevent repeated mistakes

## Artifact Routing

- **reproduction steps** — owner: evidence.
- **root cause investigation** — owner: research.
- **intended behavior clarification** — owner: spec.
- **fix execution** — owner: ticket plus local execution or Ralph packet, according to ticket facts and write-scope needs.
- **regression evidence** — owner: evidence.
- **performance baseline and after measurement** — owner: evidence.
- **CI/build output, flaky-test reproduction, or dependency/cache signal** — owner: evidence, then research when cause remains uncertain.
- **recurring evidence gap** — owner: ticket follow-up or test expectation via retrospective.
- **recurring lesson** — owner: wiki, research, spec, plan, initiative, constitution, or evidence via retrospective; memory may keep support-only recall or owner-record pointers.

## Common Rationalizations

- **Rationalization:** "The fix is obvious."
  **Reality:** Obvious fixes still need a feedback loop and evidence that the original failure no longer reproduces.
- **Rationalization:** "I cannot reproduce it, but this change might help."
  **Reality:** If reproduction is unstable, improve observation or ask for artifacts; do not claim a root-cause fix.
- **Rationalization:** "Logging everything will reveal the issue."
  **Reality:** Instrument predictions from hypotheses; broad logs create noise and cleanup debt.
- **Rationalization:** "A green nearby test proves the bug is fixed."
  **Reality:** Regression evidence must exercise the real failure pattern or explicitly state the seam is missing.
- **Rationalization:** "It feels faster now."
  **Reality:** Performance fixes need before/after measurement or an explicit reason measurement is not available.
- **Rationalization:** "CI failed, so source must be wrong."
  **Reality:** CI output is evidence to classify; environment, cache, dependency, and flake causes must be considered.

## Red Flags

- no fast or credible feedback loop before code changes
- only one hypothesis was considered for an unknown root cause
- instrumentation is untagged or not mapped to a prediction
- fix addresses symptom but not source
- performance change has no baseline or after measurement
- CI fix changes source without reproducing or classifying the failure mode
- prevention lesson is left in chat after a repeated failure

## Verification

- [ ] Original failure was reproduced or inability to reproduce is explicit.
- [ ] Hypotheses were falsifiable when root cause was unknown.
- [ ] Fix evidence includes red/green or before/after observations.
- [ ] Performance claims include baseline and after measurement or explicit measurement limits.
- [ ] CI/build failures distinguish source, environment, dependency, cache, and flake causes.
- [ ] Temporary instrumentation and prototypes are removed or contained.
- [ ] Prevention route is recorded when the lesson should persist.

## Done Means

- the failure was reproduced or the inability to reproduce is explicit
- root cause is evidence-backed or still marked unknown
- intended behavior is owned by a spec when needed
- the fix is owned by a ticket and either reconciled local execution or packetized
  child result, as appropriate
- evidence exists for before and after behavior
- prevention follow-through is explicit

## Read In This Order

Read immediately for debugging work:

1. `references/systematic-debugging.md` when root cause is unknown, time pressure
   makes guessing tempting, or previous fixes failed.
2. `skills/loom-tdd/SKILL.md` when a bug fix should begin with a failing
   reproduction check.
3. the core `loom-evidence` skill before preserving or citing reproduction,
   red/green output, logs, screenshots, or other evidence.
4. the core `loom-tickets` skill before claiming a failure is fixed, accepted, or
   ready to close.

Then read conditionally:

5. `skills/loom-performance/SKILL.md` when the failure is a performance regression.
6. the core `loom-research` skill when root cause is unknown or rejected
   hypotheses should remain citable.
7. the core `loom-specs` skill when intended behavior is ambiguous.
8. the core `loom-tickets` skill when creating or tightening the bounded fix
   ticket.
9. the core `loom-ralph` skill when the fix is ready for a packetized
   implementation iteration.
10. the core `loom-critique` skill when the fix or incident carries review risk.
11. the core `loom-retrospective` skill when the prevention lesson should persist
   beyond the ticket.
