---
id: ticket:pktgram5
kind: ticket
status: closed
change_class: protocol-authority
risk_class: high
created_at: 2026-05-02T18:58:43Z
updated_at: 2026-05-02T20:08:37Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
  packet:
    - packet:ralph-ticket-pktgram5-20260502T195332Z
    - packet:ralph-ticket-pktgram5-20260502T200144Z
  evidence:
    - evidence:packet-grammar-template-alignment-validation
  critique:
    - critique:packet-grammar-template-alignment-review
    - critique:packet-grammar-template-alignment-rereview
external_refs: {}
depends_on:
  - ticket:rtvocab1
---

# Summary

Align shared packet frontmatter grammar and Ralph/critique/wiki packet templates.

# Context

Council finding `CR-005` found drift around `context_budget.posture`, `iteration`,
`change_class`, optional `risk_class`, source freshness checks, and packet ID vs
filename mapping.

# Why Now

Packet templates are operational teaching surfaces. They need to embody shared
grammar before lifecycle parity and critique target cleanup proceed.

# Scope

- Align `skills/loom-records/references/packet-frontmatter.md` with Ralph,
  critique, and wiki packet templates.
- Clarify `iteration`, `change_class`, optional `risk_class`, ID/filename mapping,
  context budget defaults, and freshness stop conditions.
- Preserve distinction between Ralph implementation packets and critique/wiki
  sibling packet workflows.

# Out Of Scope

- Do not make critique/wiki packets Ralph-governed.
- Do not add a packet parser or schema runtime.
- Do not normalize historical packets unless needed for current references.

# Acceptance Criteria

- ACC-001: Packet frontmatter reference and packet templates agree on required
  and optional fields.
- ACC-002: Packet ID and filename conventions are explicit.
- ACC-003: `change_class`, optional `risk_class`, `iteration`, context budget, and
  source freshness expectations are documented or removed consistently.
- ACC-004: Evidence records packet-template comparison and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-005` | `evidence:packet-grammar-template-alignment-validation` | `critique:packet-grammar-template-alignment-rereview` | supported |
| `ticket:pktgram5#ACC-001` | `evidence:packet-grammar-template-alignment-validation` | `critique:packet-grammar-template-alignment-rereview` | supported |
| `ticket:pktgram5#ACC-002` | `evidence:packet-grammar-template-alignment-validation` | `critique:packet-grammar-template-alignment-review#PKTGRAM5-CRIT-001` and `critique:packet-grammar-template-alignment-review#PKTGRAM5-CRIT-002` resolved by `critique:packet-grammar-template-alignment-rereview` | supported |
| `ticket:pktgram5#ACC-003` | `evidence:packet-grammar-template-alignment-validation` | `critique:packet-grammar-template-alignment-review#PKTGRAM5-CRIT-002` resolved by `critique:packet-grammar-template-alignment-rereview` | supported |
| `ticket:pktgram5#ACC-004` | `evidence:packet-grammar-template-alignment-validation` | `critique:packet-grammar-template-alignment-rereview` | supported |
| `ticket:pktgram5#ACC-005` | `critique:packet-grammar-template-alignment-rereview` | oracle re-critique passed with no new findings | supported |

# Execution Notes

Likely touched surfaces include `skills/loom-records/references/packet-frontmatter.md`,
`skills/loom-ralph/templates/ralph-packet.md`, `skills/loom-critique/templates/critique-packet.md`,
and `skills/loom-wiki/templates/wiki-packet.md`.

# Blockers

None - `ticket:rtvocab1` is closed.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:pktlife6`.

# Route Readiness

Route: acceptance_review

Acceptance review readiness:
Evidence, repair, and re-critique disposition:
`evidence:packet-grammar-template-alignment-validation`,
`critique:packet-grammar-template-alignment-review`, and
`critique:packet-grammar-template-alignment-rereview` support acceptance with no
remaining findings.
Residual risks: evidence is structural, which is appropriate for Markdown
protocol guidance; historical packets were not normalized by scope.

# Evidence

Recorded: `evidence:packet-grammar-template-alignment-validation` with targeted
packet-field searches, template/reference comparison, and `git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: packet grammar governs bounded child authority.

Required critique profiles:

- protocol-change
- records-grammar
- routing-safety

Findings:

Recorded in `critique:packet-grammar-template-alignment-review`:

- `PKTGRAM5-CRIT-001` medium: dogfood-specific `ticket:pktgram5` examples leaked
  into product guidance.
- `PKTGRAM5-CRIT-002` medium: critique packet naming wording conflated packet
  target with structured `review_target`.

Ticket-owned finding dispositions:

- `critique:packet-grammar-template-alignment-review#PKTGRAM5-CRIT-001`:
  resolved by `packet:ralph-ticket-pktgram5-20260502T200144Z`,
  `evidence:packet-grammar-template-alignment-validation`, and
  `critique:packet-grammar-template-alignment-rereview`.
- `critique:packet-grammar-template-alignment-review#PKTGRAM5-CRIT-002`:
  resolved by `packet:ralph-ticket-pktgram5-20260502T200144Z`,
  `evidence:packet-grammar-template-alignment-validation`, and
  `critique:packet-grammar-template-alignment-rereview`.

Re-critique:

- `critique:packet-grammar-template-alignment-rereview` passed with no new findings.

Disposition status: completed

Deferral / not-required rationale:

Not deferred. Mandatory oracle re-critique passed with no remaining findings.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Packet grammar guidance was promoted into
  `skills/loom-records/references/packet-frontmatter.md`,
  `skills/loom-records/references/naming-and-ids.md`,
  `skills/loom-ralph/templates/ralph-packet.md`,
  `skills/loom-ralph/references/packet-contract.md`,
  `skills/loom-critique/templates/critique-packet.md`, and
  `skills/loom-wiki/templates/wiki-packet.md`.

Deferred / not-required rationale:

Not deferred. The durable lesson was promoted directly into the owner product
surfaces listed above; no separate wiki page, research record, spec,
constitution decision, or memory entry is needed.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation is now in the
packet grammar and template owner surfaces.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T20:08:37Z
Basis: Ralph packets `packet:ralph-ticket-pktgram5-20260502T195332Z` and
`packet:ralph-ticket-pktgram5-20260502T200144Z`; evidence
`evidence:packet-grammar-template-alignment-validation`; oracle critiques
`critique:packet-grammar-template-alignment-review` and
`critique:packet-grammar-template-alignment-rereview` with prior findings resolved
and no new findings.
Residual risks: evidence is structural, which is appropriate for Markdown
protocol guidance; historical packets were not normalized by scope.

# Dependencies

- `ticket:rtvocab1`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-005`.
- 2026-05-02T19:53:33Z: Started Ralph iteration
  `packet:ralph-ticket-pktgram5-20260502T195332Z` from baseline
  `cceb6422bf5c95cfaf2c45983bb6a412c748c94f`.
- 2026-05-02T19:56:36Z: Ralph implementation updated packet grammar references
  and templates, recorded `evidence:packet-grammar-template-alignment-validation`,
  and moved ticket to `review_required` for mandatory critique.
- 2026-05-02T20:01:44Z: Oracle critique found two medium issues. Recorded
  `critique:packet-grammar-template-alignment-review` and started repair packet
  `packet:ralph-ticket-pktgram5-20260502T200144Z`.
- 2026-05-02T20:05:16Z: Repair iteration 2 replaced product-surface
  `ticket:pktgram5` examples with neutral examples, clarified critique packet
  target/change-slug naming versus structured `review_target`, and moved the
  ticket to `review_required` for oracle re-critique. Finding dispositions remain
  pending parent/oracle rerun.
- 2026-05-02T20:08:37Z: Oracle re-critique passed with prior findings resolved
  and no new findings. Recorded acceptance and retrospective / promotion
  disposition; closed ticket.
