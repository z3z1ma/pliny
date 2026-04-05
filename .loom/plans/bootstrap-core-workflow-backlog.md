---
{
  "created_at": "2026-04-04T23:57:49Z",
  "id": "plan:bootstrap-core-workflow-backlog",
  "kind": "plan",
  "links": {
    "initiative": [
      "initiative:prove-core-loom-workflow"
    ],
    "spec": [
      "spec:minimum-proven-core-workflow-surface"
    ],
    "ticket": [
      "ticket:0003",
      "ticket:0004",
      "ticket:0005"
    ]
  },
  "repository_scope": {
    "kind": "repository",
    "repository_id": "repo:root"
  },
  "schema_version": 1,
  "status": "active",
  "updated_at": "2026-04-04T23:58:09Z"
}
---

# Purpose / Big Picture

Turn the repository's early bootstrap state into a proven core workflow path.

This plan sequences three increments: first prove one bounded Ralph -> critique
-> docs slice, then expose the resulting operator path through command entry
points, then tighten helper validation and diagnostics around the exercised
workflow.

# Progress

- 2026-04-04: created `initiative:prove-core-loom-workflow`,
  `spec:minimum-proven-core-workflow-surface`, this plan, and three linked
  backlog tickets.
- No execution has landed yet; the backlog is now framed and ordered.

# Surprises & Discoveries

- The repository already has create scripts for most canonical record kinds, so
  the more important near-term gap is command entry points and workflow proof,
  not raw create-script coverage.
- The canonical record graph was thinner than the constitution's current-focus
  language implied: there was no initiative or spec yet for the next workflow
  slice.
- The current command surface is much narrower than the overall product surface,
  which makes operator discovery harder than it should be.

# Decision Log

- 2026-04-04: prioritize one real proof flow before expanding commands or
  validation so later additions are informed by observed workflow behavior.
- 2026-04-04: keep the next backlog bounded to three tickets instead of opening
  a wide umbrella of speculative follow-ups.
- 2026-04-04: tie validation hardening only to failures or ambiguities exposed
  by the proof slice so helper logic continues to mechanize visible rules.

# Outcomes & Retrospective

This plan is still pre-execution.

Its current value is strategic: another agent can now see the intended order,
why that order exists, and which tickets own the live work.

# Context and Orientation

`constitution:main` says the next durable direction is to expand canonical
records, exercise real Ralph, critique, and docs flows, and tighten validation
only where it mechanizes published rules.

The repository has already completed one documentation-oriented slice for shared
CLI references in `ticket:0002`. The next step should move from better static
explanation to proving the actual workflow path.

# Milestones

1. Durable record chain in place for the next workflow slice.
2. One end-to-end proof flow executed and reconciled.
3. Minimal command entry points added for the proved operator path.
4. Validation and diagnostics tightened around the exercised path.

# Plan of Work

Start with one small, low-risk proof target inside `repo:root` so the workflow
can be exercised without widening scope or inventing new architecture. Use that
proof to decide what command entry points are actually necessary, then harden
validation only after the concrete flow reveals where operators or helpers still
fail.

# Concrete Steps

1. Advance `ticket:0003` on one small shipped change that benefits the product
   bundle.
2. Keep the execution packet bounded and explicit about scope, trust boundary,
   and allowed writes.
3. Reconcile the execution outcome into the ticket, critique surface, docs
   disposition, and verification evidence.
4. Use that proved path to scope the minimal command set in `ticket:0004`.
5. Add or update only the command files and references needed to make the path
   discoverable.
6. Use observed workflow failures and ambiguities to scope `ticket:0005`.
7. Run structural verification after each landed slice.

# Validation and Acceptance

- record validation should pass for the new initiative, spec, plan, and tickets
- link validation should remain clean as the graph expands
- proof-flow work should include the repo's standard structural checks such as
  `build/assemble-skills.py`, `ruff check`, `validate_record.py`,
  `check_links.py`, and `diagnose_workspace.py` as relevant to the changed
  surfaces
- acceptance should follow the normal Loom order: scope, verification,
  canonical reconciliation, critique need, and docs need

# Idempotence and Recovery

Each milestone is resumable because the strategy lives here while live progress
stays in the linked tickets.

If the proof slice fails or blocks, the next actor should update `ticket:0003`
instead of rewriting the plan. If command or validation follow-up proves
unnecessary after the proof slice, close or cancel those tickets explicitly
rather than quietly letting them drift.

# Artifacts and Notes

- Governing initiative: `initiative:prove-core-loom-workflow`
- Governing spec: `spec:minimum-proven-core-workflow-surface`
- Primary execution ticket: `ticket:0003`
- Follow-up command ticket: `ticket:0004`
- Follow-up validation ticket: `ticket:0005`
- Existing related completed slice: `ticket:0002`

# Interfaces and Dependencies

- Product surfaces likely touched by this plan: `src/commands/`, `src/skills/`,
  and related `references/` material
- Helper surfaces likely touched by the validation slice: `build/shared/_loom_lib/`
  and `build/shared/scripts/`
- Canonical reconciliation surfaces likely touched by the proof slice:
  `.loom/tickets/`, `.loom/critique/`, `.loom/docs/`, `.loom/runs/`, and
  `.loom/verification/`

# Linked Tickets

- `ticket:0003` - exercise one end-to-end proof flow
- `ticket:0004` - add core slash-command entry points
- `ticket:0005` - harden packet, scope, and workspace validation

# Risks and Open Questions

- the first proof target may still be too large unless deliberately constrained
- command design may sprawl unless grounded in the proved path
- validation changes may get ahead of the doctrine if the team is not careful
- the repo still needs later decisions about packet defaults and critique policy

# Revision Notes

- 2026-04-04: created the plan to turn the current prioritization into one
  bounded proof slice followed by command and validation hardening.
- 2026-04-04: recorded the discovery that create scripts already exist for most
  canonical kinds, which shifted the follow-up focus toward command entry points
  and proof-flow execution.
