# Session Kernel Compression

ID: ticket:20260525-session-kernel-compression
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: high - changes the session-start doctrine and preload surfaces that govern all Loom routing.
Priority: high - largest context-impact slice after the compression contract.
Depends On: ticket:20260525-compression-contract-inventory

## Summary

Compress `using-loom` and its preload references into the smallest complete session kernel. The closure claim is that a fresh model still receives complete Loom routing, activation, shaping, execution, proof, and safety posture from a smaller startup surface.

## Related Records

- `plan:20260525-loom-protocol-compression` - owns sequencing and validation posture.
- `spec:loom-protocol-compression` - defines compression requirements, especially REQ-001 through REQ-003.
- `constitution:main` - requires operational kernels and portability.
- `roadmap:loom-mill` - names protocol compression as the foundation chapter.
- `spec:ticket-owned-worker-handoffs` - worker handoff behavior that session doctrine must preserve.
- `ticket:20260525-compression-contract-inventory` - provides inventory and baseline.
- `AGENTS.md` - requires preload alignment when `using-loom` doctrine changes.

## Scope

May change `loom-core/skills/using-loom/SKILL.md`, files under `loom-core/skills/using-loom/references/`, and every Core preload surface that embeds or orders using-loom doctrine, including `loom-core/loom-core.mjs`, `loom-core/hooks/*`, and `loom-core/gemini-bootstrap.md` when present.

May update human docs only when they directly restate startup doctrine and would become misleading. Do not compress other record skills, Playbooks, or agent prompts in this ticket except for unavoidable reference updates caused by changed using-loom file names or preload ordering.

First Ralph boundary: inventory the current using-loom preload shape, propose the compressed kernel/reference topology, edit only this slice, then run targeted validation.

Stop if compression would weaken first-action skill activation, active knowledge loading, surface routing, ticket-owned Ralph execution, evidence/audit posture, or safety boundaries.

## Acceptance

- ACC-001: The session kernel preserves mandatory skill activation before clarifying questions, exploration, edits, tickets, Ralph runs, evidence claims, audit claims, and closure.
  - Evidence: Source inspection and targeted grep over compressed `using-loom` and preload surfaces.
  - Audit: Fresh-context final audit should challenge activation loss.

- ACC-002: The compressed startup doctrine still teaches the complete loop: shape, route durable truth, slice to tickets, execute bounded Ralph runs, preserve evidence, audit claims, and reconcile records.
  - Evidence: Source inspection against `spec:loom-protocol-compression#REQ-001` and `REQ-003`.
  - Audit: Fresh-context final audit should test whether a model could still follow the loop.

- ACC-003: All preload surfaces that include using-loom doctrine remain aligned with the compressed file and ordered references.
  - Evidence: Core smoke, Core pack check, and source inspection of preload outputs or source strings.
  - Audit: Review should challenge stale embedded doctrine.

- ACC-004: The ticket records before/after line counts and explains any retained verbosity by behavior requirement or known failure mode.
  - Evidence: Recorded `wc -l` output or evidence record.
  - Audit: Review should challenge false minimalism and unnecessary retained prose.

## Current State

Ready after `ticket:20260525-compression-contract-inventory` closes. The first run should not begin until the inventory and baseline are recorded.

## Journal

- 2026-05-25: Created ticket with dependency on compression contract and inventory.
