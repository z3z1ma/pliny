---
id: roadmap:bootstrap-the-markdown-first-protocol-corpus
kind: roadmap
status: active
created_at: 2026-04-01T17:45:00Z
updated_at: 2026-04-17T23:48:34Z
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

Turn this repository into an operational Loom protocol pack that another agent
can enter cold and use without transcript archaeology, helper-specific runtime
assumptions, or hidden command wrappers.

# Why Now

The product-level rewrite has already changed the protocol's public shape:
skills now teach templates and native recipes instead of shipping Python
scripts, YAML frontmatter replaces helper-oriented JSON frontmatter, and
`wiki`, `packets`, and `evidence` replace `docs`, `runs`, and `verification` as
the intended durable vocabulary.

What the repository does not yet have is full constitutional and dogfooded
record reconciliation to that rewrite. Some in-repo records and wrappers still
carry the old vocabulary or structure. This roadmap keeps the next stage
focused on that reconciliation and on real workflow proof rather than on
speculative platform growth.

Current shipped state at the time of this roadmap update:

- core doctrine files under `rules/` plus appendix support material under
  `rules/appendices/`
- flat subsystem skills and auxiliary authoring skills under `skills/`, each
  carrying references and templates
- no shipped `skills/*/scripts/*.py` files in the core Loom bundle
- top-level docs now describe YAML frontmatter, template-first record creation,
  and a native-tool operating posture
- optional harness-specific wrappers may still exist in-repo, but they are not
  part of the protocol core
- parts of the canonical `.loom/` dogfooding state still carry legacy
  `docs`/`runs`/`verification` naming and older frontmatter shape and should be
  reconciled

# Focus Areas

- keep this repository as the source tree for the portable Markdown-first Loom
  bundle
- maintain a populated constitutional layer grounded in the rewrite's actual
  protocol shape
- deepen canonical examples and durable records across the main Loom layers as
  real work appears
- reconcile legacy constitutional and dogfooded record vocabulary to
  `wiki`/`packets`/`evidence` and YAML frontmatter
- exercise real Ralph, critique, and wiki packet flows through templates and
  native Unix recipes rather than helper CLIs
- improve validation, scope, and link integrity guidance only when it
  mechanizes already-published rules
- make the current state legible enough that future agents can distinguish
  between shipped architecture, durable policy, and still-missing operational
  proof

# Milestones

1. Constitutional baseline
   Update `constitution:main`, the decision records, and the roadmap so they
   capture the template-first, native-tool rewrite explicitly.

2. Dogfooded record reconciliation
   Reconcile canonical `.loom/` examples and support records that still use the
   old vocabulary or frontmatter shape so the repository stops teaching two
   competing models.

3. Fresh-context workflow proof
   Run real bounded Ralph, critique, and wiki flows that exercise packet
   authoring, child execution, evidence capture, and parent reconciliation.

4. Acceptance hardening
   Tighten critique, wiki, freshness, and validation behavior using evidence
   from real flows instead of only from design intuition.

5. Optional accelerators
   Only after repeated real use, evaluate whether wrappers, indexes, or adapters
   earn their added complexity without becoming hidden ontology.

# Sequencing Assumptions

- do not treat speculative adapters or packaging growth as the next milestone
  while the canonical record graph is still thin
- use real packetized workflows to shape later validation and acceptance rules
- keep the protocol corpus visible and coherent before adding speed or
  convenience layers

# Downstream Work

An initiative/spec/plan/ticket chain now exists beneath this roadmap, but parts
of that graph still reflect pre-rewrite assumptions about command surfaces and
legacy vocabulary.

That graph should be reconciled before it is treated as the current durable
operator path.

The most important still-missing canonical depth is in:

- research records that capture option analysis and experiments
- initiative, spec, and plan records that bind strategic direction to execution
- critique, wiki, packets, and evidence artifacts produced by real packetized
  workflows

# Status Summary

The repository is past the earliest bootstrap stage: doctrine, skill-map,
template, query, and packet surfaces are present in source form, and the core
package no longer depends on shipped Python helpers.

The remaining work is to reconcile the constitutional and dogfooded record
layers fully to that rewrite and to prove the main workflows end to end with
real packet and evidence artifacts.

This roadmap is therefore active and focused on turning a rewritten static
corpus into a coherent and proven operational one.
