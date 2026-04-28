---
id: plan:objective-driven-parent-loop-skill
kind: plan
status: active
created_at: 2026-04-28T00:00:00Z
updated_at: 2026-04-28T00:00:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  research:
    - research:gastown-simplified-parent-driver
  specs:
    - spec:objective-driven-parent-loop
---

# Purpose

Define the execution route for adding objective-driven parent-loop behavior to
Loom without introducing scripts, daemons, or a hidden orchestration runtime.

# Strategy

Implement the behavior as visible protocol guidance first: a Loom skill or skill
reference surface that teaches the current agent how to run a high-level
objective through initiative/spec/plan/ticket/Ralph/evidence/critique/wiki loops.

The first product slice should be small enough to review: add the workflow
surface and a template or handoff shape for optional dedicated outer-loop
subagents. After that, add a golden example that proves the workflow can create a
new ticket tranche after an earlier tranche completes.

# Strategy Snapshot

The desired product behavior is now captured in
`spec:objective-driven-parent-loop`. The workflow will be implemented as a new
skill named `loom-drive`. The skill must remain a workflow coordinator over
existing owner layers, not a new truth layer.

# Workstreams

- Skill surface: create `skills/loom-drive/` and define activation, loop procedure, user-questioning posture,
  owner routing, and stop conditions.
- Outer-loop subagent handoff: define an optional bounded synthesis contract for
  fresh context without creating canonical truth outside Loom records.
- Cross-skill integration: link from workspace routing, plans slicing, Ralph
  parent/child guidance, tickets acceptance, and retrospective/wikis as needed.
- Example and review: add a golden trace and critique the workflow for scope
  creep, hidden runtime assumptions, and truth-owner drift.

# Milestones

- Milestone 1: Create the first `loom-drive` workflow surface.
- Milestone 2: Add optional outer-loop subagent handoff guidance or template.
- Milestone 3: Connect existing skills to the new route.
- Milestone 4: Add a golden example showing objective -> tranche -> Ralph ->
  reconciliation -> next tranche.
- Milestone 5: Run critique and reconcile findings.

# Sequencing

Start with the skill surface because it defines how the agent should behave when
the user sends a high-level request in chat. Add the optional subagent handoff
after the parent loop is clear enough to bound. Connect cross-skill references
after the target surface exists. Add examples and critique once the behavior is
reviewable.

# Execution Waves

Wave 1:

No tickets created yet. First ticket should cover one bounded product slice:
create the objective-loop skill/reference/template surface against
`spec:objective-driven-parent-loop`.

Wave 2:

After Wave 1, create follow-up tickets for examples, cross-skill reference
reconciliation, and critique fixes if they cannot fit safely in the first slice.

# Risks

- The workflow could accidentally become a new canonical layer instead of a route
  through initiatives, specs, plans, tickets, packets, evidence, critique, and
  wiki.
- The wording could imply a daemon or automatic background loop, violating the
  no-runtime constraint.
- A dedicated outer-loop agent could become a shadow owner if the parent does not
  reconcile its output into canonical records.
- The skill could encourage agents to invent product direction instead of asking
  the user at material tradeoff boundaries.
- The workflow could become too broad to execute or critique in one ticket.

# Evidence Strategy

Use structural evidence:

- diff review of new skill/reference/template surfaces
- targeted searches for forbidden runtime/daemon implications
- targeted searches for cross-surface links to the new workflow
- manual comparison against `spec:objective-driven-parent-loop`
- critique for protocol-boundary risk before acceptance

# Plan Readiness Review

Spec / acceptance coverage:

`spec:objective-driven-parent-loop` defines requirements and acceptance criteria.

Placeholder scan:

No placeholders are intended in downstream ticket work; ticket slices should name
concrete files and expected surfaces.

Ticket-sized slices:

The first slice should be skill creation or skill-reference creation only. Golden
examples and critique reconciliation can be separate slices if needed.

Likely write scopes:

- `skills/loom-drive/**`
- or targeted references under `skills/loom-workspace`, `skills/loom-plans`, and
  `skills/loom-ralph` if the behavior is distributed
- `.loom/tickets/**`, `.loom/evidence/**`, and `.loom/critique/**` for execution
  records
- `examples/**` only in a later example slice

Likely verification posture:

Observation-first or structural evidence. This is protocol behavior, not code
behavior, so tests are not expected unless a later optional harness adapter is
introduced.

Evidence and critique route:

Record structural validation as evidence and run critique because the workflow
affects operator behavior, scope, and completion boundaries.

Stop / loopback conditions:

Loop back to spec if the skill cannot define measurable objective satisfaction
or human-question boundaries. Loop back to constitution if the design needs a
daemon, required script, or new canonical layer.

# Exit Criteria

- The objective-driven parent loop has a visible product surface in `skills/`.
- The surface tells agents how to clarify objectives, create owner records,
  decompose tranches, execute with Ralph/subagents, reconcile truth, and continue
  or stop.
- Optional dedicated outer-loop subagent use is bounded and parent-reconciled.
- Existing routing surfaces point to the workflow where appropriate.
- A critique pass finds no unresolved medium/high findings or those findings are
  accepted as explicit follow-up work.

# Completion Basis

When `status: completed`, cite the ticket, evidence, critique, and any example
that proves the workflow landed.
