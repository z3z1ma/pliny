# Markdown-First Pi Loom

## Status

This document is no longer just an exploratory memo.

It is a consolidated architecture/specification draft for a fresh independent Loom spike built around:

- Markdown-canonical records in designated canonical subtrees of `.loom/`
- always-on Loom doctrine in `src/rules/`
- flat sibling subsystem skills in `src/skills/`
- self-contained skill distribution
- packetized fresh-context execution
- tickets as the sole execution ledger
- direct harness invocation via command shapes documented in skills
- no monolithic `loom` product CLI as the center of the system

This document is intentionally verbose.
Its purpose is to turn the Loom idea into a portable, inspectable, coherent operating system for long-horizon AI work.

---

## Locked direction

These decisions are treated as settled unless explicitly reopened:

- this is a fresh Loom spike, not a migration plan from current `pi-loom` (~/code_projects/pi-loom)
- Markdown records in designated canonical `.loom/` subtrees are canonical from day 1
- always-on cross-cutting doctrine lives in `src/rules/`
- subsystem detail lives in flat sibling skills under `src/skills/`
- distributed skills must be self-contained, with standalone script behavior committed directly inside each skill
- packet-consuming flows such as Ralph, critique, and docs update run in fresh harness contexts
- the parent agent invokes the harness directly via bash using the command shape documented in the relevant skill
- tickets remain the sole execution ledger
- packets persist by default
- packet provenance must be explicit
- hermetic packet mode is a first-class option
- no monolithic `loom` product CLI should become the center of the system

---

## Normative language

This document uses the following words in the RFC sense:

- **MUST** / **MUST NOT** — required
- **SHOULD** / **SHOULD NOT** — recommended default with valid exceptions
- **MAY** — optional

Where exploratory language remains, it is intentional and should be read as a design area still under evaluation.

---

# 1. Executive thesis

The most portable future for Loom is not “Loom rewritten in Markdown” in a naive sense.

It is:

- Loom as a protocol defined in Markdown
- Loom records represented as Markdown artifacts
- Loom runbooks, trust boundaries, and packet rules expressed as Markdown instructions
- a very small deterministic helper layer for the things models still do unreliably
- optional richer adapters as operational conveniences, not as the definition of the system

Shortest version:

**Loom should evolve from an implementation into a protocol.**

Even shorter:

**Markdown should become the ABI.**

That means:

- the protocol is visible, inspectable, editable, and portable
- the canonical project truth is inspectable in the repository
- the runtime is optional, swappable, and thin
- the most important product asset is not a package, but a durable operating discipline for long-horizon AI work

What this preserves from Loom’s current strengths:

- layered coordination
- durable context
- packetized fresh-context execution
- explicit review and documentation steps
- truthful boundaries between policy, evidence, strategy, contracts, execution, review, and explanation

What this improves:

- harness portability
- inspectability
- debuggability
- user trust
- skill-based distribution
- future reimplementation freedom

---

# 2. Architectural invariants

These invariants are the backbone of Markdown-first Loom.

## 2.1 Truth hierarchy

Loom MUST distinguish between:

1. always-on doctrine
2. subsystem operating instructions
3. canonical Markdown records
4. compiled packets and run artifacts
5. derived summaries, reports, caches, and projections

Those are not interchangeable.

## 2.2 Tickets are the execution ledger

Tickets MUST remain the sole canonical ledger of live execution state.

Plans do not own execution truth.
Run artifacts do not own execution truth.
Critiques do not own execution truth.
Docs do not own execution truth.

They may influence or summarize execution state.
They do not replace the ticket ledger.

## 2.3 Fresh context beats transcript accumulation

Packet-consuming work SHOULD run in a fresh harness context.

Loom assumes that bounded work launched from a curated packet is more reliable than a long-lived agent transcript accumulating unstructured history.

## 2.4 Rules define doctrine; skills define conditional practice

`src/rules/` MUST carry always-on Loom doctrine.

Skills MUST carry subsystem-specific instructions, references, examples, and local helper scripts.

Core doctrine MUST NOT depend on conditional skill hydration.

## 2.5 Code mechanizes visible rules

Helper scripts MUST mechanize rules that are already visible in Markdown.

They MUST NOT become a shadow ontology.

## 2.6 Scope must fail closed

If repository or worktree identity is ambiguous, Loom MUST NOT guess.

## 2.7 Packets are bounded execution contracts

A packet is not merely a context dump.

A packet MUST declare:

- target
- scope
- objective
- constraints
- verification expectations
- stop conditions
- provenance
- trust boundary

## 2.8 Canonical records must remain human-legible

Markdown records MUST be machine-structured and human-readable.
They MUST NOT devolve into metadata-only blobs or transcript dumps.

---

# 3. Why this direction makes sense now

## 3.1 The leverage has moved upward

For current frontier models, quality depends increasingly on:

- explicit scope definition
- instruction hierarchy
- packet quality
- deterministic helper tools
- verification discipline
- structured outputs
- trust boundaries
- clear separation between durable state and bounded execution context

These are mostly protocol problems, not framework problems.

## 3.2 The portable thing is the work discipline

The part of Loom most likely to survive model churn is not:

- the exact package structure
- the exact storage API
- the exact runtime wiring

It is:

- what each layer means
- what each layer owns
- how context is compiled for fresh runs
- how work resumes without transcript archaeology
- how verification gates acceptance

## 3.3 Current Loom already points here

Current Pi Loom already encodes the most important ideas:

- collaborative preparation before bounded execution
- explicit packetization
- layer honesty
- durable truth separate from exports
- fail-closed multi-repo behavior
- separate critique and docs layers

Markdown-first Loom is therefore not a random reinvention.
It is an extraction and simplification of the existing discipline.

---

# 4. Control plane vs data plane

This distinction should be explicit.

## 4.1 Control plane

The control plane decides:

- whether Loom should activate
- which subsystem owns the task
- which skill should hydrate
- which packet mode is allowed
- whether fresh-context execution is mandatory
- what write-back is allowed
- what acceptance gate applies

The control plane is expressed through:

- always-on rules
- skill trigger descriptions
- packet doctrine
- verification doctrine
- scope doctrine

## 4.2 Data plane

The data plane contains the project’s durable and derived artifacts:

- canonical records in designated canonical `.loom/` subtrees
- durable but non-canonical packet files
- durable but non-canonical run artifacts
- durable verification artifacts
- optional indexes/caches
- derived summaries/reports

### 4.2.1 Canonical vs durable artifact subtrees

Loom SHOULD explicitly separate:

- canonical truth subtrees such as `.loom/constitution`, `.loom/research`, `.loom/initiatives`, `.loom/specs`, `.loom/plans`, `.loom/tickets`, `.loom/critique`, `.loom/docs`
- durable but non-canonical artifact subtrees such as `.loom/runs` and `.loom/verification`

Being inside `.loom/` does not automatically make an artifact canonical truth.

## 4.3 Why the distinction matters

Without this distinction, systems drift into hidden behavior.

Loom’s control plane MUST remain visible in Markdown.
Its data plane MUST remain inspectable and reconstructable.

---

# 5. Layer model

The cleanest Loom architecture is not three layers but five.

## 5.1 Layer 1 — Doctrine

Always-on rules in `src/rules/`.

This is the permanent cross-cutting operating doctrine.

It defines:

- what Loom is
- when Loom applies
- truth hierarchy
- authority hierarchy
- scope doctrine
- packet doctrine
- verification doctrine
- security doctrine
- anti-drift rules

## 5.2 Layer 2 — Skills

Flat sibling subsystem skills under `src/skills/`.

Each skill defines:

- subsystem contract
- trigger conditions
- local references
- local examples
- helper scripts needed for that subsystem
- harness command shapes if that subsystem launches fresh child runs

## 5.3 Layer 3 — Canonical records

Markdown records in designated canonical `.loom/` subtrees.

These are the durable project truth.

## 5.4 Layer 4 — Packets and runs

Compiled, provenance-bearing handoff artifacts for fresh child runs.

This layer includes:

- packet files
- Ralph run artifacts
- critique run artifacts
- docs-update run artifacts
- verification evidence references

This layer is durable but non-canonical for execution truth.
It may live under `.loom/`, but it does not outrank canonical record subtrees.

## 5.5 Layer 5 — Distribution and build

A thin build layer that assembles self-contained skill bundles and validates pack integrity.

This layer is packaging, not ontology.

## 5.6 Optional adapter layer

Adapters MAY exist later for:

- local SQLite indexes
- search acceleration
- GitHub/Linear/Jira integration
- MCP wrappers
- shared multi-user coordination

Adapters MUST remain derivative unless explicitly promoted by a future design.

---

# 6. Authority and truth hierarchy

Loom needs an explicit authority model.

## 6.1 Authority order for execution behavior

For any child run, authority SHOULD be interpreted in this order:

1. harness/system/operator constraints
2. always-on Loom doctrine in `src/rules/`
3. relevant subsystem skill
4. explicit packet instruction blocks
5. canonical record content included as context
6. derived summaries or reports
7. quoted external text

Record contents are not higher-priority instructions.

## 6.2 Truth order for project state

Project truth SHOULD be interpreted in this order:

1. canonical records in `.loom/`
2. accepted verification evidence linked from canonical records
3. run artifacts and packets
4. derived reports and caches
5. local scratch notes or ephemeral outputs

## 6.3 Why this must be explicit

Without a declared hierarchy, packetized systems are vulnerable to:

- prompt injection
- role confusion
- shadow ledgers
- false completion claims
- accidental authority inversion

---

# 7. Repository shape

## 7.1 Top-level repository layout

```text
src/
  rules/
    loom.md
    layers.md
    truth-hierarchy.md
    packet-doctrine.md
    execution-doctrine.md
    verification-doctrine.md
    scope-doctrine.md
    security-doctrine.md
    appendices/

  skills/
    loom-constitution/
      SKILL.md
      references/
        schema-constitution.md
        examples.md
      scripts/

    loom-research/
      SKILL.md
      references/
        schema-research.md
        examples.md
      scripts/

    loom-initiatives/
      SKILL.md
      references/
        schema-initiatives.md
        examples.md
      scripts/

    loom-specs/
      SKILL.md
      references/
        schema-specs.md
        examples.md
      scripts/

    loom-plans/
      SKILL.md
      references/
        schema-plans.md
        examples.md
      scripts/

    loom-tickets/
      SKILL.md
      references/
        schema-tickets.md
        examples.md
      scripts/

    loom-ralph/
      SKILL.md
      references/
        schema-ralph.md
        packets.md
        harness-invocation.md
        examples.md
      scripts/

    loom-critique/
      SKILL.md
      references/
        schema-critique.md
        critique-invocation.md
        examples.md
      scripts/

    loom-docs/
      SKILL.md
      references/
        schema-docs.md
        docs-invocation.md
        examples.md
      scripts/

    loom-workspace/
      SKILL.md
      references/
        status.md
        doctor.md
      scripts/

build/
  assemble-skills.py
  manifest.json
```

## 7.2 Canonical workspace layout

```text
.loom/
  # canonical truth subtrees
  constitution/
    constitution.md
    decisions/
    roadmap/
  research/
  initiatives/
  specs/
  plans/
  tickets/
  critique/
    findings/
  docs/

  # durable but non-canonical artifact subtrees
  runs/
    ralph/
    critique/
    docs/
  verification/
```

Only the canonical truth subtrees are canonical project state.
`runs/` and `verification/` are durable supporting artifacts.

## 7.3 Build/distribution principle

Source authoring SHOULD stay direct and skill-local.
Distributed skills MUST be self-contained.

That means a loaded skill MUST NOT require another skill just to function.

---

# 8. Operating model

## 8.1 When Loom activates

Loom SHOULD activate whenever work has durable consequences or requires resumability.

Typical triggers:

- changing durable policy or direction
- storing research or reusable findings
- defining or revising a spec
- planning execution
- creating or updating execution work
- running packetized implementation/review/docs work
- recording acceptance, critique, or completion
- operating across repositories or worktrees

If a task depends on durable memory or future resumption, it belongs in Loom.

## 8.2 Parent/child execution model

The parent context owns:

- classifying work
- resolving scope
- hydrating the correct skill
- compiling the packet
- declaring the allowed write set
- selecting packet mode
- launching the child run
- reconciling results back into canonical records

The child context owns:

- bounded work inside the packet contract
- local reasoning
- direct edits only within the packet-declared allowed write set
- verification evidence generation
- explicit continue/stop/escalate signals

The child context does not own the broader workflow contract.

## 8.3 Resumption model

Resumption SHOULD work by reading durable artifacts, not transcript history.

Resume by:

1. reading current canonical target state
2. checking linked plan/spec/research/constitution state
3. reading the latest packet and run artifacts if relevant
4. deciding whether the prior packet is stale
5. compiling a fresh packet if any relevant inputs changed
6. continuing or branching intentionally

## 8.4 Write-back model

All durable project-truth changes MUST land in canonical records.

For execution packets, the default model SHOULD be:

1. the parent compiles the packet and declares the allowed write set
2. the child run may directly mutate only that allowed write set
3. the parent validates the resulting state, interprets outcome, and performs any remaining acceptance or reconciliation steps

For review-only or diagnostic packets, the child SHOULD return findings, verdicts, or proposed changes rather than mutate canonical records.

Run artifacts MAY assist, but MUST NOT replace canonical write-back.

---

# 9. Rules architecture

## 9.1 Purpose of `src/rules/`

`src/rules/` is the always-on brainstem of Loom.

It SHOULD contain:

- Loom identity and doctrine
- truth hierarchy
- layer boundaries
- scope doctrine
- packet doctrine
- fresh-context execution doctrine
- verification doctrine
- security doctrine
- write-back discipline
- prohibited behaviors

## 9.2 What `src/rules/loom.md` should do

It should not be a tiny hint file.
It should deeply embed the following:

1. what Loom is
2. when Loom must be used
3. what each layer means
4. why tickets are the sole execution ledger
5. when fresh child runs are mandatory
6. how to discover the relevant subsystem skill
7. which behaviors are forbidden

## 9.3 What SHOULD NOT live only in skills

The following MUST NOT exist only in a conditionally loaded skill:

- truth hierarchy
- scope fail-closed doctrine
- anti-shadow-ledger doctrine
- packet authority doctrine
- verification honesty doctrine
- prompt-injection defense doctrine

---

# 10. Skills architecture

## 10.1 Purpose of skills

Skills provide subsystem-specific operating instructions.

Each skill SHOULD answer:

- when to use this skill
- what artifact kinds it governs
- what statuses and transitions are allowed
- what deterministic scripts exist locally
- what harness invocation shape applies, if any
- what verification expectations apply

## 10.2 Flat sibling skill rule

Skills MUST be flat siblings under `src/skills/`.

Nested skills SHOULD NOT be used.

## 10.3 Self-contained distribution rule

A distributed skill bundle MUST include:

- `SKILL.md`
- local references
- local scripts
- local examples
- version metadata

## 10.4 Script colocation rule

If a skill depends on a script at runtime, that script MUST exist inside that skill’s distributed bundle.

## 10.5 Harness invocation rule

If a skill launches fresh packet-consuming work, it SHOULD document:

- the command shape
- the expected packet path form
- the prompt shape
- the expected output shape
- failure and retry guidance

The skill SHOULD document the command shape.
It SHOULD NOT require a dedicated Loom launcher wrapper.

---

# 11. Build and distribution model

## 11.1 Purpose

The build layer exists only to make skill distribution boring and reliable.

## 11.2 Build responsibilities

The repository SHOULD prefer direct standalone skill scripts over a separate generation layer.

If a mechanical script rewrite step exists in the future, it should stay optional, local, and subordinate to the committed skill-local source files.

## 11.3 What build MUST NOT do

The build system MUST NOT:

- invent hidden semantics
- rewrite protocol meaning
- create hidden state not reconstructable from repository contents
- centralize execution through a hidden wrapper model

---

# 12. Canonical record system

## 12.1 Record invariants

Every canonical record MUST:

- be a Markdown file
- have structured frontmatter
- have a stable `id`
- declare `kind`
- declare `schema_version`
- declare `status`
- declare timestamps
- declare scope
- declare explicit link fields
- remain legible without tooling

## 12.2 Common frontmatter shape

Illustrative common fields:

```md
---
id: ticket:pl-0001
kind: ticket
schema_version: 1
status: active
repository_scope:
  kind: repository
  repository_id: repo:root
owners:
  - platform
links:
  plan:
    - plan:protocol-cutover
updated_at: 2026-03-31T12:00:00Z
created_at: 2026-03-31T10:00:00Z
---
```

## 12.3 Common body requirements

Bodies SHOULD contain:

- rationale
- context
- assumptions
- constraints
- non-goals
- risks
- verification expectations
- open questions when applicable

## 12.4 Mutation discipline

Canonical records SHOULD be updated intentionally, not through broad auto-rewrite.

Helper scripts MAY generate templates and update explicitly owned machine sections.
They SHOULD NOT rewrite user-authored prose silently.

---

# 13. Layer-by-layer record and artifact specifications

## 13.1 Constitution

### Purpose
Stores durable project identity, principles, constraints, roadmap, and strategic decisions.

### Recommended subtypes

- `constitution.md`
- roadmap item
- decision record

### Required sections for `constitution.md`

- Vision
- Principles
- Constraints
- Strategic Direction
- Current Focus
- Open Constitutional Questions
- Change History

### Recommended statuses

- active
- revised
- superseded

### Important rules

- constitutional decisions SHOULD be durable and infrequently edited
- decision records SHOULD declare what they supersede
- roadmap items SHOULD link downstream initiatives/specs/research

## 13.2 Research

### Purpose
Stores reusable discovery before execution outruns understanding.

### Suggested subtypes

- evidence note
- experiment note
- synthesis note

### Required sections

- Question
- Objective
- Scope
- Non-goals
- Methodology
- Hypotheses
- Evidence
- Experiments
- Rejected paths
- Conclusions
- Recommendations
- Open questions
- Linked downstream artifacts

### Additional fields to add

- evidence_strength
- source_quality
- confidence
- reproducibility_notes

### Important rule
Research MUST remain curated and reusable.
It MUST NOT become a transcript dump.

## 13.3 Initiatives

### Purpose
Stores strategic outcome containers across multiple specs/plans/tickets.

### Required sections

- Objective
- Why now
- In scope
- Out of scope
- Success metrics
- Milestones
- Dependencies
- Risks
- Linked specs/plans/tickets
- Status summary

### Additional fields to add

- owner
- measurable_outcome
- milestone_state
- acceptance_criteria

## 13.4 Specs

### Purpose
Stores declarative behavior contracts.

### Required sections

- Summary
- Problem framing
- Desired behavior
- Constraints
- Capabilities
- Requirements
- Scenarios
- Acceptance
- Design notes
- Open questions

### Additional distinctions

- normative sections
- informative sections
- requirement IDs
- compatibility notes

### Hard rule
Specs MUST remain behavior-first.
They MUST NOT become rollout notes.

## 13.5 Plans

### Purpose
Stores execution strategy across a linked ticket set.

### Required sections

- Purpose / Big Picture
- Progress
- Surprises & Discoveries
- Decision Log
- Outcomes & Retrospective
- Context and Orientation
- Milestones
- Plan of Work
- Concrete Steps
- Validation and Acceptance
- Idempotence and Recovery
- Artifacts and Notes
- Interfaces and Dependencies
- Linked Tickets
- Risks and Open Questions
- Revision Notes

### Additional fields to add

- plan_state
- dependency_readiness
- ticket_coverage
- rollback_strategy
- closure_criteria

### Hard rule
Plans are strategy.
They MUST NOT become the live execution ledger.

## 13.6 Tickets

### Purpose
Stores live execution truth.

### Required sections

- Summary
- Context
- Why this work matters now
- Scope
- Non-goals
- Acceptance criteria
- Implementation plan
- Dependencies
- Risks / edge cases
- Verification
- Documentation disposition
- Journal

### Additional fields to add

- execution_mode
- current_blocker
- active_packet_ref
- latest_verification_refs
- handoff_state
- closure_authority

### Recommended statuses

- proposed
- ready
- active
- blocked
- review_required
- complete_pending_acceptance
- closed
- cancelled

### Hard rule
Tickets remain the live execution ledger.
No other layer may silently take over that role.

## 13.7 Ralph run artifact family

### Purpose
Stores bounded run artifacts for packetized execution.

### Suggested files

- run manifest
- packet
- iteration record
- reconciliation note

### Important rule
Ralph artifacts are durable execution artifacts, but they do not become canonical execution truth.
They are specified here because they are first-class Loom artifacts, not because they are canonical records.

## 13.8 Critique

### Purpose
Stores durable adversarial review.

### Suggested subtypes

- adversarial review
- design review
- docs review

### Required sections

- Target under review
- Review question
- Focus areas
- Relevant context
- Evidence reviewed
- Verdict
- Residual risks
- Follow-up tickets
- Findings summary

### Finding sections

- Problem
- Why it matters
- Evidence
- Scope
- Severity
- Confidence
- Recommended action
- Status

### Additional fields to add

- review_completeness
- finding_disposition
- accepted_or_rejected

## 13.9 Docs

### Purpose
Stores accepted explanation after work is complete.

### Suggested subtypes

- overview
- protocol guide
- operator guide
- workflow doc

### Required sections

- Overview
- Audience
- Problem framing
- Accepted system shape
- Workflow / operations details
- Rationale
- Examples
- Verification source
- Related artifacts
- Supersession / history

### Additional fields to add

- doc_status
- stale_trigger
- truth_source
- owner

---

# 14. Link semantics and graph model

## 14.1 Links must be explicit

Loom SHOULD prefer explicit typed link fields over prose-only references.

## 14.2 Link kinds

Typical link kinds include:

- constitution → roadmap / decisions / initiatives / specs / research
- research → specs / plans / tickets
- initiatives → specs / plans / tickets
- specs → plans / tickets / docs
- plans → tickets / specs / research / initiatives
- tickets → plan / spec / research / critique / docs / packet
- critique → ticket / finding / follow-up ticket
- docs → verification source / spec / ticket / plan
- packet → target / source refs / prior packet

## 14.3 Illegal links

The protocol SHOULD define illegal or suspicious links explicitly.

Example:

- a plan SHOULD NOT own execution truth
- a docs record SHOULD NOT silently close a ticket
- a Ralph artifact SHOULD NOT mutate canonical truth by implication

## 14.4 Backlinks

Backlinks MAY be computed or materialized.

Recommendation:

- compute them where possible
- materialize only if clearly useful
- validate any materialized backlinks mechanically

---

# 15. Scope and multi-repo model

## 15.1 Concrete scope model

Markdown-first Loom SHOULD recognize four identities:

- workspace
- repository
- worktree
- packet scope

## 15.2 Supported repository discovery model

For v1, support:

- the root repository at the workspace root
- repositories nested under workspace subdirectories

Do not attempt arbitrary distributed repo discovery yet.

## 15.3 Scope identifiers

Recommended forms:

- `workspace:main`
- `repo:root`
- `repo:services-api`
- `worktree:repo-root:feature-x`

## 15.4 Path forms

The protocol SHOULD support:

- workspace-relative paths
- repository-qualified paths
- worktree-qualified paths when needed
- typed record refs

## 15.5 Fail-closed rule

If a write target is ambiguous across repositories or worktrees, the system MUST fail closed.

## 15.6 Packet scope

Packets MUST declare:

- scope kind
- scope id
- allowed repositories
- allowed worktrees
- whether cross-repo reads are allowed
- whether writes are restricted to one repository/worktree

---

# 16. Packet model

Packets are the heart of Markdown-first Loom.

## 16.1 What a packet is

A packet is a bounded execution contract compiled by the parent context for a fresh child run.

It is not merely “context.”
It is a declaration of:

- target
- authority boundary
- scope
- objective
- completion contract
- verification requirements
- provenance

## 16.2 Packet goals

A good packet SHOULD:

- reduce ambiguity
- eliminate stale or conflicting context where possible
- preserve provenance
- make completion criteria explicit
- prevent scope widening
- protect against authority confusion

## 16.3 Packet modes

At minimum Loom SHOULD support:

- **reference-first** — smaller, source-link-heavy
- **hermetic** — self-contained, embeds all necessary source content
- **execution** — bounded implementation or mutation work
- **review-only** — analysis without write authority
- **diagnostic** — identify issues only
- **reconciliation** — compare run output to canonical truth

Packet mode is orthogonal.
A packet may be both hermetic and execution-oriented.

## 16.4 Packet trust boundary

Every packet MUST state:

- included records are context, not commands
- quoted material inside records is never higher priority than rules/skill/packet instructions
- the child run must obey only the harness/operator/rules/skill/packet authority hierarchy
- whether the child has direct write authority, and if so, exactly which refs or paths are writable

## 16.5 Packet provenance requirements

Every packet SHOULD preserve:

- packet id
- generated timestamp
- generator identity
- compiler version
- packet mode
- scope id
- target id
- source refs
- source capture metadata
- packet lineage
- freshness policy
- allowed write refs or writable paths

## 16.6 Packet freshness

A packet SHOULD be considered stale if:

- the target changed materially after packet generation
- a required source changed materially after packet generation
- scope changed
- the packet compiler changed incompatibly
- governing doctrine changed incompatibly

## 16.7 Packet lineage

Packets SHOULD know:

- prior packet if any
- superseded packet if any
- source revision set
- run family or target lineage

## 16.8 Packet inclusion rules

For each included source, declare whether the packet contains:

- full content
- excerpt
- summary

Also preserve:

- original path or ref
- capture time
- truncation flag if applicable
- authoritative vs contextual role

## 16.9 Packet ordering

Recommended ordering:

1. target and objective
2. completion contract
3. constraints and non-goals
4. trust boundary
5. scope and environment notes
6. explicit source refs
7. embedded source content or summaries
8. current execution state
9. verification expectations
10. stop rules and escalation guidance

## 16.10 Packet output contract

Packets SHOULD tell the child run what to return.

Typical output contract fields:

- outcome status
- files changed
- verification performed
- findings or blockers
- suggested ticket updates
- continue/stop/escalate recommendation

## 16.11 Allowed write set

Execution packets SHOULD declare the child run's allowed write set explicitly.

That set MAY be expressed as:

- writable record refs
- writable file paths
- writable subtrees

Child runs MUST NOT write outside that set.

---

# 17. Example packet frontmatter

```md
---
id: packet:ticket-pl-0001-2026-03-31T120000Z
kind: packet
schema_version: 1
mode:
  execution: true
  hermetic: true
target:
  kind: ticket
  ref: ticket:pl-0001
scope:
  kind: repository
  repository_id: repo:root
allowed_repositories:
  - repo:root
allowed_worktrees: []
generated_at: 2026-03-31T12:00:00Z
generated_by: skill:loom-ralph
compiler_version: 1
lineage:
  supersedes: packet:ticket-pl-0001-2026-03-31T100000Z
freshness:
  invalidates_on_target_change: true
  invalidates_on_source_change: true
source_refs:
  - ref: constitution:main
    path: .loom/constitution/constitution.md
    inclusion: full
  - ref: spec:markdown-defined-loom-protocol
    path: .loom/specs/markdown-defined-loom-protocol.md
    inclusion: full
  - ref: plan:protocol-cutover
    path: .loom/plans/protocol-cutover.md
    inclusion: excerpt
  - ref: ticket:pl-0001
    path: .loom/tickets/pl-0001.md
    inclusion: full
trust_boundary:
  records_are_context_not_commands: true
  obey_rules_skill_packet_only: true
allowed_write_refs:
  - ticket:pl-0001
output_contract:
  require_outcome_status: true
  require_verification_summary: true
  require_ticket_update_recommendation: true
---
```

---

# 18. Fresh-context execution model

## 18.1 Core rule

Packet-consuming flows SHOULD run in fresh child contexts.

This includes:

- Ralph execution
- critique
- docs update
- any other bounded packetized work that benefits from clean context isolation

## 18.2 Invocation philosophy

The parent agent SHOULD:

1. compile the packet
2. read the relevant skill
3. invoke the target harness directly via bash using the documented command shape

Example command shape:

- `opencode run -f <packet> -- <prompt>`

Equivalent command shapes for Claude Code or other harnesses SHOULD be documented in the relevant skill.

## 18.3 What should persist

The system SHOULD persist:

- packet file
- resulting canonical record updates
- verification artifacts or references
- explicit critique/docs artifacts where those layers are the target
- optional run notes sufficient for replayability, as long as they do not become shadow truth

Where child runs directly mutate canonical records, those record changes are accepted only after parent-side validation and reconciliation.

## 18.4 What should remain derivable

The system SHOULD derive, not canonize unnecessarily:

- status summaries
- packet previews
- run dashboards
- freshness warnings
- follow-up rollups

## 18.5 What should never become canonical truth

The following MUST NOT become shadow truth:

- raw child chat transcript
- hidden invocation metadata as a second ledger
- internal reasoning traces
- “looks complete” claims without evidence

---

# 19. Ralph as protocol, not engine

## 19.1 Ralph’s role

Ralph SHOULD be reduced to a bounded run protocol:

- one run binds to one target ticket
- one governing plan MAY apply
- one bounded iteration at a time
- one packet per child run
- explicit continue/stop/escalate outcome

## 19.2 Ralph artifacts

Possible artifact family:

```text
.loom/runs/ralph/run-0001/
  packet.md
  iteration-001.md
  iteration-002.md
```

These artifacts are useful if they preserve bounded execution history.
They MUST NOT replace ticket truth.

## 19.3 Ralph outcome discipline

Every bounded Ralph run SHOULD end with one of:

- continue
- stop
- escalate
- blocked

And the ticket MUST reflect the durable execution state before the run is considered complete.

---

# 20. Critique and docs as packet-consuming layers

## 20.1 Critique

Critique is naturally packet-driven.

It SHOULD operate from:

- a bounded review question
- explicit focus areas
- clear severity/confidence scales
- durable findings linked to follow-up work

## 20.2 Docs update

Docs update SHOULD also be packetized.

It SHOULD operate from:

- accepted system shape
- explicit audience
- verification basis
- linked canonical sources

Docs MUST NOT become a workaround for unfinished implementation.

---

# 21. Verification and acceptance model

## 21.1 Completion is not the same as code landed

Work is complete only when:

- acceptance criteria are satisfied
- required verification ran or was explicitly waived
- canonical records were updated truthfully
- blockers were resolved or converted into explicit follow-up work

## 21.2 Verification tiers

Loom SHOULD recognize multiple tiers of verification:

- structural — schema, links, statuses, scope integrity
- behavioral — tests, checks, observed outputs
- integration — cross-layer or cross-repo workflows
- human signoff — when policy requires it

## 21.3 Acceptance gates

Acceptance SHOULD require:

- evidence refs
- verification status
- scope confirmation
- follow-up disposition
- docs disposition where relevant

## 21.4 Critique gating

Critique SHOULD gate at least:

- high-risk execution
- major protocol/schema changes
- docs claims about accepted system shape
- changes with significant residual risk

## 21.5 Docs disposition

Tickets SHOULD explicitly record docs disposition:

- no docs needed
- docs update required
- docs update deferred with reason

---

# 22. Deterministic helper layer

## 22.1 Purpose

The helper layer exists for the small set of things models still do poorly or inconsistently.

## 22.2 Minimal script families

Recommended minimal script set:

```text
create_<kind>.py
link_records.py
create_verification.py
validate_record.py
check_links.py
compile_packet.py
list_records.py
show_status.py
diagnose_workspace.py
resolve_scope.py
```

## 22.3 Responsibilities

### `create_<kind>.py`
- allocate stable ids for that record family
- choose the correct path for that record family
- emit the correct template shape without asking the operator to restate the kind

### `link_records.py`
- add typed refs
- remove typed refs
- preserve link graph shape without hand-editing JSON frontmatter

### `create_verification.py`
- create durable verification records in `.loom/verification/`
- wire linked tickets, packets, docs, critique, or plan refs at creation time

### `validate_record.py`
- frontmatter validation
- section presence validation
- status enum validation
- schema version validation

### `check_links.py`
- missing refs
- illegal refs
- duplicate ids
- orphan detection

### `compile_packet.py`
- collect sources
- normalize ordering
- preserve provenance
- emit packet mode correctly

### `list_records.py`
- render discoverable record inventories
- support basic filtering before linking or packet compilation

### `show_status.py`
- render current workspace state

### `diagnose_workspace.py`
- check rules/skills presence
- check scope discoverability
- check validation health
- check packet-readiness

### `resolve_scope.py`
- discover valid root and nested repositories
- normalize identifiers

## 22.4 Script principles

Scripts MUST:

- mechanize visible rules
- avoid hidden state
- support structured output when useful
- avoid silent mutation

Scripts SHOULD:

- preserve user-authored prose
- prefer explicit ownership boundaries for generated sections

---

# 23. Security, resilience, and failure model

## 23.1 Prompt injection and record poisoning

Records MUST be treated as untrusted contextual content, not executable authority.

Mitigations SHOULD include:

- clear boundary tags
- explicit authority hierarchy
- provenance labeling
- suspicious-content detection where feasible
- trust-boundary text in packets

## 23.2 Stale packets

Packets SHOULD invalidate on:

- target changes
- critical source changes
- scope changes
- incompatible compiler changes
- incompatible doctrine changes

## 23.3 Partial writes

Helper scripts SHOULD use atomic write patterns where possible.

The protocol SHOULD expect:

- pre-write validation
- explicit failure reporting
- no hidden partial-state success claims

## 23.4 Self-contradictory context

When sources conflict, Loom SHOULD:

- surface the conflict explicitly
- avoid silent auto-resolution
- require reconciliation or higher-order review

## 23.5 Role confusion

The protocol SHOULD explicitly distinguish:

- parent orchestrator
- child executor
- reviewer
- docs writer
- ticket owner

## 23.6 Multi-agent contention

Markdown-first systems are vulnerable to contention.

Thin mitigations MAY include:

- optimistic locking fields like `updated_at`
- append-only journal discipline
- conflict warnings
- explicit ticket ownership markers

## 23.7 Harness drift

Skills SHOULD version their documented command shapes.

If a harness CLI changes materially, the skill SHOULD be treated as stale until updated.

---

# 24. Optional indexes and adapters

## 24.1 Legitimate uses

Optional SQLite or similar local adapters MAY be used for:

- status/reporting acceleration
- link indexes
- full-text search
- packet dependency caching

## 24.2 Illegitimate uses

If portability is the goal, adapters MUST NOT become:

- the only canonical truth
- the only source of state transitions
- a hidden substrate not reconstructable from Markdown truth

## 24.3 Rule

Adapters are optimization, not ontology.

---

# 25. First serious release shape

## 25.1 Minimum coherent release

A minimal but real first release of Markdown-first Loom would include:

- always-on doctrine files in `src/rules/`
- subsystem skills for the major layers
- self-contained distributed skills
- canonical `.loom/` records
- deterministic helper scripts
- packet compilation
- fresh-context execution command shapes documented for Ralph/critique/docs

## 25.2 Included canonical layers

- constitution
- research
- initiatives
- specs
- plans
- tickets
- critique
- docs

## 25.3 Included durable non-canonical artifact families

- Ralph run artifacts
- critique run artifacts when persisted separately from critique records
- docs-update run artifacts when persisted separately from docs records
- verification artifacts

## 25.4 Explicit non-goals

- canonical database
- long-running service
- heavy orchestration server
- complex UI/TUI
- monolithic `loom` product CLI
- generalized workflow automation engine
- arbitrary multi-user concurrency guarantees

---

# 26. Adoption strategy for this fresh Loom spike

This is not a migration plan from current `pi-loom`, but it still helps to think in phases.

## Phase 1 — Doctrine

Write:

- `src/rules/loom.md`
- `src/rules/truth-hierarchy.md`
- `src/rules/packet-doctrine.md`
- `src/rules/execution-doctrine.md`
- `src/rules/verification-doctrine.md`
- `src/rules/scope-doctrine.md`
- `src/rules/security-doctrine.md`

## Phase 2 — Skill map and distribution model

Define:

- subsystem skill boundaries
- build/distribution model
- self-contained skill invariant

## Phase 3 — Canonical schemas

Write schemas and examples for every layer.

## Phase 4 — Packet spec and compiler behavior

Define:

- packet modes
- trust boundary
- provenance fields
- freshness/invalidation rules
- output contract

## Phase 5 — Fresh-context execution model

Define per-skill harness invocation contracts for Ralph/critique/docs.

## Phase 6 — Real end-to-end workflows

Run full flows in file-first mode and refine based on actual friction.

## Phase 7 — Optional accelerators

Only after real usage, add indexes or adapters if they clearly earn their complexity.

---

# 27. Open design questions

These remain worth deliberate exploration.

## 27.1 Should packets default to reference-first or hermetic?

Hermetic packets are better for replayability and child-run isolation.
Reference-first packets are smaller and cheaper.

The protocol likely wants both.

## 27.2 Should backlinks be materialized or computed?

Computed backlinks are more truthful.
Materialized backlinks may improve readability.

## 27.3 How much run artifact persistence is worth it?

The protocol must preserve enough to support replayability and diagnosis, without inventing a shadow ledger.

## 27.4 What is the lightest acceptable contention model?

File-first systems need some story here, even if thin.

## 27.5 When should critique be mandatory?

This should likely become policy-driven by risk class.

---

# 28. Recommended additions to the spec corpus

The following appendix/spec artifacts SHOULD exist eventually. The current appendix files live under `src/rules/appendices/`.

## Appendix A — Common schema conventions

Current file: `src/rules/appendices/common-schema-conventions.md`

- frontmatter field definitions
- timestamp format
- id format
- status enum conventions
- scope field conventions

## Appendix B — Per-layer schemas and artifact schemas

Current file: `src/rules/appendices/layer-schemas.md`

- constitution
- research
- initiatives
- specs
- plans
- tickets
- Ralph
- critique
- docs

## Appendix C — State machines

Current file: `src/rules/appendices/state-machines.md`

- ticket state machine
- plan state machine
- critique finding state machine
- docs state machine
- packet lifecycle

## Appendix D — Packet templates

Current file: `src/rules/appendices/packet-templates.md`

- ticket execution packet
- critique packet
- docs update packet
- diagnostic packet
- reconciliation packet

## Appendix E — Harness invocation templates

Current file: `src/rules/appendices/harness-invocation-templates.md`

Per packet-consuming subsystem, document:

- command shape
- arguments
- prompt shape
- output shape
- failure behavior

## Appendix F — Validation rules

Current file: `src/rules/appendices/validation-rules.md`

- schema validation
- link validation
- scope validation
- packet freshness validation
- transition validation

## Appendix G — Naming conventions

Current file: `src/rules/appendices/naming-conventions.md`

- ids
- refs
- directories
- filenames
- version markers

## Appendix H — Security model

Current file: `src/rules/appendices/security-model.md`

- authority hierarchy
- packet trust boundary
- prompt-injection handling
- suspicious-content handling

---

# 29. Raw design slogans worth keeping

- Loom should be a protocol pack, not an app.
- Markdown should become the ABI.
- The valuable part of Loom is the work discipline, not the current package code.
- Packets matter more than transcripts.
- Tickets remain the execution ledger.
- If a rule matters, it must be visible.
- Use code only where models are still unreliable.
- Adapters are optimization, not ontology.
- The protocol should be reimplementable in any harness.

---

# 30. Final judgment

The portable future of Loom is not a thinner clone of the current codebase.

It is:

- a Markdown-defined long-horizon AI work protocol
- backed by always-on rules, flat sibling subsystem skills, and thin Python scripts
- centered on packets as bounded execution contracts
- executed through fresh harness contexts for packet-consuming work
- protected by explicit truth hierarchy, provenance, and verification discipline
- extensible through optional adapters only where scale truly demands them

That is the version of Loom most likely to:

- scale with model capability
- remain harness-agnostic
- stay inspectable
- avoid bespoke glue sprawl
- preserve the parts of Loom that are genuinely novel and valuable

If the goal is portability without losing discipline, this is the direction to take.

---

# 31. Source notes and references

## Current Pi Loom context consulted

- `README.md`
- `AGENTS.md`
- `CONSTITUTION.md`
- `DATA_PLANE.md`

## External references consulted

### Anthropic

- Anthropic Skills README: https://github.com/anthropics/skills/blob/main/README.md
- Anthropic skill-creator guidance: https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md
- Anthropic long-context prompt structure examples: https://github.com/anthropics/courses/
- Agent Skills specification: https://agentskills.io/specification

### OpenAI

- GPT-5.4 prompt guidance: https://developers.openai.com/api/docs/guides/prompt-guidance
- Structured outputs guide: https://developers.openai.com/api/docs/guides/structured-outputs
- Latest model/tool guidance: https://developers.openai.com/api/docs/guides/latest-model
- Prompt engineering / coding best practices: https://developers.openai.com/api/docs/guides/prompt-engineering

## External guidance synthesized, not copied verbatim

- explicit instructions beat vague prompts
- clear structure improves long-context reliability
- progressive disclosure is useful
- deterministic scripts are valuable for repetitive structured tasks
- structured output contracts improve reliability
- clear tool contracts and completion criteria improve agent behavior
