---
{
  "created_at": "2026-04-01T17:45:00Z",
  "id": "roadmap:bootstrap-the-markdown-first-protocol-corpus",
  "kind": "roadmap",
  "links": {
    "decision": [
      "decision:0001",
      "decision:0002",
      "decision:0003",
      "decision:0004"
    ]
  },
  "repository_scope": {
    "kind": "repository",
    "repository_id": "repo:root"
  },
  "schema_version": 1,
  "status": "active",
  "updated_at": "2026-04-06T06:53:44Z"
}
---

# Strategic Theme

Turn this repository from a strong source architecture memo plus first-pass corpus into an operational, self-validating Loom protocol pack that another agent can enter cold and use without transcript archaeology.

# Why Now

The repository already contains the core rule set, appendix material, the current skill bundle, committed standalone skill-local CLIs, and an initial canonical record surface.

What it does not yet have is the same depth of durable canonical state and real end-to-end workflow proof across the major Loom layers. This roadmap keeps the next stage focused on that gap rather than on speculative platform growth.

Current shipped state at the time of this roadmap update:

- core doctrine files under `rules/` plus appendix support material under `rules/appendices/`
- flat subsystem skills and auxiliary authoring skills under `skills/`
- committed standalone `skills/*/scripts/*.py` files inside the skill bundle
- canonical `.loom/constitution/` records plus one smoke-test ticket under `.loom/tickets/`
- no populated canonical research, initiative, spec, plan, critique, docs, run, or verification record families yet

# Focus Areas

- keep this repository as the source tree for the portable Markdown-first Loom bundle
- maintain a populated constitutional layer grounded in `CONSTITUTION.md` and the current repository shape
- deepen canonical examples and durable records across the main Loom layers as real work appears
- exercise real Ralph, critique, and docs packet flows against the current helper layer
- improve validation, scope, and link integrity helpers only when they mechanize already-published rules
- make the current state legible enough that future agents can distinguish between shipped architecture, durable policy, and still-missing operational proof

# Milestones

1. Constitutional baseline
   Update `constitution:main` and seed durable decision and roadmap records that capture the locked architectural direction already reflected in the repository.

2. Canonical record depth
   Add stronger durable examples and real records across the `.loom/` subtrees so the record graph stops being mostly aspirational.

3. Fresh-context workflow proof
   Run real bounded Ralph, critique, and docs flows that exercise packet compilation, child execution, verification, and parent reconciliation.

4. Acceptance hardening
   Tighten critique, docs, freshness, and validation behavior using evidence from real flows instead of only from design intuition.

5. Optional accelerators
   Only after repeated real use, evaluate whether indexes or adapters earn their added complexity without becoming hidden ontology.

# Sequencing Assumptions

- do not treat speculative adapters or packaging growth as the next milestone while the canonical record graph is still thin
- use real packetized workflows to shape later validation and acceptance rules
- keep the protocol corpus visible and coherent before adding speed or convenience layers

# Downstream Work

No downstream initiative, spec, or plan graph exists yet beneath this roadmap.

`ticket:0001` exists as a smoke-test ticket, but it is a workflow example rather than the delivery vehicle for this roadmap. Real roadmap progress should eventually be expressed through linked specs, plans, research notes, and execution tickets.

The most important still-missing canonical depth is in:

- research records that capture option analysis and experiments
- initiative, spec, and plan records that bind strategic direction to execution
- critique, docs, runs, and verification artifacts produced by real packetized workflows

# Status Summary

The repository is past the earliest bootstrap stage: doctrine, skill-map, schema-reference, packet, and helper surfaces are substantially present in source form, including the committed standalone skill-local CLIs.

The work is still early in broader canonical record population and in real end-to-end execution proof. The constitutional layer now captures the major architectural judgment frames more clearly, but the broader record graph is still sparse.

This roadmap is therefore active and focused on turning a strong static corpus into a proven operational one.
