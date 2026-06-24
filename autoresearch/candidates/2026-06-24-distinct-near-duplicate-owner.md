# Candidate: Distinct Near-Duplicate Owner

Candidate ID: `candidate-distinct-near-duplicate-owner-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: active
Promotion: manual-only

## Target Behavior

When records contain an existing ticket for a similar problem, the agent should
reuse that ticket only if it actually owns the same behavioral surface. A shared
symptom, file format, field name, or failure class is not enough to collapse
distinct scopes.

The target is the residual risk from recent record-economy improvements:
avoiding duplicate records must not bury a separate follow-up whose actor,
path, lifecycle, acceptance criteria, or explicit exclusions make it distinct.

## Proposed Instruction Overlay

Add near "Fish Before Opening":

```text
Near-duplicate records require ownership comparison, not keyword matching.
Before reusing an existing ticket for a newly requested follow-up, compare the
actor, code path, data path, lifecycle, acceptance criteria, and explicit
exclusions.

Reuse or update the existing ticket only when it owns the same behavioral
surface. If the existing ticket explicitly excludes the requested path or its
acceptance criteria cannot prove the requested outcome, create the smallest
separate owner and cross-reference the related ticket.

Do not create duplicate tickets for the same work. Do not over-deduplicate
distinct work merely because the same symptom, file format, or failure class is
mentioned in both records.
```

## Expected Score Movement

- S002 Record Graph Fitness should improve by keeping ownership accurate:
  neither duplicate nor over-collapsed.
- S005 Scope Minimalism should hold because the new owner must be the smallest
  bounded follow-up.
- S007 Human Shaping Quality may improve when the final answer names why the
  existing record is related but insufficient.

## Scenario Coverage

Primary scenario:

- SCN-005: existing visible-rows CSV quote/newline ticket is related to, but
  does not own, requested legacy nightly/archive CSV quote/newline coverage.

Secondary scenarios:

- SCN-009 closure follow-up ownership.
- SCN-010 minimalism when a similar existing record might appear to make new
  tracking unnecessary.

## Expected Failure Modes

- Under-tracking: agent says the visible-rows ticket owns archive export
  coverage even though it excludes archive behavior.
- Over-tracking: agent creates a broad "all CSV escaping" ticket instead of a
  bounded legacy/archive owner.
- Duplicate tracking: agent creates a second visible-rows quote/newline ticket.
- Source mutation despite ticket-only prompt.

## Promotion Boundary

Promote only if current over-deduplicates the archive/legacy gap into the
visible-rows ticket, creates a vague catch-all, or otherwise fails ownership
comparison while candidate creates exactly one bounded archive/legacy follow-up
and cites the related visible-rows ticket. Discard if current already performs
the correct ownership comparison.
