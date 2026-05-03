---
id: ticket:wssupp4
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T00:56:36Z
updated_at: 2026-05-03T01:53:08Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
  plan:
    - plan:skills-corpus-residual-protocol-sharpening-pass
  research:
    - research:skills-corpus-residual-audit-synthesis
  packet:
    - packet:ralph-ticket-wssupp4-20260503T014057Z
  evidence:
    - evidence:workspace-support-grammar-validation
  critique:
    - critique:workspace-support-grammar-review
external_refs: {}
depends_on: []
---

# Summary

Complete workspace/support lifecycle and query grammar without making support
surfaces canonical.

# Context

Council finding `NC2-004` and older audit actions 1 and 5 found residual gaps in
workspace/support status and query grammar even though `.loom/support/` framing is
mostly now present.

# Why Now

Workspace and support files help recovery. If lifecycle/query guidance omits them,
fresh agents may treat them as accidental or, conversely, as canonical owner
layers.

# Scope

- Add `kind: workspace` lifecycle guidance.
- Extend query/discovery examples for `.loom/workspace.md`, `.loom/harness.md`,
  and optional `.loom/support/` paths.
- Preserve the noncanonical support boundary for workspace metadata, harness
  records, memory, packets, and support artifacts.

# Out Of Scope

- Do not make `.loom/support/` part of required bootstrap materialization.
- Do not make workspace/harness records own project truth.
- Do not add a validator or schema engine.

# Acceptance Criteria

- ACC-001: Status lifecycle includes `kind: workspace` with clear lifecycle
  values.
- ACC-002: Query/linking guidance discovers workspace, harness, and support paths
  without treating them as canonical owners.
- ACC-003: Naming/path guidance remains consistent with lazy-materialized
  `.loom/support/drive-handoffs/` support.
- ACC-004: Evidence records before/after workspace/support searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-006`
- `ticket:wssupp4#ACC-001`
- `ticket:wssupp4#ACC-002`
- `ticket:wssupp4#ACC-003`
- `ticket:wssupp4#ACC-004`
- `ticket:wssupp4#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-006` | `evidence:workspace-support-grammar-validation` | `critique:workspace-support-grammar-review` | supported |
| `ticket:wssupp4#ACC-001` | `evidence:workspace-support-grammar-validation` | `critique:workspace-support-grammar-review` | supported |
| `ticket:wssupp4#ACC-002` | `evidence:workspace-support-grammar-validation` | `critique:workspace-support-grammar-review#WSSUPP4-ORACLE-001 resolved` | supported |
| `ticket:wssupp4#ACC-003` | `evidence:workspace-support-grammar-validation` | `critique:workspace-support-grammar-review` | supported |
| `ticket:wssupp4#ACC-004` | `evidence:workspace-support-grammar-validation` | `critique:workspace-support-grammar-review` | supported |
| `ticket:wssupp4#ACC-005` | `critique:workspace-support-grammar-review` | oracle critique passed after repair | supported |

# Execution Notes

Implemented grammar changes touch status lifecycle, query/linking, workspace tree,
and status snapshot guidance. Naming/path guidance for lazy
`.loom/support/drive-handoffs/` remained aligned with the existing
`naming-and-ids.md` and `frontmatter.md` support-artifact grammar.

# Blockers

None.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:claimmx5` or
plan updates from the new audit claims.

# Route Readiness

Acceptance review readiness:
Evidence `evidence:workspace-support-grammar-validation` and oracle critique
`critique:workspace-support-grammar-review` support closure with no unresolved
findings.

# Evidence

Recorded: `evidence:workspace-support-grammar-validation` with before/after
searches for `kind: workspace`, `.loom/workspace.md`, `.loom/harness.md`,
`.loom/support`, `drive-handoffs`, `workspace-support`, `support-artifact`,
support/canonical boundary wording, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: workspace/support grammar affects recovery and owner-boundary
safety.

Required critique profiles:

- owner-boundary
- records-grammar
- operator-clarity

Findings:

`critique:workspace-support-grammar-review#WSSUPP4-ORACLE-001` - resolved by
narrowing the support discovery query in `query-and-linking.md`.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Workspace/support lifecycle and query grammar were promoted directly into the
  touched status lifecycle, query/linking, workspace tree, and status snapshot
  guidance.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the product guidance itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
touched workspace/support guidance.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T01:53:08Z
Basis: Ralph packet `packet:ralph-ticket-wssupp4-20260503T014057Z`; evidence
`evidence:workspace-support-grammar-validation`; oracle critique
`critique:workspace-support-grammar-review` with `WSSUPP4-ORACLE-001` resolved.
Residual risks: validation is structural/manual; there is no automated
protocol-template test suite.

# Dependencies

None.

# Journal

- 2026-05-03T00:56:36Z: Created from council finding `NC2-004` and older audit
  actions 1 and 5.
- 2026-05-03T01:40:57Z: Moved to `active` and compiled
  `packet:ralph-ticket-wssupp4-20260503T014057Z` for workspace/support lifecycle
  and query grammar cleanup.
- 2026-05-03T01:42:43Z: Ralph iteration updated workspace/support lifecycle and
  query grammar, recorded `evidence:workspace-support-grammar-validation`, and
  moved the ticket to `review_required` for mandatory oracle critique.
- 2026-05-03T01:45:48Z: Parent reconciled Ralph output, marked
  `packet:ralph-ticket-wssupp4-20260503T014057Z` consumed, and normalized claim
  matrix pending-review statuses to `supported_pending_review` before oracle
  critique.
- 2026-05-03T01:49:55Z: Mandatory oracle critique found low-severity
  `WSSUPP4-ORACLE-001` about noisy support discovery output. Parent repaired the
  query by keeping `^status:` on `.loom/support` only and searching skill
  templates only for support-artifact fields; `git diff --check` passed. Pending
  oracle re-critique.
- 2026-05-03T01:53:08Z: Oracle re-critique passed and marked
  `WSSUPP4-ORACLE-001` resolved. Parent recorded critique disposition,
  retrospective / promotion disposition, and accepted closure.
