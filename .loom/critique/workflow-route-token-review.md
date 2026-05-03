---
id: critique:workflow-route-token-review
kind: critique
status: final
created_at: 2026-05-02T23:51:06Z
updated_at: 2026-05-02T23:51:06Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: "ticket:routewf10 diff 3bfbe92..working-tree"
links:
  ticket:
    - ticket:routewf10
  evidence:
    - evidence:workflow-route-token-validation
  packet:
    - packet:ralph-ticket-routewf10-20260502T234101Z
external_refs: {}
---

# Summary

Oracle critique for `ticket:routewf10` route-token alignment after the first
Ralph iteration.

# Review Target

Current working-tree diff from baseline
`3bfbe9226ecf2001fc5fd1d07d9efb999f8d156d`, covering shared route vocabulary,
dependent route-token lists/examples, ticket, evidence, and Ralph packet.

Required critique profiles: `routing-safety`, `operator-clarity`, and
`records-grammar`.

# Verdict

`changes_required` - two medium findings block acceptance until remediated or
ticket-dispositioned.

# Findings

## FIND-001: Downstream route guidance still has stale or incomplete route lists

Severity: medium
Confidence: high
State: open

Observation:

`skills/loom-tickets/references/readiness.md` still describes ready tickets as
routing to the older set and omits `debugging`, `spike`, `codemap`, and `ship` in
one introductory list. `skills/loom-tickets/templates/ticket.md` lists the new
tokens but its route-readiness prompts do not include readiness shapes for those
new workflow routes. Additional route-option prose in
`skills/loom-plans/references/slicing.md` and
`skills/loom-ralph/references/work-driver.md` still uses labels such as "Ralph
packet", "outer-loop refinement", and "acceptance" without clearly routing
through current tokens.

Why it matters:

This weakens `ticket:routewf10#ACC-002` because downstream route examples/lists
can still teach non-canonical or incomplete route choices.

Follow-up:

Update stale route lists or mark them as non-exhaustive prose that defers to
`skills/loom-records/references/route-vocabulary.md`. Add or reference readiness
guidance for `debugging`, `spike`, `codemap`, and `ship` in the ticket template.

Challenges:

- `ticket:routewf10#ACC-002`

## FIND-002: Route-decision priority can let `ralph` swallow workflow coordinator routes

Severity: medium
Confidence: medium
State: open

Observation:

`skills/loom-drive/references/tranche-decision-protocol.md` says the first true
condition wins, but the `ralph` row says "A ticket is Ralph-ready or needs fresh
bounded context" and appears before `debugging`, `spike`, and `codemap`. Those
workflows often also need bounded or fresh context and should win when diagnosis,
discovery, or mapping is the next governed move.

Why it matters:

The priority order risks implementation-first routing instead of reproduce-first
debugging, bounded discovery, or repository mapping.

Follow-up:

Narrow the `ralph` condition to bounded implementation packets or reorder/clarify
the workflow coordinator rows so `debugging`, `spike`, and `codemap` win when
those workflows own the next governed move.

Challenges:

- `ticket:routewf10#ACC-001`
- `ticket:routewf10#ACC-002`

# Evidence Reviewed

- Current `git status --short`, `git diff`, and `git diff --check`; `git diff
  --check` passed.
- Current HEAD `3bfbe9226ecf2001fc5fd1d07d9efb999f8d156d`.
- Target route vocabulary, ticket, workspace, drive, evidence, and Ralph packet
  files for `ticket:routewf10`.
- Route-token searches across `skills/`.
- Workflow skill surfaces for `loom-debugging`, `loom-spike`, `loom-codemap`, and
  `loom-ship`.

# Residual Risks

- Evidence is structural and search-based; it does not prove operator clarity.
- Evidence currently overstates downstream alignment until the open findings are
  resolved.

# Required Follow-up

Resolve `FIND-001` and `FIND-002`, rerun route-token checks and `git diff
--check`, then run mandatory oracle re-review before acceptance.

# Acceptance Recommendation

`follow-up-needed-before-acceptance`
