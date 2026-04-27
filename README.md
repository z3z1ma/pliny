# Loom

Loom is Markdown-native project state for AI agents.

![Loom banner](assets/banner.png)

It exists because long-running AI work needs a better home than chat.

The code changes. The transcript knows why. Then the session ends, the context fills up, the conversation compacts, or a new worker starts cold. The project has the diff, but it does not have the investigation, the rejected paths, the evidence, the critique, the acceptance state, or the next move.

Loom puts that work in the repo.

It treats the filesystem as the interface, Markdown as the durable medium, and fresh-context packets as the default way to delegate bounded implementation. Claude Code, Codex, OpenCode, Cursor, Gemini CLI, and local agents can operate the same Loom graph if they can read skills, edit files, and use normal shell tools.

The worker is disposable. The graph is durable.

Sounds great, how do I [install](#quick-install) it?

## The claim

The individual pieces in Loom are familiar.

Teams already use specs, plans, tickets, research notes, decision records, test output, review notes, wiki pages, Git branches, and release summaries. Agent workflows added more pieces: prompts, scratchpads, memory files, context management, subagents, and clean execution loops.

Loom’s contribution is the composition.

It gives each kind of project truth one Markdown owner, then teaches agents how to route work through those owners. The skills do not only name the layers. They describe when to use them, how they link, how work moves between them, and how completion is judged.

Once the vocabulary exists, workflows emerge from it.

Debugging, spiking, planning, reviewing, shipping, repair, retrospective, codebase mapping, wiki synthesis, and Ralph-style implementation become routes through the same graph instead of separate systems with separate hidden state.

Loom is not a bag of agent docs.

Loom is the vocabulary that long-running agent work compiles to.

## Why this matters

A bigger context window helps an agent carry more state.

Loom moves the state out of the window.

That shift changes the work. A fresh worker does not need the whole conversation. It needs the relevant records, a bounded contract, a write scope, stop conditions, and a clear output shape. After the worker returns, the parent reconciles what happened back into the graph.

The child does one slice.

The parent decides what became true.

The project keeps the record.

## The owner layers

Loom separates project truth into canonical owner layers.

| Layer | Owns |
| --- | --- |
| `constitution` | durable identity, principles, hard constraints, precedent, roadmap direction |
| `initiative` | strategic outcomes, success metrics, cross-cutting result framing |
| `research` | investigations, tradeoffs, experiments, rejected paths, null results, evidence synthesis |
| `spec` | intended behavior, requirements, scenarios, acceptance contracts |
| `plan` | execution strategy, decomposition, sequencing, rollout |
| `ticket` | live execution state, scoped work, blockers, acceptance disposition, closure |
| `evidence` | observed artifacts, validation output, reproduction steps, logs, screenshots, scan results |
| `critique` | adversarial findings, review verdicts, residual risks |
| `wiki` | accepted explanation, architecture concepts, reusable workflow knowledge |
| `packet` | bounded child-worker contracts, not project truth |
| `memory` | optional support recall only |

The rule that keeps the graph coherent is simple:

```text
truth ownership is by layer, not by recency
```

The newest message does not win. The longest summary does not win. The artifact that owns that kind of truth wins.

For software work, the source tree owns current implementation reality. Git owns file history. Specs own intended behavior. Tickets own live execution and acceptance. Evidence bridges implementation to claims. Critique judges whether that bridge is strong enough. Wiki holds explanation that has become safe to reuse.

Memory can help an agent recover context. It does not own project truth.

## What changes in the agent

The agent stops using the transcript as the workspace.

It starts placing truth.

| Situation | Loom route |
| --- | --- |
| missing understanding | research |
| unclear behavior | spec |
| unclear sequencing | plan |
| live work | ticket |
| observed output | evidence |
| concern or review pressure | critique |
| stable understanding | wiki |
| bounded implementation | packet |
| support recall | memory, until it deserves promotion |

This sounds small until you watch it happen.

A vague bug report becomes reproduction evidence, root-cause research, a tightened spec if behavior is ambiguous, a ticket for the fix, a packet for the implementation pass, green evidence, critique when risk warrants, and wiki promotion if the lesson should survive.

Nothing magical happened.

The agent used the vocabulary.

## The loops

Loom has two loops.

The outer loop shapes work and routes truth.

The inner loop executes bounded work with a clean context window.

Keeping those loops separate matters because shaping work and doing work are different jobs.

### Outer loop

The outer loop asks what kind of truth needs to change next.

Its backbone progression is:

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

### Inner loop

The inner loop is Ralph-shaped:

```text
one packet
one fresh worker
one bounded mutation
one parent reconciliation
```

A parent agent compiles a packet, launches or delegates one fresh-context execution step, receives a bounded outcome, and reconciles the result back into the graph.

The child owns one iteration.

The packet owns the child contract.

The ticket owns live execution.

The parent owns reconciliation.

Critique and wiki may reuse packet discipline, but their domain skills own review and synthesis. They are sibling routes, not implementation passes pretending to be Ralph.

## Packets

Packets create clean work.

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

A packet is a contract.

It is not project truth.

After the child returns, the parent reconciles the result into tickets, evidence, critique, research, specs, plans, wiki, or memory as needed.

## Transaction spine

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
10. Promote durable learning into research or wiki.
11. Close when the graph is consistent.

That is Loom.

## When work is done

Work is not done when the code compiles.

It is done when the project is consistent.

For software work, closure usually requires:

* the relevant spec is satisfied, or ticket-local acceptance criteria are explicit
* evidence supports the claim being made
* critique is resolved, accepted, or recorded as residual risk
* the ticket reflects the actual final state
* durable learning has been promoted to research or wiki when it should survive the task

A child worker saying “done” is not enough.

A commit is not enough.

A green test is not enough if the ticket still lies.

Done is a property of the graph.

## Research is first-class

A lot of software work is knowledge work before it is code.

Agents explore libraries, inspect implementation paths, test approaches, compare options, discover constraints, and learn that something does not work. If that work stays in chat, the next session repeats it.

Research gives that work a durable home:

* questions
* options
* experiments
* rejected approaches
* null results
* supporting evidence
* open questions
* evidence-grounded recommendations

A failed path can be valuable. A rejected option can save the next worker an hour. A null result can be the most important thing the project learned that day.

This is where Loom crosses from coding workflow into knowledge-work protocol.

## Workflows emerge from the vocabulary

Most agent systems package workflows.

Loom defines the pieces those workflows are made from.

The workflow skills in Loom coordinate routes through existing owner layers. They do not create new ledgers unless a genuinely new kind of truth exists.

Examples:

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

You do not invent a workflow every time.

You route through the owner graph.

## Nearby systems

Loom is influenced by Superpowers, GSD, Speckit, Beads, Ralph, ECC and many more projects, but it is not just an adaptation of them.

Superpowers showed how much better coding agents get when they have explicit development skills.

GSD showed how much context engineering matters when work gets large.

Speckit showed that well defined specifications can act as executables and directly generate working, coherent implementations.

Beads showed that local tickets/issues are a great way to externalize context, manage long horizon work, and leverage a more action-oriented form of memory. It also showed that tools designed to be used exclusively by AI work well when the generalization latent in data AI is trained on maps to the tool surface and vernacular.

Ralph showed the value of clean context windows, bounded tasks, disk-backed state, commits, and restart loops.

ECC (everything-claude-code) put a lot of thought into continuous learning and compound engineering.

Loom moves one level down.

It defines the owner vocabulary those workflows are made from.

Brainstorming becomes research, spec, plan, and ticket shaping. Test-driven development becomes packet verification posture plus evidence and ticket acceptance. Review becomes critique. Finishing becomes ticket acceptance, ship packaging, and retrospective promotion. Ralph becomes packet, child worker, bounded mutation, and parent reconciliation.

You can run other tools beside Loom. For many projects, you may not need to. Loom’s skills already teach the agent how to route the same underlying work through the repo.

## Markdown, on purpose

Loom is Markdown-native.

No service. No daemon. No hidden runtime database.

The graph is files.

Agents already know how to:

* search with `grep` or `rg`
* traverse with `find`
* inspect with `cat`
* compare with `git diff`
* edit records
* move files
* version with `git`
* compose shell tools with `awk`, `sed`, `xargs`, and pipes

That is enough.

Optional utilities may validate, project, or summarize state. They do not own Loom semantics.

Harness adapters may preload bootstrap references where a harness supports it cleanly. That is an adapter optimization over the same skill package, not a second doctrine source.

The protocol is the corpus.

## What ships

This repository is intentionally not a runtime, service, daemon, MCP server, product CLI, workflow engine, or prompt dump.

It ships:

* `skills/`, the canonical Loom surface
* `loom-bootstrap`, the mandatory entry skill
* owner-layer skills for constitution, initiatives, research, specs, plans, tickets, evidence, critique, wiki, and memory
* workflow skills for workspace entry, records, Ralph, Git, debugging, spike, codemap, ship, retrospective, and skill authoring
* templates and references for Markdown-native operation
* harness manifests and adapters where useful
* `PROTOCOL.md`, the stable protocol summary
* `ARCHITECTURE.md`, the implementation and package architecture notes
* examples and fixtures for protocol behavior

The product surface is the skill package.

The skills are the protocol in operational form.

## Skill inventory

| Skill | Role |
| --- | --- |
| `loom-bootstrap` | mandatory first-read doctrine and route into Loom |
| `loom-workspace` | workspace entry, structure check, first routing decision |
| `loom-records` | shared grammar for IDs, frontmatter, typed links, status, validation, repair |
| `loom-constitution` | project identity, constraints, decisions, roadmap direction |
| `loom-initiatives` | strategic outcomes and success framing |
| `loom-research` | reusable discovery, experiments, tradeoffs, null results |
| `loom-specs` | intended behavior and acceptance contracts |
| `loom-plans` | sequencing, decomposition, rollout strategy |
| `loom-tickets` | live execution ledger and acceptance gate |
| `loom-evidence` | observed artifacts and claim support or challenge |
| `loom-critique` | adversarial review, findings, verdicts, residual risk |
| `loom-wiki` | accepted explanation and reusable understanding |
| `loom-memory` | optional support recall without shadow truth |
| `loom-ralph` | bounded fresh-context implementation loop |
| `loom-git` | implementation isolation, baseline, branch/worktree provenance |
| `loom-debugging` | reproduce-first debug workflow through existing layers |
| `loom-spike` | bounded investigation and sketch workflow through research and evidence |
| `loom-codemap` | repository atlas workflow through evidence, research, and wiki |
| `loom-ship` | PR, release, handoff, risk, and follow-up packaging |
| `loom-retrospective` | compounding pass that promotes accepted learning into owner layers |
| `loom-skill-authoring` | maintaining Loom-compatible skills without breaking the protocol |

## Repository layout

```text
.
├── README.md
├── PROTOCOL.md
├── ARCHITECTURE.md
├── AGENTS.md
├── examples/             # golden protocol fixtures and traces, not truth owners
├── optional-utilities/   # helpers that do not own semantics
└── skills/               # canonical Loom skill package
```

Inside a Loom-enabled project, the canonical runtime tree looks roughly like this:

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

## Installation model

Loom installs as a skills package.

Native harness adapters may add metadata, manifests, or preload hooks around `skills/`, but they do not add a second Loom ontology and they do not replace the skills.

The intended installation pattern is:

1. install or expose `skills/` as the Loom package
2. keep skill names and descriptions from `skills/*/SKILL.md` visible
3. use `loom-bootstrap` first unless the same ordered doctrine is already loaded by the adapter
4. hydrate the task-specific skill when that skill owns the next truth change
5. let the model read templates and references from that skill as needed

## Required loading model

`loom-bootstrap` is mandatory.

Agents should use it before starting work unless the same ordered bootstrap doctrine is already loaded in the current context by a native adapter.

`loom-bootstrap` reads these references in order:

1. `skills/loom-bootstrap/references/01-core-identity.md`
2. `skills/loom-bootstrap/references/02-truth-and-authority.md`
3. `skills/loom-bootstrap/references/03-outer-loop.md`
4. `skills/loom-bootstrap/references/04-ralph-inner-loop.md`
5. `skills/loom-bootstrap/references/05-critique-and-wiki.md`
6. `skills/loom-bootstrap/references/06-filesystem-and-tooling.md`
7. `skills/loom-bootstrap/references/07-validation-and-honesty.md`

When a harness has an `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, user rules, or a similar instruction surface, point it at the skill rather than copying doctrine:

```md
Loom is active in this workspace. Before any work, use the `loom-bootstrap` skill unless Loom's ordered bootstrap doctrine is already loaded in the current context. After bootstrap, route work through the Loom skill that owns the next truth change.
```

That instruction is a pointer, not a new source of truth.

## Quick install

> [!TIP]
> Loom is just a `skills/` directory with zero runtime dependencies. You should be able to use it in almost any coding harness by cloning or downloading this repo and putting `skills/` wherever that harness expects skills. The table below provides first-class install paths per harness as a convenience.

| Harness | Command |
| --- | --- |
| Claude Code | `claude plugin marketplace add z3z1ma/agent-loom && claude plugin install loom@agent-loom --scope user` |
| OpenCode | `opencode plugin open-loom --global` |
| Codex | `codex plugin marketplace add z3z1ma/agent-loom` |
| Cursor | `mkdir -p ~/.cursor/plugins/local && git clone https://github.com/z3z1ma/agent-loom.git ~/.cursor/plugins/local/agent-loom` |
| Gemini CLI | `gemini extensions install https://github.com/z3z1ma/agent-loom` |

Codex currently requires opening `/plugins` after marketplace registration to install or enable `loom`.

Cursor uses the local plugin directory until `agent-loom` is listed in Cursor Marketplace. After listing, the Cursor Agent chat command should be:

```text
/add-plugin agent-loom
```

## Harness notes

The following sections go into more details on installation compared to the quick install section above. You should only need this if you are interested in specific details or iterating on loom locally.

### Claude Code

This repository includes a Claude Code plugin manifest at `.claude-plugin/plugin.json` and a local marketplace catalog at `.claude-plugin/marketplace.json`.

The plugin exposes canonical `skills/` directly from the repository root and declares `claude-hooks/hooks.json` as its Claude hook config. Loom uses that hook surface to emit the ordered `loom-bootstrap` references as same-session `SessionStart` hook stdout.

Local development:

```bash
claude --plugin-dir /absolute/path/to/agent-loom
```

Local marketplace testing:

```bash
claude plugin marketplace add /absolute/path/to/agent-loom
claude plugin install loom@agent-loom --scope project
```

Remote install:

```bash
claude plugin marketplace add z3z1ma/agent-loom && claude plugin install loom@agent-loom --scope user
```

Validate the local plugin structure with:

```bash
claude plugin validate /absolute/path/to/agent-loom
```

The hook preload is a bonus. The canonical surface remains `skills/`, especially `skills/loom-bootstrap`.

### Codex

This repository includes a Codex plugin manifest at `.codex-plugin/plugin.json` and a marketplace catalog at `.agents/plugins/marketplace.json`. The plugin exposes canonical `skills/` directly from the repository root and is shaped for a Git-backed remote marketplace entry.

The target native remote path is Codex marketplace registration with the repository URL:

```bash
codex plugin marketplace add z3z1ma/agent-loom
```

Once installed plugin skill discovery is validated, users should be able to open Codex's `/plugins` browser and install or enable `loom` from the `agent-loom` marketplace.

Current evidence still needs installed plugin skill-discovery validation for `loom-bootstrap`, so this is not yet a broadly accepted Codex release path. The repository `.codex/` hook fixture proves optional trusted project preload of bootstrap references. It is not the product install path.

### OpenCode

This repository includes the `open-loom` OpenCode plugin at `open-loom.mjs`.

`open-loom` requires OpenCode `>=1.14.22 <2`.

Normal users can install the OpenCode plugin and update global config with:

```bash
opencode plugin open-loom --global
```

Equivalent package plugin entry:

```json
{
  "plugin": ["open-loom"]
}
```

Users working from a cloned repository should point OpenCode at the local plugin file instead:

```json
{
  "plugin": ["file:///absolute/path/to/agent-loom/open-loom.mjs"]
}
```

`open-loom` registers the bundled skill root with `config.skills.paths` and adds ordered `loom-bootstrap` references to `config.instructions`.

For a local structural check that does not require a model request, run:

```bash
node open-loom.mjs --smoke
```

### Cursor

This repository includes a Cursor plugin manifest at `.cursor-plugin/plugin.json`.

The manifest follows Cursor's native plugin format and exposes canonical `skills/` with `"skills": "./skills/"`.

Until `agent-loom` is listed in Cursor Marketplace, install from the Git repository as a local native Cursor plugin:

```bash
mkdir -p ~/.cursor/plugins/local && git clone https://github.com/z3z1ma/agent-loom.git ~/.cursor/plugins/local/agent-loom
```

Restart Cursor or run Developer: Reload Window after cloning.

Once the Marketplace listing exists, install from Cursor Agent chat with:

```text
/add-plugin agent-loom
```

### Gemini CLI

This repository includes a Gemini CLI extension manifest at `gemini-extension.json`.

The extension exposes canonical `skills/` and uses `contextFileName` to load `gemini-bootstrap.md`, which imports the ordered `skills/loom-bootstrap/references/*.md` files with Gemini's native context import syntax.

Install from the Git repository with:

```bash
gemini extensions install https://github.com/z3z1ma/agent-loom
```

Local development can link the repository instead:

```bash
gemini extensions link /absolute/path/to/agent-loom
```

Validate the local extension structure with:

```bash
gemini extensions validate /absolute/path/to/agent-loom
```

The context preload is a bonus. The canonical surface remains `skills/`, especially `skills/loom-bootstrap`.

## What Loom can replace

Loom can coexist with external issue trackers, planning tools, code-review systems, workflow packages, and agent command surfaces.

It can also make many of them unnecessary for the agent-facing work record.

That is the stronger claim.

The skills already prescribe the owner layers, the routing rules, the execution loop, the acceptance gate, the evidence posture, the review layer, the knowledge promotion path, and the handoff package. Once those terms exist inside the repo, the agent can compose the workflows directly.

External systems can mirror Loom state.

They should not be the only place the agent learns what is true.

## What Loom is

Loom is a way to keep AI work from dissolving into conversation.

It gives agents a vocabulary for placing work where it belongs.

It gives projects a memory that survives context windows, compaction, worker handoff, and time.

It is a project-state protocol for long-horizon AI knowledge work.

## What Loom is not

Loom is not a replacement for your codebase.

It is not a replacement for Git.

It is not a runtime, service, daemon, MCP server, product CLI, workflow engine, or hidden database.

It does not ask every task to use every layer.

It does not turn a typo fix into a ceremony.

It makes sure meaningful work has somewhere honest to go.

For small edits, skip the graph.

For long-running work, the graph prevents collapse.

## Costs

Loom asks for discipline.

Broken links matter. Stale records matter. Evidence that overclaims matters. A ticket that says the work is accepted when critique is unresolved is worse than no ticket at all.

Loom also has a threshold. If the work is small, local, and obvious, use the source tree and Git. Do not create a graph-shaped shrine around a one-line edit.

The graph pays for itself when work crosses sessions, changes behavior, needs review, involves research, carries risk, or leaves behind knowledge the next worker would otherwise rediscover.

## The point

The pieces already existed.

Loom puts them in one place and gives each one a job.

Once that happens:

```text
the work stops drifting
the agent stops carrying everything
the project starts remembering
```

That is the whole protocol.
