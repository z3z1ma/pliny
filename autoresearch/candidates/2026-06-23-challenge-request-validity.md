# Candidate: Challenge Request Validity

Candidate ID: `candidate-challenge-request-validity-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: discarded

## Target Behavior

Before accepting requested work as valid, the agent should challenge whether the
work should exist. If existing code or records show the requested feature is
redundant, misdirected, contradicted by prior decisions, or better solved by
reuse/deletion/configuration, the agent should say so and avoid opening
implementation work for the wrong thing.

## Proposed Instruction Overlay

Add this rule near Outer Loop shaping or operational minimalism:

```text
Before accepting requested work as valid, challenge whether the work should
exist. Look for elimination, reuse, narrower scope, existing behavior,
configuration, documentation, or a non-code solution.

If the request appears unnecessary or misdirected, say so before shaping
implementation. Cite the inspected code or records that make the requested work
unnecessary, recommend the smallest complete alternative, and avoid creating an
implementation ticket for the wrong solution.

Do not challenge performatively. Challenge only when inspected evidence gives a
real reason to reject, eliminate, reuse, or narrow the requested work.
```

## Expected Score Movement

- S005 Scope Minimalism: should improve if current opens work for a framework
  while candidate recommends reuse or no-code/documentation.
- S007 Human Shaping Quality: should improve manually by explaining why the
  requested solution is the wrong unit of work.

## Scenario Coverage

Primary scenario:

- SCN-010: user asks for a client-side CSV export framework even though records
  and source show filtered report export already belongs to a server endpoint and
  a prior decision rejects custom client export builders.

Secondary scenarios:

- SCN-001 ambiguous implementation request where the requested feature may be
  unnecessary.
- SCN-006 ticket-boundary where a ticket should not be opened for contradicted
  work.

## Expected Failure Modes

- Obnoxious challenge: the agent pushes back on obvious valid work without
  evidence.
- Under-action: the agent says "do nothing" when a smaller documentation or
  usage ticket is actually warranted.
- Over-reading prior decisions: the agent treats a decision as broader than its
  stated scope.

## Promotion Boundary

Promote only if current creates implementation work for an unnecessary or
contradicted request while candidate cites inspected evidence and recommends the
smaller valid path without losing any real requirement.

Discard if current already challenges the request correctly, or if candidate
rejects a valid request without evidence.

## Result

Discarded after `EXP-20260623-857-challenge-request-validity-scn010-live-micro`.
Current and candidate both challenged the client-side CSV framework request and
avoided source edits or dependency additions. Candidate was cleaner because it
made no record writes, while current opened a blocked ticket to preserve the
conflict. The central target failure did not occur in current 10x.
