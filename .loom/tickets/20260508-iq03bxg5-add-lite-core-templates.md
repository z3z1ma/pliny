---
id: ticket:iq03bxg5
kind: ticket
status: closed
change_class: protocol-authority
risk_class: high
created_at: 2026-05-08T07:41:56Z
updated_at: 2026-05-08T07:56:34Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
  plan:
    - plan:point-of-use-ergonomics-and-mechanical-simplicity
  evidence:
    - evidence:lite-core-templates-check
  critique:
    - critique:lite-core-templates-review
external_refs: {}
depends_on: []
---

# Summary

Add lite ticket, spec, and evidence templates to `loom-core` while preserving the
existing generic templates as the full copy targets.

# Context

This implements the first point-of-use ergonomics slice from
`spec:point-of-use-ergonomics-and-mechanical-simplicity` and
`plan:point-of-use-ergonomics-and-mechanical-simplicity`.

# Scope

In:

- Add `loom-core/skills/loom-tickets/templates/ticket-lite.md`.
- Add `loom-core/skills/loom-specs/templates/spec-lite.md`.
- Add `loom-core/skills/loom-evidence/templates/evidence-lite.md`.
- Preserve `ticket.md`, `spec.md`, and `evidence.md` as full copy targets.
- Update the owning skill guidance so agents know when to use lite versus full.
- Teach full-template escalation triggers from the governing spec.

Out:

- No `ticket-full.md`, `spec-full.md`, or `evidence-full.md` unless the spec is
  amended.
- No `using-loom` compression.
- No table-removal sweep beyond files directly touched for template guidance.
- No package-script enforcement.

Assumptions / decision triggers:

- Generic full templates remain the compatibility path.
- Lite templates still include YAML frontmatter.
- If implementation reveals a lite template cannot stay truthful with the agreed
  body shape, loop back to the spec before widening scope.

# Acceptance

Owner: spec-owned.

Covered IDs:

- `spec:point-of-use-ergonomics-and-mechanical-simplicity#ACC-001`
- `spec:point-of-use-ergonomics-and-mechanical-simplicity#ACC-002`
- `spec:point-of-use-ergonomics-and-mechanical-simplicity#ACC-003`

Ticket-local criteria:

- ACC-LOCAL-001: `ticket-lite.md` uses `Summary`, `Scope`, `Acceptance`,
  `Evidence`, `Status / Next Move`, and `Journal` after frontmatter.
- ACC-LOCAL-002: `spec-lite.md` uses the behavior-compact section shape recorded
  in the spec.
- ACC-LOCAL-003: `evidence-lite.md` uses the observation-compact section shape
  recorded in the spec.

# Current State

Status rationale: closed; implementation, structural evidence, mandatory
critique, and ticket acceptance are complete for this slice.

Blockers: None.

Execution notes: Packet `packet:ralph:20260508T074551Z-ticket-iq03bxg5-iter-01`
added the three lite templates and updated owning skill guidance. Parent adjusted
the ticket creation snippet to keep `ticket.md` as the default full copy target
unless `ticket-lite.md` is explicitly chosen.

Continuation note: Implement the templates and guidance only within the scoped
core skill surfaces, then record template inventory and frontmatter evidence.

# Evidence

Disposition: sufficient.

Records:

- `evidence:lite-core-templates-check` — supports `ACC-001`, `ACC-002`,
  `ACC-003`, and ticket-local lite section-shape criteria.

Gaps / limits: Evidence is structural and does not replace mandatory critique.

# Review And Follow-Through

Critique policy: mandatory.
Critique rationale: core template behavior changes point-of-use record creation
and escalation guidance.
Critique disposition: completed.

Required critique profiles:

- protocol-authority
- records-grammar
- operator-ergonomics

Findings:

- None - `critique:lite-core-templates-review` returned `pass` with no findings.

Promotion disposition: not_required.
Promotion / deferral rationale: durable behavior is captured in the spec, ticket,
templates, owning skill guidance, evidence, and critique. No separate wiki
promotion is needed for this bounded template slice.

Promoted / deferred:

- None - not required for this bounded product-surface slice.

Wiki disposition: not_required - no accepted explanation beyond product-surface
guidance is needed for this slice.

# Acceptance Decision

Accepted by: OpenCode agent per user-delegated implementation authority.
Accepted at: 2026-05-08T07:56:34Z
Basis: `evidence:lite-core-templates-check` supports the template inventory,
frontmatter, heading, guidance, generic-full preservation, and smoke-check claims;
`critique:lite-core-templates-review` returned `pass` with no findings.
Residual risks: No real-world usability trial of agents creating records from the
lite templates has occurred; misuse remains possible if operators copy lite
templates without reading owning skill guidance.

# Dependencies

None.

# Journal

- 2026-05-08T07:41:56Z: Created as a ready execution ticket from the active spec
  and plan.
- 2026-05-08T07:45:51Z: Moved to active and compiled Ralph packet
  `packet:ralph:20260508T074551Z-ticket-iq03bxg5-iter-01`.
- 2026-05-08T07:50:31Z: Ralph child returned `stop`; parent verified the scoped
  product diff, corrected the ticket creation snippet to keep full generic
  default behavior, recorded `evidence:lite-core-templates-check`, and moved the
  ticket to `review_required` for mandatory critique.
- 2026-05-08T07:56:34Z: Recorded `critique:lite-core-templates-review` with
  verdict `pass` and no findings, marked promotion/wiki follow-through not
  required, accepted the ticket, and closed it.
