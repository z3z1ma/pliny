---
id: ticket:pktlife6
kind: ticket
status: closed
change_class: protocol-authority
risk_class: high
created_at: 2026-05-02T18:58:43Z
updated_at: 2026-05-02T20:16:28Z
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
    - packet:ralph-ticket-pktlife6-20260502T201044Z
  evidence:
    - evidence:packet-lifecycle-parity-validation
  critique:
    - critique:packet-lifecycle-parity-review
external_refs: {}
depends_on:
  - ticket:pktgram5
---

# Summary

Strengthen critique/wiki packet lifecycle and parent merge reconciliation parity
with Ralph packet discipline.

# Context

Council finding `CR-006` found critique/wiki packet templates can leave
`parent_merge_scope` empty and do not strongly require status movement from
`compiled` after reconciliation.

# Why Now

Packet output must be reconciled into owner truth rather than left in support
artifacts.

# Scope

- Require explicit critique/wiki packet merge targets or `None - rationale`.
- Add Done Means guidance for packet status movement to terminal states.
- Align critique/wiki packet templates with shared packet lifecycle grammar.

# Out Of Scope

- Do not make critique/wiki packets Ralph packets.
- Do not require packetization for every critique or wiki pass.
- Do not change canonical critique/wiki ownership.

# Acceptance Criteria

- ACC-001: Critique/wiki packet templates require parent merge targets or explicit
  rationale.
- ACC-002: Critique/wiki packet guidance requires terminal lifecycle status after
  reconciliation.
- ACC-003: Domain skills explain parent merge notes and owner-layer reconciliation.
- ACC-004: Evidence records lifecycle/template searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-006`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-006` | `evidence:packet-lifecycle-parity-validation` | `critique:packet-lifecycle-parity-review` | supported |
| `ticket:pktlife6#ACC-001` | `evidence:packet-lifecycle-parity-validation` | `critique:packet-lifecycle-parity-review` | supported |
| `ticket:pktlife6#ACC-002` | `evidence:packet-lifecycle-parity-validation` | `critique:packet-lifecycle-parity-review` | supported |
| `ticket:pktlife6#ACC-003` | `evidence:packet-lifecycle-parity-validation` | `critique:packet-lifecycle-parity-review` | supported |
| `ticket:pktlife6#ACC-004` | `evidence:packet-lifecycle-parity-validation` | `critique:packet-lifecycle-parity-review` | supported |
| `ticket:pktlife6#ACC-005` | `critique:packet-lifecycle-parity-review` | oracle critique passed with no findings | supported |

# Execution Notes

Likely touched surfaces include `skills/loom-critique`, `skills/loom-wiki`, and
shared packet frontmatter lifecycle guidance.

Ralph iteration `packet:ralph-ticket-pktlife6-20260502T201044Z` updated the
allowed critique/wiki packet templates, critique/wiki skill Done Means guidance,
shared packet frontmatter guidance, and shared status lifecycle guidance. Evidence
is recorded in `evidence:packet-lifecycle-parity-validation`.

# Blockers

None - `ticket:pktgram5` is closed.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:revtgt7x`.

# Route Readiness

Route: acceptance_review

Acceptance review readiness:
Evidence and critique disposition: `evidence:packet-lifecycle-parity-validation`
and `critique:packet-lifecycle-parity-review` support acceptance with no findings.
Residual risks: evidence is structural, which is appropriate for Markdown
protocol guidance.

# Evidence

Recorded:

- `evidence:packet-lifecycle-parity-validation` — before/after searches for
  `parent_merge_scope`, `compiled`, terminal packet statuses, `Parent Merge
  Notes`, `Done Means`, ownership guardrails, and `git diff --check`.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: packet lifecycle affects support artifact reconciliation and
closure honesty.

Required critique profiles:

- protocol-change
- records-grammar
- routing-safety

Findings:

Recorded in `critique:packet-lifecycle-parity-review`:

- None - no findings.

Disposition status: completed

Deferral / not-required rationale:

Not deferred. Mandatory oracle critique passed with no findings.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Critique/wiki packet lifecycle parity was promoted into
  `skills/loom-critique/SKILL.md`,
  `skills/loom-critique/templates/critique-packet.md`,
  `skills/loom-wiki/SKILL.md`, `skills/loom-wiki/templates/wiki-packet.md`,
  `skills/loom-records/references/packet-frontmatter.md`, and
  `skills/loom-records/references/status-lifecycle.md`.

Deferred / not-required rationale:

Not deferred. The durable lesson was promoted directly into the owner product
surfaces listed above; no separate wiki page, research record, spec,
constitution decision, or memory entry is needed.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation is now in the
packet lifecycle owner surfaces.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T20:16:28Z
Basis: Ralph packet `packet:ralph-ticket-pktlife6-20260502T201044Z`; evidence
`evidence:packet-lifecycle-parity-validation`; oracle critique
`critique:packet-lifecycle-parity-review` with no findings.
Residual risks: evidence is structural, which is appropriate for Markdown
protocol guidance.

# Dependencies

- `ticket:pktgram5`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-006`.
- 2026-05-02T20:10:44Z: Started Ralph iteration
  `packet:ralph-ticket-pktlife6-20260502T201044Z` from baseline
  `3b65266ffe67195bb548c8aa4a8e8db481fd92e1`.
- 2026-05-02T20:12:20Z: Ralph iteration updated packet lifecycle parity
  guidance and recorded `evidence:packet-lifecycle-parity-validation`; moved to
  `review_required` for mandatory oracle critique.
- 2026-05-02T20:16:28Z: Oracle critique passed with no findings. Recorded
  acceptance and retrospective / promotion disposition; closed ticket.
