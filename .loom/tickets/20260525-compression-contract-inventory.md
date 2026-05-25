# Compression Contract And Inventory

ID: ticket:20260525-compression-contract-inventory
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - establishes the shared contract and baseline that all compression work will rely on.
Priority: high - must happen before source compression tickets.

## Summary

Confirm the Loom protocol compression contract and capture the model-visible surface inventory before editing source doctrine. The closure claim is that downstream compression tickets have a stable behavior contract, a known surface list, and baseline size measurements.

## Related Records

- `plan:20260525-loom-protocol-compression` - owns the decomposition and sequencing.
- `spec:loom-protocol-compression` - defines the compression quality bar.
- `constitution:main` - defines the protocol/Mill split and operational-kernel principle.
- `roadmap:loom-mill` - identifies compression as the current foundation chapter.
- `research:20260524-loom-mill-software-factory` - explains why compression is needed.
- `AGENTS.md` - lists product-surface and validation constraints.

## Scope

May change `.loom/specs/loom-protocol-compression.md`, `plan:20260525-loom-protocol-compression`, and this ticket if inspection shows the contract or plan needs correction. May create evidence for baseline inventory if the observations should survive the session.

Read scope includes `loom-core/skills/**`, `loom-core/agents/**`, `loom-core/codex/agents/**`, `loom-playbooks/playbooks/**`, generated command surfaces, root/package docs, package manifests, tests that validate activation or generated surfaces, and existing Loom records listed above.

Do not compress source surfaces in this ticket. Do not change package behavior. Do not create implementation tickets beyond the plan's child set without returning to planning.

First Ralph boundary: inspect the model-visible surface inventory, compare it to the plan, record baseline line counts and notable risk areas, then update the spec/plan only if needed.

## Acceptance

- ACC-001: `spec:loom-protocol-compression` is present and active, and source inspection finds no contradiction with current constitution, roadmap, or active specs.
  - Evidence: Source inspection notes or evidence record citing the relevant records.
  - Audit: Final compression audit should confirm the contract remained the governing behavior source.

- ACC-002: A baseline inventory exists for model-visible surfaces to be compressed or aligned, including Core skills/references, Core agents, Codex agent copies, Playbooks, generated commands, and relevant docs/tests.
  - Evidence: Recorded command output or evidence record with `wc -l`/surface list observations and limits.
  - Audit: Final compression audit should check that later tickets addressed the inventory or explicitly excluded surfaces.

- ACC-003: The plan and downstream tickets are updated if the inventory reveals missing slices, wrong sequencing, or an unsafe compression boundary.
  - Evidence: Git diff or ticket journal showing either no changes were needed or the plan/tickets were corrected.
  - Audit: Review should challenge whether any important model-visible surface was omitted.

## Current State

Ready to start. The first run should inspect the source inventory and record baseline line counts before any source compression begins.

## Journal

- 2026-05-25: Created ticket from the protocol compression plan. First move is inventory and baseline, not source rewriting.
