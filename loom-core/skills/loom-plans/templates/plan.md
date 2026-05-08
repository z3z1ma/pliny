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

What someone gains when this plan succeeds, why the work matters, and how the
result should become observable. State why this needs more than one bounded ticket
or execution unit.

# Context And Orientation

Explain the current situation for a fresh agent. Link the governing initiative,
spec, research, decision, wiki, or ticket records. Define non-obvious terms. Name
important source areas, records, systems, interfaces, or constraints only when they
shape execution strategy.

# Strategy

The overall route. Explain why this decomposition and order fit the purpose,
constraints, and risks. Include the main rejected route if it is likely to recur.

# Planning Decisions

Execution-strategy decisions that future tickets should inherit. Do not use this as
a live decision log for implementation progress; ticket journals and owner records
own live updates.

- Decision:
  - Rationale:
  - Date / owner:
  - Owner-layer route if this stops being plan truth:

# Workstreams

Optional conceptual grouping for large work. Write `None - reason` when the work is
better understood directly as execution units. Workstreams are not tickets and not
progress state.

# Execution Units / Ticket Slices

Each unit should be detailed enough to become one ticket or a short staged sequence
of tickets. Prefer vertical slices that produce observable, reviewable progress.

## Unit: <unit name>

- Source claim / input:
- Observable outcome:
- Likely ticket: <ticket:<token> or proposed>
- Likely write scope:
- Dependencies / order reason:
- Verification / evidence target:
- Critique posture:
- Non-goals:
- Stop or loopback condition:

Repeat one `Unit` block per ticket-ready slice.

# Milestones

Narrative checkpoints across units. Each milestone should say what will exist at
the end that did not exist before, which units/tickets it contains, how it will be
validated, and what evidence or critique should be available. Do not use milestones
as live progress state.

## Milestone: <milestone name>

Scope:

Expected result:

Units / tickets:

Validation and evidence:

Acceptance checkpoint:

# Sequencing

Why the order looks this way. Name dependencies, risk ordering, and fail-fast choices.

# Claim / Acceptance Coverage

Map upstream initiative objectives, spec acceptance IDs, and ticket-local criteria
into downstream tickets. Tickets own live coverage state, evidence disposition,
and acceptance decisions.

- <TBD or None - reason>:
  - Downstream ticket: <ticket:<token> or proposed>
  - Coverage expectation: <what must be covered>
  - Evidence / critique expectation: <expected evidence/review>
  - Notes: <notes>

# Validation And Acceptance Strategy

How downstream tickets should prove the plan is working. Name expected commands,
manual observations, red/green checks, screenshots, traces, critique profiles, or
evidence records when known. Tickets own live evidence sufficiency and acceptance
decisions.

# Interfaces And Dependencies

External libraries, services, modules, schemas, APIs, records, migrations, data
sets, flags, or environment assumptions that shape execution. State why each
dependency matters and what downstream work should verify.

# Idempotence And Recovery

How this plan should remain safe to resume, retry, or partially roll back. Name
stateful resources, migrations, generated files, lockfiles, caches, flags, cleanup
routes, and where a fresh agent should look to recover current live state.

# Execution Waves

Optional. Use only when same-wave tickets can run independently or when sequential
waves need explicit dependency boundaries.

- <TBD or None - no wave needed>:
  - Tickets: <tickets>
  - Independent because: <non-overlap rationale>
  - Write-scope / shared-state check: <contention check>
  - Parent reconciliation: <merge/validation path>

# Risks And Loopbacks

What could break or distort the plan, and which owner layer should receive new
truth if execution discovers the plan is wrong.

# Supporting Artifacts And Notes

Concise links or excerpts that help future tickets execute: research conclusions,
evidence records, prototype notes, diagrams, command examples, or external sources.
Do not dump raw logs here; preserve observations in evidence and synthesis in
research or wiki.

# Plan Readiness Review

- Claim coverage:
- Execution units / ticket-sized slices:
- Context and orientation:
- Narrative milestones:
- Likely write scopes:
- Validation and acceptance strategy:
- Interfaces and dependencies:
- Idempotence and recovery:
- Parallel / wave independence:
- Stop / loopback conditions:

# Exit Criteria

What must be true before the plan can be considered complete or retired.

# Completion Basis

When `status: completed`, explain which exit criteria were met and where any
remaining execution truth lives.
