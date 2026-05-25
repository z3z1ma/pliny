# Loom Protocol Compression

ID: plan:20260525-loom-protocol-compression
Type: Plan
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: high - compresses core model-visible doctrine that controls routing, execution, evidence, audit, and future Loom behavior across adapters.

## Summary

This plan decomposes compression of the portable Loom protocol into ticket-ready slices. The outcome is a smaller skill and agent corpus that preserves Loom's behavior as a prose-first software factory protocol while removing repeated explanation, philosophy, and product-surface leakage.

This needs more than one ticket because session preload doctrine, record station skills, agent prompts, Playbook/doc restatements, and final validation have different write boundaries and closure stories.

## Related Records

- `constitution:main` - defines the protocol/Mill split and the principle that skills should be operational kernels.
- `roadmap:loom-mill` - identifies protocol compression as the foundation chapter before Loom Mill.
- `research:20260524-loom-mill-software-factory` - records why the protocol is conceptually correct but too verbose.
- `spec:loom-protocol-compression` - behavior contract this plan implements.
- `spec:ticket-owned-worker-handoffs` - worker handoff behavior that compression must preserve.
- `spec:loom-driver-agent` - Driver prompt behavior that compression must preserve.
- `spec:loom-weaver-agent` - Weaver prompt behavior that compression must preserve.
- `AGENTS.md` - contributor constraints for product-surface leakage and validation commands.

## Strategy

Use a contract-first route. The compression spec is the shared quality bar. First lock the model-visible inventory and baseline so later tickets can prove they compressed the right surfaces. Then compress the session kernel because `using-loom` and its preload references have the largest context impact and drive all later routing. After that, compress the record skills into station kernels, then align Driver/Weaver prompts with Design Office and Factory Floor roles, then align Playbooks and public docs that restate Core behavior.

Validation runs last because it needs the full compressed surface: package smoke/pack checks, Markdown diff checks, targeted behavior/leakage searches, and fresh-context audit. Replan if compression reveals behavior that cannot be safely shortened, if active specs contradict the compression contract, or if adapter preload surfaces cannot stay aligned with the new session kernel.

Compression is behavior-first. Each execution ticket should record before/after line counts, but no ticket should delete a guardrail merely to satisfy a numeric target.

## Execution Units

### Unit: Compression Contract And Inventory

Ticket: ticket:20260525-compression-contract-inventory

Establish the shared compression contract and model-visible inventory. The ticket should confirm `spec:loom-protocol-compression`, capture the baseline size of Core skills, references, agents, Playbooks, generated commands, and docs that expose protocol behavior, and update this plan if the inventory changes the route.

Likely scope boundary: `.loom/specs/loom-protocol-compression.md`, this plan, inventory notes in the ticket or evidence, and read-only inspection of model-visible source surfaces.

Order reason: all later tickets need the same compression quality bar and baseline.

Validation: source inventory, before line counts, targeted surface list, and `git diff --check` for record changes.

Stop condition: return to shaping if the compression contract conflicts with active specs or constitution records.

### Unit: Session Kernel Compression

Ticket: ticket:20260525-session-kernel-compression

Compress `using-loom` and its ordered references into the smallest complete session kernel while preserving activation discipline, loop order, surface ownership, shaping, ticket-owned Ralph handoff, evidence, audit, safety, and active knowledge loading.

Likely scope boundary: `loom-core/skills/using-loom/**`, Core preload surfaces such as `loom-core/loom-core.mjs`, `loom-core/hooks/*`, `loom-core/gemini-bootstrap.md`, and docs only when they directly restate startup doctrine.

Order reason: session doctrine constrains every other skill and adapter preload.

Validation: before/after line counts, source inspection, Core smoke/pack, targeted searches for activation and preload alignment, and `git diff --check`.

Stop condition: block if the session kernel cannot stay complete without retaining a reference topology that needs operator approval.

### Unit: Record Skill Kernels

Ticket: ticket:20260525-record-skill-kernels

Compress Core record skills and references into station kernels while preserving each surface's owner truth, lifecycle, record shape, stop conditions, and evidence/audit posture.

Likely scope boundary: `loom-core/skills/loom-constitution/**`, `loom-core/skills/loom-specs/**`, `loom-core/skills/loom-plans/**`, `loom-core/skills/loom-tickets/**`, `loom-core/skills/loom-research/**`, `loom-core/skills/loom-evidence/**`, `loom-core/skills/loom-audit/**`, `loom-core/skills/loom-knowledge/**`, `loom-core/skills/loom-retrospective/**`, `loom-core/skills/loom-ralph/**`, and templates only when compression requires alignment.

Order reason: depends on the session kernel vocabulary and compression contract.

Validation: before/after line counts, source inspection for required station content, Core smoke/pack, targeted searches for behavior loss and leakage, and `git diff --check`.

Stop condition: split the ticket if one skill family reveals independent behavior changes rather than compression.

### Unit: Agent Prompt Kernels

Ticket: ticket:20260525-agent-prompt-kernels

Compress Driver and Weaver prompts around factory roles: Weaver as Design Office, Driver as Factory Floor coordinator. Remove duplicated skill doctrine while preserving write boundaries, routing, evidence, audit, and worker-output reconciliation.

Likely scope boundary: `loom-core/agents/**`, `loom-core/codex/agents/**`, `.loom/specs/loom-driver-agent.md`, `.loom/specs/loom-weaver-agent.md`, and adapter-facing docs only when they directly restate agent behavior.

Order reason: agent prompts should consume the compressed Core vocabulary rather than define a second protocol.

Validation: before/after line counts, source inspection against agent specs, Core smoke/pack if agent surfaces affect package output, targeted searches for doctrine duplication and leakage, and `git diff --check`.

Stop condition: return to specs if factory-role alignment changes intended Driver or Weaver behavior rather than prompt wording.

### Unit: Playbook And Doc Alignment

Ticket: ticket:20260525-playbook-doc-compression-alignment

Align optional Playbooks, generated command surfaces, and human docs with the compressed Core protocol without making Playbooks a second source of doctrine.

Likely scope boundary: `loom-playbooks/playbooks/**`, `loom-playbooks/commands/*.toml`, `loom-playbooks/loom-playbooks.mjs` only if generation output changes, root/package docs such as `README.md`, `PROTOCOL.md`, `ARCHITECTURE.md`, package READMEs, and tests only when directly tied to exposed protocol language.

Order reason: docs and Playbooks should restate the settled Core compression rather than drive it.

Validation: Playbooks smoke/pack, targeted generated-command comparison, targeted grep for old verbose doctrine and leakage, and `git diff --check`.

Stop condition: block if aligning docs would require changing protocol behavior beyond the compression spec.

### Unit: Validation, Evidence, And Audit

Ticket: ticket:20260525-compression-validation-audit

Run final validation and fresh-context audit over the compressed protocol. Preserve evidence, fix or route findings, update this plan, and move the plan toward completion only when the graph supports the claim.

Likely scope boundary: `.loom/evidence/**`, `.loom/audit/**`, this plan, child ticket state, and small source fixes only if validation exposes direct compression regressions within previous-ticket scope.

Order reason: closure depends on all compression slices being implemented.

Validation: Core smoke, Core pack check, Playbooks smoke/pack where touched, `git diff --check`, targeted behavior/leakage searches, and Ralph-backed audit.

Stop condition: route back to the responsible ticket if audit finds behavior loss, unsupported closure claims, or product-surface leakage.

## Milestones

### Milestone: Compression Contract Ready

Child tickets: ticket:20260525-compression-contract-inventory

The compression spec, inventory, and baseline are available for all downstream tickets.

### Milestone: Core Kernel Compressed

Child tickets: ticket:20260525-session-kernel-compression, ticket:20260525-record-skill-kernels

The Core protocol surfaces are smaller operational kernels and still preserve routing, handoff, evidence, audit, and safety behavior.

### Milestone: Consumer Surfaces Aligned

Child tickets: ticket:20260525-agent-prompt-kernels, ticket:20260525-playbook-doc-compression-alignment

Agent prompts, Playbooks, generated command surfaces, and docs consume the compressed Core protocol without becoming parallel doctrine.

### Milestone: Proof And Review Complete

Child tickets: ticket:20260525-compression-validation-audit

Validation evidence and fresh-context audit support the compression closure claim.

## Current State

Open. The compression contract spec and child tickets have been created. Next move is `ticket:20260525-compression-contract-inventory`, which should confirm the inventory and baseline before source compression begins.

## Journal

- 2026-05-25: Created plan from `constitution:main`, `roadmap:loom-mill`, `research:20260524-loom-mill-software-factory`, and `spec:loom-protocol-compression` with six child execution units.
