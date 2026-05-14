# Agent Loom Core

The required Loom package.

Core teaches agents how to turn software work into `.loom/` records: shape the
goal, keep live work in tickets, prove claims with evidence, challenge important
claims with Ralph-backed audit, hand bounded work to packets, and preserve useful
lessons in knowledge.

Core also teaches activation discipline. `using-loom` is the first-action loop that
makes the agent check the relevant Loom surface or skill before responding,
clarifying, inspecting, editing, creating tickets, or launching Ralph when Loom may
apply.

The operating loop is: shape with the human, route durable truth, slice into
bounded tickets, execute ticket slices through Ralph packets, preserve evidence,
audit claims, and reconcile records.

If the ask is not concrete enough for execution, Core keeps the agent in shaping
instead of letting it infer tickets, packets, or patches from hidden product or
system-shape choices.

If a harness installs only one Loom package, install this one.

[Agent Loom](../README.md) / [Protocol](../PROTOCOL.md) / [Install](../INSTALL.md) / [Playbooks](../loom-playbooks/README.md)

## What Core Does

Core gives agents the operating doctrine and the record surfaces that make Loom
work recoverable.

- `using-loom` loads the posture every Loom session needs
- activation checks keep skill and surface routing from becoming an afterthought
- record skills tell the agent which surface owns each kind of truth
- templates give records enough shape for continuation, proof, review, and handoff
- references teach the protocol without requiring a hidden runtime
- Loom Weaver provides optional explicit shaping persona surfaces for
  pre-implementation work that writes only under `.loom/`

The harness is transport. The protocol is this package's `skills/` corpus.

## The Surfaces

| Surface | Job |
| --- | --- |
| `constitution` | durable judgment, policy, constraints, ADRs, roadmap direction |
| `tickets` | bounded executable work, live state, acceptance, closure |
| `research` | investigations, tradeoffs, rejected paths, null results, conclusions |
| `specs` | intended behavior, requirements, scenarios, interfaces |
| `plans` | strategy for complex work that needs several ticket-ready units |
| `evidence` | observations, outputs, reproductions, screenshots, logs, validation |
| `audit` | Ralph-backed review, findings, verdicts, residual risk |
| `knowledge` | preferences, procedures, accepted explanations, atlases, retrieval cues |
| `packets` | bounded ticket execution and worker contracts under `.loom/packets/ralph/` |

Retrospective is a promotion pass over those surfaces. It has no directory of its
own.

## The Skills

| Skill | Job |
| --- | --- |
| `using-loom` | entry doctrine and session posture |
| `loom-constitution` | durable project judgment and precedent |
| `loom-tickets` | executable work units and closure |
| `loom-research` | investigation and synthesis |
| `loom-specs` | intended behavior contracts |
| `loom-plans` | multi-ticket strategy and sequencing |
| `loom-evidence` | durable observations and artifacts |
| `loom-audit` | Ralph-backed review and findings |
| `loom-knowledge` | reusable understanding and retrieval |
| `loom-ralph` | packetized worker handoff |
| `loom-retrospective` | promotion and prevention after significant work |

## The Route

```text
shape with the human -> route to the right surface -> execute bounded work -> evidence -> audit -> reconcile -> promote
```

Small tasks can stay small. Create records when they make the work easier to
recover, trust, hand off, review, or reuse.

## Install Or Expose Core

Expose the package root when your harness understands package roots:

```text
/absolute/path/to/agent-loom/loom-core
```

Expose the skill tree when your harness wants raw skills:

```text
/absolute/path/to/agent-loom/loom-core/skills
```

OpenCode can load `loom-core.mjs`. Claude Code, Codex, Cursor, and Gemini CLI use
the native manifests or bootstrap files in this package. Harness-specific commands
live in [INSTALL.md](../INSTALL.md).

## Boundary

This package carries Loom bootstrap doctrine, canonical record behavior, and the
optional Loom Weaver shaping prompt surfaces. It ships as Markdown and TOML
surfaces, with no daemon, database, dashboard, product CLI, or MCP server.

Optional workflow routes live in [Loom Playbooks](../loom-playbooks/README.md).
Those routes use Loom records instead of adding another durable truth layer.
