---
{
  "created_at": "2026-04-04T23:57:48Z",
  "id": "initiative:prove-core-loom-workflow",
  "kind": "initiative",
  "links": {
    "plan": [
      "plan:bootstrap-core-workflow-backlog"
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

# Objective

Establish a proven, package-local Loom maintainer path from canonical record
framing through one fresh-context proof run and the follow-up command and
validation hardening that should emerge from that proof.

# Why Now

The repository already has a strong doctrine corpus, skill bundle layout, and a
thin helper layer, but the durable execution graph is still early: one
constitution, one active plan, two tickets, no initiatives or specs, and only
memory-oriented slash commands. The next highest-value work is to prove the main
protocol path rather than add more disconnected surfaces.

# In Scope

- add one strategic initiative/spec/plan/ticket chain for the next workflow
  slice
- execute one real root-repository Ralph -> critique -> docs proof flow on a
  small shipped change
- add a minimal set of slash-command entry points for the canonical workflows
  operators reach first
- tighten structural validation where the exercised flow exposes rule-backed
  gaps in scope, packets, links, or workspace diagnostics

# Out of Scope

- a monolithic `loom` CLI or long-running orchestration service
- speculative multi-repository automation beyond fail-closed scope rules
- broad runtime features outside the shipped Markdown-first bundle
- validation rules that invent policy not already visible in doctrine

# Success Metrics

- a future agent can read the initiative, spec, plan, and three tickets and
  understand the intended sequence without transcript context
- one bounded proof slice lands through execution, critique, docs disposition,
  and ticket reconciliation
- `src/commands/` exposes a small core workflow surface beyond the two current
  memory commands
- helper validation and diagnostics catch the main structural failures surfaced
  by the proof slice

# Milestones

1. Seed the durable record chain for the next workflow slice.
2. Prove one end-to-end Ralph -> critique -> docs path on a small repo-local
   target.
3. Expose the resulting operator path through a minimal command surface.
4. Harden validation and diagnostics around the exercised path.

# Dependencies

- current doctrine and `constitution:main` remain the governing source of truth
- existing critique, docs, Ralph, plans, specs, and tickets skills remain
  package-local and self-contained
- helper changes stay standard-library-only and continue to mechanize visible
  rules instead of introducing hidden workflow logic

# Risks

- overdesigning the workflow before one small slice is proven
- adding too many command entry points before the minimal set is clear
- tightening validation faster than the written doctrine can support
- choosing a proof target that is too large to run cleanly in one bounded fresh
  context

# Linked Specs, Plans, and Tickets

- Spec: `spec:minimum-proven-core-workflow-surface`
- Plan: `plan:bootstrap-core-workflow-backlog`
- Ticket: `ticket:0003` - prove one end-to-end flow
- Ticket: `ticket:0004` - add core command entry points
- Ticket: `ticket:0005` - harden structural validation

# Status Summary

This initiative now owns the next three increments for the repository's main
workflow maturation. `ticket:0003` is the first ready execution slice. `ticket:0004`
and `ticket:0005` are sequenced follow-up tickets that should stay bounded by
what the proof slice actually teaches.
