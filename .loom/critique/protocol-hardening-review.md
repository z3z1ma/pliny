---
id: critique:protocol-hardening-review
kind: critique
status: final
created_at: 2026-04-22T09:10:31Z
updated_at: 2026-04-22T16:09:59Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: ticket:vairivh8
links:
  ticket:
    - ticket:vairivh8
  packet:
    - packet:critique-ticket-vairivh8-20260422T091030Z
external_refs: {}
---

# Summary

Reviewed the protocol hardening patch for command canonicality, transaction
boundaries, claim coverage, critique follow-through, and operator clarity.

# Review Target

`ticket:vairivh8` and the staged protocol hardening diff.

# Verdict

Accept the direction, but keep the ticket in `review_required` until the
follow-up findings below are resolved, accepted as deferred, or intentionally
split from this ticket's acceptance.

# Findings

## FIND-001: Legacy dogfood directories still teach retired vocabulary

Severity: medium
Confidence: high
Disposition: resolved

Observation:

The workspace still contains `.loom/docs`, `.loom/runs`, and
`.loom/verification` directories. The protocol source now consistently teaches
`wiki`, `packets`, and `evidence`, but a cold agent inspecting the dogfood tree
will still see the older vocabulary.

Why it matters:

This weakens the workspace-shape story and can confuse agents trying to infer the
current canonical tree from the repository's own `.loom` state.

Follow-up:

- ticket:lj6g3e1y

Resolution:

Removed the empty legacy directories from the working tree. No files required
migration.

## FIND-002: Golden examples are only partially converted to fixtures

Severity: low
Confidence: high
Disposition: resolved

Observation:

`examples/03-feature-with-spec-plan-ticket-ralph` now has before/after fixture
slices, but the other examples remain protocol traces only.

Why it matters:

The examples are useful, but they are not yet strong enough to serve as a
broader protocol eval suite.

Follow-up:

- ticket:0od11m0z

Resolution:

Added fixture structure to all five examples: operator request, expected route,
common wrong behavior, and before/after slices.

# Evidence Reviewed

- `git diff --cached --stat`
- `git diff --check`
- `git diff --cached --check`
- `bash -n scripts/install-loom.sh`
- targeted searches for stale wording and leakage terms
- `.loom` directory listing

# Residual Risks

The staged patch is broad and should still receive human review before closure.
No evidence of transcript-language leakage was found in the changed protocol
surfaces.

# Required Follow-up

None for this critique. Both findings are resolved.

# Acceptance Recommendation

Move `ticket:vairivh8` to `complete_pending_acceptance` if validation remains
clean.
