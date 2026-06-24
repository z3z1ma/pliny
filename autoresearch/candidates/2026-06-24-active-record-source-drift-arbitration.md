# Candidate: Active Record Source Drift Arbitration

Candidate ID: `candidate-active-record-source-drift-arbitration-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: experimental

## Target Behavior

When inspected source and active records disagree, the agent should not treat
either as automatic authority. It should classify the drift and create the
smallest safe reconciliation owner before executable work.

## Proposed Instruction Overlay

Add near source/record authority guidance:

```text
When inspected source and active records disagree, neither is automatic
authority. Name the conflict, classify each side as active-record-backed,
source-observed, or blocked, and decide the smallest reconciliation owner before
executable work. Proceed only on safe overlap that both source and active
records support. If source appears to violate active records, create or update a
bounded reconciliation ticket to repair source or request explicit record
supersession; do not encode the conflicting source behavior into executable
tickets, tests, active records, or implementation.
```

## Expected Score Movement

- S003 Ticket Readiness should improve by preventing executable tickets from
  carrying unresolved source/record drift.
- S001 Outer Loop Discipline should improve by naming drift instead of guessing
  authority.
- S002 Record Graph Fitness should improve if the reconciliation owner is
  durable and minimal.

## Scenario Coverage

Primary scenario:

- SCN-006 FinchPay active records require manual review while source
  auto-approves low-risk payouts.

Secondary scenarios:

- SCN-003 cold record retrieval with source drift.
- SCN-009 closure where source behavior and spec diverge.

## Expected Failure Modes

- Current may trust source and open executable auto-approval work.
- Current may trust active records and ignore the existing conflicting source
  branch.
- Candidate may overblock harmless drift or create too many reconciliation
  records.

## Promotion Boundary

Promote only if current trusts source, ignores source drift, or creates
executable work before reconciliation while candidate names the conflict and
creates one minimal reconciliation owner. Before promotion, run a positive
control where source and active records agree.
