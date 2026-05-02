---
id: ticket:9c2delu8
kind: ticket
status: closed
change_class: protocol-authority
risk_class: high
created_at: 2026-05-02T15:25:50Z
updated_at: 2026-05-02T17:13:16Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-perfection-council-followup
  plan:
    - plan:skills-corpus-perfection-council-followup
  packet:
    - packet:ralph-ticket-9c2delu8-20260502T165707Z
    - packet:ralph-ticket-9c2delu8-20260502T170610Z
  evidence:
    - evidence:drive-continuity-vocabulary-validation
  critique:
    - critique:drive-continuity-vocabulary-review
external_refs: {}
depends_on:
  - ticket:3twzep5n
  - ticket:lqiw3hvp
---

# Summary

Simplify `loom-drive` continuity/checkpoint/tranche vocabulary while preserving
parent-loop autonomy, restart safety, and owner-layer boundaries.

# Context

Council finding `COUNCIL-FIND-011` found overlapping drive terms: continuity
contract, checkpoint, snapshot, tranche contract, gap matrix, route exit, and
resume instruction. Drive is powerful but risks feeling bureaucratic.

# Why Now

After disposition and support artifact grammar are settled, drive can be made
lighter and more operational without weakening safety gates.

# Scope

- Consolidate drive vocabulary around a small canonical continuity/checkpoint
  shape.
- Make advanced tranche/gap guidance conditional rather than always-on.
- Preserve explicit owner-record checkpoint requirements before child launch,
  compaction, or handoff.
- Keep drive coordination from owning project truth.

# Non-goals

- Do not remove drive safety gates.
- Do not create a new drive record kind or ledger.
- Do not rewrite unrelated skills.

# Acceptance Criteria

- ACC-001: Drive references use a smaller, coherent continuity vocabulary.
- ACC-002: Checkpoint/resume safety remains explicit and fail-closed.
- ACC-003: Advanced tranche/gap guidance is clearly conditional.
- ACC-004: Drive still routes durable truth to owner layers and tickets.
- ACC-005: Evidence records term searches, pressure-scenario spot checks, and
  `git diff --check`.
- ACC-006: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-perfection-council-followup#OBJ-006`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-perfection-council-followup#OBJ-006` | `evidence:drive-continuity-vocabulary-validation` | `critique:drive-continuity-vocabulary-review` with all findings resolved | supported |

# Execution Notes

Council affected surfaces include `skills/loom-drive/references/checkpoint-resume-protocol.md`,
`skills/loom-drive/references/continuity-contract.md`, and
`skills/loom-drive/references/tranche-decision-protocol.md`.

# Blockers

None. Dependencies `ticket:3twzep5n` and `ticket:lqiw3hvp` are closed.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:wfxfu4zp`.

# Route Readiness

Route: ticket acceptance review completed.

Review target: repaired drive continuity/resume route vocabulary.

Evidence reviewed: `evidence:drive-continuity-vocabulary-validation`, Ralph
packets, oracle critique, and the git diff.

Acceptance result: close-ready with no remaining oracle findings.

# Evidence

Expected:

- `git diff --check`
- targeted searches for drive vocabulary before/after
- pressure-scenario spot checks for cold resume, blocked critique, next-route
  selection, and child handoff

Recorded:

- `evidence:drive-continuity-vocabulary-validation`

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale: drive coordinates broad autonomous work and checkpoint safety.

Required critique profiles:

- protocol-change
- operator-clarity
- routing-safety

Findings:

Recorded in `critique:drive-continuity-vocabulary-review`:

- `critique:drive-continuity-vocabulary-review#ORACLE-9C2DELU8-FIND-001` - resolved.

Disposition status: completed

Deferral / not-required rationale:

Not deferred. Mandatory oracle critique passed with no remaining findings.

# Wiki Disposition

Retrospective disposition complete. Durable lessons were promoted directly into
the owner product surfaces: drive continuity wording, checkpoint/resume protocol,
tranche decision protocol, drive loop guidance, and the outer-loop handoff
template. No separate wiki page, research record, spec, constitution decision, or
memory entry is needed for this ticket.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T17:13:16Z
Basis: Ralph packets `packet:ralph-ticket-9c2delu8-20260502T165707Z` and
`packet:ralph-ticket-9c2delu8-20260502T170610Z`; evidence
`evidence:drive-continuity-vocabulary-validation`; final oracle critique
`critique:drive-continuity-vocabulary-review` with no remaining findings.
Residual risks: validation and critique were structural/textual; future operator
application is not proven beyond corpus consistency.

# Dependencies

- `ticket:3twzep5n`
- `ticket:lqiw3hvp`

# Journal

- 2026-05-02T15:25:50Z: Created from council finding `COUNCIL-FIND-011`.
- 2026-05-02T16:57:07Z: Dependencies closed. Moved to active and compiled Ralph
  packet `packet:ralph-ticket-9c2delu8-20260502T165707Z` from commit
  `e3fa3b42946a4ccbe519563c6054dfeadff3dd94`.
- 2026-05-02T17:00:25Z: Ralph implementation simplified the drive continuity
  vocabulary, recorded `evidence:drive-continuity-vocabulary-validation`, and
  moved the ticket to `review_required` for mandatory oracle critique.
- 2026-05-02T17:02:26Z: Parent reconciliation normalized claim-matrix status and
  updated this ticket to route-neutral readiness for the critique route.
- 2026-05-02T17:06:10Z: Oracle critique found one blocking vocabulary issue.
  Recorded `critique:drive-continuity-vocabulary-review`, moved back to active,
  and compiled repair packet `packet:ralph-ticket-9c2delu8-20260502T170610Z`.
- 2026-05-02T17:07:31Z: Repair iteration aligned continuity snapshot and
  checkpoint/resume wording on `next route` / `next route owner`, refreshed
  validation evidence, and moved back to `review_required` for oracle re-check.
- 2026-05-02T17:07:31Z: Parent reconciliation normalized ticket claim and
  critique disposition status vocabulary before oracle re-check.
- 2026-05-02T17:13:16Z: Oracle re-check passed with the prior finding resolved and
  no new findings. Recorded final critique, retrospective disposition, and
  acceptance; closed ticket.
