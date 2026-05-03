---
id: ticket:critph28
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T06:20:11Z
updated_at: 2026-05-03T08:48:45Z
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
    - research:skills-corpus-third-pass-follow-up-validation
  critique:
    - critique:critique-packet-placeholder-safety-review
external_refs: {}
depends_on:
  - ticket:shipacc1
  - ticket:gitstat26
---

# Summary

Make critique packet placeholders consistently safe and quoted.

# Context

The critique packet template uses quoted `<TBD: ...>` form for many fields but
still has some generic or unquoted placeholder shapes.

# Why Now

Critique packets are copied during high-risk review work and should be YAML-safe
until filled.

# Scope

- Quote remaining copyable placeholder values in critique packet frontmatter.
- Prefer `<TBD: ...>` placeholders with explicit replacement instructions.

# Out Of Scope

- Do not change critique packet semantics.
- Do not add a packet validator.

# Acceptance Criteria

- ACC-001: Critique packet copyable frontmatter placeholders use quoted
  `<TBD: ...>` form consistently where YAML scalar safety matters.
- ACC-002: Template still points to current critique packet grammar.
- ACC-003: No critique packet field becomes fake precision or a required runtime.
- ACC-004: Evidence records targeted critique placeholder searches and
  `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-029`
- `ticket:critph28#ACC-001`
- `ticket:critph28#ACC-002`
- `ticket:critph28#ACC-003`
- `ticket:critph28#ACC-004`
- `ticket:critph28#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-029` | `evidence:critique-packet-placeholder-validation` | `critique:critique-packet-placeholder-safety-review` | supported |
| `ticket:critph28#ACC-001` | `evidence:critique-packet-placeholder-validation` | `critique:critique-packet-placeholder-safety-review` | supported |
| `ticket:critph28#ACC-002` | `evidence:critique-packet-placeholder-validation` | `critique:critique-packet-placeholder-safety-review` | supported |
| `ticket:critph28#ACC-003` | `evidence:critique-packet-placeholder-validation` | `critique:critique-packet-placeholder-safety-review` | supported |
| `ticket:critph28#ACC-004` | `evidence:critique-packet-placeholder-validation` | `critique:critique-packet-placeholder-safety-review` | supported |
| `ticket:critph28#ACC-005` | `evidence:critique-packet-placeholder-validation` | `critique:critique-packet-placeholder-safety-review` | supported |

# Execution Notes

Likely touched file: `skills/loom-critique/templates/critique-packet.md`.

# Blockers

None - prerequisites `ticket:shipacc1` and `ticket:gitstat26` are closed and
pushed.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to the next open ticket.

Ralph packet `packet:ralph-ticket-critph28-20260503T084309Z` completed in scope,
evidence was recorded, mandatory critique passed with no findings, and acceptance
is complete.

# Route Readiness

Ralph readiness:
Bounded iteration: critique packet placeholder quoting.
Write boundary: critique packet template only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, placeholder observations, and critique
recommendation.

Acceptance review readiness:
Evidence `evidence:critique-packet-placeholder-validation` and mandatory critique
`critique:critique-packet-placeholder-safety-review` support closure.

# Evidence

Expected: targeted searches for unquoted placeholders, `<TBD:`, critique packet
frontmatter, and `git diff --check`.

Recorded:

- `evidence:critique-packet-placeholder-validation`

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: critique packet templates are high-copy review surfaces.

Required critique profiles:

- template-safety
- packet-safety
- operator-clarity

Findings:

`critique:critique-packet-placeholder-safety-review`: no findings; mandatory
critique passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Critique packet placeholder safety guidance was promoted into
  `skills/loom-critique/templates/critique-packet.md`.

Deferred / not-required rationale:

No separate wiki, research, spec, constitution, or memory record is needed. The
durable operator guidance belongs in the critique packet template itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted guidance lives in the
critique packet template.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T08:48:45Z
Basis: Ralph packet `packet:ralph-ticket-critph28-20260503T084309Z`; evidence
`evidence:critique-packet-placeholder-validation`; mandatory critique
`critique:critique-packet-placeholder-safety-review` with no findings.
Residual risks: Copied packets still depend on operators replacing `<TBD: ...>`
placeholders before use; accepted because this ticket explicitly avoids adding a
parser-backed validator.

# Dependencies

- `ticket:shipacc1`
- `ticket:gitstat26`

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass secondary polish finding.
- 2026-05-03T08:43:09Z: Parent confirmed prerequisites are closed and pushed,
  moved this ticket to active, and compiled Ralph iteration 1.
- 2026-05-03T08:45:34Z: Ralph child returned `stop`; parent accepted the scoped
  implementation output, recorded evidence, consumed the packet, and moved to
  mandatory critique.
- 2026-05-03T08:48:45Z: Mandatory critique
  `critique:critique-packet-placeholder-safety-review` passed with no findings.
  Parent recorded retrospective / promotion disposition and accepted closure.
