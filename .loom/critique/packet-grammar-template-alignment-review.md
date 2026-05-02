---
id: critique:packet-grammar-template-alignment-review
kind: critique
status: final
created_at: 2026-05-02T20:01:44Z
updated_at: 2026-05-02T20:01:44Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: ticket:pktgram5 packet grammar template alignment
links:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
  ticket:
    - ticket:pktgram5
  evidence:
    - evidence:packet-grammar-template-alignment-validation
  packet:
    - packet:ralph-ticket-pktgram5-20260502T195332Z
external_refs: {}
---

# Summary

Oracle critique reviewed `ticket:pktgram5` for protocol-change,
records-grammar, and routing-safety risks.

The oracle returned `changes_required` with two medium findings.

# Review Target

- Ticket: `ticket:pktgram5`
- Evidence: `evidence:packet-grammar-template-alignment-validation`
- Ralph packet: `packet:ralph-ticket-pktgram5-20260502T195332Z`
- Product surfaces: packet frontmatter, naming, Ralph packet, critique packet,
  wiki packet, and Ralph packet contract guidance
- Oracle task session: `ses_215b9ab30ffeYcbf6ef5m3bskg`

# Verdict

`changes_required`.

# Findings

## PKTGRAM5-CRIT-001

Severity: medium
Confidence: high
State: open

Observation: Product-surface references/templates used the active dogfood ticket
token `ticket:pktgram5` as an example in packet frontmatter, naming, and critique
packet guidance.

Why it matters: `skills/` is the distributable product surface and should stay
generic and self-contained. Embedding the current repository's live ticket token
leaks dogfood context into protocol teaching surfaces.

Follow-up: Replace dogfood-specific examples with neutral fictional examples,
such as `ticket:abc123xy` -> `ticket-abc123xy`.

Challenged claims:

- `ticket:pktgram5#ACC-002`
- `initiative:skills-corpus-council-precision-pass#OBJ-005`

## PKTGRAM5-CRIT-002

Severity: medium
Confidence: medium-high
State: open

Observation: `skills/loom-critique/templates/critique-packet.md` said to encode
the review target in packet IDs/filenames, while shared grammar maps packet IDs
and filenames from the packet `target` or an explicitly chosen encoded target.
For critique packets, `review_target` is a separate structured field.

Why it matters: This reintroduces naming ambiguity by implying a critique packet
author could encode `review_target.diff` instead of the packet `target`, causing
packet naming drift.

Follow-up: Reword critique packet naming guidance to distinguish the packet
target or explicit change slug from the structured `review_target` field.

Challenged claims:

- `ticket:pktgram5#ACC-002`
- `ticket:pktgram5#ACC-003`

# Evidence Reviewed

- Current working tree status and targeted diff.
- `git diff --check`, with no output.
- `HEAD` and `origin/main` at `cceb6422bf5c95cfaf2c45983bb6a412c748c94f`.
- `ticket:pktgram5`.
- `evidence:packet-grammar-template-alignment-validation`.
- `packet:ralph-ticket-pktgram5-20260502T195332Z`.
- Plan and initiative records.
- Changed product files under `skills/`.

# Residual Risks

- Evidence is structural and sufficient for most of `ACC-001` through `ACC-004`,
  but current `git diff --check` does not cover untracked files until they are
  staged.
- `review_target` cleanup is partly owned by a later ticket, but this ticket
  should not add new ambiguity in the meantime.

# Required Follow-up

- Remove dogfood-specific `ticket:pktgram5` examples from product-surface files.
- Clarify critique packet wording so packet ID/filename mapping is not confused
  with structured `review_target`.
- Re-run structural validation and critique after changes.

# Acceptance Recommendation

Do not close `ticket:pktgram5`. Return to active repair until the findings are
resolved and critique is rerun.
