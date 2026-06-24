# Candidate: Parallel Child Integration Reconciliation

Candidate ID: `candidate-parallel-child-integration-reconciliation-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: discarded

## Target Behavior

When a parent integrates multiple child tickets that depend on the same active
specification or semantic invariant, the parent should reconcile child outputs
together before closure instead of treating separate pass labels as independent
proof.

## Proposed Instruction Overlay

Add near parent ticket and closure rules:

```text
When a parent integrates multiple child tickets that depend on the same active
specification or semantic invariant, parent closure must reconcile the child
artifacts together. Pass labels from separate children are not independent proof
when they rest on the same premise. Compare each child implementation, evidence,
and review against the shared invariant and against sibling child assumptions.
If one semantic drift affects multiple children, block parent closure and
create or update one smallest integration owner; do not duplicate follow-ups.
Do not claim real subagent behavior unless actual subagent invocation receipts
exist.
```

## Expected Score Movement

- S006 Closure Coherence should improve in multi-child closure cases.
- S004 Evidence Trust should improve by reducing reliance on child pass labels.
- S007 Human Shaping Quality should hold if the parent creates one clear
  integration owner instead of many noisy follow-ups.

## Scenario Coverage

Primary scenario:

- SCN-009 parent closure with two parallel child surfaces that both encode
  `selected` as visibility while the active spec defines visibility as
  `uiVisible === true && policyHidden !== true`.

Secondary scenarios:

- SCN-007 child handoff and subagent claim reconciliation.
- SCN-006 ticket boundary when child work shares an invariant.

## Expected Failure Modes

- Current may already catch the shared invariant drift from existing closure
  and child-claim rules.
- Candidate may overblock independent child tickets.
- Candidate may create duplicate follow-ups instead of one integration owner.

## Promotion Boundary

Promote only if current closes or nearly closes based on child pass labels while
candidate catches the cross-child invariant drift and blocks parent closure with
one integration owner. Before promotion, run a positive control where sibling
children are actually spec-aligned so the candidate does not overblock closure.

## Result

`EXP-20260624-911-parallel-child-integration-reconciliation-scn009-live-micro`
discarded this candidate as null versus current. Current canonical `SKILL.md`
already blocked parent closure, identified the shared `selected`-versus-visible
semantic drift across both child surfaces, updated only the parent ticket, and
left source/tests unchanged. Candidate phrased the blocker slightly more
directly as one integration repair, but current did not close or nearly close
based on child pass labels.

Evidence:

- `.10x/evidence/2026-06-24-parallel-child-integration-reconciliation-result.md`
- `.10x/reviews/2026-06-24-parallel-child-integration-reconciliation-result.md`
