# Agent Loom

The missing middle between prompt and patch.

![Loom banner](assets/banner.png)

**Coding agents do better work when the work has a shape.**

Agent Loom is a protocol for project memory and execution discipline. It structures how knowledge, decisions, research, specs, work, evidence, and reviews are captured and used across sessions and agents.

The protocol lives in [`PROTOCOL.md`](PROTOCOL.md). Paste it into your `AGENTS.md`, `CLAUDE.md`, or equivalent harness instructions.

## How It Works

Loom splits agent behavior into two loops:

**Outer loop** — when intent is unclear, interrogate. Challenge vague terms, propose concrete scenarios, build shared vocabulary, and externalize what crystallizes into typed records on disk.

**Inner loop** — when scope is clear, execute with discipline. Tickets are the unit of work. Sub-agents produce claims. Closure requires coherence across the record graph.

The records live in `.loom/`:

```
.loom/
  decisions/       — durable choices, ADR format
  research/        — investigations, sources, dead ends, conclusions
  specs/           — intended behavior, scenarios, acceptance criteria
  tickets/         — bounded work, scope, progress, closure
  evidence/        — observed facts, test output, screenshots, logs
  reviews/         — adversarial critique, findings, verdicts
  knowledge/       — shared vocabulary, conventions, procedures
```

## When It Helps

Use Loom when the work should be recoverable:

- behavior changes where intent matters
- bugs that need reproduction or root-cause work
- multi-step changes that benefit from planning as parent/child tickets
- work that crosses sessions, models, or harnesses
- tasks needing durable evidence, review, or knowledge capture

For a one-line obvious edit, just use Git.

## Loom Mill

Loom Mill is a companion application that provides a visual interface for the `.loom/` record graph — shaping sessions, ticket visualization, and execution observation. It reads and writes the same Markdown records the protocol defines.

See [`loom-mill/`](loom-mill/) for details.

## Try It

1. Copy the contents of [`PROTOCOL.md`](PROTOCOL.md) into your project's `AGENTS.md`, `CLAUDE.md`, or equivalent.
2. Start working with your coding agent. The protocol changes how it behaves — shaping before executing, externalizing as it goes, building shared vocabulary.
3. Records appear in `.loom/` as the agent works.

## Repository Layout

```
.
├── PROTOCOL.md          — the protocol (paste this into your harness)
├── AGENTS.md            — contributor guidelines for this repo
├── loom-mill/           — companion visual application
├── loom-core/           — package skeleton (OpenCode plugin)
├── loom-playbooks/      — package skeleton (OpenCode plugin)
└── .loom/               — dogfood records for this repo
```
