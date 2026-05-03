---
id: ticket:minpol10
kind: ticket
status: ready
change_class: record-hygiene
risk_class: low
created_at: 2026-05-03T00:56:36Z
updated_at: 2026-05-03T00:56:36Z
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

# Why Now

These are low-risk, but closing them keeps the corpus crisp after the higher-risk
grammar tickets are done.

# Scope

- Normalize memory entity template headings if still H3 immediately under H1.
- Clarify skill-root-relative template path wording where a current reference can
  mislead readers.
- Clarify `loom-records` wording if it implies records owns templates rather than
  shared grammar for using owner templates.
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
- ACC-004: Evidence records targeted polish searches, including checks for tracked
  records templates, plain copyable `TBD`, duplicate drive read-order numbering,
  and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-012`
- `ticket:minpol10#ACC-001`
- `ticket:minpol10#ACC-002`
- `ticket:minpol10#ACC-003`
- `ticket:minpol10#ACC-004`
- `ticket:minpol10#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-012` | pending | pending | open |
| `ticket:minpol10#ACC-001` through `ticket:minpol10#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-memory/templates/entities.md`,
`skills/loom-wiki/references/page-types.md`, and `skills/loom-records/SKILL.md`.

# Blockers

None.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Route: ralph

Bounded iteration: minor template/path polish.
Write boundary: the targeted minor polish files, this ticket, one evidence record,
one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for memory entity headings, template path wording,
tracked records templates, plain `TBD`, drive read-order numbering, and
`git diff --check`.

# Critique Disposition

Risk class: low

Critique policy: mandatory

Policy rationale: user instruction requires oracle critique for every ticket;
copyability polish still affects fresh-agent safety.

Required critique profiles:

- template-safety
- operator-clarity

Findings:

None - no critique yet.

Disposition status: pending

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Pending after critique.

# Wiki Disposition

Pending retrospective decision after critique.

# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:

# Dependencies

None.

# Journal

- 2026-05-03T00:56:36Z: Created from council finding `NC2-007` and older audit
  action 10.
