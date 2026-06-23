# Candidate: Record Economy Threshold

Candidate ID: `candidate-record-economy-threshold-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental
Promotion: manual-only

## Target Behavior

The agent should preserve durable memory without creating redundant records.
When a fact, observation, or follow-up appears record-shaped, the agent should
first decide whether it needs a distinct new record or belongs in an existing
owning record's progress, evidence, or notes.

This is an instruction overlay candidate. It is not a canonical change to
`SKILL.md`.

## Proposed Instruction Overlay

Add this record-economy rule near "Externalize Context as It Crystallizes" and
"Open Tickets Autonomously":

```text
Before creating a new `.10x/` record, apply the record-economy threshold.

Create a new record only when the content has a distinct durable owner and at
least one of these is true:

- A future executor, reviewer, or decision-maker would make a materially worse
  decision without this standalone record.
- The content has independent lifecycle/status from the current owning record.
- The record is required to prove ticket closure, support a promotion/rejection,
  preserve a non-trivial investigation, or track actionable work outside the
  current ticket.

Prefer updating the existing owning record when the information is progress,
context, a small observation, a local note, or a detail that does not need its
own lifecycle. Do not create a decision/spec/research/evidence/ticket spread
just because several record categories could technically apply.

Open a follow-up ticket only for actionable work with a clear owner, outcome,
and acceptance test. If the observation is useful but not actionable yet, record
it in the current ticket, research note, or review residual risk instead of
opening a placeholder ticket.

Evidence records are for observations that must survive independently: closure
proof, reproduction steps, contested claims, promotion evidence, or results a
future agent must be able to audit. Do not create a separate evidence record
for every inspection command when the owning ticket or research record can
carry the observation without loss.

Minimal does not mean silent. If durable context matters, capture it. The
economy test decides the smallest coherent owner, not whether to preserve
truth.
```

## Expected Score Movement

- S002 Record Graph Fitness: should improve by reducing duplicate and
  placeholder records while preserving required durable context.
- S005 Scope Minimalism: should improve in record-heavy situations by avoiding
  unnecessary record spread and follow-up-ticket scaffolding.

## Scenario Coverage

Primary scenario:

- SCN-005 record-spam-trap

Secondary scenarios:

- SCN-004 record-routing
- SCN-008 evidence-overclaim
- SCN-009 closure-coherence

## Expected Failure Modes

- Under-recording: the agent may keep durable facts only in chat or an
  inappropriate owning record.
- Weak evidence: the agent may skip a separate evidence record when closure,
  promotion, or reproduction requires one.
- Actionable debt loss: the agent may bury a real follow-up instead of opening
  a ticket.

## Promotion Boundary

This candidate cannot be promoted without live evidence, manual inspection,
review, and explicit human promotion. It must not directly edit `SKILL.md`.
