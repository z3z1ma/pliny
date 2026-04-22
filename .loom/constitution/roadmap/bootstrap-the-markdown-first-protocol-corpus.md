---
id: roadmap:bootstrap-the-markdown-first-protocol-corpus
kind: roadmap
status: active
created_at: 2026-04-01T17:45:00Z
updated_at: 2026-04-22T06:39:03Z
scope:
  kind: workspace
links:
  decision:
    - decision:0001
    - decision:0002
    - decision:0003
    - decision:0004
---

# Strategic Theme

Turn this repository into an operational Loom control-plane pack that another
agent can enter cold and use without transcript archaeology, helper-specific
runtime assumptions, hidden command wrappers, or competing truth ledgers.

# Why Now

The product-level rewrite changed the protocol's public shape: skills now teach
templates and native recipes instead of shipping Python scripts, YAML
frontmatter replaces helper-oriented JSON frontmatter, and `wiki`, `packets`,
and `evidence` replace `docs`, `runs`, and `verification` as the intended
durable vocabulary.

The strategic frame is now sharper: Loom is a Markdown-native control plane for
AI knowledge work. Its layer model is a source-of-truth type system, and Ralph
is the transaction protocol for bounded mutation by disposable worker contexts.

What the repository does not yet have is enough regularity around that model.
Some public docs still reference non-existent aggregate files, some dogfooded
records still carry legacy vocabulary, and several high-value workflows are
implicit rather than encoded as visible routes through existing layers.

This roadmap keeps the next stage focused on cutting the existing primitives
cleanly instead of turning Loom into a larger platform.

Current shipped state at the time of this roadmap update:

- core doctrine files under `rules/`
- flat subsystem skills and auxiliary authoring skills under `skills/`, each
  carrying references and templates
- workflow skills now exist for codebase atlas, debugging, spikes/sketches, and
  shipping, all routed through existing owner layers
- no shipped `skills/*/scripts/*.py` files in the core Loom bundle
- top-level docs now describe YAML frontmatter, template-first record creation,
  and a native-tool operating posture
- shared record guidance now covers lifecycle statuses, claim coverage,
  external references, packet freshness, and context budgets
- optional command wrappers cover map, debug, spike, sketch, and ship workflows
- optional harness-specific wrappers may still exist in-repo, but they are not
  part of the protocol core
- examples now provide protocol traces for representative routes
- parts of the canonical `.loom/` dogfooding state may still carry legacy
  record vocabulary or older frontmatter shape and should be reconciled when
  touched

# Focus Areas

- keep this repository as the source tree for the portable Markdown-native Loom
  protocol bundle
- preserve the anti-runtime boundary: harnesses may execute Loom, but they do
  not own Loom ontology
- fix public product-surface inconsistencies before adding new workflow
  surfaces
- reconcile legacy dogfooding vocabulary to `wiki`/`packets`/`evidence`,
  singular `.loom/memory`, and YAML frontmatter
- make non-ticket record lifecycles explicit enough that records age
  deliberately
- add claim-level coverage conventions so requirements, acceptance, tickets,
  packets, evidence, and critique can be traced with ordinary search
- make packet freshness and context-budget discipline inspectable
- express codebase atlas, debug, spike, sketch, ship, retrospective prevention,
  execution waves, and external reference provenance as routes through existing
  owner layers
- deepen canonical examples and golden traces so the protocol can be evaluated
  across harnesses without a runtime

# Milestones

1. Product-surface correction
   Align `README.md`, `INSTALL.md`, `AGENTS.md`, and architecture notes with the
   files that actually ship and with the control-plane framing.

2. Dogfooded record reconciliation
   Reconcile canonical `.loom/` examples and support records that still use old
   vocabulary or outdated frontmatter shape so the repository stops teaching
   two competing models.

3. Lifecycle grammar
   Add shared status lifecycle guidance for non-ticket records and reflect it
   in relevant templates and validation guidance.

4. Claim coverage
   Add acceptance and claim coverage conventions across specs, tickets,
   packets, evidence, and critique.

5. Packet discipline
   Add packet freshness and context-budget fields, and tighten parent launch
   checks around stale packets.

6. Review discipline
   Add named critique risk profiles and let tickets declare critique
   disposition without turning reviewers into separate layers.

7. Orientation and investigation workflows
   Add codebase atlas, debug, spike, and sketch workflows as orchestration over
   wiki, research, evidence, specs, tickets, Ralph, and critique.

8. Parallel and external coordination
   Add execution waves, external reference provenance, and path-scoped context
   adapter rules while preserving ticket truth and owner-layer authority.

9. Shipping and prevention
   Add `/loom-ship` packaging guidance and sharpen retrospective prevention so
   repeated mistakes promote into exactly one owner artifact.

10. Golden examples and protocol evals
    Add example traces that show correct routes, expected artifacts, final
    states, and common wrong behavior for representative workflows.

# Sequencing Assumptions

- fix inaccurate public guidance before building on top of it
- regularize statuses, coverage, packet freshness, and critique before adding
  broad workflow wrappers
- prefer one workflow surface that routes through existing layers over one new
  canonical layer
- use real packetized workflows to shape later validation and acceptance rules
- keep adapters, indexes, command wrappers, and external integrations secondary
  until repeated use proves they are worth their complexity
- do not let optional parallelism, generated context files, issue trackers, or
  PR packaging become competing execution ledgers

# Downstream Work

The first implementation pass has landed the product-surface correction,
lifecycle, coverage, packet freshness, critique profile, workflow command, and
golden-example scaffolding.

Existing initiative/spec/plan/ticket records may need reconciliation before
they are treated as the current durable operator path because parts of that
graph still reflect pre-rewrite assumptions about command surfaces and legacy
vocabulary.

The most important still-missing canonical depth is in:

- full dogfooded reconciliation of older initiative/spec/plan/ticket records
- deeper examples that include concrete starting `.loom` slices, not only
  protocol traces
- critique, wiki, packets, and evidence artifacts produced by real packetized
  workflows
- repair/status/accept command hardening against the new lifecycle and coverage
  grammar after real use

# Status Summary

The repository is past the earliest bootstrap stage: doctrine, skill-map,
template, query, and packet surfaces are present in source form, and the core
package no longer depends on shipped Python helpers.

The next phase is not platform expansion. It is protocol sharpening: make the
existing ownership graph more regular, traceable, reviewable, and testable with
ordinary Markdown and filesystem tools.

This roadmap remains active and now focuses on turning a rewritten static
corpus into a coherent, proven, and extensible control plane.
