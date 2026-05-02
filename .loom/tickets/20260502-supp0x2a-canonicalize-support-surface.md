---
id: ticket:supp0x2a
kind: ticket
status: closed
change_class: protocol-authority
risk_class: high
created_at: 2026-05-02T18:58:43Z
updated_at: 2026-05-02T19:32:39Z
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
    - packet:ralph-ticket-supp0x2a-20260502T191626Z
    - packet:ralph-ticket-supp0x2a-20260502T192522Z
  evidence:
    - evidence:support-surface-validation
  critique:
    - critique:support-surface-review
external_refs: {}
depends_on:
  - ticket:rtvocab1
---

# Summary

Make `.loom/support/` handling explicit and non-canonical wherever saved support
artifacts and workspace shape are taught.

# Context

Council finding `CR-002` found `.loom/support/drive-handoffs/` taught by drive but
not consistently reflected in workspace tree, README runtime tree, status, or
support artifact doctrine.

# Why Now

Support paths must be discoverable without becoming hidden shadow truth.

# Scope

- Decide the corpus wording for `.loom/support/` as optional, lazy-materialized,
  non-canonical support surface.
- Align workspace tree/status, drive handoff, and records/frontmatter guidance.
- Update README only if product framing would otherwise diverge from skills.

# Out Of Scope

- Do not make `.loom/support/` a canonical owner layer.
- Do not require saved drive handoffs for normal operation.
- Do not add support artifact runtime tooling.

# Acceptance Criteria

- ACC-001: `.loom/support/` is either consistently documented as optional
  non-canonical support or saved support handoffs are demoted from product
  guidance.
- ACC-002: Workspace tree/status and drive handoff guidance agree.
- ACC-003: Support surfaces explicitly do not own objective state, live ticket
  state, acceptance, evidence sufficiency, critique verdicts, wiki truth,
  canonical truth, or packet lifecycle.
- ACC-004: Evidence records before/after support-path searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-002`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-002` | `evidence:support-surface-validation` | `critique:support-surface-review` with findings resolved and re-check passed | supported |
| `ticket:supp0x2a#ACC-001` | `evidence:support-surface-validation` | `critique:support-surface-review` | supported |
| `ticket:supp0x2a#ACC-002` | `evidence:support-surface-validation` | `critique:support-surface-review` | supported |
| `ticket:supp0x2a#ACC-003` | `evidence:support-surface-validation` | `critique:support-surface-review` | supported |
| `ticket:supp0x2a#ACC-004` | `evidence:support-surface-validation` | `critique:support-surface-review` | supported |
| `ticket:supp0x2a#ACC-005` | `critique:support-surface-review` | `critique:support-surface-review` re-check passed with no findings | supported |

# Execution Notes

Likely touched surfaces include `skills/loom-workspace/references/workspace-tree.md`,
`skills/loom-drive`, `skills/loom-records/references/frontmatter.md`, and README
runtime tree if needed.

# Blockers

None.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:retrod3p`.

# Route Readiness

Route: acceptance_review

Acceptance review readiness:
Evidence and critique disposition: `evidence:support-surface-validation` and
`critique:support-surface-review` support acceptance with both oracle findings
resolved and re-check passed.
Residual risks: validation is structural/manual; README runtime tree remains
concise while fuller framing lives in bootstrap/protocol/architecture/skills.

# Evidence

- `evidence:support-surface-validation`: records before/after `.loom/support`,
  `drive-handoffs`, `support-artifact`, bootstrap, `PROTOCOL.md`,
  `ARCHITECTURE.md`, and support ownership observations plus `git diff --check`
  result.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: support-surface wording can create shadow paths if ambiguous.

Required critique profiles:

- protocol-change
- records-grammar
- routing-safety

Findings:

Recorded in `critique:support-surface-review`:

- `critique:support-surface-review#ORACLE-SUPP0X2A-001` - resolved; first packet
  is `consumed`, parent merge notes name the stale-lifecycle finding and repair
  packet, and oracle re-check passed.
- `critique:support-surface-review#ORACLE-SUPP0X2A-002` - resolved; bootstrap,
  `PROTOCOL.md`, and `ARCHITECTURE.md` now name optional, lazy-materialized,
  non-canonical `.loom/support/` framing, evidence was refreshed, and oracle
  re-check passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred. Mandatory oracle critique and re-check passed with no findings.

# Wiki Disposition

Retrospective / promotion disposition complete. Durable support-surface learning
was promoted directly into the owner product surfaces: bootstrap truth reference,
`PROTOCOL.md`, `ARCHITECTURE.md`, README, workspace tree/status, drive handoff
guidance, and record grammar references. No separate wiki page, research record,
spec, constitution decision, or memory entry is needed for this ticket.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T19:32:39Z
Basis: Ralph packets `packet:ralph-ticket-supp0x2a-20260502T191626Z` and
`packet:ralph-ticket-supp0x2a-20260502T192522Z`; evidence
`evidence:support-surface-validation`; oracle critique
`critique:support-surface-review` with both findings resolved and re-check passing
with no findings.
Residual risks: validation is structural/manual; no automated schema or rendered
document validation exists for this Markdown corpus.

# Dependencies

- `ticket:rtvocab1`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-002`.
- 2026-05-02T19:16:26Z: Started Ralph iteration
  `packet:ralph-ticket-supp0x2a-20260502T191626Z` from baseline
  `63f68637ae4ff7ae2e13c901a235ad362791fbcc` after dependency
  `ticket:rtvocab1` closed.
- 2026-05-02T19:20:06Z: Ralph iteration updated support-surface product
  guidance, recorded `evidence:support-surface-validation`, and moved ticket to
  `review_required` for mandatory oracle critique. Ticket remains open.
- 2026-05-02T19:25:22Z: Oracle critique found two blocking medium findings:
  stale Ralph packet lifecycle and missing bootstrap/PROTOCOL/ARCHITECTURE support
  framing. Parent recorded `critique:support-surface-review`, consumed the first
  packet, and compiled repair packet
  `packet:ralph-ticket-supp0x2a-20260502T192522Z`.
- 2026-05-02T19:26:53Z: Ralph repair iteration verified the first packet is
  `consumed`, aligned bootstrap/`PROTOCOL.md`/`ARCHITECTURE.md` with optional
  lazy-materialized non-canonical `.loom/support/`, refreshed
  `evidence:support-surface-validation`, and returned the ticket to
  `review_required` for oracle re-check. Ticket remains open.
- 2026-05-02T19:32:39Z: Oracle re-check passed with no findings. Recorded
  acceptance and retrospective disposition; closed ticket.
