---
id: constitution:main
kind: constitution
status: active
created_at: 2026-03-31T12:00:00Z
updated_at: 2026-04-22T08:50:46Z
scope:
  kind: workspace
links: {}
---

# Vision

Make Loom a Markdown-native control plane for durable AI knowledge work.

Loom is not a runtime, daemon, model router, dashboard, MCP bundle, or product
CLI. It is a protocol that turns work into a typed artifact graph, then teaches
agents how to mutate that graph honestly with ordinary files.

The protocol core in this repository is `rules/`, `skills/`, their templates
and references, and the canonical examples that demonstrate them. Optional
harness wrappers may exist, but they do not define Loom's ontology.

Loom should not try to make agents smarter by stuffing more context into each
context window. It should make the work recoverable, bounded, reviewable, and
composable even when every individual agent context is disposable.

Another agent should be able to enter this repository cold, read the corpus,
and continue work without reconstructing hidden norms from chat history,
private memory, or a hidden runtime.

The deepest primitive is ownership-preserving mutation: every durable claim,
behavior, proof, risk, and explanation should land in the artifact layer that
owns that kind of truth.

# Principles

- Markdown canonical records are the source of truth.
- Loom is a source-of-truth type system plus a transaction protocol for AI
  work.
- The layer model is the type system: each layer owns one kind of truth, and
  ownership wins over recency.
- Ralph is the transaction protocol: a parent frames the next bounded mutation,
  a packet declares read/write/stop/output contracts, a fresh worker executes
  one slice, and the parent reconciles truth back into the ticket and related
  owners.
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
- New workflows should first be expressed as disciplined routes through
  existing owner layers, not as new canonical layers.
- Harnesses, adapters, command wrappers, external issue trackers, and generated
  context files may make Loom easier to execute. They must not become Loom's
  ontology or live ledger.
- Traceability should stay grep-friendly: stable IDs, typed links, explicit
  coverage, evidence, and critique references are preferred over hidden indexes.
- Important instructions should be stated positively and operationally before
  narrow prohibitions are added.
- The repository should teach another agent what to do next, not merely warn
  about what to avoid.

# Constraints

- no monolithic `loom` CLI
- no long-running orchestration service or canonical database at the center of
  the system
- no required dashboard, model-routing layer, MCP server, background daemon, or
  telemetry channel as the primary state surface
- no shipped Python scripts as a required part of the core Loom bundle
- no hidden shadow ontology in helpers, wrappers, or runtimes
- no requirement that a harness-specific `commands/` surface exist for Loom to
  make sense
- no implicit widening of scope or write authority
- no canonical truth outside designated canonical `.loom/` subtrees
- no external system, PR description, issue tracker, chat transcript, or
  path-local instruction file that silently outranks Loom records
- no generated `AGENTS.md` or equivalent context adapter that defines
  independent project truth instead of pointing to Loom owner records
- no helper-optimized JSON-frontmatter requirement in canonical record grammar
- strict structural validation with soft prose validation
- local automation should stay thin, inspectable, and subordinate to published
  doctrine

This repository is a Markdown-first protocol bundle built from rules, skills,
templates, references, and canonical records rather than from a conventional
application stack. Structural completeness without instructional clarity is not
enough.

# Strategic Direction

Keep building Loom as a visible protocol corpus and control plane rather than
as a hidden engine.

The rewrite established the anti-runtime posture: no shipped Python helpers,
templates and native Unix recipes in place of scaffolding CLIs, YAML
frontmatter instead of helper-oriented JSON frontmatter, and `wiki`, `packets`,
and `evidence` as the durable vocabulary for explanation, bounded work, and
proof.

The next durable direction is regularity. Loom should cut the existing
primitives sharper without making the system heavier in spirit:

- status lifecycles should be explicit across record kinds
- claim and acceptance coverage should connect specs, tickets, packets,
  evidence, and critique
- packet freshness and context budget should be inspectable
- critique should support named risk profiles
- codebase atlases should live in wiki/research/evidence, not in a new layer
- debug, spike, sketch, ship, and retrospective prevention workflows should be
  routes through existing owners
- execution waves should derive from `depends_on` and non-overlapping
  child write scopes
- external reference provenance should let GitHub, Jira, Linear, and similar
  systems mirror Loom without owning Loom truth
- golden examples should make the protocol evaluable across harnesses

Future work should keep rules, skills, templates, packet contracts, validation
behavior, and acceptance gates visible in prose and ordinary files rather than
only inferable from helper code, wrapper conventions, or external work systems.

# Current Focus

- keep public docs, always-on rules, skills, templates, optional commands, and
  examples aligned as one protocol corpus
- reconcile remaining canonical examples that still describe scripts, `docs`,
  `runs`, `verification`, or helper-oriented frontmatter
- prove the new lifecycle, claim coverage, packet freshness, execution wave,
  critique profile, external reference, map, debug, spike, sketch, ship, and
  retrospective-prevention guidance through real workflows
- keep the protocol kernel distinct from workflow packs, harness adapters, and
  optional utilities
- keep command wrappers thin enough that deleting them does not remove a Loom
  capability
- harden transaction boundaries: child write scope, parent merge scope,
  packet lifecycle, evidence validity, and critique finding disposition
- deepen durable examples across initiatives, research, specs, plans, tickets,
  critique, wiki, packets, and evidence so the protocol is shown, not only
  stated
- keep optional harness wrappers and external systems clearly secondary to
  rules, skills, and canonical records

The immediate quality bar is no longer just that the files exist. The most
important rules, skills, appendices, and canonical records should read like one
coherent operating manual.

# Open Constitutional Questions

- the exact allowed status sets for each non-ticket record kind
- how formal claim coverage IDs should become before they feel like ceremony
- which packet freshness fields are required versus optional in normal Ralph
  work
- when critique becomes mandatory by risk class, and which named profiles
  should exist first
- how codebase atlas pages should age and be re-verified without becoming
  behavior owners
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
- how much path-scoped context adapter generation is useful without creating
  shadow truth

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
- 2026-04-22: promoted the Markdown-native control-plane, typed ownership, and
  transaction-protocol framing into the constitutional direction and identified
  the next regularization priorities
- 2026-04-22: added first-pass protocol surfaces for lifecycle grammar, claim
  coverage, packet freshness, execution waves, critique profiles, external
  references, map/debug/spike/sketch/ship workflows, retrospective prevention,
  examples, and singular `.loom/memory`
- 2026-04-22: hardened the protocol/kernel boundary by moving command-owned
  procedures into skill references, quarantining optional utility skills, and
  tightening ticket, claim, packet, critique, evidence, structural checks, and
  versioning guidance
