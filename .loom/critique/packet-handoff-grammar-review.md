---
id: critique:packet-handoff-grammar-review
kind: critique
status: final
created_at: 2026-05-02T09:54:27Z
updated_at: 2026-05-02T09:54:27Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: ticket:0cd38381
links:
  tickets:
    - ticket:0cd38381
  evidence:
    - evidence:packet-handoff-grammar-validation
  packets:
    - packet:ralph-ticket-0cd38381-20260502T094123Z
external_refs: {}
---

# Summary

Oracle-assisted critique of packet and handoff grammar changes for
`ticket:0cd38381`.

# Review Target

Reviewed current diff for:

- `skills/loom-ralph/**`
- `skills/loom-records/**`
- `skills/loom-critique/**`
- `skills/loom-wiki/**`
- `skills/loom-drive/**`

Reviewed against `ticket:0cd38381` acceptance criteria ACC-001 through ACC-006
with protocol-change, routing-safety, and records-grammar profiles.

# Verdict

`pass_with_findings`.

The first oracle pass found two blocking grammar issues. The fixer resolved both,
and the final oracle pass returned `pass` with no product-surface blockers.

# Findings

## FIND-001: Common packet frontmatter omitted `packet_kind`

Severity: high

Confidence: high

Disposition: resolved

Observation:

Shared frontmatter guidance listed packet-specific fields but omitted
`packet_kind`, even though packet family grammar depends on `packet_kind` plus
path.

Why it matters:

Future packet authors could follow common frontmatter guidance and create
family-ambiguous packets.

Follow-up:

Resolved by adding `packet_kind` to packet frontmatter guidance.

Challenges:

- `ticket:0cd38381` ACC-001

## FIND-002: Drive handoff `status` was not classified

Severity: high

Confidence: high

Disposition: resolved

Observation:

The drive outer-loop handoff template used `status: draft` and had been classified
as transient/support, but the status field itself was not explained.

Why it matters:

Without classification, a support-handoff status could be mistaken for ticket
state, canonical record lifecycle, or packet lifecycle.

Follow-up:

Resolved by documenting the status as support-local proposal status for that
handoff only, not canonical record truth, ticket execution state, or shared packet
lifecycle status. Shared lifecycle guidance now includes a narrow support-handoff
template-local status note.

Challenges:

- `ticket:0cd38381` ACC-005

# Evidence Reviewed

- Ralph packet `packet:ralph-ticket-0cd38381-20260502T094123Z`
- Validation evidence `evidence:packet-handoff-grammar-validation`
- Oracle critique pass `ses_217ea2434ffeZLVIBR1Hwoi86f`
- Final oracle critique pass `ses_217e605dbffeJW6uxQfb8scNm7`
- Current diff for packet/handoff grammar surfaces

# Residual Risks

- Markdown-only protocol guidance can still drift without validators.
- Rejected-child status choices still require parent judgment; the guidance is
  now explicit but not mechanically enforced.

# Required Follow-up

No required follow-up blocks this ticket's acceptance.

# Acceptance Recommendation

Close-ready. The ticket has structural evidence and final oracle review with all
blocking findings resolved.
