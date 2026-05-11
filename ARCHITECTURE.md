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
| `loom-core/` | mandatory `using-loom` doctrine and Core record skills |
| `loom-playbooks/` | optional workflow routes that require Core |

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
| audit | `.loom/audit/` | fresh-context review, findings, verdicts, residual risk |
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
3. `loom-core/skills/using-loom/references/directory-structure.md`
4. `loom-core/skills/using-loom/references/shaping-with-humans.md`
5. `loom-core/skills/using-loom/references/delegating-to-workers.md`
6. `loom-core/skills/using-loom/references/proving-the-work.md`
7. `loom-core/skills/using-loom/references/staying-safe.md`

OpenCode registers those files through `config.instructions` and exposes
`loom-core/skills` through `config.skills.paths`. Claude, Codex, Cursor, and
Gemini use their native manifest, hook, or static context surfaces where those are
available.

Preload is convenience. If preload is absent, the agent loads `using-loom` from
Core.

## Record Grammar

Skills use frontmatter because harnesses expect it. Loom records use grepable body
labels because humans and fresh agents can inspect and repair them without a
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

The inner loop executes bounded work. Tickets drive live execution. Ralph packets
hand one bounded run to a worker. Evidence records what happened. Audit challenges
important claims with fresh context. The parent reconciles the result into the
owning surfaces.

This split is the core architecture. Coding harnesses can add transport, but they
should not replace the outer-loop shaping or the inner-loop contract.

## Ralph And Audit

Ralph packets are contracts for one worker run. They name target, mission, context
style, read scope, write scope, source snapshot, stop conditions, and output
contract.

A packet is not accepted project truth. After the worker returns, the parent reads
the packet output, diffs, records, and evidence, then updates the consuming
surface.

Substantive audit requires fresh context. The same session can prepare the audit
request and record the result, but the adversarial judgment must come from a fresh
pass. Same-context inspection may help, but it should not be saved as `Type:
Audit`.

## Adapter Rule

Adapters may preload doctrine, expose skills, validate package shape, or make
installation easier. They must not define another ontology.

Generated context files, external issue trackers, dashboards, MCPs, and local
scripts may transport or mirror Loom work. The owning truth still lives in Core
records unless a future constitutional record changes that boundary.

## Repository-Only Material

This repo has support material that is not product doctrine:

- `examples/` contains internal fixtures and traces for maintainer review
- `.loom/` contains dogfood records for this repo
- `.opencode/` is a local consumption surface
- `optional-utilities/` contains utility skills outside the default install

Use those for review or dogfooding. Keep product behavior in `loom-core/skills`
and `loom-playbooks/skills`.

## Design Checks

A Loom change should preserve these properties:

- a fresh agent can find the right record with filenames, IDs, labels, and grep
- tickets remain the only live execution ledger
- evidence records observations without deciding acceptance
- audit records review without closing work
- packets bound worker runs without becoming project state
- knowledge stores accepted reusable understanding without replacing specs, evidence, audit, or tickets
- playbooks route through Core instead of adding durable surfaces
- helper code stays derivative of the Markdown protocol
