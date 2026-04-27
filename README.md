# Loom

Loom is Markdown-native project state for AI agents.

![Loom banner](assets/banner.png)

The code changed. The transcript knew why. The repo did not.

That is the failure Loom is built around. Long-running agent work leaves behind investigations, rejected paths, evidence, critique, acceptance decisions, and lessons worth keeping. If that work stays in chat, the next session starts cold or inherits a swollen context window.

Loom puts the project record in the repo.

It gives agents a vocabulary for placing work where it belongs, then uses that vocabulary in two directions:

1. The outer loop routes truth into owner records.
2. The inner loop compiles those records into bounded packets for clean workers.
3. Retrospective promotes accepted learning back into the graph.

The worker is disposable. The graph compounds.

```text
project truth -> compiled packet -> bounded worker -> evidence and critique -> promoted learning -> better project truth
```

[Install Loom](INSTALL.md) · [Read the protocol](PROTOCOL.md) · [Architecture notes](ARCHITECTURE.md)

## The claim

The pieces are familiar. Teams already use specs, plans, tickets, research notes, test output, review notes, wiki pages, Git branches, and release summaries. Agent workflows added prompts, memory files, context management, subagents, skills, local task stores, and clean execution loops.

Loom's contribution is the composition.

Each kind of project truth gets one Markdown owner. The skills teach agents when to use each owner, how records link, how work moves between records, and when the graph is consistent enough to close.

Once the vocabulary exists, common workflows become routes through the same graph. Debugging, spiking, planning, reviewing, shipping, repair, retrospective, codebase mapping, wiki synthesis, and Ralph-style implementation no longer need separate hidden state.

Loom is the vocabulary long-running agent work compiles to.

## Why this changes the work

A bigger context window lets an agent carry more state.

Loom moves the state out of the window.

A fresh worker should not need the whole conversation. It should receive the relevant project records, a bounded goal, a write scope, stop conditions, and an output contract. After the worker returns, the parent reconciles what happened back into the graph.

The child does one slice.

The parent decides what became true.

The project keeps the record.

## Owner layers

Loom separates project truth into canonical owner layers.

| Layer | Owns |
| --- | --- |
| `constitution` | Durable identity, principles, hard constraints, precedent, roadmap direction |
| `initiative` | Strategic outcomes, success metrics, cross-cutting result framing |
| `research` | Investigations, tradeoffs, experiments, rejected paths, null results, evidence synthesis |
| `spec` | Intended behavior, requirements, scenarios, acceptance contracts |
| `plan` | Execution strategy, decomposition, sequencing, rollout |
| `ticket` | Live execution state, scoped work, blockers, acceptance disposition, closure |
| `evidence` | Observed artifacts, validation output, reproduction steps, logs, screenshots, scan results |
| `critique` | Adversarial findings, review verdicts, residual risk |
| `wiki` | Accepted explanation, architecture concepts, reusable workflow knowledge |
| `packet` | Bounded child-worker contracts, not project truth |
| `memory` | Optional support recall only |

The rule that keeps the graph coherent:

```text
truth ownership is by layer, not by recency
```

The newest message does not win. The longest summary does not win. The artifact that owns that kind of truth wins.

For software work, the source tree owns current implementation reality. Git owns file history. Specs own intended behavior. Tickets own live execution and acceptance. Evidence bridges implementation to claims. Critique judges whether the bridge is strong enough. Wiki holds explanation that has become safe to reuse.

Memory can help an agent recover context. It does not own project truth.

## How agents use the vocabulary

The agent stops using the transcript as the workspace. It starts placing truth.

| Situation | Loom route |
| --- | --- |
| Missing understanding | `research` |
| Unclear behavior | `spec` |
| Unclear sequencing | `plan` |
| Live work | `ticket` |
| Observed output | `evidence` |
| Concern, review pressure, residual risk | `critique` |
| Stable understanding | `wiki` |
| Bounded implementation | `packet` |
| Support recall | `memory`, until it deserves promotion |

A vague bug report becomes reproduction evidence, root-cause research, a tightened spec if behavior is ambiguous, a ticket for the fix, a packet for the implementation pass, green evidence, critique when risk warrants, and wiki promotion if the lesson should survive.

No new workflow was invented. The agent used the vocabulary.

## Two loops

Loom separates shaping work from doing work.

### Outer loop: route truth

The outer loop asks which owner should change next.

```text
constitution -> initiative -> plan -> ticket
```

Conditional gates keep the agent honest:

```text
need discovery or tradeoff analysis -> research
need behavior clarity -> spec
need sequencing -> plan
need bounded execution -> ticket
need observations -> evidence
need pressure-testing -> critique
need accepted explanation -> wiki
```

If a step cannot be completed honestly, route backward to the owner that can fix the gap.

Do not advance on vibes.

### Inner loop: run clean workers

The inner loop is Ralph-shaped:

```text
one packet
one fresh worker
one bounded mutation
one parent reconciliation
```

A parent compiles a packet, delegates one fresh-context execution step, receives a bounded outcome, and reconciles the result back into the graph.

The child owns one iteration. The packet owns the child contract. The ticket owns live execution. The parent owns reconciliation.

Critique and wiki may reuse packet discipline, but their domain skills own review and synthesis. They are sibling routes, not implementation passes pretending to be Ralph.

## Packets compile project truth

A packet is a compiled contract.

A parent builds it from the upstream graph: relevant constitution records, initiative context, research, spec, plan, ticket, evidence, critique, source fingerprint, execution context, write scope, verification posture, stop conditions, and output contract.

The worker gets less context by volume, but better context by shape.

A strong packet states:

* the ticket or owner record being served
* the bounded goal for this iteration
* what the worker can read
* what the worker can write
* the source fingerprint
* the Git branch or worktree context when files will change
* the verification posture
* stop conditions
* the output contract
* what the parent will do after return

Packets prevent context drift, hidden assumptions, uncontrolled changes, and scope creep.

A packet is a contract. It is not project truth.

After the child returns, the parent reconciles the result into tickets, evidence, critique, research, specs, plans, wiki, constitution, initiatives, or memory as needed.

## The transaction spine

Non-trivial Loom work follows one spine:

```text
route -> shape -> ready -> execute -> reconcile -> verify -> accept -> promote -> close
```

A transaction does not need every layer. It does need to preserve ownership.

Example bug fix:

1. Capture reproduction evidence.
2. Research the root cause if it is unknown.
3. Update or create a spec if the intended behavior is fuzzy.
4. Create or tighten the ticket.
5. Compile a packet for one implementation pass.
6. Run a fresh worker.
7. Record red and green evidence.
8. Route critique when risk warrants.
9. Accept only when the ticket reflects reality.
10. Promote durable learning into research, wiki, spec, plan, initiative, constitution, evidence, or memory.
11. Close when the graph is consistent.

That is Loom.

## Done is a property of the graph

Work is not done when the code compiles. It is done when the project is consistent.

For software work, closure usually requires:

* the relevant spec is satisfied, or ticket-local acceptance criteria are explicit
* evidence supports the claim being made
* critique is resolved, accepted, or recorded as residual risk
* the ticket reflects the actual final state
* durable learning has been promoted when it should survive the task

A child worker saying done is not enough. A commit is not enough. A green test is not enough if the ticket still lies.

Done is a property of the graph.

## Research is first-class

A lot of software work is knowledge work before it is code.

Agents explore libraries, inspect implementation paths, test approaches, compare options, discover constraints, and learn that something does not work. If that work stays in chat, the next session repeats it.

Research gives that work a durable home: questions, options, experiments, rejected approaches, null results, supporting evidence, open questions, and evidence-grounded recommendations.

A failed path can be valuable. A null result can be the most important thing the project learned that day.

This is where Loom crosses from coding workflow into knowledge-work protocol.

## Workflows emerge from the vocabulary

Workflow skills coordinate routes through owner layers. They do not create new ledgers unless a new kind of truth exists.

```text
debug:
evidence -> research -> spec if needed -> ticket -> packet -> evidence -> critique -> retrospective

spike:
research -> throwaway scope if needed -> evidence -> conclusions/null results -> downstream spec, plan, ticket, or wiki

code map:
scan evidence -> research where structure is uncertain -> wiki atlas when accepted

review:
critique -> evidence -> ticket reconciliation -> acceptance or repair

implementation:
ticket -> packet -> worker -> evidence -> reconcile

ship:
ticket/evidence/critique/wiki disposition -> PR summary, release note, risk summary, follow-up list

repair:
evidence -> critique -> ticket -> packet -> evidence -> accept

retrospective:
ticket or initiative lessons -> wiki, research, spec, plan, initiative, constitution, evidence, or memory
```

You do not invent a workflow every time. You route through the owner graph.

## Influences

Loom is influenced by Superpowers, GSD, Spec Kit, Beads, Ralph, ECC, and the broader field of agent-skills projects.

Superpowers showed how much better coding agents get when they have explicit development skills. GSD showed how context engineering changes long-running work. Spec Kit showed that well-defined specs can drive implementation. Beads showed that local agent-facing tickets externalize context and make long-horizon work easier to manage. Ralph showed the value of clean context windows, bounded tasks, disk-backed state, commits, and restart loops. ECC put real effort into continuous learning and compound engineering.

Loom makes the shared vocabulary explicit.

Brainstorming becomes research, spec, plan, and ticket shaping. Test-driven development becomes packet verification posture plus evidence and ticket acceptance. Review becomes critique. Finishing becomes ticket acceptance, ship packaging, and retrospective promotion. Ralph becomes packet, child worker, bounded mutation, and parent reconciliation.

You can run other tools beside Loom. For many projects, you may not need to. Loom's skills already teach the agent how to route the same underlying work through the repo.

## Markdown, on purpose

Loom is Markdown-native.

No service. No daemon. No hidden runtime database.

The graph is files. Agents already know how to search with `rg`, traverse with `find`, inspect with `cat`, compare with `git diff`, edit records, move files, and compose shell tools with `awk`, `sed`, `xargs`, and pipes.

That is enough.

Optional utilities may validate, project, or summarize state. They do not own Loom semantics.

Harness adapters may preload bootstrap references where a harness supports it cleanly. That is an adapter optimization over the same skill package, not a second doctrine source.

The protocol is the corpus.

## What ships

This repository ships the Loom skill package.

It is not a runtime, service, daemon, MCP server, product CLI, workflow engine, hidden database, or prompt dump.

Included:

* `skills/`, the canonical Loom surface
* `loom-bootstrap`, the mandatory entry skill
* owner-layer skills for constitution, initiatives, research, specs, plans, tickets, evidence, critique, wiki, and memory
* workflow skills for workspace entry, records, Ralph, Git, debugging, spike, codemap, ship, retrospective, and skill authoring
* templates and references for Markdown-native operation
* harness manifests and adapters where useful
* `PROTOCOL.md`, the stable protocol summary
* `ARCHITECTURE.md`, the implementation and package architecture notes
* examples and fixtures for protocol behavior

The product surface is the skill package. The skills are the protocol in operational form.

## Skill map

| Skill | Role |
| --- | --- |
| `loom-bootstrap` | Mandatory first-read doctrine and route into Loom |
| `loom-workspace` | Workspace entry, structure check, first routing decision |
| `loom-records` | IDs, frontmatter, typed links, status, validation, repair |
| `loom-constitution` | Project identity, constraints, decisions, roadmap direction |
| `loom-initiatives` | Strategic outcomes and success framing |
| `loom-research` | Reusable discovery, experiments, tradeoffs, null results |
| `loom-specs` | Intended behavior and acceptance contracts |
| `loom-plans` | Sequencing, decomposition, rollout strategy |
| `loom-tickets` | Live execution ledger and acceptance gate |
| `loom-evidence` | Observed artifacts and claim support or challenge |
| `loom-critique` | Adversarial review, findings, verdicts, residual risk |
| `loom-wiki` | Accepted explanation and reusable understanding |
| `loom-memory` | Optional support recall without shadow truth |
| `loom-ralph` | Bounded fresh-context implementation loop |
| `loom-git` | Implementation isolation, baseline, branch/worktree provenance |
| `loom-debugging` | Reproduce-first debug workflow through existing layers |
| `loom-spike` | Bounded investigation and sketch workflow through research and evidence |
| `loom-codemap` | Repository atlas workflow through evidence, research, and wiki |
| `loom-ship` | PR, release, handoff, risk, and follow-up packaging |
| `loom-retrospective` | Compounding pass that promotes accepted learning into owner layers |
| `loom-skill-authoring` | Maintaining Loom-compatible skills without breaking the protocol |

## Repository layout

```text
.
├── README.md
├── INSTALL.md
├── PROTOCOL.md
├── ARCHITECTURE.md
├── AGENTS.md
├── examples/             # golden protocol fixtures and traces, not truth owners
├── optional-utilities/   # helpers that do not own semantics
└── skills/               # canonical Loom skill package
```

Inside a Loom-enabled project, the runtime tree looks roughly like this:

```text
.loom/
├── constitution/
├── initiatives/
├── research/
├── specs/
├── plans/
├── tickets/
├── evidence/
├── critique/
├── wiki/
├── packets/
│   ├── ralph/
│   ├── critique/
│   └── wiki/
└── memory/        # optional
```

Use `loom-workspace`, `loom-constitution`, and `loom-tickets` for the first records.

## Install

Loom installs as a skills package. The fastest path is to expose `skills/` to your harness and use `loom-bootstrap` first.

```bash
git clone https://github.com/z3z1ma/agent-loom.git
```

First-class harness paths are in [INSTALL.md](INSTALL.md):

* Claude Code
* OpenCode
* Codex
* Cursor
* Gemini CLI
* generic skills-directory install

After install, start with:

```text
Use the loom-bootstrap skill. Then route the work through the Loom skill that owns the next truth change.
```

## What Loom can replace

Loom can coexist with external issue trackers, planning tools, review systems, workflow packages, and agent command surfaces.

It can also make many of them unnecessary for the agent-facing work record.

The skills already prescribe owner layers, routing rules, execution, acceptance, evidence, review, knowledge promotion, and handoff packaging. Once those terms exist inside the repo, the agent can compose the workflows directly.

External systems can mirror Loom state. They should not be the only place the agent learns what is true.

## Costs

Loom asks for discipline.

Broken links matter. Stale records matter. Evidence that overclaims matters. A ticket that says the work is accepted when critique is unresolved is worse than no ticket at all.

Loom also has a threshold. If the work is small, local, and obvious, use the source tree and Git. Do not create a graph-shaped shrine around a one-line edit.

The graph pays for itself when work crosses sessions, changes behavior, needs review, involves research, carries risk, or leaves behind knowledge the next worker would otherwise rediscover.

## The point

Loom is a way to keep AI work from dissolving into conversation.

It gives agents a vocabulary for placing work where it belongs.

It gives projects a memory that survives context windows, compaction, worker handoff, and time.

The pieces already existed. Loom puts them in one place and gives each one a job.

```text
the work stops drifting
the agent stops carrying everything
the project starts remembering
```
