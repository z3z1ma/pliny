---
id: critique:support-surface-review
kind: critique
status: final
created_at: 2026-05-02T19:25:22Z
updated_at: 2026-05-02T19:32:39Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: ticket:supp0x2a support surface canonicalization
links:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
  ticket:
    - ticket:supp0x2a
  evidence:
    - evidence:support-surface-validation
  packet:
    - packet:ralph-ticket-supp0x2a-20260502T191626Z
    - packet:ralph-ticket-supp0x2a-20260502T192522Z
external_refs: {}
---

# Summary

Oracle critique reviewed `ticket:supp0x2a` support-surface canonicalization for
protocol-change, records-grammar, and routing-safety risks.

The first pass found two medium findings. A repair iteration resolved both, and
oracle re-check returned `pass` with no findings.

# Review Target

- Ticket: `ticket:supp0x2a`
- Evidence: `evidence:support-surface-validation`
- Ralph packet: `packet:ralph-ticket-supp0x2a-20260502T191626Z`
- Product surfaces: README, workspace tree/status, drive handoff guidance, records
  frontmatter/naming/status lifecycle, bootstrap truth reference, `PROTOCOL.md`,
  and `ARCHITECTURE.md`
- Oracle task session: `ses_215dbd583ffeiqtIEJIdFFZibU`

# Verdict

`pass` after repair and re-check.

# Findings

## ORACLE-SUPP0X2A-001: Ralph packet still looked compiled after child output

Severity: medium
Confidence: high
State: open

Observation:

The Ralph packet had child output but still used `status: compiled`, and parent
merge notes still said `Pending child execution`.

Why it matters:

Packet lifecycle truth is part of checkpoint/resume safety. Child output returned,
so parent must reconcile the packet to a terminal state.

Follow-up:

Resolved. Iteration 1 packet is `status: consumed` with parent merge notes naming
the stale-lifecycle finding and repair packet. Oracle re-check confirmed the
finding resolved.

Challenges:

- `ticket:supp0x2a#ACC-005`

## ORACLE-SUPP0X2A-002: Higher-level package and bootstrap surfaces omit `.loom/support/`

Severity: medium
Confidence: high
State: open

Observation:

README and lower skill docs now teach `.loom/support/`, but bootstrap truth/support
layer doctrine, `PROTOCOL.md`, and `ARCHITECTURE.md` still omit optional saved
support artifacts from support-surface framing. The evidence did not include those
surfaces.

Why it matters:

This is a protocol-authority change. Bootstrap and package framing should not
leave `.loom/support/` discoverability dependent only on lower skill docs while
README claims the support surface exists.

Follow-up:

Resolved. Bootstrap, `PROTOCOL.md`, and `ARCHITECTURE.md` now document optional,
lazy-materialized, non-canonical `.loom/support/` saved support artifacts with
non-ownership boundaries. Evidence was refreshed to include those surfaces, and
oracle re-check confirmed the finding resolved.

Challenges:

- `initiative:skills-corpus-council-precision-pass#OBJ-002`
- `ticket:supp0x2a#ACC-001`
- `ticket:supp0x2a#ACC-004`

# Evidence Reviewed

- Current `git status` and working tree diff.
- `git diff --check`, with no output.
- `ticket:supp0x2a`.
- `evidence:support-surface-validation`.
- `packet:ralph-ticket-supp0x2a-20260502T191626Z`.
- `plan:skills-corpus-council-precision-pass`.
- `initiative:skills-corpus-council-precision-pass`.
- Changed files: `README.md`, workspace tree/status docs, drive skill/template,
  records frontmatter/naming/status docs.
- Adjacent authority/package surfaces: bootstrap truth reference, `PROTOCOL.md`,
  and `ARCHITECTURE.md`.
- Oracle re-check of both Ralph packets, refreshed evidence, README,
  `PROTOCOL.md`, `ARCHITECTURE.md`, bootstrap truth reference, and changed
  workspace/drive/records support-surface docs.

# Residual Risks

- README runtime tree says optional/non-canonical but is less explicit than skill
  docs about lazy materialization.
- No automated test suite exists; validation is structural/manual.

# Required Follow-up

None before ticket acceptance.

# Acceptance Recommendation

Close-ready.
