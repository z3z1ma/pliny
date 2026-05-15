# Tighten Loom Driver Orchestration Posture

ID: ticket:20260515-loom-driver-orchestration-tightening
Type: Ticket
Status: closed
Created: 2026-05-15
Updated: 2026-05-15
Risk: high - revises a model-visible agent persona, its behavior spec, and OpenCode permissions after operator review.
Priority: high - corrects the central behavioral frame before the new agent surface is trusted.

## Summary

Tighten Loom Driver so it behaves as an inner-loop coordination lead rather than a direct implementer. Driver should compile packets, coordinate workers, reconcile outputs, preserve evidence, request audit, escalate on authority gaps, and keep progressing through all graph-supported execution work in scope while direction-setting Loom records remain respected inputs.

Single closure claim: the Driver spec, canonical prompt, Codex TOML, docs, and OpenCode permissions all present Driver as a packet-and-worker coordinator with execution-record write scope, high-authority record read-only posture, and completion pressure bounded by the Loom graph.

## Related Records

- `spec:loom-driver-agent` - behavior contract to amend.
- `ticket:20260515-loom-driver-agent` - original Driver implementation ticket and validation story.
- `evidence:20260515-loom-driver-agent-validation` - prior validation baseline.
- `audit:20260515-loom-driver-agent-audit` and `audit:20260515-loom-driver-final-audit` - prior review baseline.
- `loom-core/agents/loom-driver.md` - canonical prompt to revise.
- `loom-core/codex/agents/loom-driver.toml` - Codex copy that must remain aligned.
- `loom-core/loom-core.mjs` - OpenCode agent registration and smoke checks.
- `packet:20260515T062418Z-loom-driver-orchestration-tightening` - implementation packet and worker output for this follow-up.
- `evidence:20260515-loom-driver-orchestration-tightening-validation` - validation observations for amended spec, prompt/TOML parity, permissions, docs, and package checks.
- `packet:20260515T063801Z-loom-driver-orchestration-audit` - fresh Ralph review packet for `ACC-006`.
- `audit:20260515-loom-driver-orchestration-tightening-audit` - fresh clear audit for this follow-up.

## Scope

May change:

- `spec:loom-driver-agent` requirements, scenarios, evidence plan, quality bar, and interface contract for the same product slice.
- `loom-core/agents/loom-driver.md` and `loom-core/codex/agents/loom-driver.toml`.
- `loom-core/loom-core.mjs` Driver permission and smoke-check logic.
- Human-facing docs that describe Driver, if their wording implies direct implementation.
- New validation evidence, audit records, and Ralph packets for this follow-up.

Must not change:

- Do not alter Weaver behavior.
- Do not change harness invocation claims beyond wording needed for Driver's corrected role.
- Do not add runtime infrastructure or helper tooling.
- Do not weaken `using-loom`, ticket, Ralph, evidence, or audit doctrine.
- Do not mutate constitution, plans, or research synthesis for this follow-up.

System-shape constraints:

- The spec remains the behavior source; prompt and TOML carry model-visible runtime behavior.
- OpenCode permissions should reflect Driver's coordination role by limiting direct edits to execution records while allowing worker orchestration.
- Prompt language should be direct and operational, without process commentary, self-justification, or unnecessary contrast framing.

First Ralph packet:

- `packet:20260515T062418Z-loom-driver-orchestration-tightening` should update the spec, prompt, TOML, registration checks, and docs; then produce fresh validation evidence.

## Acceptance

- ACC-001: `spec:loom-driver-agent` describes Driver as an inner-loop coordinator that carries graph-supported work through packets, workers, evidence, audit, and ticket reconciliation until completion, blockage, or escalation.
  - Evidence: source inspection of the spec requirements, scenarios, quality bar, and interface contract.
  - Audit: review should challenge whether the spec still implies direct implementation or insufficient completion pressure.

- ACC-002: The canonical prompt and Codex TOML align with the amended spec, avoid direct implementation framing, and keep high-authority records read-only while execution records remain writable.
  - Evidence: source inspection plus parity check from Core smoke.
  - Audit: review should challenge behavioral disposition, high-authority record handling, and whether the prompt is concise enough to steer real model behavior.

- ACC-003: OpenCode Driver permissions no longer allow direct source editing and instead allow only execution-record updates while preserving worker orchestration ability.
  - Evidence: Core smoke output and source inspection of `loom-core/loom-core.mjs`.
  - Audit: review should challenge permission pattern order and whether checks cover the intended boundary.

- ACC-004: Human-facing docs describe Driver as coordination for packetized execution without implying it edits code itself.
  - Evidence: source inspection of updated docs.
  - Audit: review should challenge docs for drift from prompt behavior or unsupported harness claims.

- ACC-005: Fresh validation passes after the changes.
  - Evidence: `npm --prefix loom-core run smoke`, `npm --prefix loom-core run pack:check`, `git diff --check`, and Claude validation if the manifest is touched.
  - Audit: review should challenge whether validation covers all touched surfaces.

- ACC-006: A fresh Ralph-backed audit challenges this follow-up before closure.
  - Evidence: audit record or packet output covering spec, prompt, TOML, permissions, docs, validation, and product-surface leakage.
  - Audit: this criterion requires separate review before closure.

## Current State

Closed. The amended Driver spec, canonical prompt, Codex TOML, OpenCode permissions, manifests, and docs now present Driver as an inner-loop coordinator for packets, workers, evidence, audit, and ticket reconciliation. `evidence:20260515-loom-driver-orchestration-tightening-validation` supports `ACC-001` through `ACC-005`, and `audit:20260515-loom-driver-orchestration-tightening-audit` satisfies `ACC-006` with a clear verdict and no material findings.

Residual limits remain explicit: live runtime invocation was not tested in OpenCode, Claude Code, Codex, Cursor, or Gemini; OpenCode runtime permission matching was not proven beyond source inspection and smoke output; and non-OpenCode record/source boundaries depend on prompt-level behavior unless a harness enforces equivalent permissions.

## Journal

- 2026-05-15: Created follow-up ticket from operator review. Scope is to tighten Driver's role around packet and worker coordination, record boundaries, graph-supported completion, and escalation on higher-authority ambiguity.
- 2026-05-15: Consumed `packet:20260515T062418Z-loom-driver-orchestration-tightening`; amended the spec, prompt, Codex TOML, OpenCode permissions, and docs. Recorded validation in `evidence:20260515-loom-driver-orchestration-tightening-validation`.
- 2026-05-15: Moved status to review for fresh Ralph-backed audit before closure.
- 2026-05-15: Consumed `packet:20260515T063801Z-loom-driver-orchestration-audit`; recorded `audit:20260515-loom-driver-orchestration-tightening-audit` with clear verdict and no material findings. Closed ticket with runtime-validation residual limits explicit.
