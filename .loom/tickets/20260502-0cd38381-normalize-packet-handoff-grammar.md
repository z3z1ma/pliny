---
id: ticket:0cd38381
kind: ticket
status: closed
change_class: protocol-authority
risk_class: high
created_at: 2026-05-02T08:46:28Z
updated_at: 2026-05-02T09:54:27Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  roadmap:
    - roadmap:bootstrap-the-markdown-first-protocol-corpus
  initiative:
    - initiative:skills-corpus-protocol-sharpening
  research:
    - research:skills-corpus-council-review
  evidence:
    - evidence:skills-corpus-council-review
    - evidence:packet-handoff-grammar-validation
  critique:
    - critique:packet-handoff-grammar-review
  packet:
    - packet:ralph-ticket-0cd38381-20260502T094123Z
  plan:
    - plan:skills-corpus-protocol-sharpening
  supersedes:
    - ticket:3uv5l5fh
external_refs: {}
depends_on:
  - ticket:4e8ebe92
---

# Summary

Normalize packet, handoff, source-scope, and rejected-iteration grammar across
Ralph, critique, wiki, records, and drive-adjacent handoff surfaces.

# Context

The council found that Ralph packet guidance is strong, but critique/wiki packets
and drive handoffs are less consistently named and scoped. It also flagged
`write_scope` versus `child_write_scope` drift and the need to make packet
terminal statuses visible where packet consumers look.

# Why Now

Ralph iterations depend on precise packet contracts. Before implementation work
fans out, the corpus should clearly distinguish implementation packets, sibling
critique/wiki packets, drive handoffs, packet terminal statuses, and parent
reconciliation of rejected or overscoped child output.

# Scope

- Normalize packet ID families and naming guidance for Ralph, critique, and wiki
  packets.
- Make packet terminal statuses `consumed`, `superseded`, and `abandoned` visible
  in `loom-ralph` and linked shared grammar surfaces.
- Clarify whether critique/wiki packets use `verification_posture`, another
  posture field, or domain-specific evidence expectations.
- Resolve `write_scope` versus `child_write_scope` wording drift.
- Decide whether the drive outer-loop handoff template is a durable packet-like
  support artifact, transient handoff note, or frontmatter-bearing support record.
- Add parent-side guidance for rejected, corrupted, or overscoped Ralph results.

# Non-goals

- Do not change the Ralph parent/child model or create a new packet owner layer.
- Do not update ticket acceptance gate grammar beyond direct links to packet
  outcomes; that belongs to `ticket:50ded996`.
- Do not rewrite all of `loom-drive`; only handoff/packet-adjacent wording belongs
  here.

# Acceptance Criteria

- ACC-001: Packet ID/path guidance covers Ralph, critique, and wiki packet
  families or explicitly explains why only Ralph has canonical packet IDs.
- ACC-002: Packet terminal statuses are easy to find from `loom-ralph` and remain
  consistent with shared status lifecycle guidance.
- ACC-003: Critique and wiki packet guidance clearly states what posture or
  evidence expectation replaces or reuses `verification_posture`.
- ACC-004: `write_scope` / `child_write_scope` drift is removed or explained with
  a compatibility note.
- ACC-005: Drive handoff template status is explicitly classified without turning
  it into a new truth owner.
- ACC-006: Rejected or overscoped Ralph iteration guidance tells the parent how to
  update ticket truth and packet status without pretending the child succeeded.

# Coverage

Covers:

- `initiative:skills-corpus-protocol-sharpening#OBJ-002`
- `initiative:skills-corpus-protocol-sharpening#OBJ-004`
- `research:skills-corpus-council-review#CLAIM-005`
- `research:skills-corpus-council-review#CLAIM-008`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-protocol-sharpening#OBJ-002` | `evidence:packet-handoff-grammar-validation` | `critique:packet-handoff-grammar-review` | supported |
| `initiative:skills-corpus-protocol-sharpening#OBJ-004` | `evidence:packet-handoff-grammar-validation` | `critique:packet-handoff-grammar-review` | supported |
| `research:skills-corpus-council-review#CLAIM-005` | `evidence:skills-corpus-council-review`; `evidence:packet-handoff-grammar-validation` | `critique:packet-handoff-grammar-review` | supported |
| `research:skills-corpus-council-review#CLAIM-008` | `evidence:skills-corpus-council-review`; `evidence:packet-handoff-grammar-validation` | `critique:packet-handoff-grammar-review` | supported |

# Execution Notes

Keep packet discipline as a bounded support contract. Do not let packets, handoff
templates, or child outputs own project truth or ticket closure.

# Blockers

Do not start until shared record grammar in `ticket:4e8ebe92` has landed or been
deferred.

# Next Move / Next Route

Ralph implementation packet for packet and handoff grammar.

# Ralph Readiness

Bounded iteration:

Normalize packet families, terminal statuses, handoff classification, scope field
names, and rejected-iteration recovery guidance.

Write boundary:

- `skills/loom-ralph/**`
- `skills/loom-records/**`
- `skills/loom-critique/**`
- `skills/loom-wiki/**`
- `skills/loom-drive/**`
- targeted ticket references only if needed for packet outcome reconciliation

Likely verification posture:

Observation-first structural validation.

Expected output contract:

- changed files,
- packet family/status decisions,
- handoff template classification,
- grep output showing no unexplained `write_scope` drift,
- residual questions or follow-up recommendations.

# Evidence

Recorded:

- `evidence:packet-handoff-grammar-validation`
- `git diff --check` passed with no output.
- Targeted searches confirmed packet families, terminal statuses,
  `child_write_scope`/`write_scope` classification, critique/wiki posture
  expectations, rejected-child recovery, and drive handoff status classification.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale:

This changes packet contract language and parent/child execution recovery, which
is core protocol behavior.

Required critique profiles:

- protocol-change
- routing-safety
- records-grammar

Findings:

All findings resolved in `critique:packet-handoff-grammar-review`.

Disposition status: complete

Deferral / not-required rationale:

Not deferred. Mandatory critique is recorded in
`critique:packet-handoff-grammar-review`.

# Wiki Disposition

Deferred intentionally. Retrospective found no separate wiki page needed because
the accepted guidance now lives in the owning Ralph, records, critique, wiki, and
drive surfaces. Final integration review may still choose broader wiki promotion
for the full sharpening pass.

# Acceptance Decision

Accepted by: OpenCode parent agent

Accepted at: 2026-05-02T09:54:27Z

Basis: Ralph packet `packet:ralph-ticket-0cd38381-20260502T094123Z`, validation
evidence `evidence:packet-handoff-grammar-validation`, and final oracle critique
`critique:packet-handoff-grammar-review` with all findings resolved.

Residual risks: Markdown-only packet grammar still depends on operator discipline;
final corpus-wide validation remains owned by `ticket:cdf664af`.

# Dependencies

- `ticket:4e8ebe92`

# Journal

- 2026-05-02T08:46:28Z: Split from cancelled broad ticket `ticket:3uv5l5fh` as
  the packet and handoff grammar slice.
- 2026-05-02T09:41:24Z: Started Ralph iteration
  `packet:ralph-ticket-0cd38381-20260502T094123Z` for packet and handoff grammar.
- 2026-05-02T09:54:27Z: Accepted and closed after Ralph implementation,
  structural validation, oracle critique, resolved packet/handoff findings, and
  retrospective disposition. No ticket-scoped follow-up remains.
