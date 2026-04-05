---
{
  "created_at": "2026-04-04T23:57:48Z",
  "id": "spec:minimum-proven-core-workflow-surface",
  "kind": "spec",
  "links": {
    "initiative": [
      "initiative:prove-core-loom-workflow"
    ],
    "plan": [
      "plan:bootstrap-core-workflow-backlog"
    ],
    "ticket": [
      "ticket:0003",
      "ticket:0004",
      "ticket:0005"
    ]
  },
  "repository_scope": {
    "kind": "repository",
    "repository_id": "repo:root"
  },
  "schema_version": 1,
  "status": "active",
  "updated_at": "2026-04-04T23:58:09Z"
}
---

# Summary

Define the minimum proven Loom workflow surface that this repository should
support next: a maintainer can enter cold, follow durable records, execute one
bounded fresh-context slice, reconcile critique and docs outcomes, and use
package-local command and helper surfaces without guessing.

# Problem Framing

The current repository proves that Loom's rules, skills, and helper scripts can
be shipped, but it does not yet prove the main operator path end to end. The
canonical graph is still thin, no initiative or spec previously owned this next
slice, and `src/commands/` currently covers only memory work even though the
product exposes broader canonical record and review workflows.

# Desired Behavior

A capable maintainer should be able to start from canonical records, identify
one ready ticket, compile or assemble the needed bounded context, run one fresh
execution slice inside root-repository scope, reconcile critique and docs
follow-through, and leave the ticket ledger and supporting artifacts truthful.

The operator path should stay visible in shipped Markdown and deterministic
helpers rather than depending on hidden runtime behavior or transcript memory.

# Constraints

- no monolithic `loom` CLI
- protocol over hidden runtime or service orchestration
- helpers may mechanize only already-published rules
- scope and write authority must fail closed
- `src/` surfaces must remain package-local and self-contained
- ticket truth must remain in tickets rather than in plans, docs, or runs
- Python scripts are justified only when they provide value the agent cannot
  achieve with standard bash/Unix tools: structural validation, link integrity,
  frontmatter scaffolding and creation, and frontmatter-aware querying. All
  other record work -- populating content, searching, reading, editing, running
  workflow steps -- is agent work with normal tools.
- Ralph execution is an agent running a headless invocation of itself with a
  compiled packet. No custom orchestration script is needed; the agent handles
  context assembly, child launch, output capture, and reconciliation directly.

# Capabilities

- durable initiative/spec/plan/ticket framing for the next workflow slice
- one bounded Ralph -> critique -> docs proof path in `repo:root`, driven by the
  agent using standard tools, not by a custom orchestration script
- package-local command entry points that route operators to the correct owning
  skill and record surfaces
- deterministic validation and diagnostics for scope, packet shape, link
  integrity, and workspace readiness where doctrine already requires them
- the agent can populate, search, and edit canonical records directly; scripts
  handle only the mechanical structural work that benefits from determinism

# Requirements

- maintain one explicit initiative/spec/plan/ticket chain for this workflow
  slice
- keep at least one ticket in `ready` state with enough detail to execute
  without relying on chat history
- the proof flow must declare repository scope, packet mode, source refs, trust
  boundary, output contract, and allowed write set before child execution
- execution outcomes must reconcile into the ticket plus linked critique, docs,
  and verification artifacts, or explain explicitly why a linked artifact was
  not created
- new command entry points must remain Markdown prompt definitions under
  `src/commands/` and must not reference non-package-local paths
- validation and diagnostics must catch ambiguous scope, broken canonical links,
  and missing packet structure that doctrine already defines as required

# Scenarios

- a fresh maintainer reads the canonical records and can safely begin
  `ticket:0003`
- a user wants to create or advance core Loom work through a command entry point
  instead of discovering everything from skill surfaces alone
- packet or scope information is incomplete and validation fails closed with a
  clear explanation
- a proved workflow change needs docs follow-through or an explicit
  docs-not-required decision

# Acceptance

- the initiative, spec, plan, and three backlog tickets exist and are linked
  coherently
- `ticket:0003` is actionable without transcript archaeology
- later command and helper changes can be judged against this contract without
  redefining what the workflow is supposed to do
- no accepted addition violates package-local isolation or the no-monolithic-CLI
  constraint

# Design Notes

- prove one small root-repository path before broadening coverage
- treat commands as prompt entry points, not runtime orchestrators
- let validation follow doctrine rather than anticipating future policy
- prefer one real worked path over many speculative surfaces
- scripts earn their place only when they do something the agent genuinely
  cannot do well: structural integrity checks, frontmatter parsing, link
  resolution, and record scaffolding. Record population, content search,
  workflow orchestration, and Ralph execution are agent responsibilities.

# Open Questions

- which packet mode should become the default long-term posture for common runs
- when critique should become mandatory by risk class rather than recommendation
- how much packet freshness and acceptance logic should eventually move from
  prose into deterministic validation
- what the smallest stable core command set should be after the proof slice
