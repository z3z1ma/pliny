---
id: ticket:planwv11
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-02T18:58:43Z
updated_at: 2026-05-02T21:26:35Z
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
    - packet:ralph-ticket-planwv11-20260502T210325Z
    - packet:ralph-ticket-planwv11-20260502T211053Z
    - packet:ralph-ticket-planwv11-20260502T212006Z
  evidence:
    - evidence:plan-wave-coverage-validation
  critique:
    - critique:plan-wave-coverage-review
    - critique:plan-wave-coverage-rereview
    - critique:plan-wave-coverage-final-review
external_refs: {}
depends_on:
  - ticket:rtvocab1
  - ticket:retrod3p
  - ticket:pktgram5
---

# Summary

Improve plan acceptance coverage and parallel-wave independence checks.

# Context

Council finding `CR-011` found plan templates do not fully model spec/ticket claim
mapping or execution-wave independence/write-scope overlap checks.

# Why Now

Plans bridge strategy into tickets and may authorize parallel Ralph. Unsafe plan
defaults can create downstream ambiguity or overlap.

# Scope

- Add plan template/reference cues for spec-to-ticket or initiative-to-ticket
  claim coverage.
- Add explicit parallel-wave independence and write-scope overlap checks.
- Cross-link to Ralph/Git parallel guidance where useful.

# Out Of Scope

- Do not make plans own ticket execution progress.
- Do not require parallel execution.
- Do not add a planner runtime.

# Acceptance Criteria

- ACC-001: Plan template/readiness cues claim/acceptance coverage mapping.
- ACC-002: Execution waves require independence and write-scope overlap checks or
  explicit `None - reason`.
- ACC-003: Parallel guidance preserves ticket and packet authority boundaries.
- ACC-004: Evidence records before/after plan-wave searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-011`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-011` | `evidence:plan-wave-coverage-validation` records before/after structural searches and repair observations | `critique:plan-wave-coverage-final-review` | supported |
| `ticket:planwv11#ACC-001` | `evidence:plan-wave-coverage-validation` shows new claim coverage mapping cues | `critique:plan-wave-coverage-final-review` | supported |
| `ticket:planwv11#ACC-002` | `evidence:plan-wave-coverage-validation` shows wave independence, write scope overlap, and separate real-wave/no-wave examples | `critique:plan-wave-coverage-final-review` | supported |
| `ticket:planwv11#ACC-003` | `evidence:plan-wave-coverage-validation` shows guidance preserving ticket/packet authority and canonical owner surfaces | `critique:plan-wave-coverage-final-review` | supported |
| `ticket:planwv11#ACC-004` | `evidence:plan-wave-coverage-validation` records before/after searches, packet lifecycle wording, and `git diff --check` | `critique:plan-wave-coverage-final-review` | supported |
| `ticket:planwv11#ACC-005` | `critique:plan-wave-coverage-final-review` | oracle final re-critique passed with no findings | supported |

# Execution Notes

Likely touched surfaces include `skills/loom-plans/templates/plan.md`,
`skills/loom-plans/references/plan-shape.md`, and relevant Ralph/Git cross-links.

Ralph iteration `packet:ralph-ticket-planwv11-20260502T210325Z` is scoped to add
plan coverage mapping and parallel-wave independence checks.

Iteration output updated plan template/readiness guidance and `plan-shape.md`.
Evidence is recorded in `evidence:plan-wave-coverage-validation`. Live execution
state remains owned by this ticket; plan guidance now explicitly routes coverage
and waves without making plans own ticket progress.

Mandatory oracle critique `critique:plan-wave-coverage-review` returned
`changes_required` with four findings. Repair iteration
`packet:ralph-ticket-planwv11-20260502T211053Z` applied repairs for route/status
grammar, the wave example, the launch-notes owner wording, and stale packet
lifecycle text. Mandatory oracle re-critique is required before acceptance.

Oracle re-critique `critique:plan-wave-coverage-rereview` confirmed the original
four findings are resolved and opened two new record-grammar findings:
claim-matrix status normalization and repair-packet lifecycle wording. Repair
iteration `packet:ralph-ticket-planwv11-20260502T212006Z` is scoped to those two
issues.

Second repair iteration `packet:ralph-ticket-planwv11-20260502T212006Z`
normalized claim matrix status cells to the claim-coverage vocabulary, kept
repair narration in execution/disposition/evidence prose, and aligned the
iteration 2 packet body lifecycle wording with parent reconciliation. Mandatory
oracle re-critique remains required before acceptance.

Final oracle re-critique `critique:plan-wave-coverage-final-review` passed with no
findings and resolved all findings from the prior critiques.

# Blockers

None - tickets `rtvocab1`, `retrod3p`, and `pktgram5` are closed.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:cmdroute`.

# Route Readiness

Route: acceptance_review

Acceptance review readiness:
Evidence `evidence:plan-wave-coverage-validation` and final oracle critique
`critique:plan-wave-coverage-final-review` support closure with no findings.

# Evidence

Recorded: `evidence:plan-wave-coverage-validation` includes before/after searches
for `Execution Waves`, `write scope`, `claim coverage`, `child_write_scope`,
`parallel`, `None - reason`, repair observations for all four critique findings,
record-grammar repair observations for both re-critique findings, and
`git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: user requires oracle critique; plan guidance can authorize unsafe
parallel work.

Required critique profiles:

- routing-safety
- operator-clarity
- records-grammar

Findings:

- `critique:plan-wave-coverage-review#PLANWV11-CRIT-001` - medium, resolved by
  repair and `critique:plan-wave-coverage-final-review`.
- `critique:plan-wave-coverage-review#PLANWV11-CRIT-002` - medium, resolved by
  repair and `critique:plan-wave-coverage-final-review`.
- `critique:plan-wave-coverage-review#PLANWV11-CRIT-003` - low, resolved by repair
  and `critique:plan-wave-coverage-final-review`.
- `critique:plan-wave-coverage-review#PLANWV11-CRIT-004` - low, resolved by repair
  and `critique:plan-wave-coverage-final-review`.
- `critique:plan-wave-coverage-rereview#PLANWV11-RCRIT-001` - medium, resolved by
  repair and `critique:plan-wave-coverage-final-review`.
- `critique:plan-wave-coverage-rereview#PLANWV11-RCRIT-002` - low, resolved by
  repair and `critique:plan-wave-coverage-final-review`.
- `critique:plan-wave-coverage-final-review` - no findings; all prior findings
  resolved.

Disposition status: completed

Deferral / not-required rationale:

Not deferred. Mandatory oracle final re-critique passed with no findings.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Plan claim/acceptance coverage mapping and parallel-wave independence checks
  were promoted into `skills/loom-plans/templates/plan.md` and
  `skills/loom-plans/references/plan-shape.md`.
- Repair lessons for canonical claim-matrix status vocabulary and packet lifecycle
  honesty were applied to the ticket and packets for this work.

Deferred / not-required rationale:

Not deferred. The durable product lesson was promoted into the plan product
surfaces listed above; no separate wiki page, research record, spec,
constitution decision, or memory entry is needed.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation now lives in the
plan product surfaces.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T21:26:35Z
Basis: Ralph packets `packet:ralph-ticket-planwv11-20260502T210325Z`,
`packet:ralph-ticket-planwv11-20260502T211053Z`, and
`packet:ralph-ticket-planwv11-20260502T212006Z`; evidence
`evidence:plan-wave-coverage-validation`; final oracle critique
`critique:plan-wave-coverage-final-review` with no findings.
Residual risks: validation is structural and cannot guarantee future plan authors
will fill wave checks correctly.

# Dependencies

- `ticket:rtvocab1`
- `ticket:retrod3p`
- `ticket:pktgram5`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-011`.
- 2026-05-02T21:03:25Z: Started Ralph iteration
  `packet:ralph-ticket-planwv11-20260502T210325Z` from baseline
  `cb69ab9efdefbe4dabb9c86f34048687a0c8930e`.
- 2026-05-02T21:04:27Z: Ralph child updated plan guidance and recorded
  `evidence:plan-wave-coverage-validation`; ticket moved to `review_required`
  for mandatory oracle critique before acceptance.
- 2026-05-02T21:10:53Z: Mandatory oracle critique recorded
  `critique:plan-wave-coverage-review` with four findings; compiled repair Ralph
  iteration `packet:ralph-ticket-planwv11-20260502T211053Z`.
- 2026-05-02T21:12:04Z: Repair iteration applied all four critique finding
  repairs, refreshed `evidence:plan-wave-coverage-validation`, and returned the
  ticket to `review_required` for mandatory oracle re-critique.
- 2026-05-02T21:20:05Z: Oracle re-critique recorded
  `critique:plan-wave-coverage-rereview`; original findings were resolved, but
  two new record-grammar findings require repair iteration
  `packet:ralph-ticket-planwv11-20260502T212006Z`.
- 2026-05-02T21:21:53Z: Second repair iteration normalized claim matrix status
  cells, aligned repair-packet lifecycle body wording, refreshed evidence, and
  returned the ticket to `review_required` for mandatory oracle re-critique.
- 2026-05-02T21:26:35Z: Final oracle re-critique passed with no findings. Recorded
  acceptance and retrospective / promotion disposition; closed ticket.
