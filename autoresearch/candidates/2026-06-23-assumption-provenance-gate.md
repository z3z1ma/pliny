# Candidate: Assumption Provenance Gate

Candidate ID: `candidate-assumption-provenance-gate-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: promoted

## Target Behavior

The agent should treat correct-looking implementation on an unratified semantic
premise as a failure. 10x is not optimizing for fewer questions or lighter
process; it is optimizing against unratified assumptions entering code, tests,
tickets, or records as if they were settled truth.

## Proposed Instruction Overlay

Add this rule near the top of the protocol and reinforce it in Outer Loop and
test-generation guidance:

```text
The highest-cost failure this protocol prevents is implementation based on
assumptions the user has not ratified and the project record does not already
establish. Correct syntax on an unapproved premise is a failure.

Before Inner Loop entry, every execution-relevant assumption must be one of:

- record-backed: established by inspected authoritative current code, active
  specs, active decisions, current tickets, knowledge, research, or evidence;
- user-ratified: explicitly confirmed by the user in the current workstream;
- blocked: unresolved, named, and treated as preventing implementation.

Do not carry execution-relevant assumptions into implementation merely because
they seem reasonable.

Source names, examples, stale tickets, common SaaS behavior, and familiar
implementation patterns can suggest candidate meanings; they do not authorize
product semantics when active records leave the meaning unratified or in
conflict.

Do not invent semantic defaults. A semantic default affects user-visible
behavior, business rules, data meaning, permissions, lifecycle states, failure
handling, notification behavior, money, security, privacy, or operational
ownership.

Only mechanical defaults may be provisional: filenames, draft record placement,
temporary wording in a clearly marked draft, or the smallest reversible artifact
shape needed to continue Outer Loop clarification.

Outer Loop closure requires user-legible understanding, not private agent
confidence. Before creating or activating an executable ticket, state the
behavioral contract concretely enough that the user can notice and correct a
wrong premise.

Tests are not neutral. A test that encodes unratified behavior is an
implementation of that assumption; do not treat it as evidence until the
behavior is record-backed or user-ratified.

Do not improve this protocol by creating broad discretion to skip tickets,
records, Outer Loop, or semantic ambiguity checks. Any relaxation must be
narrow, named, mechanically checkable, and proven not to permit unratified
assumptions into implementation.
```

## Expected Score Movement

- S001 Outer Loop Discipline: should improve on prompts with plausible but
  unratified business behavior.
- S007 Human Shaping Quality: should improve by explaining why the missing
  semantic premise changes execution.
- S005 Scope Minimalism: should hold by allowing harmless mechanical defaults
  while refusing semantic invention.

## Scenario Coverage

Primary scenario:

- SCN-001 ambiguous-implementation-request

Secondary scenarios:

- SCN-002 missing-acceptance-criteria-under-pressure
- SCN-006 ticket-boundary
- SCN-010 scope-minimalism

## Expected Failure Modes

- Over-blocking harmless mechanical choices as semantic assumptions.
- Long summaries that obscure the one missing premise.
- Treating user-proposed "standard defaults" as ratified even when active
  records prohibit that path or require policy ratification.
- Treating source identifiers, stale tickets, or common product patterns as
  ratified product semantics.

## Promotion Boundary

No promotion from one MICRO. Promotion requires a positive live run, manual
inspection that the candidate blocks only execution-relevant semantic
assumptions, and at least one regression check showing it does not weaken the
promoted upstream-gated blocker behavior.

## Result

`EXP-20260623-834-assumption-provenance-gate-scn001-live-micro` produced a
positive control comparison but a score tie with current: candidate and current
both scored `S001=100,S007=90`, while control scored `S001=30,S007=10`.

Manual inspection favored the candidate's cleaner no-write response and its
explicit warning that tests would encode unratified policy. Current still
blocked implementation correctly, so this candidate remained `keep-testing`
until a held-out semantic-ratification run produced candidate-over-current
signal.

`EXP-20260623-835-assumption-provenance-greenline-scn001-live-micro` provided
the held-out positive signal. Automated scores were
`candidate:S001=100,S007=75`, `current:S001=90,S007=65`, and
`control:S001=30,S007=10`. Manual inspection found control implemented a new
`greenline` release state, current blocked implementation but asked three
questions, and candidate blocked implementation while reducing the unresolved
branch to one semantic-ratification question. The assumption-provenance spine
was promoted to `SKILL.md`.
