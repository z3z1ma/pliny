---
id: critique:owner-surface-consolidation-review
kind: critique
status: final
created_at: 2026-05-02T11:05:21Z
updated_at: 2026-05-02T11:05:21Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: ticket:53cf2989
links:
  tickets:
    - ticket:53cf2989
  packets:
    - packet:ralph-ticket-53cf2989-20260502T105317Z
  evidence:
    - evidence:owner-surface-consolidation-validation
  plan:
    - plan:skills-corpus-protocol-sharpening
external_refs: {}
---

# Summary

Oracle critique of owner-surface consolidation for atlas, retrospective,
spike/sketch, and skill metadata doctrine under `ticket:53cf2989`.

# Review Target

Reviewed the current working-tree diff for:

- atlas/codemap owner-surface consolidation
- retrospective owner-surface consolidation
- research/spike/sketch owner-surface consolidation
- skill-authoring metadata conventions
- `ticket:53cf2989`
- `packet:ralph-ticket-53cf2989-20260502T105317Z`
- `evidence:owner-surface-consolidation-validation`

Required critique profiles:

- operator-clarity
- routing-safety

# Verdict

`pass`.

Initial oracle critique found two medium issues. Parent resolved both, and final
oracle re-check returned `pass` with no new findings.

# Findings

## FIND-001: Retrospective procedure nuance was not fully relocated

Severity: medium
Confidence: high
Disposition: resolved

Observation:

Initial consolidation reduced `skills/loom-records/references/retrospective.md`
to shared grammar and pointed to `loom-retrospective` for the
`observe/distill/promote/prevent` procedure, but `loom-retrospective` did not yet
carry the named loop or detailed prevention mapping.

Why it matters:

The pointer would have led operators to an owner surface that did not contain the
promised procedure, losing useful prevention nuance.

Follow-up:

Resolved by adding the `observe -> distill -> promote -> prevent` loop and
prevention artifact mapping to `skills/loom-retrospective/SKILL.md`, while
keeping `skills/loom-records/references/retrospective.md` at shared grammar and
routing-pointer scope.

Challenges:

- `ticket:53cf2989` ACC-002 and ACC-005 before repair.

## FIND-002: Metadata convention conflicted with memory support-layer metadata

Severity: medium
Confidence: high
Disposition: resolved

Observation:

Initial `skills/loom-skill-authoring/references/structure.md` said support-layer
skills should not name `metadata.owns_layer`, while `skills/loom-memory/SKILL.md`
uses `metadata.owns_layer: memory`.

Why it matters:

The convention would have made existing memory metadata ambiguous just as this
ticket was supposed to settle metadata guidance.

Follow-up:

Resolved by allowing support-layer skills to name `metadata.owns_layer` for a
named non-canonical support layer such as memory, with explicit wording that this
does not make the support layer canonical truth.

Challenges:

- `ticket:53cf2989` ACC-004 before repair.

# Evidence Reviewed

- Current working-tree diff.
- `git diff --check`, with no whitespace output.
- `ticket:53cf2989` reconciliation, acceptance criteria, evidence posture, and
  critique posture.
- `packet:ralph-ticket-53cf2989-20260502T105317Z` contract and child output.
- `evidence:owner-surface-consolidation-validation`.
- Product files for atlas, codemap, retrospective, records, research/spike, and
  skill-authoring metadata.
- Targeted searches for stale duplicate doctrine and metadata conflicts.

# Residual Risks

- Review was limited to the current diff and targeted surfaces; examples and
  unrelated skills were not exhaustively audited.
- Validation remains structural/manual, which matches this repository's
  verification model.

# Required Follow-up

None for this ticket. The final corpus validation ticket remains responsible for
broader cross-surface review.

# Acceptance Recommendation

Close-ready. `ticket:53cf2989` ACC-001 through ACC-005 are satisfied.
