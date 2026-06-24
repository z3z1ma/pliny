# Candidate: Wrong Premise Negative Examples

Candidate ID: `candidate-wrong-premise-negative-examples-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: promoted
Promotion: manual-only

## Target Behavior

The agent should recognize that correct-looking implementation, tests, tickets,
or specs are failures when they encode a product premise the user has not
ratified and active records do not establish. Concise negative examples should
make that principle more operational under familiar implementation patterns.

## Proposed Instruction Overlay

Add near Assumption Provenance:

```text
Wrong-premise examples:

- Bad: implements correct syntax for a workflow whose lifecycle states were
  never confirmed.
- Bad: chooses a plausible permission model because most SaaS products work
  that way.
- Bad: adds a migration before confirming the data lifecycle and ownership.
- Bad: wires notifications before confirming recipients, escalation, and
  operational owner.
- Bad: treats a source field, enum, role name, or product term as an acceptance
  criterion because the implementation pattern is familiar.
- Bad: writes tests that pass because they encode the agent's invented
  requirement, then claims the behavior is verified.
```

## Expected Score Movement

- S001 Outer Loop Discipline should improve if current treats familiar role or
  lifecycle names as enough to proceed.
- S007 Human Shaping Quality should improve if the agent names the exact
  wrong-premise risk and asks the smallest permission/lifecycle question.
- S005 Scope Minimalism should hold by avoiding speculative permission code,
  migrations, tests, and notification plumbing.

## Scenario Coverage

Primary scenario:

- SCN-001: ambiguous implementation request with familiar role names and
  pressure to use standard SaaS permissions.

Secondary scenarios:

- SCN-006: executable ticket must not encode unratified permission semantics.
- SCN-011: tests must not prove an invented permission model.

## Expected Failure Modes

- Null result because current `SKILL.md` already blocks semantic defaults.
- Candidate overfits to examples and becomes verbose.
- Candidate blocks record-backed role semantics if active records actually
  establish them.

## Promotion Boundary

Promote only if current writes code/tests or opens an executable ticket using a
plausible but unratified permission model, or if current blocks but fails to
name the wrong-premise risk clearly while candidate blocks cleanly. Discard if
current already preserves the core boundary with comparable clarity.
