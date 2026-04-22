# Architecture Notes

This package is a reconstruction of Loom around its strongest ideas.

## What Loom Is Today

Loom is not best understood as a toolchain.

It is a **Markdown-native control plane for AI knowledge work** with these
defining properties:

- project truth lives in visible files
- the artifact graph is layered on purpose
- the layer model acts as a source-of-truth type system
- the outer loop shapes the work before execution starts
- the inner loop advances one bounded mutation at a time through fresh context
- Ralph acts as a transaction protocol for fallible worker contexts
- critique is first-class, not optional polish
- explanation should compound into durable knowledge, not vanish into chat
- the filesystem is already a graph database if you design the records properly

The older repository already contained those ideas.
What it still carried was a helper-script worldview that made the protocol feel more implementation-bound than it needed to be.

The key distinction is that Loom does not try to make each agent context
smarter by stuffing more context into it. Loom makes the work recoverable,
bounded, reviewable, and composable when individual contexts are disposable.

The deepest architectural invariant is ownership-preserving mutation: every
claim, behavior, proof, risk, and explanation should land in the artifact layer
that owns that kind of truth.

## The Main Architectural Moves In This Rewrite

### 1. Rules become stronger and fewer

The always-on rules are not generic etiquette.
They are the model's operating doctrine.

They teach:

- what Loom is
- which loop to use
- who owns what
- when a packet is required
- how critique and wiki fit
- which safety and honesty constraints are non-negotiable

### 2. Skills become full subsystem playbooks

Each skill now contains:

- a strong activation description
- operational posture
- stepwise execution guidance
- references for shape and review
- templates for the artifacts it owns

This is what replaces the old scaffolding scripts.
The model no longer calls a thin helper because it needs permission to think.
It reads the subsystem playbook and uses ordinary tools.

### 3. Templates replace record-creation CLIs

Every record kind that previously benefited from deterministic scaffolding now has a Markdown template.

That gives the agent three portable creation paths:

- copy the template and edit it
- render a here-doc directly
- generate the file with a short inline script if that is clearer

The protocol no longer depends on one helper implementation.

### 4. Packets become explicit Markdown contracts

The old repo already knew this in spirit.
This rewrite makes it unavoidable in form.

Packets are now plainly authored Markdown artifacts with sections for:

- mission
- bound context
- source snapshot
- task
- stop conditions
- output contract
- working notes
- child output
- parent merge notes

A packet is no longer just "what a script emits".
It is a first-class protocol object.

### 5. Truth ownership becomes explicit type discipline

Loom's layer model is not just folder organization.
It is the source-of-truth type system:

- constitution owns durable identity and constraints
- initiatives own strategic outcomes
- research owns investigated evidence and options
- specs own intended behavior and acceptance
- plans own sequencing
- tickets own live execution state
- packets own bounded child-worker contracts
- evidence owns proof artifacts
- critique owns adversarial findings
- wiki owns accepted explanation
- memory owns support context only

When records disagree, the owning layer wins for that kind of truth. Newer
files do not automatically outrank older owner records.

### 6. Docs evolves into Wiki

The old docs layer was close to a wiki but framed too narrowly.

The new wiki layer is for **persistent, interlinked accepted understanding**.

A good answer, workflow explanation, architecture note, comparison, or troubleshooting guide should not die in chat if future agents will need it again.
It should be promoted into `.loom/wiki/`.

### 7. Evidence becomes explicit

Structural verification and observed outputs still matter, but the more general and useful concept is evidence.

Evidence records are durable proof artifacts.
They justify progress, critique, and wiki pages without pretending to own project truth themselves.

### 8. Workflows stay routes, not new ontologies

Loom can express codebase maps, debugging, spikes, sketches, execution waves,
shipping, external reference provenance, and retrospective prevention without
adding new canonical layers.

The design rule is that a new workflow should route through the owner graph:
research for investigation, specs for intended behavior, plans for sequencing,
tickets for live execution, packets for bounded work, evidence for proof,
critique for adversarial review, and wiki for accepted explanation.

### 9. Examples make the protocol reviewable

The `examples/` tree contains golden traces, not runtime fixtures and not
canonical project truth.

Each example should show a starting `.loom` slice, operator request, expected
route, expected artifacts, final state, and common wrong behavior. That gives
contributors a way to review whether a protocol change preserves Loom's
intended shape across harnesses.

## Design Philosophy

This rewrite optimizes for:

- portability across harnesses
- legibility to a fresh agent
- durability of process knowledge
- freedom of implementation
- explicit truth ownership
- grep-friendly traceability
- small-scope iteration
- strong adversarial review
- knowledge compounding

It deliberately de-optimizes for:

- convenience wrappers that hide the method
- magical runtime behavior
- opaque helper scripts as a second ontology
- one-command "project management"
- external systems that become competing ledgers
- generated context files that define project truth independently of Loom

## The Intended User Experience

A future engineer should be able to install this package, load the rules, expose the skills, and have the agent operate with a disciplined methodology rather than a pile of prompts.

That is the point of Loom.
