---
id: initiative:skills-corpus-protocol-sharpening
kind: initiative
status: active
created_at: 2026-05-02T07:58:42Z
updated_at: 2026-05-02T07:58:42Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  roadmap:
    - roadmap:bootstrap-the-markdown-first-protocol-corpus
  research:
    - research:skills-corpus-council-review
  evidence:
    - evidence:skills-corpus-council-review
  plan:
    - plan:skills-corpus-protocol-sharpening
  ticket:
    - ticket:3uv5l5fh
---

# Objective

Make the shipped `skills/` corpus and its supporting public framing read as one
exceptionally precise Loom operating manual: self-contained, internally
consistent, hard to mis-route, and faithful to Loom's Markdown-native
source-of-truth model.

This initiative does not seek a new runtime, command layer, database, or hidden
orchestrator. It sharpens the existing protocol corpus so disposable agent
contexts can recover, execute, validate, review, and hand off work through Loom's
visible owner layers.

# Why Now

The council review of `skills/` found the corpus already strong, but also found
several high-leverage drifts and grammar gaps that matter precisely because
`skills/` is the product surface. If those gaps remain, future agents may still
infer the right behavior from context, but the corpus will not be as cold-start
recoverable, grep-checkable, or authority-safe as Loom's premise requires.

The active roadmap already says the next phase is protocol sharpening rather than
platform expansion. This initiative turns the council findings into one durable
outcome container so downstream plan and ticket work does not live only in chat.

# In Scope

- Reconcile README, protocol summary, architecture notes, bootstrap doctrine, and
  skills where the same Loom concept is currently framed differently.
- Surface `loom-drive` as a first-class workflow coordinator wherever skill maps
  and routing summaries enumerate workflow skills.
- Make cold-start and post-compaction recovery a workspace-entry behavior, not a
  side implication of `loom-drive` only.
- Tighten shared record grammar for objective coverage, valid `kind:` values,
  canonical ID/path forms, packet families, packet terminal statuses, risk/change
  class use, semantic link vocabulary, and external references.
- Improve operator ergonomics for scratchpad avoidance, concurrent file-first
  edits, rejected or overscoped Ralph results, follow-up ticket conversion, memory
  pruning, and pre-compaction checkpoints.
- Consolidate duplicated doctrine for atlas pages, retrospective mechanics, and
  spike/sketch variants under the owner skill that should teach each shape.
- Record structural evidence, critique findings, accepted risks, and follow-up
  boundaries before claiming the sharpening pass is accepted.

# Out Of Scope

- No required Loom CLI, daemon, MCP server, model router, dashboard, database, or
  background orchestration service.
- No new canonical owner layer for drive, resume, external references, scratch
  notes, handoffs, or retrospectives.
- No source-repo-only assumptions inside the shipped `skills/` corpus.
- No broad rewrite for tone alone. Editorial changes must reduce ambiguity,
  remove drift, improve routing, or strengthen validation.
- No treatment of internal examples as product-surface truth. Example updates may
  be proposed as follow-up if the protocol change makes fixtures stale, but this
  initiative is centered on `skills/` and public framing.
- No closure without evidence and mandatory critique disposition.

# Success Metrics

- OBJ-001: A fresh agent can read README plus `skills/loom-bootstrap` and recover
  the same layer model, canonical/support boundary, and workflow map that the
  skill corpus teaches.
- OBJ-002: The shared grammar in `loom-records` covers the record, coverage,
  packet, risk, external-reference, and semantic-link forms that downstream skills
  actually use.
- OBJ-003: Workspace entry and related workflow skills teach cold-start recovery,
  compaction recovery, scratchpad avoidance, and file-first concurrency in a way
  that prevents shadow truth without adding ceremony.
- OBJ-004: Duplicated atlas, retrospective, spike/sketch, packet, and metadata
  instructions have one clear owner surface, with other skills pointing rather
  than re-teaching competing variants.
- OBJ-005: Every high-risk protocol-authority edit in this sharpening pass is
  backed by structural evidence and mandatory critique before ticket acceptance.

# Milestones

1. Council findings are preserved as evidence and synthesized into reusable
   research.
2. A Loom plan sequences the sharpening work into safe implementation waves.
3. One detailed execution ticket owns the first comprehensive sharpening pass and
   makes critique, evidence, wiki, and follow-up gates explicit.
4. Public framing and skill maps are aligned with the actual shipped skill set and
   canonical/support boundary.
5. Shared record grammar is extended or clarified where the existing skills have
   outgrown the current references.
6. Workflow and operator ergonomics gaps are closed without turning them into new
   truth layers or command requirements.
7. Duplicated or drifting doctrine is consolidated under the proper owner skill.
8. Structural validation evidence and mandatory critique support acceptance, or
   unresolved issues are converted into linked follow-up tickets.

# Dependencies

- `constitution:main` owns the no-runtime, skills-only product-surface, and
  owner-layer authority constraints.
- `roadmap:bootstrap-the-markdown-first-protocol-corpus` owns the current protocol
  sharpening direction.
- `research:skills-corpus-council-review` synthesizes the council findings into
  reusable recommendations.
- `evidence:skills-corpus-council-review` records the observed council output that
  triggered this initiative.
- `plan:skills-corpus-protocol-sharpening` sequences execution.
- `ticket:3uv5l5fh` owns live execution state for the first comprehensive pass.

# Risks

- A large polish pass could accidentally change protocol authority without making
  the change class, evidence, and critique route explicit.
- Tightening grammar could make Loom feel heavier if examples and guardrails are
  not framed as useful recovery aids rather than bureaucracy.
- Adding resume and checkpoint guidance could create a second ledger if it is not
  routed through tickets, evidence, memory, and workspace entry correctly.
- Consolidating duplicated guidance could remove useful domain-specific nuance if
  owner surfaces are chosen carelessly.
- Editing bootstrap or record grammar could ripple across every skill; mandatory
  critique is required before acceptance.

# Linked Work

- Research: `research:skills-corpus-council-review`
- Evidence: `evidence:skills-corpus-council-review`
- Plan: `plan:skills-corpus-protocol-sharpening`
- Ticket: `ticket:3uv5l5fh`
- Roadmap: `roadmap:bootstrap-the-markdown-first-protocol-corpus`

# Status Summary

Council findings have been promoted out of chat into research and evidence. The
next owner for execution strategy is `plan:skills-corpus-protocol-sharpening`,
and the next live execution owner is `ticket:3uv5l5fh`. Implementation has not
started under this initiative.

# Completion Basis

When `status: completed`, cite the final ticket disposition, structural evidence,
mandatory critique verdict, any follow-up tickets created for accepted residual
work, and any wiki or retrospective promotion decision.
