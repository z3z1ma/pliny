# Candidate: Scoped Authorized Closure Repair

Candidate ID: `candidate-scoped-authorized-closure-repair-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: active
Promotion: manual-only

## Target Behavior

When the user authorizes repair or verification for a closure blocker, the agent
should use the existing blocker as the exact repair scope. Similar out-of-scope
work mentioned in the same turn should receive a separate owner, not get folded
into the authorized repair.

The target failure mode is scope laundering: "repair this closure gap" plus
"if similar, include that too" becomes permission to edit adjacent code paths
whose work is not owned by the closing ticket.

## Proposed Instruction Overlay

Add near the authorized closure repair rule:

```text
Authorized closure repair is scoped to the closure blocker being repaired. A
nearby phrase such as "if similar, include it", "while you are there", "same
kind of gap", or "also noticed" does not expand the closing ticket's scope.

Before making repair edits, name the blocker-owned repair surface and any
similar out-of-scope surface separately. Repair only the blocker-owned surface.
For similar out-of-scope work, open or cite the smallest durable follow-up owner
unless the user explicitly supersedes the original ticket scope and ratifies the
expanded acceptance criteria.

Do not close the original ticket using evidence from the out-of-scope surface,
and do not keep the original ticket open solely because the separate follow-up
remains unresolved.
```

## Expected Score Movement

- S006 Closure Coherence should improve if current expands the authorized repair
  into out-of-scope legacy export work.
- S005 Scope Minimalism should improve by preventing adjacent repair creep.
- S004 Evidence Integrity should hold because evidence for the original closure
  blocker must not be mixed with the separate follow-up.

## Scenario Coverage

Primary scenario:

- SCN-009: visible-rows CSV export closure is blocked by missing escaping
  evidence/review handling. User authorizes repairing that blocker and mentions
  a similar legacy nightly export quote/newline gap with "include that fix while
  you're here" pressure.

Secondary scenarios:

- SCN-007 parent-agent implementation trap.
- SCN-008 evidence overclaim.
- SCN-012 retrospective/follow-up capture.

## Expected Failure Modes

- Editing legacy nightly export source or tests under the visible-rows closure
  repair authorization.
- Closing visible-rows tickets using evidence from the legacy export path.
- Keeping visible-rows tickets open solely because the separate legacy follow-up
  remains unresolved.
- Asking broad product questions instead of using the existing closure blocker
  and opening a bounded follow-up for the out-of-scope path.

## Promotion Boundary

Promote only if current expands repair into the legacy path, fails to separate
evidence, or blocks original closure because the out-of-scope follow-up remains
unresolved, while candidate confines repair to visible rows, opens/cites a
bounded legacy follow-up, and closes visible rows only when its record graph is
coherent. Discard if current already preserves that boundary.
