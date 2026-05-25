# Record Skill Kernels

ID: ticket:20260525-record-skill-kernels
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: high - rewrites the Core record station skills that preserve graph truth, execution state, evidence, audit, and reusable knowledge.
Priority: high - compresses the main portable protocol after the session kernel.
Depends On: ticket:20260525-session-kernel-compression

## Summary

Compress the Core record skills and references into station kernels. The closure claim is that each surface still teaches its owner truth, lifecycle, inspect/write/update path, stop conditions, and critical non-examples with materially less repeated prose.

## Related Records

- `plan:20260525-loom-protocol-compression` - owns sequencing and validation posture.
- `spec:loom-protocol-compression` - defines record skill compression requirements, especially REQ-004 and REQ-005.
- `spec:ticket-owned-worker-handoffs` - ticket and Ralph compression must preserve worker handoff behavior.
- `ticket:20260525-session-kernel-compression` - provides the compressed shared session vocabulary this ticket should consume.
- `AGENTS.md` - product-surface leakage and validation constraints.

## Scope

May change Core record skills and references under:

- `loom-core/skills/loom-constitution/**`
- `loom-core/skills/loom-specs/**`
- `loom-core/skills/loom-plans/**`
- `loom-core/skills/loom-tickets/**`
- `loom-core/skills/loom-research/**`
- `loom-core/skills/loom-evidence/**`
- `loom-core/skills/loom-audit/**`
- `loom-core/skills/loom-knowledge/**`
- `loom-core/skills/loom-retrospective/**`
- `loom-core/skills/loom-ralph/**`

Templates may change only when wording becomes stale or prevents station-kernel behavior. Do not change record filenames, IDs, statuses, or directory structure unless a specific skill's behavior requires it and the ticket records why. Do not edit Playbooks, agent prompts, or public docs except for links that would break because of reference topology changes.

First Ralph boundary: compress one skill family at a time, preserve required record shapes and lifecycle behavior, run checks, and update the ticket with before/after counts.

Stop if a skill family reveals a behavior change rather than compression; split or route back to specs/constitution.

## Acceptance

- ACC-001: Each compressed record skill clearly states its station owner truth, use triggers, read/inspect path, write/update path, status or lifecycle rules, stop conditions, and critical non-examples.
  - Evidence: Source inspection matrix or evidence record mapping each skill to required station content.
  - Audit: Fresh-context final audit should challenge missing station behavior.

- ACC-002: Skill references are retained, merged, or removed according to `spec:loom-protocol-compression#REQ-005`, with no orphaned references or broken links.
  - Evidence: Source inspection and targeted grep for referenced file names.
  - Audit: Review should challenge references that became manuals or missing detail cards.

- ACC-003: Ticket, Ralph, evidence, and audit skills preserve the execution spine: one ticket, bounded Ralph, evidence as backpressure, audit as inspection, worker output as claim.
  - Evidence: Source inspection against `spec:ticket-owned-worker-handoffs` and `spec:loom-protocol-compression#REQ-001`.
  - Audit: Review should specifically challenge behavior loss in the execution spine.

- ACC-004: Before/after line counts show material compression or the ticket explains why retained prose is necessary for behavior preservation.
  - Evidence: Recorded `wc -l` output or evidence record.
  - Audit: Review should challenge both over-compression and unnecessary retained verbosity.

- ACC-005: Core package validation passes for touched packaged surfaces.
  - Evidence: `npm --prefix loom-core run smoke`, `npm --prefix loom-core run pack:check`, and `git diff --check` outputs recorded or cited.
  - Audit: Final audit should inspect the evidence limits.

## Current State

Ready after `ticket:20260525-session-kernel-compression` closes. The first run should use the compressed session vocabulary and avoid changing agent prompts or Playbooks.

## Journal

- 2026-05-25: Created ticket with dependency on session kernel compression.
