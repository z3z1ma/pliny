---
id: constitution:main
kind: constitution
status: active
created_at: 2026-03-31T12:00:00Z
updated_at: 2026-04-17T23:48:34Z
scope:
  kind: workspace
links: {}
---

# Vision

Make Loom a harness-agnostic Markdown-defined operating protocol for durable
AI work.

In this repository, that means `rules/`, `skills/`, their templates and
references, and canonical `.loom/` records together form the visible source
bundle for Loom's operating model. Optional harness wrappers may exist, but
they do not define Loom's core protocol.

Another agent should be able to enter this repository cold, read the corpus,
and continue work without reconstructing hidden norms from chat history,
private memory, or a hidden runtime.

# Principles

- Markdown canonical records are the source of truth.
- Rules remain always on.
- `constitution:main` must be read before starting work so local decisions stay
  aligned with durable project policy.
- Skills stay flat, self-contained, and subsystem-scoped through Markdown,
  templates, and references rather than shipped scripts.
- Packet-consuming work prefers fresh harness contexts.
- Tickets remain the sole execution ledger.
- Packets are bounded execution contracts, not transcript dumps.
- Record creation, packet compilation, validation, and graph inspection are
  protocol behaviors taught in visible guidance, not hidden helper behavior.
- YAML frontmatter is the canonical human-editable metadata surface for Loom
  records.
- Templates plus native Unix recipes are the default creation and inspection
  path; optional automation stays derivative.
- Wiki is the persistent explanation layer, and evidence is the proof-artifact
  layer.
- Parent workflow judgment and child bounded execution should remain explicitly
  separate.
- Scope and write authority must fail closed rather than being guessed.
- Important instructions should be stated positively and operationally before
  narrow prohibitions are added.
- The repository should teach another agent what to do next, not merely warn
  about what to avoid.

# Constraints

- no monolithic `loom` CLI
- no long-running orchestration service or canonical database at the center of
  the system
- no shipped Python scripts as a required part of the core Loom bundle
- no hidden shadow ontology in helpers, wrappers, or runtimes
- no requirement that a harness-specific `commands/` surface exist for Loom to
  make sense
- no implicit widening of scope or write authority
- no canonical truth outside designated canonical `.loom/` subtrees
- no helper-optimized JSON-frontmatter requirement in canonical record grammar
- strict structural validation with soft prose validation
- local automation should stay thin, inspectable, and subordinate to published
  doctrine

This repository is a Markdown-first protocol bundle built from rules, skills,
templates, references, and canonical records rather than from a conventional
application stack. Structural completeness without instructional clarity is not
enough.

# Strategic Direction

Keep building Loom as a visible protocol corpus rather than as a hidden engine.

The rewrite now pushes Loom further toward visible protocol behavior: no shipped
Python helpers, templates and native Unix recipes in place of scaffolding CLIs,
YAML frontmatter instead of helper-oriented JSON frontmatter, and `wiki`,
`packets`, and `evidence` as the durable vocabulary for explanation, bounded
work, and proof.

The next durable direction is to finish reconciling the constitutional layer,
dogfooded canonical examples, and remaining repository guidance to that rewrite
so a future agent sees one coherent model instead of a mix of legacy and new
shapes.

Future work should keep rules, skills, templates, packet contracts, validation
behavior, and acceptance gates visible in prose and ordinary files rather than
only inferable from helper code or wrapper conventions.

# Current Focus

- reconcile remaining constitutional and canonical examples that still describe
  scripts, `docs`, `runs`, `verification`, or helper-oriented frontmatter
- deepen durable examples across initiatives, research, specs, plans, tickets,
  critique, wiki, and evidence so the rewritten protocol is shown, not only
  stated
- exercise real Ralph, critique, and wiki packet flows using templates and
  native Unix recipes rather than bundled helpers
- keep optional harness wrappers clearly secondary to rules, skills, and
  canonical records
- tighten validation, query guidance, and workspace diagnostics only where they
  mechanize already-published rules

The immediate quality bar is no longer just that the files exist. The most
important rules, skills, appendices, and canonical records should read like one
coherent operating manual.

# Open Constitutional Questions

- when critique becomes mandatory by risk class
- how much optional harness sugar should exist outside the core package without
  becoming a second protocol surface
- how prescriptive Loom's shared query recipes should become while preserving
  native-tool freedom
- whether reference-first or hermetic packets should become the default packet
  posture over time
- what the lightest acceptable contention model is for file-first multi-actor
  work
- how much validation and audit logic should stay as visible recipes versus
  move into optional automation without creating dependency
- whether constitutional subtypes need more specialized template and validation
  support as the record graph grows
- how much packet freshness and acceptance logic should stay in prose versus
  move into more standardized reusable checks

# Change History

- 2026-03-31: seeded canonical constitution for `agent-loom-2`
- 2026-03-31: expanded the constitutional statement to emphasize positive-first
  operational clarity as part of the protocol's core quality bar
- 2026-04-01: made reading `constitution:main` before starting work an explicit
  project rule
- 2026-04-01: reconciled `constitution:main` with `CONSTITUTION.md`, the
  shipped rules/skills/build layout, and new supporting decision and roadmap
  records
- 2026-04-01: expanded the constitutional baseline to capture
  control-plane/data-plane boundaries, self-contained flat skill distribution,
  and a sharper inventory of shipped repository state
- 2026-04-06: replaced the committed shared zipapp with committed standalone
  skill-local CLI files as the direct source of truth
- 2026-04-07: clarified that `constitution:main` is workspace-scoped and that
  nested repositories bind work through explicit scope fields instead of child
  `.loom/` trees
- 2026-04-17: updated the constitutional layer for the rewrite to
  template-first, native-tool Loom with YAML frontmatter and
  `wiki`/`packets`/`evidence` vocabulary
