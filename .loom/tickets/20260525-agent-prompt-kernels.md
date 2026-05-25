# Agent Prompt Kernels

ID: ticket:20260525-agent-prompt-kernels
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - changes model-visible Driver and Weaver prompts plus adapter copies, but should preserve accepted behavior.
Priority: medium - aligns explicit agents after Core compression.
Depends On: ticket:20260525-record-skill-kernels

## Summary

Compress Loom Driver and Loom Weaver prompts around their factory roles. The closure claim is that Weaver remains the Design Office and Driver remains the Factory Floor coordinator while duplicated skill doctrine is removed and adapter copies stay aligned.

## Related Records

- `plan:20260525-loom-protocol-compression` - owns sequencing and validation posture.
- `spec:loom-protocol-compression` - defines agent prompt compression in REQ-006.
- `constitution:main` - defines the factory role mapping.
- `spec:loom-driver-agent` - behavior contract for Driver.
- `spec:loom-weaver-agent` - behavior contract for Weaver.
- `ticket:20260525-record-skill-kernels` - provides compressed Core skill vocabulary.
- `AGENTS.md` - product-surface leakage and validation constraints.

## Scope

May change `loom-core/agents/loom-driver.md`, `loom-core/agents/loom-weaver.md`, adapter-specific copies under `loom-core/codex/agents/**`, and the Driver/Weaver specs if their accepted behavior needs wording alignment with the factory framing.

May update package smoke expectations if agent surfaces affect generated or packed output. Do not compress record skills, Playbooks, or broad docs in this ticket.

First Ralph boundary: compare prompts against their specs and the compressed Core skills, remove duplicated doctrine, add factory-role language where it clarifies behavior, align adapter copies, then validate package output.

Stop if factory-role wording would change Weaver or Driver authority, write scope, or execution behavior rather than compressing prompt instructions.

## Acceptance

- ACC-001: Weaver prompt is a concise Design Office instruction: shape records, challenge ambiguity, write only under `.loom/`, and do not launch worker or review runs.
  - Evidence: Source inspection against `spec:loom-weaver-agent` and `constitution:main`.
  - Audit: Fresh-context final audit should challenge authority or write-scope drift.

- ACC-002: Driver prompt is a concise Factory Floor coordinator instruction: start from shaped graph state, coordinate ticket-owned Ralph runs, reconcile output, preserve evidence, route audit, and stop for blockers or higher-authority ambiguity.
  - Evidence: Source inspection against `spec:loom-driver-agent` and `spec:ticket-owned-worker-handoffs`.
  - Audit: Fresh-context final audit should challenge execution and proof loss.

- ACC-003: Canonical and adapter-specific agent surfaces are aligned and do not duplicate full Core skill doctrine.
  - Evidence: Source inspection of `loom-core/agents/**` and `loom-core/codex/agents/**`, plus before/after line counts.
  - Audit: Review should challenge stale adapter copies and hidden second doctrine.

- ACC-004: Product-surface leakage is not introduced.
  - Evidence: Targeted grep/source inspection for package smoke, adapter self-justification, dogfood assumptions, and repository workflow language.
  - Audit: Final audit should inspect leakage search limits.

- ACC-005: Relevant package validation passes.
  - Evidence: Core smoke/pack when touched plus `git diff --check` outputs recorded or cited.
  - Audit: Final audit should inspect evidence sufficiency.

## Current State

Ready after `ticket:20260525-record-skill-kernels` closes. The first run should align prompts to compressed Core vocabulary and avoid changing workflow behavior.

## Journal

- 2026-05-25: Created ticket with dependency on record skill compression.
