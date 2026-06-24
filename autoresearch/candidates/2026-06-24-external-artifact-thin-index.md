# Candidate: External Artifact Thin Index

Candidate ID: `candidate-external-artifact-thin-index-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: experimental

## Target Behavior

When an external artifact has the force of a specification, plan, decision,
ticket, evidence record, review, research finding, skill, or durable knowledge
record, the agent should create a thin `.10x` index record instead of ignoring
the artifact or copying it wholesale.

## Proposed Instruction Overlay

Add near the "Keep 10x as the Index" section:

```text
When an external artifact has the force of a specification, plan, decision,
ticket, evidence record, review, research finding, skill, or durable knowledge
record, create a thin 10x index record instead of ignoring it or copying it
wholesale.

A thin index record must include normal status headers, the record
classification, a concise summary sufficient for routing, the canonical
external pointer, observed revision/date if available, and a clear statement
that the external artifact remains authoritative. Preserve only the minimum
local context needed for future agents to find and use the artifact. Do not
duplicate full PRDs, issue bodies, PR threads, or design documents into `.10x`
unless the user explicitly makes the local record canonical.
```

## Expected Score Movement

- S002 Record Graph Fitness should improve when external canonical context gets
  represented by a correctly typed local record.
- S003 Ticket Readiness should hold because no executable ticket should be
  opened from a PRD-indexing request alone.
- S005 Economy should improve if the agent avoids copying large canonical
  artifacts into `.10x`.

## Scenario Coverage

Primary scenario:

- SCN-004 simulated approved Google Doc PRD remains canonical and should be
  represented by one thin `.10x/specs/` index record.

Secondary scenarios:

- SCN-003 records-first retrieval from a thin external index.
- SCN-008 research or evidence indexing for external canonical artifacts.

## Expected Failure Modes

- Current may already have enough instruction in "Keep 10x as the Index",
  producing a null result.
- Agents may copy the full PRD into `.10x/specs/`, making the local record look
  canonical.
- Agents may create implementation tickets before the request asks for any
  implementation.

## Promotion Boundary

Promote only if current ignores the external artifact, copies it wholesale, or
creates an ambiguous local record, while the candidate creates a minimal correct
thin index. Before promotion, run a positive control where the user explicitly
makes a local `.10x` spec canonical so the candidate does not over-apply thin
indexing.
