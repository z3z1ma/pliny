# Agent Loom Playbooks

Workflow paperwork for coding agents.

Agent Loom gives coding agents a graph of shaped work products. Playbooks help agents move through that graph when a task has a recognizable workflow shape: debug this, review this, migrate this safely, verify this UI, ground this in current docs, simplify this without changing behavior, prepare this for release.

Playbooks are optional. They do not replace [Loom Core](../loom-core/README.md).

Core gives the owner layers. Playbooks give practiced routes through them.

[Agent Loom](../README.md) / [Protocol](../PROTOCOL.md) / [Install](../INSTALL.md) / [Loom Core](../loom-core/README.md)

## Why Playbooks Exist

Many agent workflows are useful but easy to let disappear into chat.

An agent can debug by poking around, but never preserve the reproduction. It can review a diff, but leave findings as transient comments. It can prepare a release note, but accidentally overstate what the ticket accepted. It can run a migration, but skip usage proof and cleanup evidence. It can polish a UI, but leave no browser observation behind.

The workflow happened.

The work products did not compound.

Playbooks fix that by adding workflow-specific pressure while keeping truth in Core's owner layers.

```text
workflow route, not truth owner
```

A playbook can guide how the agent works. It cannot silently decide where project truth lives.

## What They Add

Playbooks are for recurring engineering shapes that need more than generic routing.

They help agents remember to:

- reproduce before fixing
- write or observe a failing check before claiming behavior changed
- measure before optimizing
- isolate Git scope before parallel work
- preserve review findings in critique
- route security-sensitive work through threat-aware review
- keep migration cleanup tied to evidence and ticket disposition
- verify UI changes in the browser when runtime behavior matters
- ground framework or library choices in current source and official docs
- make docs, release notes, and PR summaries mirror owner truth instead of inventing it

Playbooks make the workflow path explicit, repeatable, and recoverable.

## The Playbook Set

| Skill | What it helps with |
| --- | --- |
| `loom-debugging` | reproduce-first debugging and root-cause discipline |
| `loom-tdd` | red/green behavior proof |
| `loom-incremental-implementation` | small verified implementation slices |
| `loom-code-review` | implementation review through critique and ticket disposition |
| `loom-git` | branch, worktree, diff, commit, merge, and provenance discipline |
| `loom-agent-orchestration` | safe worker partitioning and parent review |
| `loom-context-engineering` | curated context for bounded agent work |
| `loom-drive` | long-horizon objective driving through owner layers |
| `loom-product-discovery` | shaping raw ideas into initiatives, research, specs, plans, or tickets |
| `loom-spike` | bounded prototypes, sketches, and investigations |
| `loom-codemap` | repository and module mapping through evidence, research, and wiki |
| `loom-architecture` | seams, module boundaries, adapters, and testability |
| `loom-simplification` | behavior-preserving cleanup and reduction |
| `loom-migration` | staged migrations, deprecations, removals, usage proof, cleanup |
| `loom-security` | auth, authorization, secrets, sensitive data, and hardening routes |
| `loom-performance` | measure, optimize, and guard performance work |
| `loom-ui-browser` | frontend and browser-runtime verification |
| `loom-ci-cd` | automated quality gates, rollout, rollback, and pipeline repair |
| `loom-source-grounding` | current-source and official-reference grounding |
| `loom-docs-sync` | README, API, changelog, and operator-doc synchronization |
| `loom-ship` | PR, release, handoff, risk, and follow-up packaging |
| `loom-skill-authoring` | maintaining Loom-compatible skills and routing boundaries |

The list is intentionally workflow-oriented. These are not new record layers.

## How They Stay Loom

Every playbook routes durable facts back to Core.

- debugging may create evidence, research, a spec update, a ticket, critique, or wiki promotion
- code review may create critique findings, but the ticket owns finding disposition and acceptance
- Git coordination may protect branches and worktrees, but the ticket still owns live execution state
- docs sync may update README files, but owner records still own decisions, behavior, evidence, risk, and accepted explanation
- ship may draft summaries, but the ticket and evidence decide what can honestly be claimed

This keeps workflows from becoming shadow ledgers.

The playbook is the route. The owner record is the truth.

## Installing Or Exposing Playbooks

Install or expose Loom Core first. Playbooks expect Core to supply `using-loom`, the owner layers, record grammar, packet discipline, evidence, critique, and ticket acceptance rules.

The portable local setup exposes both package roots or both skill trees:

```text
/absolute/path/to/agent-loom/loom-core
/absolute/path/to/agent-loom/loom-playbooks
/absolute/path/to/agent-loom/loom-core/skills
/absolute/path/to/agent-loom/loom-playbooks/skills
```

Some harnesses also consume adapter metadata or the JavaScript package-plugin entrypoint in this directory. Those are transport surfaces around the same skills.

Harness-specific instructions live in [INSTALL.md](../INSTALL.md).

## Boundary

Playbooks are not a second protocol, not a workflow engine, and not a replacement for tickets, evidence, critique, specs, research, plans, wiki, or constitution.

They are reusable workflow routes for coding agents.

Use Core when the next owner-layer move is obvious. Add Playbooks when the workflow itself needs structure.

The workflow is disposable. The owner graph is not.
