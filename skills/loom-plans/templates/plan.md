---
id: plan:<slug>
kind: plan
status: active
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
links: {}
---

# Purpose

Why this plan exists.

# Strategy

The overall route or approach.

# Strategy Snapshot

Current strategic picture only. Do not use this as a progress log; live state
belongs in tickets.

# Workstreams

Major streams or phases of execution strategy.

# Milestones

Execution-sequencing checkpoints. Do not use these as initiative outcome
metrics, roadmap commitments, or ticket progress state.

# Sequencing

Why the order looks the way it does.

# Claim / Acceptance Coverage

Map upstream initiative objectives, spec claim IDs, and ticket-local acceptance
criteria into downstream tickets. The plan routes claim coverage; tickets own live
coverage state, evidence disposition, and acceptance decisions.

| Source claim / acceptance ID | Downstream ticket | Coverage expectation | Evidence / critique route | Notes |
| --- | --- | --- | --- | --- |
| `<record>#<claim-or-ACC>` | `ticket:<token>` | What the ticket must cover | Expected evidence or critique | `None - reason` only when no claim-bearing source applies |

# Execution Waves

Use when multiple tickets can be sequenced or run independently from the plan.

Save-ready rule: remove unused wave examples and placeholder rows before saving.
Replace placeholders with real tickets, write scopes, and routes, or use a
meaningful `None - reason` when a wave or coverage item genuinely does not
apply; keep claim / acceptance coverage, evidence / critique route, readiness,
exit, and completion gates intact.

Do not require parallel execution by default. Before any sibling Ralph work runs
in parallel, record the independence and write scope overlap check here. Real
waves require a concrete non-overlap summary; write `None - reason` only when no
parallel wave applies.

Wave 1:

List real ticket IDs, why they can run independently, expected packet
`child_write_scope` or likely write scope, dependency/contention checks, and the
parent reconciliation route. If no wave applies, write `None - reason`.

Wave 2:

List real ticket IDs, dependencies on prior wave results, any changed write scope
overlap risk, and parent integration validation. If no wave applies, write
`None - reason`.

Wave readiness table:

| Wave | Tickets | Independent because | Expected `child_write_scope` / write scope overlap check | Dependency / shared-state check | Parent reconciliation |
| --- | --- | --- | --- | --- | --- |
| `Wave 1` | `ticket:<token-a>`, `ticket:<token-b>` | No same-wave dependency | `ticket:<token-a>` writes `<path-a>`; `ticket:<token-b>` writes `<path-b>`; no overlapping `child_write_scope` paths | No generated file, lockfile, migration, or stateful contention | Ticket-owned update plus evidence/critique route |
| No wave | `None - reason` | `None - reason` | `None - reason` | `None - reason` | Continue with sequential ticket route |

# Risks

What could break or distort the plan.

# Evidence Strategy

How the work under this plan should generally be evidenced or validated.

# Plan Readiness Review

Claim coverage:

Spec / acceptance coverage:

Placeholder scan:

Ticket-sized slices:

Likely write scopes:

Parallel / wave independence:

Expected packet `child_write_scope` / write scope overlap check:

Likely verification posture:

Evidence and critique route:

Stop / loopback conditions:

# Exit Criteria

What must be true before the plan can be considered complete or retired.

# Completion Basis

When `status: completed`, explain which exit criteria were met and where any
remaining execution truth lives.
