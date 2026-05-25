# Compression Validation And Audit

ID: ticket:20260525-compression-validation-audit
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-25
Risk: medium - validates high-risk protocol compression and may need to route findings back to earlier tickets.
Priority: high - required before claiming compression complete.
Depends On: ticket:20260525-playbook-doc-compression-alignment

## Summary

Validate the completed Loom protocol compression and run fresh-context audit before plan closure. The closure claim is that the compressed protocol is smaller, behavior-preserving, evidence-supported, and audit-reviewed.

## Related Records

- `plan:20260525-loom-protocol-compression` - owns final compression strategy and completion state.
- `spec:loom-protocol-compression` - defines the validation and audit bar.
- `ticket:20260525-compression-contract-inventory` - provides baseline inventory.
- `ticket:20260525-session-kernel-compression` - session kernel slice to validate.
- `ticket:20260525-record-skill-kernels` - record skill slice to validate.
- `ticket:20260525-agent-prompt-kernels` - agent prompt slice to validate.
- `ticket:20260525-playbook-doc-compression-alignment` - Playbook/doc slice to validate.
- `AGENTS.md` - lists repository validation commands and product-surface constraints.

## Scope

May create evidence records under `.loom/evidence/`, audit records under `.loom/audit/`, update this ticket, update child tickets for validation state, and update the plan Current State/Journal. May make small direct fixes only when validation exposes a clear regression within the completed compression scope; otherwise route findings back to the responsible child ticket.

Read scope includes the full diff for the compression plan, all child tickets, related specs/constitution/research, Core/Playbooks package surfaces, and docs/tests that changed.

First Ralph boundary: run final checks, preserve evidence, launch a bounded Ralph audit over the compressed surfaces and evidence, reconcile findings, then update the plan and tickets truthfully.

Stop if audit finds behavior loss, unsupported evidence, product-surface leakage, broken generated surfaces, or missing validation that must be fixed before closure.

## Acceptance

- ACC-001: Required validation commands pass or failures are recorded with truthful blockers.
  - Evidence: Evidence record with Core smoke, Core pack check, Playbooks smoke/pack where touched, `git diff --check`, and targeted searches.
  - Audit: Fresh-context audit should inspect the evidence and its limits.

- ACC-002: Targeted searches/source inspection show compressed surfaces preserve activation, shaping, ticket-owned Ralph, evidence, audit, worker-output reconciliation, portability, and product-surface hygiene.
  - Evidence: Evidence record with search patterns, inspected paths, and limits.
  - Audit: Fresh-context audit should challenge missed behavior loss.

- ACC-003: Fresh-context Ralph audit is recorded and either clear or all findings are routed to responsible tickets before closure.
  - Evidence: Audit record in `.loom/audit/` with target, inspected material, findings, verdict, and required follow-up.
  - Audit: The audit record itself is the review artifact; closure depends on its verdict and follow-up state.

- ACC-004: The plan and child tickets tell one truthful story about what was compressed, what evidence exists, what audit found, and what residual risks remain.
  - Evidence: Updated plan Current State/Journal and child ticket journals.
  - Audit: Audit should challenge closure story consistency.

## Current State

Ready after `ticket:20260525-playbook-doc-compression-alignment` closes. This is the final proof and audit station for the compression plan.

## Journal

- 2026-05-25: Created ticket as final validation and audit slice for protocol compression.
