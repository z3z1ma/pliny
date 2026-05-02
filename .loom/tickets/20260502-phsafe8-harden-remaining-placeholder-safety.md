---
id: ticket:phsafe8
kind: ticket
status: closed
change_class: record-hygiene
risk_class: medium
created_at: 2026-05-02T22:03:13Z
updated_at: 2026-05-02T23:27:33Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
  plan:
    - plan:skills-corpus-template-grammar-safety-pass
  packet:
    - packet:ralph-ticket-phsafe8-20260502T232054Z
  evidence:
    - evidence:placeholder-safety-validation
  critique:
    - critique:placeholder-safety-review
external_refs: {}
depends_on:
  - ticket:accspec6
  - ticket:sibpkt7
---

# Summary

Harden remaining copyable placeholders and accepted-status defaults that can look
save-ready.

# Context

Council finding `NC-008` found remaining template/example surfaces that may still
save unsafe placeholders or accepted statuses over placeholder content.

# Why Now

Templates should fail closed when copied. Placeholder text should be obviously
unsafe to save as project truth.

# Scope

- Targeted scan of `skills/**/templates` and relevant examples in `skills/**/references`.
- Harden remaining copyable `TBD`, `Replace with`, or accepted-status placeholder
  defaults that can look valid.
- Preserve useful instructional examples.

# Out Of Scope

- Do not rewrite all templates for style.
- Do not remove examples that are clearly non-copyable instruction.

# Acceptance Criteria

- ACC-001: Remaining unsafe placeholders in touched surfaces are fail-closed.
- ACC-002: Accepted/final statuses are not defaulted over placeholder content.
- ACC-003: Template usefulness is preserved.
- ACC-004: Evidence records placeholder/status searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-008`
- `ticket:phsafe8#ACC-001`
- `ticket:phsafe8#ACC-002`
- `ticket:phsafe8#ACC-003`
- `ticket:phsafe8#ACC-004`
- `ticket:phsafe8#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-008` | `evidence:placeholder-safety-validation` | `critique:placeholder-safety-review` | supported |
| `ticket:phsafe8#ACC-001` | `evidence:placeholder-safety-validation` | `critique:placeholder-safety-review` | supported |
| `ticket:phsafe8#ACC-002` | `evidence:placeholder-safety-validation` | `critique:placeholder-safety-review` | supported |
| `ticket:phsafe8#ACC-003` | `evidence:placeholder-safety-validation` | `critique:placeholder-safety-review` | supported |
| `ticket:phsafe8#ACC-004` | `evidence:placeholder-safety-validation` | `critique:placeholder-safety-review` | supported |
| `ticket:phsafe8#ACC-005` | `critique:placeholder-safety-review` | oracle critique passed with no findings | supported |

# Execution Notes

Likely touched surfaces include `skills/loom-wiki/templates/index.md`,
`skills/loom-bootstrap/references/06-filesystem-and-tooling.md`, and
`skills/loom-initiatives/templates/initiative.md`, plus any targeted scan results.

# Blockers

None - dependencies `ticket:accspec6` and `ticket:sibpkt7` are closed.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:critrec9`.

# Route Readiness

Acceptance review readiness:
Evidence `evidence:placeholder-safety-validation` and oracle critique
`critique:placeholder-safety-review` support closure with no findings.

# Evidence

Recorded: `evidence:placeholder-safety-validation` captures before/after searches
for `TBD`, `Replace with`, authoritative placeholder statuses, rationale for
unchanged scanned matches, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: unsafe placeholders can create false project truth.

Required critique profiles:

- template-safety
- records-grammar
- operator-clarity

Findings:

`critique:placeholder-safety-review` - no findings; mandatory oracle critique
passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Placeholder/status safety wording was promoted directly into
  `skills/loom-wiki/templates/index.md`,
  `skills/loom-bootstrap/references/06-filesystem-and-tooling.md`, and
  `skills/loom-initiatives/templates/initiative.md`.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the product guidance itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
touched template/reference guidance.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T23:27:33Z
Basis: Ralph packet `packet:ralph-ticket-phsafe8-20260502T232054Z`; evidence
`evidence:placeholder-safety-validation`; oracle critique
`critique:placeholder-safety-review` with no findings.
Residual risks: validation is structural/manual. Some templates still depend on
operator discipline to replace prompts before saving, intentionally within scope.

# Dependencies

- `ticket:accspec6`
- `ticket:sibpkt7`

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-008`.
- 2026-05-02T23:20:54Z: Confirmed dependencies `ticket:accspec6` and
  `ticket:sibpkt7` are closed, compiled Ralph packet
  `packet:ralph-ticket-phsafe8-20260502T232054Z`, and moved ticket to `active`.
- 2026-05-02T23:22:58Z: Ralph child hardened the scoped placeholder/status
  surfaces, recorded `evidence:placeholder-safety-validation`, and moved the
  ticket to `review_required` for mandatory oracle critique.
- 2026-05-02T23:24:37Z: Parent reconciled Ralph output, marked
  `packet:ralph-ticket-phsafe8-20260502T232054Z` consumed, normalized claim
  statuses, and confirmed the ticket is ready for mandatory oracle critique.
- 2026-05-02T23:27:33Z: Mandatory oracle critique
  `critique:placeholder-safety-review` passed with no findings. Parent recorded
  retrospective / promotion disposition and accepted closure.
