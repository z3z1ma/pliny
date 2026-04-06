---
{
  "created_at": "2026-03-31T12:00:00Z",
  "id": "constitution:main",
  "kind": "constitution",
  "links": {},
  "repository_scope": {
    "kind": "repository",
    "repository_id": "repo:root"
  },
  "schema_version": 1,
  "status": "active",
  "updated_at": "2026-04-06T06:53:44Z"
}
---

# Vision

Make Loom a harness-agnostic Markdown-defined operating protocol for durable AI work.

In this repository, that means `rules/`, `skills/`, canonical `.loom/` records, and the committed standalone `skills/*/scripts/*.py` files together form the visible source bundle for Loom's operating model.

Another agent should be able to enter this repository cold, read the corpus, and continue work without reconstructing hidden norms from chat history, private memory, or a hidden runtime.

# Principles

- Markdown canonical records are the source of truth.
- Rules remain always on.
- `constitution:main` must be read before starting work so local decisions stay aligned with durable project policy.
- Skills stay flat, self-contained, and subsystem-scoped.
- Packet-consuming work prefers fresh harness contexts.
- Tickets remain the sole execution ledger.
- Packets are bounded execution contracts, not transcript dumps.
- Parent workflow judgment and child bounded execution should remain explicitly separate.
- Scope and write authority must fail closed rather than being guessed.
- Important instructions should be stated positively and operationally before narrow prohibitions are added.
- The repository should teach another agent what to do next, not merely warn about what to avoid.

# Constraints

- no monolithic `loom` CLI
- no long-running orchestration service or canonical database at the center of the system
- no hidden shadow ontology in scripts
- no implicit widening of scope or write authority
- no canonical truth outside designated canonical `.loom/` subtrees
- strict structural validation with soft prose validation
- helpers should stay thin, deterministic, self-contained, and standard-library-first

This repository is a Markdown-first product with bundled Python helpers rather than a conventional application stack. Structural completeness without instructional clarity is not enough.

# Strategic Direction

Keep building Loom as a visible protocol corpus rather than as a hidden engine.

The repository now contains the first-pass doctrine set, appendix corpus, flat subsystem skills, committed standalone skill-local CLIs, and an initial canonical record set. The next durable direction is to turn that scaffold into a stronger constitutional record graph and a proven operational workflow set.

That means future work should keep rules, skills, canonical records, packet contracts, validation behavior, and acceptance gates visible in prose rather than only inferable from helpers or from `CONSTITUTION.md`.

The constitutional layer should also preserve the main architectural judgment frames already visible in the source memo: protocol over product runtime, explicit control-plane and data-plane boundaries, fresh-context packetized execution, and self-contained flat skill distribution.

# Current Focus

- reconcile the canonical constitution layer with `CONSTITUTION.md` and the repository's shipped structure
- expand canonical records beyond the seed constitution and one smoke-test ticket so more of the workflow is grounded in durable examples
- preserve the current shipped state truthfully: the rules corpus, appendix corpus, the current skill bundle, standalone skill-local CLIs, one roadmap, four active constitutional records, and only one smoke-test ticket so far
- exercise real Ralph, critique, and docs packet flows against current helpers and records
- tighten validation, link integrity, and workspace diagnostics only where they mechanize already-published rules

The immediate quality bar is no longer just that the files exist. The most important rules, skills, appendices, and canonical records should read like one coherent operating manual.

# Open Constitutional Questions

- when critique becomes mandatory by risk class
- whether reference-first or hermetic packets should become the default packet posture over time
- what the lightest acceptable contention model is for file-first multi-actor work
- how strict per-kind frontmatter and legal-link validation should become in deterministic helpers
- whether constitutional subtypes need more specialized template and validation support as the record graph grows
- how much packet freshness and acceptance logic should stay in prose versus move into deterministic validation

# Change History

- 2026-03-31: seeded canonical constitution for `agent-loom-2`
- 2026-03-31: expanded the constitutional statement to emphasize positive-first operational clarity as part of the protocol's core quality bar
- 2026-04-01: made reading `constitution:main` before starting work an explicit project rule
- 2026-04-01: reconciled `constitution:main` with `CONSTITUTION.md`, the shipped rules/skills/build layout, and new supporting decision and roadmap records
- 2026-04-01: expanded the constitutional baseline to capture control-plane/data-plane boundaries, self-contained flat skill distribution, and a sharper inventory of shipped repository state
- 2026-04-06: replaced the committed shared zipapp with committed standalone skill-local CLI files as the direct source of truth
