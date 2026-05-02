# Agent Loom

Treat your coding-agent sessions like cattle, not pets.

![Loom banner](assets/banner.png)

**Agent Loom makes the repo remember.**

A session should be restartable, replaceable, compactable, and safe to hand off. The important state should live in the project, not in one precious chat.

Loom is a Markdown-native truth graph for agentic software work:

- every durable claim has one owning record
- every fresh worker receives a bounded packet, not vibes
- every task closes with evidence, critique, and promotion when needed

**The worker is disposable. The graph compounds.**

[Install Loom](INSTALL.md) · [Read the protocol](PROTOCOL.md) · [Architecture notes](ARCHITECTURE.md)

---

## The problem

Most agent workflows eventually create a junk drawer.

`PLAN.md` becomes the spec, todo list, research log, failed-attempt record, review trail, status update, and handoff summary. Scratch files litter the repo. The active chat becomes a pet: overloaded with volatile decisions, painful to abandon, and weirdly valuable because the repo does not know what happened.

When the work stops, resumes, compacts, switches models, or hands off to another worker, the next agent has to infer what is still true.

The model did not just forget.

The project never knew.

Loom fixes that by giving each kind of truth a home.

---

## The idea

The active session is the wrong place for canonical project memory.

A bigger context window lets an agent carry more state. Good compaction can preserve useful continuity. Loom is complementary: it moves durable state into repository records, so summaries can carry file paths, record IDs, and next actions while the full-fidelity truth stays in the repo.

Once installed, Loom is meant to feel ambient. The skills teach the agent where durable information belongs, so ordinary coding work can flow into records without the user saying `use Loom` every turn.

A fresh worker should not inherit a giant transcript or a folklore summary. It should inherit:

- the relevant project records
- the current ticket
- the evidence so far
- the open critique
- the exact read and write scope
- the stop conditions
- the output contract

That compiled handoff is a **packet**.

The child does one bounded slice. The parent reconciles what happened. The repo keeps the memory.

The session is disposable. The graph compounds.

```text
project state -> packet -> fresh worker -> evidence/critique -> reconciliation -> promoted learning -> better project state
```

---

## 🧪 Try the cattle-not-pets demo

The fastest way to understand Loom is to stop protecting one precious agent session.

1. Start a nontrivial coding-agent task.
2. Let the work cross at least one ambiguity: a behavior question, failed attempt, review concern, research finding, partial implementation, or open risk.
3. Let the installed Loom skills place durable truth into owner records such as tickets, research, specs, evidence, critique, and wiki, with packets as bounded handoff support when needed.
4. Stop the session: close the chat, compact the context, switch models, switch harnesses, hand the work to another agent, or come back tomorrow.
5. Start from a fresh session and ask for the next step:

```text
Continue the active work from the repo's project records. Do not rely on prior chat context.
```

You usually should not need to say the magic words. If a harness or cold session does not route automatically, a nudge is fine:

```text
Use loom-bootstrap, then continue from the project records.
```

Without durable records, the new session usually guesses or tries to reconstruct the missing story.

With Loom, it should find the owner records, identify what is canonical, stay inside scope, and continue from repo state.

Compaction is not the enemy. With Loom, compaction can carry high-value record paths and IDs while the records themselves preserve full-fidelity project truth.

That is the product: sessions can die; the project keeps the plot.

---

## ⚙️ Install

Loom installs as a skills package. The fastest path is to expose `skills/` to your coding harness.

```bash
git clone https://github.com/z3z1ma/agent-loom.git
```

First-class harness instructions are in [INSTALL.md](INSTALL.md):

- Claude Code
- OpenCode
- Codex
- Cursor
- Gemini CLI
- generic skills-directory install

After install, work normally. In a skills-aware harness, Loom should feel much like Superpowers: the agent discovers the bootstrap and downstream skills when the work calls for them.

Explicit prompts are escape hatches, not the main UX. They are still useful when you want to prod a cold session or force repair:

```text
Use loom-bootstrap, then continue from the project records.
```

```text
Use loom-records to inspect the graph and repair any broken links before continuing.
```

---

## When Loom pays rent

Loom is overkill for a one-line edit.

Use the source tree and Git when the work is tiny, local, and obvious.

Loom starts paying for itself when work crosses sessions, changes behavior, needs research, involves review, carries risk, requires handoff, prepares future work, or leaves behind knowledge the next worker would otherwise rediscover.

Reach for Loom when the cost of losing the plot is higher than the cost of keeping the graph honest.

---

## 🧭 How Loom works

Loom has two loops.

The **outer loop** decides where truth belongs and shapes the next bounded move.
Its backbone is:

```text
constitution -> initiative -> plan -> ticket
```

Research and specs strengthen that backbone when evidence or intended behavior is
missing. Evidence, critique, and wiki are follow-through routes for observations,
review, and accepted explanation. Packets, memory, and saved support artifacts are
support surfaces: packets carry bounded worker contracts, memory holds optional
recall, and support artifacts help handoff audit or recovery without owning
project truth.

The **inner loop** compiles a packet for a fresh worker:

```text
goal + read scope + write scope + source fingerprint + verification posture + stop conditions + output contract
```

The parent reconciles the worker result back into the graph.

No hidden database. No daemon. No SaaS. No special runtime required.

Just Markdown records the agent can read, write, diff, and review.

---

## The core rule

```text
placement beats recency
```

The newest chat message does not win. The longest summary does not win. The right record owns the claim.

For software work:

- the source tree owns implementation reality
- Git owns file history
- specs own intended behavior
- tickets own live execution state and acceptance
- evidence owns observed validation
- critique owns adversarial review and residual risk
- wiki owns accepted reusable explanation
- memory can support retrieval cues, preferences, and reminders without owning project truth

Memory can help the agent recover context. It does not become shadow truth. The project must remain truthful if memory is absent or stale.

---

## 🗂️ Project layers

Loom separates project state into canonical owner layers and durable support
surfaces.

Canonical owner layers own project truth:

| Layer | What goes there |
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

Durable support surfaces help execution and recovery without owning project truth:

| Surface | What goes there |
| --- | --- |
| `packet` | Bounded child-worker contracts; durable support, not project truth |
| `memory` | Optional support recall: retrieval cues, preferences, entities, reminders, and hot context |
| `support` | Optional, lazy-materialized saved support artifacts such as drive handoffs; not canonical truth |

The layers are ordinary Markdown records inside the repo. They are structured enough for agents to reason over and simple enough for humans to inspect.

---

## How agents route work

The agent starts by asking one question:

**What kind of truth is this?**

| Situation | Loom route |
| --- | --- |
| Missing understanding | `research` |
| Unclear intended behavior | `spec` |
| Unclear sequencing | `plan` |
| Live scoped work | `ticket` |
| Observed output or validation | `evidence` |
| Review pressure, concern, or residual risk | `critique` |
| Stable accepted understanding | `wiki` |
| Bounded implementation pass | Ralph with a Ralph packet |
| Retrieval cue, preference, reminder, or hot context | `memory`, until it deserves promotion |

A vague bug report becomes reproduction evidence, root-cause research, a tightened spec if behavior is ambiguous, a ticket for the fix, a Ralph packet for the implementation pass, green evidence, critique when risk warrants, and wiki promotion if the lesson should survive.

No new workflow was invented. The agent used the vocabulary.

---

## Outer loop: route work

The outer loop shapes work before execution.

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

If a step cannot be completed honestly, route backward to the layer that can fix the gap.

Do not advance on vibes.

---

## Inner loop: run clean workers

The inner loop is Ralph-shaped:

```text
one packet
one fresh worker
one bounded mutation
one parent reconciliation
```

A parent compiles a packet, delegates one fresh-context execution step, receives a bounded outcome, and reconciles the result back into the graph.

The child handles one iteration. The packet defines the child contract. The ticket tracks live execution. The parent decides what became true.

Critique and wiki may reuse packet discipline, but their domain skills handle review and synthesis. They are sibling routes, not implementation passes pretending to be Ralph.

---

## Packets compile project state

A packet is a contract for a fresh worker.

A parent builds it from the upstream graph: relevant constitution records, initiative context, research, spec, plan, ticket, evidence, critique, source fingerprint, execution context, write scope, verification posture, stop conditions, and output contract.

The worker gets less context by volume, but better context by shape.

A strong packet states:

- the ticket or project record being served
- the bounded goal for this iteration
- what the worker may read
- what the worker may write
- the source fingerprint
- the Git branch or worktree context when files will change
- the verification posture
- stop conditions
- the output contract
- what the parent will do after return

Packets prevent context drift, hidden assumptions, uncontrolled changes, and scope creep.

A packet is not the project record. After the child returns, the parent reconciles the result into tickets, evidence, critique, research, specs, plans, wiki, constitution, initiatives, or memory as needed.

---

## Done is a property of the graph

Work is not done when the code compiles.

Work is done when the project is consistent.

For software work, closure usually requires:

- the relevant spec is satisfied, or ticket-local acceptance criteria are explicit
- evidence supports the claim being made
- critique is resolved, accepted, or recorded as residual risk
- the ticket reflects the actual final state
- durable learning has been promoted when it should survive the task

A child worker saying "done" is not enough. A commit is not enough. A green test is not enough if the ticket still lies.

**Done is a property of the graph.**

---

## Example: a bug fix through Loom

A non-trivial bug fix usually follows this spine:

```text
route -> shape -> ready -> execute -> reconcile -> verify -> accept -> promote -> close
```

1. Capture reproduction evidence.
2. Research the root cause if it is unknown.
3. Update or create a spec if intended behavior is fuzzy.
4. Create or tighten the ticket.
5. Compile a Ralph packet for one implementation pass.
6. Run a fresh worker.
7. Record red and green evidence.
8. Route critique when risk warrants.
9. Accept only when the ticket reflects reality.
10. Promote durable learning into research, wiki, spec, plan, initiative, constitution, evidence, or memory.
11. Close when the graph is consistent.

The same pattern works for features, spikes, reviews, refactors, migrations, codebase mapping, and release preparation.

---

## Research is first-class

A lot of software work is knowledge work before it is code.

Agents explore libraries, inspect implementation paths, test approaches, compare options, discover constraints, and learn that something does not work. If that work stays in scratch files or short-lived context, the next session repeats it.

Research gives that work a durable place: questions, options, experiments, rejected approaches, null results, supporting evidence, open questions, and evidence-grounded recommendations.

A failed path can be valuable. A null result can be the most important thing the project learned that day.

This is where Loom crosses from coding workflow into knowledge-work protocol.

---

## Workflows emerge from the vocabulary

Workflow skills coordinate routes through existing owner layers. They do not create ledgers or new owner layers.

```text
brainstorm:
workspace problem shaping -> research/spec as needed -> plan -> ticket

test-first implementation:
ticket -> Ralph packet with verification_posture:test-first -> red evidence -> green evidence -> ticket acceptance

debug:
evidence -> root-cause research -> spec if needed -> ticket -> Ralph packet -> evidence -> critique -> retrospective

spike:
research -> throwaway scope if needed -> evidence -> conclusions/null results -> downstream spec, plan, ticket, or wiki

code map:
scan evidence -> research where structure is uncertain -> wiki atlas when accepted

review:
critique -> evidence -> ticket reconciliation -> acceptance or repair

parallel execution:
plan execution waves -> non-overlapping tickets/Ralph packets/worktrees -> child results -> parent integration evidence -> reconciliation

git isolation:
ticket/Ralph packet scope -> explicit baseline -> branch/worktree -> diff provenance -> handoff evidence

implementation:
ticket -> Ralph packet -> worker -> evidence -> reconcile

ship:
ticket/evidence/critique/wiki disposition -> PR summary, release note, risk summary, follow-up list

retrospective:
ticket or initiative lessons -> wiki, research, spec, plan, initiative, constitution, evidence, or memory
```

You do not invent a workflow every time. You route through the project graph.

---

## How Loom relates to adjacent tools

Loom is not trying to replace every agent workflow project.

It is the source-of-truth layer underneath long-running agent work.

| Project | Primary contribution | How Loom differs |
| --- | --- | --- |
| Superpowers | Better agent habits and explicit development skills | Loom focuses on where durable truth lives after those habits run |
| GSD | Context engineering and workflow acceleration | Loom focuses on project-state integrity, owner layers, and reconciliation |
| Spec Kit | Specs as central implementation drivers | Loom treats specs as one owner layer among research, tickets, evidence, critique, and wiki |
| Beads | Local agent-facing task graph | Loom includes tickets, but broadens the graph to behavior, research, validation, review, and durable knowledge |
| Ralph | Fresh-context workers and restartable bounded loops | Loom turns that loop into packet, child worker, evidence, and parent reconciliation |

The short version:

```text
Superpowers: better agent habits
Beads: task graph
Spec Kit: executable specs
GSD: workflow/context harness
Ralph: clean worker loop
Loom: repo-local truth ownership
```

You can run other tools beside Loom. Loom's job is to make sure the project knows what became true.

Because Loom is delivered as skills, it should usually feel like an ambient operating vocabulary rather than a command line the user has to remember.

---

## Markdown, on purpose

Loom is Markdown-native.

No service. No daemon. No hidden runtime database.

The graph is files. Agents already know how to search with `rg`, traverse with `find`, inspect with `cat`, compare with `git diff`, edit records, move files, and compose shell tools with `awk`, `sed`, `xargs`, and pipes.

That is enough.

Optional utilities may validate, project, or summarize state. They do not define Loom semantics.

Harness adapters may preload bootstrap references where a harness supports it cleanly. That is an adapter optimization over the same skill package, not a second doctrine source.

The protocol is the corpus.

---

## 📦 What ships

This repository ships the Loom skill package.

It is not a runtime, service, daemon, MCP server, product CLI, workflow engine, hidden database, or prompt dump.

Included:

- `skills/`, the canonical Loom surface
- `loom-bootstrap`, the entry skill that anchors the rest of the package
- project-owner skills for constitution, initiatives, research, specs, plans, tickets, evidence, critique, and wiki
- the `loom-memory` support skill for optional recall without shadow truth
- workflow skills for workspace entry, records, `loom-drive` objective/workflow driving, Ralph, Git, debugging, spike, codemap, ship, retrospective, and skill authoring
- templates and references for Markdown-native operation
- harness manifests and adapters where useful
- `PROTOCOL.md`, the stable protocol summary
- `ARCHITECTURE.md`, the implementation and package architecture notes
- internal examples and fixtures for maintainer review, not product-surface guidance

The product surface is the skill package. The skills are the protocol in operational form.

---

## Skill map

| Skill | Role |
| --- | --- |
| `loom-bootstrap` | Entry doctrine and route into Loom; usually reached automatically through skills |
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
| `loom-memory` | Support recall, retrieval cues, preferences, and reminders without shadow truth |
| `loom-drive` | Objective and workflow coordination that routes work through owner layers without owning project truth |
| `loom-ralph` | Bounded fresh-context implementation loop |
| `loom-git` | Implementation isolation, baseline, branch/worktree provenance |
| `loom-debugging` | Reproduce-first debug workflow through existing layers |
| `loom-spike` | Bounded investigation and sketch workflow through research and evidence |
| `loom-codemap` | Repository atlas workflow through evidence, research, and wiki |
| `loom-ship` | PR, release, handoff, risk, and follow-up packaging |
| `loom-retrospective` | Compounding pass that promotes accepted learning into project layers |
| `loom-skill-authoring` | Maintaining Loom-compatible skills without breaking the protocol |

---

## Repository layout

```text
.
├── README.md
├── INSTALL.md
├── PROTOCOL.md
├── ARCHITECTURE.md
├── AGENTS.md
├── examples/             # internal fixtures and traces, not product surface or project records
├── optional-utilities/   # helpers that do not define semantics
└── skills/               # canonical Loom skill package
```

Inside a Loom-enabled project, the runtime tree looks roughly like this:

```text
.loom/
├── constitution/
│   ├── constitution.md
│   ├── decisions/
│   └── roadmap/
├── initiatives/
├── research/
├── specs/
├── plans/
├── tickets/
├── critique/
├── wiki/
├── packets/
│   ├── ralph/
│   ├── critique/
│   └── wiki/
├── evidence/
├── memory/        # optional support recall
│   ├── system/
│   └── user/
└── support/       # optional saved support artifacts; non-canonical
    └── drive-handoffs/
```

First records usually emerge through `loom-workspace`, `loom-constitution`, and `loom-tickets`.

---

## Costs

Loom asks for discipline.

Broken links matter. Stale records matter. Evidence that overclaims matters. A ticket that says the work is accepted when critique is unresolved is worse than no ticket at all.

Loom also has a threshold. Do not create a graph-shaped shrine around a one-line edit.

The graph pays for itself when work crosses sessions, changes behavior, needs review, involves research, carries risk, requires handoff, prepares future work, or leaves behind knowledge the next worker would otherwise rediscover.

---

## The point

Loom keeps AI work from scattering across chat, plan files, tool state, and stale scratchpads.

It gives agents a vocabulary for placing work where it belongs.

It gives projects a memory that survives stopped sessions, context compaction, model switches, worker handoff, and time.

Compaction can preserve a pointer. Loom preserves the thing being pointed at.

The pieces already existed. Loom gives each one a job.

```text
the work stops drifting
the agent stops carrying everything
the project starts remembering
```
