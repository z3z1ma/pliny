---
id: ticket:minpol10
kind: ticket
status: closed
change_class: record-hygiene
risk_class: low
created_at: 2026-05-03T00:56:36Z
updated_at: 2026-05-03T03:26:21Z
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
external_refs: {}
depends_on: []
---

# Summary

Apply remaining minor template/path polish that affects copyability or operator
clarity.

# Context

Council finding `NC2-007` and older audit action 10 found small polish items:
memory entity headings jump from H1 to H3, skill-root-relative template path
wording can be clearer, and `loom-records` wording should not imply it owns a
record template family when no tracked records templates exist.

Follow-up validation also found the direct critique template's scalar
`review_target` placeholder is unquoted, which is a small copyability hazard in a
frontmatter field that intentionally stays scalar.

# Why Now

These are low-risk, but closing them keeps the corpus crisp after the higher-risk
grammar tickets are done.

# Scope

- Normalize memory entity template headings if still H3 immediately under H1.
- Clarify skill-root-relative template path wording where a current reference can
  mislead readers.
- Clarify `loom-records` wording if it implies records owns templates rather than
  shared grammar for using owner templates.
- Quote or otherwise make the direct critique template's scalar `review_target`
  placeholder copy-safe.
- Verify the older plain `TBD` and drive duplicate-numbering findings remain
  resolved or record why no change is needed.

# Out Of Scope

- Do not shorten activation descriptions.
- Do not rewrite unrelated style.
- Do not create a ticket solely to delete an untracked empty directory.

# Acceptance Criteria

- ACC-001: Memory entity template heading levels are not misleading.
- ACC-002: Template path wording is unambiguous about skill-root-relative or full
  corpus paths where the audit found ambiguity.
- ACC-003: `loom-records` wording does not imply it owns a template family it does
  not ship.
- ACC-004: Direct critique template `review_target` frontmatter remains scalar but
  is copy-safe.
- ACC-005: Evidence records targeted polish searches, including checks for tracked
  records templates, plain copyable `TBD`, duplicate drive read-order numbering,
  critique `review_target`, and `git diff --check`.
- ACC-006: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-012`
- `ticket:minpol10#ACC-001`
- `ticket:minpol10#ACC-002`
- `ticket:minpol10#ACC-003`
- `ticket:minpol10#ACC-004`
- `ticket:minpol10#ACC-005`
- `ticket:minpol10#ACC-006`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-012` | `evidence:minor-template-path-polish-validation` | `critique:minor-template-path-polish-review` | supported |
| `ticket:minpol10#ACC-001` | `evidence:minor-template-path-polish-validation` | `critique:minor-template-path-polish-review` | supported |
| `ticket:minpol10#ACC-002` | `evidence:minor-template-path-polish-validation` | `critique:minor-template-path-polish-review` | supported |
| `ticket:minpol10#ACC-003` | `evidence:minor-template-path-polish-validation` | `critique:minor-template-path-polish-review` | supported |
| `ticket:minpol10#ACC-004` | `evidence:minor-template-path-polish-validation` | `critique:minor-template-path-polish-review` | supported |
| `ticket:minpol10#ACC-005` | `evidence:minor-template-path-polish-validation` | `critique:minor-template-path-polish-review` | supported |
| `ticket:minpol10#ACC-006` | None - critique outcome is the acceptance instrument | `critique:minor-template-path-polish-review` | supported |

# Execution Notes

Likely touched surfaces include `skills/loom-memory/templates/entities.md`,
`skills/loom-wiki/references/page-types.md`, `skills/loom-records/SKILL.md`, and
`skills/loom-critique/templates/critique.md`.

# Blockers

None.

# Next Move / Next Route

Closed. Commit and push this ticket, then reassess plan and initiative closure.

Ralph packet `packet:ralph-ticket-minpol10-20260503T031118Z` was consumed in
scope, evidence was recorded, oracle critique passed after three ticket-record
findings were resolved, and acceptance is complete.

# Route Readiness

Acceptance review readiness:

Evidence `evidence:minor-template-path-polish-validation` and oracle critique
`critique:minor-template-path-polish-review` support closure with all findings
resolved.

# Evidence

Recorded: `evidence:minor-template-path-polish-validation`.

# Critique Disposition

Risk class: low

Critique policy: mandatory

Policy rationale: user instruction requires oracle critique for every ticket;
copyability polish still affects fresh-agent safety.

Required critique profiles:

- template-safety
- operator-clarity

Findings:

- `critique:minor-template-path-polish-review#MINPOL10-ORC-001` - resolved.
  Parent split `ACC-006` out of evidence-supported coverage before final critique.
- `critique:minor-template-path-polish-review#MINPOL10-ORC-002` - resolved.
  Parent replaced stale Ralph route readiness with critique readiness.
- `critique:minor-template-path-polish-review#MINPOL10-ORC-003` - resolved.
  Parent replaced non-canonical bundled claim-matrix rows with per-claim rows and
  canonical status vocabulary.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Minor template/path polish was promoted directly into the owning product
  surfaces: memory entity template headings, wiki atlas page-type guidance,
  `loom-records` owner-template wording, and direct critique template scalar
  `review_target` quoting.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the product guidance itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
updated skill/template guidance.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T03:26:21Z
Basis: Ralph packet `packet:ralph-ticket-minpol10-20260503T031118Z`; evidence
`evidence:minor-template-path-polish-validation`; oracle critique
`critique:minor-template-path-polish-review` with three ticket-record findings
resolved and no unresolved findings.
Residual risks: validation is structural/manual, which is appropriate for this
Markdown-only polish pass; future clarity depends on operators reading the updated
templates and references.

# Dependencies

None.

# Journal

- 2026-05-03T00:56:36Z: Created from council finding `NC2-007` and older audit
  action 10.
- 2026-05-03T03:11:18Z: Started Ralph iteration
  `packet:ralph-ticket-minpol10-20260503T031118Z` from clean `main` at
  `8c93219`.
- 2026-05-03T03:14:13Z: Ralph iteration
  `packet:ralph-ticket-minpol10-20260503T031118Z` completed in scope. Evidence
  recorded in `evidence:minor-template-path-polish-validation`; next route is
  mandatory oracle critique.
- 2026-05-03T03:18:43Z: Initial oracle critique found ticket-record drift in the
  claim matrix and route-readiness section. Parent split `ACC-006` into its own
  critique-pending row and replaced stale Ralph readiness with critique readiness.
- 2026-05-03T03:22:33Z: Follow-up oracle critique confirmed the first two
  findings were resolved and found non-canonical claim-matrix statuses. Parent
  replaced bundled claim rows with per-claim rows using canonical claim coverage
  status vocabulary.
- 2026-05-03T03:26:21Z: Final oracle critique
  `critique:minor-template-path-polish-review` passed with no unresolved findings.
  Parent recorded retrospective / promotion disposition and accepted closure.
