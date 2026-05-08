# Agent Loom Core

Structured paperwork for coding agents.

Agent Loom starts from a simple premise: coding agents do better work when the work has a shape. A model prompted to "fix this" can compress an entire engineering process into one patch. Loom refuses that compression by making the agent externalize the work: what is intended, what is known, what is assumed, what was observed, what remains risky, and why the work can be accepted.

Loom Core is the required part of that system.

It gives an agent the shared owner graph and the core skills for working inside it. Before optional workflows matter, the agent needs to know where each kind of truth belongs: specs for intended behavior, tickets for live execution, evidence for observations, critique for risk, wiki for accepted explanation, packets for bounded handoff, and constitution records for durable constraints.

The result is not "more Markdown."

The result is that code becomes downstream of explicit, inspectable work products.

[Agent Loom](../README.md) / [Protocol](../PROTOCOL.md) / [Install](../INSTALL.md) / [Loom Playbooks](../loom-playbooks/README.md)

## What Core Is For

Core is the Loom package an agent needs before it can do Loom work honestly.

It teaches the operating posture:

- use `using-loom` before nontrivial work
- choose the artifact layer that owns the next truth change
- keep live execution state in tickets
- separate evidence from inference
- preserve critique instead of smoothing over risk
- use packets for bounded fresh-context work
- promote accepted reusable understanding into wiki
- keep memory as support recall, not project truth

Core is intentionally portable. Claude Code, OpenCode, Codex, Cursor, Gemini CLI, a generic skills directory, or another harness may expose it differently. The harness is transport. The protocol is the skills corpus.

## The Core Idea

```text
placement beats recency
```

The newest chat message does not win. The longest summary does not win. The most confident model output does not win.

The right record owns the claim.

Core gives agents the record vocabulary for that placement:

| Layer | What it owns |
| --- | --- |
| `constitution` | durable identity, principles, constraints, decisions, roadmap direction |
| `initiative` | strategic outcomes and success framing |
| `research` | investigations, tradeoffs, rejected paths, null results |
| `spec` | intended behavior and acceptance contracts |
| `plan` | complex-change decomposition, sequencing, rollout |
| `ticket` | live execution state, blockers, acceptance disposition, closure |
| `evidence` | observed artifacts and validation output |
| `critique` | adversarial findings, verdicts, residual risk |
| `wiki` | accepted reusable explanation |
| `packet` | bounded worker contracts, not project truth |
| `memory` | support recall and retrieval cues, not project truth |

This is the difference between a helpful note and a reliable work surface.

## What Core Contains

The core skill set is the Loom protocol in operational form.

| Skill | Role |
| --- | --- |
| `using-loom` | entry doctrine and operating posture |
| `loom-workspace` | workspace orientation and routing |
| `loom-records` | IDs, frontmatter, links, statuses, validation, repair |
| `loom-constitution` | durable identity, constraints, decisions, roadmap direction |
| `loom-initiatives` | strategic outcomes and success framing |
| `loom-research` | reusable investigations, tradeoffs, rejected paths, null results |
| `loom-specs` | intended behavior and acceptance contracts |
| `loom-plans` | high-level complex-change planning and sequencing |
| `loom-tickets` | live execution ledger and acceptance gate |
| `loom-ralph` | bounded fresh-context implementation packets |
| `loom-evidence` | observed artifacts that support or challenge claims |
| `loom-critique` | adversarial review, findings, verdicts, residual risk |
| `loom-wiki` | accepted explanation and reusable understanding |
| `loom-retrospective` | promotion of durable learning into owner layers |
| `loom-memory` | support recall without shadow truth |

Core also carries the templates and references those skills need. The templates are not decoration. They are reasoning tools. They slow the agent down at the point where fast guessing is expensive.

## How It Feels In Use

Core turns a vague request into a placed work product.

```text
prompt -> route -> owner record -> bounded work -> evidence -> critique -> acceptance -> promotion
```

A bug report may begin as reproduction evidence, become root-cause research, tighten a spec if intended behavior is fuzzy, create a ticket for the fix, use a Ralph packet for a bounded implementation pass, collect green evidence, route critique if risk warrants, and promote the lesson into wiki if future agents should not rediscover it.

Not every task needs every layer.

The point is not ceremony. The point is that each durable claim lands where a future agent can recover it.

## Installing Or Exposing Core

The portable install model is simple: expose this directory's `skills/` tree, or expose the package root when the harness understands package roots.

Common local surfaces:

```text
/absolute/path/to/agent-loom/loom-core
/absolute/path/to/agent-loom/loom-core/skills
```

Some harnesses also consume adapter metadata or the JavaScript package-plugin entrypoint in this directory. Those are transport surfaces around the same skills.

Harness-specific instructions live in [INSTALL.md](../INSTALL.md).

## Boundary

Core is mandatory. It owns the Loom bootstrap doctrine and canonical owner-layer skills.

Core is not a runtime, service, daemon, MCP server, product CLI, hidden database, or prompt dump. It is a Markdown-native skill corpus.

Optional workflow routes live in [Loom Playbooks](../loom-playbooks/README.md). Playbooks help with recurring workflows such as debugging, TDD, code review, Git coordination, migration, security, performance, UI/browser verification, shipping, source grounding, and orchestration. They depend on Core because Core owns the graph those workflows must route through.

The session is disposable. The work products compound.
