---
id: ticket:tplsave3
kind: ticket
status: closed
change_class: template-safety
risk_class: medium
created_at: 2026-05-03T04:09:51Z
updated_at: 2026-05-03T05:08:33Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-context-integrity-hardening-pass
  plan:
    - plan:skills-corpus-context-integrity-hardening-pass
  research:
    - research:skills-corpus-context-integrity-hardening-review
external_refs: {}
depends_on:
  - ticket:vocabx08
---

# Summary

Add save-ready pruning rules to copy-heavy ticket and plan templates.

# Context

Council found large templates can teach agents to preserve unused branches,
placeholder text, and ceremony.

# Why Now

Templates are copied into real records. They must make the saved-record shape
explicit enough to avoid Markdown junk drawers.

# Scope

- Add concise save-ready instructions to ticket and plan templates.
- Preserve acceptance, evidence, critique, and closure gates.
- Update related references only if needed for consistency.

# Out Of Scope

- Do not create template generators, schemas, or separate canonical minimal/full
  template families.
- Do not remove required acceptance or critique guidance.

# Acceptance Criteria

- ACC-001: Ticket template tells agents to remove unused readiness branches and
  replace placeholders before saving.
- ACC-002: Plan template tells agents to remove unused wave examples/placeholders
  or replace them with meaningful `None - reason`.
- ACC-003: The rules preserve evidence, critique, acceptance, and retrospective
  closure gates.
- ACC-004: Evidence records targeted placeholder/template checks and
  `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-004`
- `ticket:tplsave3#ACC-001`
- `ticket:tplsave3#ACC-002`
- `ticket:tplsave3#ACC-003`
- `ticket:tplsave3#ACC-004`
- `ticket:tplsave3#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-004` | `evidence:template-save-ready-validation` | `critique:template-save-ready-review` | supported |
| `ticket:tplsave3#ACC-001` | `evidence:template-save-ready-validation` | `critique:template-save-ready-review` | supported |
| `ticket:tplsave3#ACC-002` | `evidence:template-save-ready-validation` | `critique:template-save-ready-review` | supported |
| `ticket:tplsave3#ACC-003` | `evidence:template-save-ready-validation` | `critique:template-save-ready-review` | supported |
| `ticket:tplsave3#ACC-004` | `evidence:template-save-ready-validation` | `critique:template-save-ready-review` | supported |
| `ticket:tplsave3#ACC-005` | None - critique outcome is the acceptance instrument | `critique:template-save-ready-review` | supported |

# Execution Notes

Likely touched files: `skills/loom-tickets/templates/ticket.md` and
`skills/loom-plans/templates/plan.md`.

# Blockers

None.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:pktfam04`.

Ralph packet `packet:ralph-ticket-tplsave3-20260503T050338Z` was consumed in
scope, evidence was recorded, mandatory critique passed with no findings, and
acceptance is complete.

# Route Readiness

Acceptance review readiness:
Evidence `evidence:template-save-ready-validation` and mandatory critique
`critique:template-save-ready-review` support closure with no findings.

# Evidence

Recorded: `evidence:template-save-ready-validation`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: templates directly shape future saved records.

Required critique profiles:

- template-safety
- closure-honesty
- operator-clarity

Findings:

`critique:template-save-ready-review` - no findings; mandatory critique passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Save-ready placeholder and unused-branch pruning guidance was promoted directly
  into `skills/loom-tickets/templates/ticket.md`.
- Wave/placeholder pruning guidance was promoted directly into
  `skills/loom-plans/templates/plan.md`.

Deferred / not-required rationale:

No separate wiki, research, spec, constitution, or memory record is needed. The
durable lesson is template-local authoring guidance.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
templates.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T05:08:33Z
Basis: Ralph packet `packet:ralph-ticket-tplsave3-20260503T050338Z`; evidence
`evidence:template-save-ready-validation`; mandatory critique
`critique:template-save-ready-review` with no findings.
Residual risks: Existing route-readiness guidance still permits marking unrelated
route sections `N/A`; later template tightening may prefer removal-only wording,
but critique found the current save-ready rule clear enough for this ticket.

# Dependencies

- `ticket:vocabx08`

# Journal

- 2026-05-03T04:09:51Z: Created from council template right-sizing finding.
- 2026-05-03T05:03:38Z: Started Ralph iteration
  `packet:ralph-ticket-tplsave3-20260503T050338Z` from clean `main` at
  `e5abe40`.
- 2026-05-03T05:05:24Z: Ralph iteration
  `packet:ralph-ticket-tplsave3-20260503T050338Z` completed in scope. Evidence
  recorded in `evidence:template-save-ready-validation`; next route is mandatory
  critique.
- 2026-05-03T05:08:33Z: Mandatory critique
  `critique:template-save-ready-review` passed with no findings. Parent recorded
  retrospective / promotion disposition and accepted closure.
