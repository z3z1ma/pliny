---
id: ticket:bootinv1
kind: ticket
status: closed
change_class: protocol-authority
risk_class: high
created_at: 2026-05-03T04:09:51Z
updated_at: 2026-05-03T04:19:29Z
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
depends_on: []
---

# Summary

Add minimal first-contact bootstrap orientation for how a fresh model should see
Loom.

# Context

Council found that README's core orientation is stronger than the loaded
bootstrap surface. User specifically warned that bootstrap is the first thing a
model sees and must not leak internal framing.

# Why Now

Bootstrap doctrine governs every downstream workflow and should carry the minimal
worldview needed for placement, owner truth, and recoverable sessions.

# Scope

- Update `skills/loom-bootstrap/references/01-core-identity.md` only if possible.
- Add concise operational orientation: placement beats recency, the graph carries
  durable truth, sessions/workers are disposable, and records/packets/evidence /
  critique/reconciliation are the recovery path.
- Keep wording generic and immediately actionable for a never-seen-Loom model.

# Out Of Scope

- Do not add marketing, internal product positioning, viral framing, or external
  article references.
- Do not change the layer model.
- Do not add new bootstrap references unless critique requires it.

# Acceptance Criteria

- ACC-001: Bootstrap contains minimal first-contact orientation for Loom's
  worldview without relying on README.
- ACC-002: The new text is operational doctrine, not marketing or internal framing.
- ACC-003: Existing owner-layer, ticket-ledger, packet, evidence, critique, and
  wiki boundaries remain unchanged.
- ACC-004: Evidence records targeted bootstrap wording checks and `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-001`
- `ticket:bootinv1#ACC-001`
- `ticket:bootinv1#ACC-002`
- `ticket:bootinv1#ACC-003`
- `ticket:bootinv1#ACC-004`
- `ticket:bootinv1#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-001` | `evidence:bootstrap-invariant-validation` | `critique:bootstrap-invariant-review` | supported |
| `ticket:bootinv1#ACC-001` | `evidence:bootstrap-invariant-validation` | `critique:bootstrap-invariant-review` | supported |
| `ticket:bootinv1#ACC-002` | `evidence:bootstrap-invariant-validation` | `critique:bootstrap-invariant-review` | supported |
| `ticket:bootinv1#ACC-003` | `evidence:bootstrap-invariant-validation` | `critique:bootstrap-invariant-review` | supported |
| `ticket:bootinv1#ACC-004` | `evidence:bootstrap-invariant-validation` | `critique:bootstrap-invariant-review` | supported |
| `ticket:bootinv1#ACC-005` | None - critique outcome is the acceptance instrument | `critique:bootstrap-invariant-review` | supported |

# Execution Notes

Likely touched file: `skills/loom-bootstrap/references/01-core-identity.md`.

# Blockers

None.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:trustbd2`.

Ralph packet `packet:ralph-ticket-bootinv1-20260503T041454Z` was consumed in
scope, evidence was recorded, mandatory critique passed with no findings, and
acceptance is complete.

# Route Readiness

Acceptance review readiness:
Evidence `evidence:bootstrap-invariant-validation` and mandatory critique
`critique:bootstrap-invariant-review` support closure with no findings.

# Evidence

Recorded: `evidence:bootstrap-invariant-validation`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: bootstrap authority affects every future Loom activation.

Required critique profiles:

- protocol-change
- operator-clarity
- owner-boundary

Findings:

`critique:bootstrap-invariant-review` - no findings; mandatory critique passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Minimal first-contact orientation was promoted directly into
  `skills/loom-bootstrap/references/01-core-identity.md`.

Deferred / not-required rationale:

No separate wiki, research, spec, constitution decision, or memory record is
needed. The durable lesson is the bootstrap doctrine itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
bootstrap reference.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T04:19:29Z
Basis: Ralph packet `packet:ralph-ticket-bootinv1-20260503T041454Z`; evidence
`evidence:bootstrap-invariant-validation`; mandatory critique
`critique:bootstrap-invariant-review` with no findings.
Residual risks: The new invariant is slightly repetitive with later recovery
wording, but critique accepted that as appropriate for first-contact doctrine.

# Dependencies

None.

# Journal

- 2026-05-03T04:09:51Z: Created from council finding to promote core orientation
  into bootstrap, constrained by user warning to avoid internal framing.
- 2026-05-03T04:14:54Z: Started Ralph iteration
  `packet:ralph-ticket-bootinv1-20260503T041454Z` from clean `main` at
  `1d8ad24`.
- 2026-05-03T04:16:21Z: Ralph iteration
  `packet:ralph-ticket-bootinv1-20260503T041454Z` completed in scope. Evidence
  recorded in `evidence:bootstrap-invariant-validation`; next route is mandatory
  critique.
- 2026-05-03T04:19:29Z: Mandatory critique
  `critique:bootstrap-invariant-review` passed with no findings. Parent recorded
  retrospective / promotion disposition and accepted closure.
