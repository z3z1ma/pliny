---
id: ticket:pktprov4
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-02T22:03:13Z
updated_at: 2026-05-02T22:48:30Z
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
    - packet:ralph-ticket-pktprov4-20260502T224150Z
  evidence:
    - evidence:packet-provenance-sources-validation
  critique:
    - critique:packet-provenance-sources-review
external_refs: {}
depends_on:
  - ticket:pktsupp1
---

# Summary

Define the split between packet `source_fingerprint.compiled_from` provenance and
the packet `sources` context set.

# Context

Council finding `NC-004` found semantic overlap between `compiled_from` and
`sources` in packet frontmatter guidance and packet templates.

# Why Now

Packet provenance should remain inspectable without performative duplication or
inconsistent source lists.

# Scope

- Clarify `compiled_from` as provenance for packet compilation baseline.
- Clarify `sources` as context sources the child/reviewer/synthesizer should read.
- Align Ralph, critique, and wiki packet templates with the split.

# Out Of Scope

- Do not add a parser or schema.
- Do not make critique/wiki packets Ralph-governed.

# Acceptance Criteria

- ACC-001: Shared packet frontmatter defines the provenance/context split.
- ACC-002: Ralph, critique, and wiki packet templates align with the split.
- ACC-003: Packet family boundaries remain intact.
- ACC-004: Evidence records packet provenance/source searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-004`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-004` | `evidence:packet-provenance-sources-validation` | `critique:packet-provenance-sources-review` | supported |
| `ticket:pktprov4#ACC-001` | `evidence:packet-provenance-sources-validation` | `critique:packet-provenance-sources-review` | supported |
| `ticket:pktprov4#ACC-002` | `evidence:packet-provenance-sources-validation` | `critique:packet-provenance-sources-review` | supported |
| `ticket:pktprov4#ACC-003` | `evidence:packet-provenance-sources-validation` | `critique:packet-provenance-sources-review` | supported |
| `ticket:pktprov4#ACC-004` | `evidence:packet-provenance-sources-validation` | `critique:packet-provenance-sources-review` | supported |
| `ticket:pktprov4#ACC-005` | `critique:packet-provenance-sources-review` | oracle critique passed with no findings | supported |

# Execution Notes

Likely touched surfaces include `skills/loom-records/references/packet-frontmatter.md`
and packet templates under `skills/loom-ralph`, `skills/loom-critique`, and
`skills/loom-wiki`.

# Blockers

Depends on `ticket:pktsupp1`.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:tkrout5`.

# Route Readiness

Route: acceptance_review

Acceptance review readiness:
Evidence `evidence:packet-provenance-sources-validation` and oracle critique
`critique:packet-provenance-sources-review` support closure with no findings.

# Evidence

Expected: before/after searches for `compiled_from`, `sources:`, packet templates,
and `git diff --check`.

Observed: `evidence:packet-provenance-sources-validation`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: packet provenance ambiguity weakens replayable handoff contracts.

Required critique profiles:

- records-grammar
- routing-safety
- owner-boundary

Findings:

`critique:packet-provenance-sources-review` - no findings; mandatory oracle
critique passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Packet provenance/context split was promoted directly into
  `skills/loom-records/references/packet-frontmatter.md` and the Ralph, critique,
  and wiki packet templates.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the packet grammar product wording itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
touched packet grammar guidance.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T22:48:30Z
Basis: Ralph packet `packet:ralph-ticket-pktprov4-20260502T224150Z`; evidence
`evidence:packet-provenance-sources-validation`; oracle critique
`critique:packet-provenance-sources-review` with no findings.
Residual risks: validation is structural Markdown review only; evidence covers
the targeted shared reference and three packet templates, not every historical
packet surface.

# Dependencies

- `ticket:pktsupp1`

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-004`.
- 2026-05-02T22:41:50Z: Compiled Ralph packet
  `packet:ralph-ticket-pktprov4-20260502T224150Z` and moved ticket to `active`.
- 2026-05-02T22:42:54Z: Ralph child clarified packet provenance/context grammar,
  aligned Ralph/critique/wiki templates, recorded
  `evidence:packet-provenance-sources-validation`, and moved ticket to
  `review_required` for mandatory oracle critique.
- 2026-05-02T22:45:58Z: Parent reconciled Ralph output, normalized claim matrix
  statuses to canonical claim-coverage vocabulary, expanded evidence sections,
  and marked the Ralph packet consumed.
- 2026-05-02T22:48:30Z: Mandatory oracle critique
  `critique:packet-provenance-sources-review` passed with no findings. Parent
  recorded retrospective / promotion disposition and accepted closure.
