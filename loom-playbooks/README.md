# Agent Loom Playbooks

Optional workflow routes for Loom.

The required package gives agents the record skills and surfaces. Playbooks help
agents move through those surfaces when the task has a familiar shape: debug this,
test this first, map this codebase, verify this UI, review this diff, migrate this
safely, prepare this for release.

Install [loom-core](../loom-core/README.md) first. Playbooks assume the
`using-loom` skill is already loaded.

[Agent Loom](../README.md) / [Protocol](../PROTOCOL.md) / [Install](../INSTALL.md) / [loom-core](../loom-core/README.md)

## What Playbooks Add

A workflow-specific skill routes task-shaped work. A record skill owns a Loom
surface and its procedure. Loom records carry durable facts.

A workflow-specific skill gives the agent workflow pressure while results still
land in Loom records: reproduction evidence, research, specs, tickets, plans,
audit findings, knowledge, or constitution decisions.

When a workflow-specific skill routes results through another Loom skill, follow
the target skill's procedure and guidance completely. The route is a required
handoff, not a shortcut around the target skill.

Vague work stays in outer-loop shaping until the next Loom surface is clear. A
playbook must not turn ambiguity into an implementation shortcut; it should expose
the missing scope, system-shape, data-model, state, evidence, and coherence choices.
Complex work becomes ticket-ready slices; delegated worker runs use Ralph packets.

Use workflow-specific skills when general Loom routing is too thin for the work.
Examples:

- debugging should preserve the failure before the fix
- TDD should preserve red and green evidence
- performance work should measure before changing code
- UI work should use browser observation when runtime behavior matters
- migrations should keep rollout, proof, cleanup, and follow-up connected
- review work should route findings through audit and tickets
- release work should claim only what tickets and evidence support

## The Set

The package currently ships 25 playbooks.

Planning and shaping:

- `loom-idea-refine`
- `loom-domain-language-and-decisions`
- `loom-codebase-atlas`
- `loom-architecture-deepening`
- `loom-intake-triage`
- `loom-prototype-and-spike`

Implementation and verification:

- `loom-incremental-implementation`
- `loom-test-driven-development`
- `loom-source-driven-development`
- `loom-doubt-driven-development`
- `loom-frontend-ui-engineering`
- `loom-api-and-interface-design`
- `loom-browser-testing-with-devtools`
- `loom-debugging-and-error-recovery`

Coordination and review:

- `loom-git-workspace-isolation`
- `loom-parallel-worker-coordination`
- `loom-code-review-and-quality`
- `loom-review-response`
- `loom-branch-finish`

Hardening and release:

- `loom-code-simplification`
- `loom-security-and-hardening`
- `loom-performance-optimization`
- `loom-ci-cd-and-automation`
- `loom-deprecation-and-migration`
- `loom-shipping-and-launch`

The skill descriptions are the activation surface. Keep them visible to the
harness.

## How They Stay Loom

Playbooks use record skills and their procedures.

- debugging can create evidence, research, specs, tickets, audit, and knowledge
- architecture work can create specs, plans, tickets, evidence, and audit
- review response can update tickets, audit, specs, evidence, research, constitution, or knowledge
- Git coordination can protect branches and worktrees while tickets keep live execution state
- shipping can draft communication while tickets and evidence control what can be claimed

The workflow can end. Loom records keep the result.

## Install Or Expose Playbooks

Expose `loom-core` first, then Playbooks:

```text
/absolute/path/to/agent-loom/loom-core
/absolute/path/to/agent-loom/loom-playbooks
```

Or expose both skill trees:

```text
/absolute/path/to/agent-loom/loom-core/skills
/absolute/path/to/agent-loom/loom-playbooks/skills
```

OpenCode can load `loom-playbooks.mjs`. Git-based installs for Claude Code,
Codex, Cursor, and Gemini CLI use the native manifests in this package. The npm
package exposes the OpenCode entrypoint and `skills/` tree. Harness-specific
commands live in [INSTALL.md](../INSTALL.md).

## Boundary

Playbooks are reusable routes for coding agents. They do not add durable surfaces
or weaken record-skill procedure.

Use a record skill when the next record move is clear. Add a playbook when the
workflow itself needs pressure.
