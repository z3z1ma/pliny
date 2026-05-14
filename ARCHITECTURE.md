# Architecture

Loom is boring by design.

The product is a Markdown skill corpus. The runtime state is Markdown under
`.loom/`. Package entrypoints, manifests, hooks, and extensions expose the corpus
to different harnesses. They do not own the protocol.

Loom ships no hidden runtime, daemon, database, dashboard, required helper script,
or product CLI.

## Product Boundary

The product surface lives in two package roots:

| Package | Job |
| --- | --- |
| `loom-core/` | mandatory `using-loom` doctrine and record skills |
| `loom-playbooks/` | optional workflow-specific skills that assume the required package is installed |

Inside each package, `skills/` is the source of behavior. The package root may add
transport files for OpenCode, Claude Code, Codex, Cursor, or Gemini CLI.

Content inside package `skills/` must stay self-contained. Use generic `.loom/...`
runtime paths. Do not teach source-repo-only assumptions from this repository as
Loom doctrine.

## Runtime State

A Loom workspace materializes records only when it needs them:

```text
.loom/
|-- constitution/
|   |-- constitution.md
|   |-- decisions/
|   `-- roadmap/
|-- tickets/
|-- research/
|   `-- artifacts/
|-- specs/
|-- plans/
|-- evidence/
|   `-- artifacts/
|-- audit/
|-- knowledge/
`-- packets/
    `-- ralph/
```

Missing empty directories are fine. A directory matters when the current work
needs that surface.

## Core Surfaces

Each surface owns one kind of truth.

| Surface | Runtime Path | Owns |
| --- | --- | --- |
| constitution | `.loom/constitution/` | durable judgment, policy, principles, constraints, ADRs, roadmap direction |
| tickets | `.loom/tickets/` | bounded executable work, live state, acceptance, closure |
| research | `.loom/research/` | investigations, tradeoffs, rejected paths, null results, conclusions |
| specs | `.loom/specs/` | intended behavior, requirements, scenarios, interfaces |
| plans | `.loom/plans/` | strategy and decomposition for complex work |
| evidence | `.loom/evidence/` | observations, outputs, reproductions, screenshots, logs, validation |
| audit | `.loom/audit/` | Ralph-backed review, findings, verdicts, residual risk |
| knowledge | `.loom/knowledge/` | preferences, procedures, accepted explanation, atlases, retrieval cues |
| packets | `.loom/packets/ralph/` | bounded worker contracts |

Retrospective is a promotion and prevention pass over existing surfaces. It has no
record directory of its own.

## Bootstrap

`using-loom` is mandatory before Loom work unless the adapter has already loaded
the same files with clear source markers.

Load order:

1. `loom-core/skills/using-loom/SKILL.md`
2. `loom-core/skills/using-loom/references/how-loom-thinks.md`
3. `loom-core/skills/using-loom/references/activation-discipline.md`
4. `loom-core/skills/using-loom/references/directory-structure.md`
5. `loom-core/skills/using-loom/references/shaping-with-humans.md`
6. `loom-core/skills/using-loom/references/delegating-to-workers.md`
7. `loom-core/skills/using-loom/references/proving-the-work.md`
8. `loom-core/skills/using-loom/references/staying-safe.md`

OpenCode exposes `loom-core/skills` through `config.skills.paths` and injects the
stripped `using-loom` doctrine plus ordered references into the first user message
with `experimental.chat.messages.transform`. Claude, Codex, Cursor, and Gemini use
their native manifest, hook, or static context surfaces where those are available.

Preload is convenience. If preload is absent, the agent loads `using-loom` from
Core.

Preload alone is not the behavior. `using-loom` contains the first-action routing
loop that tells the agent to check likely Loom surfaces and skills before answering,
asking clarifying questions, inspecting files, editing, creating tickets, or
launching Ralph when Loom may apply. Static smoke checks guard that activation
doctrine and trigger-oriented skill descriptions remain present.

## Record Grammar

Skills use frontmatter because harnesses expect it. Loom records use grepable body
labels because humans and future agents can inspect and repair them without a
parser.

```text
ID: <typed-id>
Type: <record type>
Status: <status>
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
```

Templates stay small. They force the agent to name scope, evidence, risks,
acceptance, and links without turning Markdown into a hidden schema engine.

## The Two Loops

The outer loop shapes work with the operator. The agent inspects first, asks only
material questions, and routes durable truth to the surface that owns it. Work
stays in this loop while intent, scope, evidence, risk, or authority is unclear.

That gate is mandatory. A fuzzy ask must not become a ticket, packet, or patch
until the missing outcome, boundary, constraints, evidence posture, non-goals,
system-shape, data-model or state implications, and design-coherence questions are
shaped with the operator or the owning Loom surface.

Record skills own Loom surfaces and their procedures. Workflow-specific skills
run inside this architecture: they add guidance after Loom routing has identified
the owning surface and whether the work is shaped enough to execute. When a
workflow-specific skill routes to another Loom skill, the target skill's procedure
and guidance still apply completely.

The inner loop executes bounded work. Tickets drive live execution state. Ralph
packets execute bounded ticket slices and worker runs. Evidence records what
happened. Audit records adversarial review returned from Ralph review packets. The
parent reconciles the result into the owning surfaces.

This split is the core architecture. Coding harnesses can add transport, but they
should not replace the outer-loop shaping or the inner-loop contract.

## Ralph And Audit

Ralph packets are contracts for one worker run. They name target, mission, context
style, read scope, write scope, source snapshot, stop conditions, and output
contract.

The packet is written under `.loom/packets/ralph/` before the worker launch. The
launch transport points to that packet so the handoff is recoverable from the
Markdown graph, not only from harness logs.

A packet is not accepted project truth. After the worker returns, the parent reads
the packet output, diffs, records, and evidence, then updates the consuming
surface.

Substantive audit requires a Ralph review packet. The same session can prepare the
audit request and record the result, but the adversarial judgment must come from
the Ralph review run. Local inspection may help, but it should not be saved as
`Type: Audit`.

## Adapter Rule

Adapters may preload doctrine, expose skills, validate package shape, or make
installation easier. They must not define another ontology.

Generated context files, external issue trackers, dashboards, MCPs, and local
scripts may transport or mirror Loom work. The owning truth still lives in Loom
records unless a future constitutional record changes that boundary.

## Repository-Only Material

This repo has support material that is not product doctrine:

- `examples/` contains internal fixtures and traces for maintainer review
- `.loom/` contains dogfood records for this repo
- `.opencode/` is a local consumption surface

Use those for review or dogfooding. Keep product behavior in `loom-core/skills`
and `loom-playbooks/skills`.

## Design Checks

A Loom change should preserve these properties:

- a future agent can find the right record with filenames, IDs, labels, and grep
- tickets remain the only live execution ledger
- evidence records observations without deciding acceptance
- audit records review without closing work
- packets bound worker runs without becoming project state
- knowledge stores accepted reusable understanding without replacing specs, evidence, audit, or tickets
- workflow-specific skills route through Loom surfaces instead of adding durable surfaces
- helper code stays derivative of the Markdown protocol
