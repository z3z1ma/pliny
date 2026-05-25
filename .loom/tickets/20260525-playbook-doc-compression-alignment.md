# Playbook And Doc Compression Alignment

ID: ticket:20260525-playbook-doc-compression-alignment
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - aligns optional Playbook and documentation surfaces with compressed Core protocol without changing Core behavior.
Priority: medium - prevents drift after Core and agent compression.
Depends On: ticket:20260525-agent-prompt-kernels

## Summary

Align Playbooks, generated command surfaces, and human docs with the compressed Loom protocol. The closure claim is that non-Core surfaces restate the protocol succinctly without becoming a second source of doctrine.

## Related Records

- `plan:20260525-loom-protocol-compression` - owns sequencing and validation posture.
- `spec:loom-protocol-compression` - defines portability, product-surface hygiene, and validation requirements.
- `spec:playbook-explicit-macros` - owns Playbook invocation behavior.
- `ticket:20260525-agent-prompt-kernels` - provides settled Core/agent compression for downstream restatements.
- `AGENTS.md` - lists package docs, product-surface leakage, and validation constraints.
- `knowledge:playbook-activation-tests-procedure` - preserves Playbook activation validation limits and expectations.

## Scope

May change `loom-playbooks/playbooks/**`, `loom-playbooks/commands/*.toml`, `loom-playbooks/loom-playbooks.mjs` only if generated command output needs regeneration/alignment, root/package docs such as `README.md`, `PROTOCOL.md`, `ARCHITECTURE.md`, package READMEs, and tests that directly validate command generation or activation behavior.

Do not change Core skills or agent prompts except for direct fixes discovered by validation that should be routed back to earlier tickets. Do not introduce Loom Mill implementation documentation into model-visible product doctrine.

First Ralph boundary: inspect Playbook and doc references to Core protocol language, shorten repeated doctrine, regenerate/check command surfaces if needed, and validate no Playbook becomes ambient model pressure.

Stop if alignment requires changing Playbook behavior beyond `spec:playbook-explicit-macros` or Core compression behavior.

## Acceptance

- ACC-001: Playbook macro/source language preserves Core routing, evidence, audit, ticket, and ticket-owned Ralph discipline without repeating full Core doctrine.
  - Evidence: Source inspection against `spec:playbook-explicit-macros` and compressed Core surfaces.
  - Audit: Final audit should challenge Playbook drift or bypass behavior.

- ACC-002: Generated command surfaces are aligned with Playbook source when generation output is affected.
  - Evidence: Playbooks smoke/pack and targeted source/generated comparison.
  - Audit: Review should challenge stale generated files.

- ACC-003: Human docs restate the compressed protocol succinctly and do not become a second source of model doctrine.
  - Evidence: Source inspection of touched docs and targeted grep for stale verbose doctrine or product-surface leakage.
  - Audit: Final audit should inspect doc drift and leakage search limits.

- ACC-004: Playbook activation behavior remains explicit-only where required.
  - Evidence: Existing activation tests or targeted checks following `knowledge:playbook-activation-tests-procedure` when touched.
  - Audit: Review should challenge false-positive test gaps.

- ACC-005: Relevant validation passes.
  - Evidence: `npm --prefix loom-playbooks run smoke`, `npm --prefix loom-playbooks run pack:check`, relevant Core checks if Core is touched, and `git diff --check` outputs recorded or cited.
  - Audit: Final audit should inspect evidence sufficiency.

## Current State

Ready after `ticket:20260525-agent-prompt-kernels` closes. The first run should treat Playbooks and docs as consumers of Core compression, not drivers of protocol changes.

## Journal

- 2026-05-25: Created ticket with dependency on agent prompt compression.
