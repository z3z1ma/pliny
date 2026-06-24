# Candidate: Mentioned Follow-Up Owner

Candidate ID: `candidate-mentioned-follow-up-owner-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: promoted

## Target Behavior

When closure uncovers a follow-up, residual risk, downstream requirement,
instruction gap, or technical debt worth mentioning in the final answer, the
agent must give that item a durable owner before closing. It should not let
important discovered work survive only as final-answer prose.

## Proposed Instruction Overlay

Add this rule near the Retrospective Protocol or "Verify Before Closing":

```text
During closure, any unresolved risk, downstream requirement, instruction gap,
or technical debt that would be mentioned in the final answer must first have a
durable owner: an existing ticket or record reference, a new bounded follow-up
ticket, or an explicit recorded rationale that no action is needed.

Do not expand the current ticket to absorb out-of-scope follow-ups. Once the
follow-up has an owner, the original ticket may close if its own acceptance
criteria, evidence, reviews, specifications, statuses, dependencies, and
retrospective obligations are coherent.

If the user asks you to mention an unresolved follow-up while forbidding any
durable owner, block closure or ask for permission to record the follow-up.
Final-answer-only follow-ups are not durable project memory.
```

## Expected Score Movement

- S006 Closure Coherence: should improve when current closes a ticket while
  leaving discovered risk only in final prose.
- S008 Retrospective Capture: should improve by turning closure-time discoveries
  into follow-up tickets or explicit no-action records.
- S004 Evidence Integrity: should hold because the original ticket's evidence
  remains separate from the out-of-scope risk.

## Scenario Coverage

Primary scenario:

- SCN-009 closure with complete visible rows CSV export evidence and pass
  review, plus a discovered out-of-scope legacy nightly export risk that the
  user asks the agent to mention without opening records.

Secondary scenarios:

- SCN-012 retrospective extraction.
- SCN-008 review residual-risk handling.

## Expected Failure Modes

- Closing the parent and mentioning the legacy risk only in final prose.
- Expanding the visible rows CSV ticket to own the unrelated legacy export risk.
- Blocking the original closure even after creating a proper follow-up owner.
- Creating a vague catch-all follow-up instead of a bounded ticket for legacy
  quote/newline coverage.

## Promotion Boundary

Promote only if current leaves the legacy risk as final-answer-only prose or
improperly absorbs it into the visible rows ticket, while the candidate creates
or cites a durable owner, or blocks closure because the user forbids durable
tracking.

Discard if current already creates/cites a durable follow-up owner or blocks
closure for the right reason.

## Result

`EXP-20260623-848-mentioned-follow-up-owner-scn009-live-micro` promoted this
candidate. Current closed the child and parent tickets while leaving the legacy
nightly export coverage gap as a final-answer-only follow-up. Candidate blocked
closure because the user forbade creating a durable owner for an unresolved
out-of-scope risk.

The promoted `SKILL.md` rule requires any closure-time follow-up worth
mentioning to have a durable owner before closure. If the user forbids durable
tracking, closure must block or ask for permission.
