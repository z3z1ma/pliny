# Agent Loom

Agent Loom is a harness-agnostic, Markdown-first protocol for durable AI work.

This repository does not ship a conventional app, service, or framework runtime. It ships a reusable bundle of `rules/`, `skills/`, `commands/`, and standalone skill-local Python helpers that another project can copy into its own harness surface and use as an operating system for long-horizon agent work.

## What This Repository Ships

The product in this repo is the top-level:

- `rules/` - always-on Loom doctrine
- `skills/` - self-contained task-specific operating bundles
- `commands/` - slash-command prompt definitions
- `skills/*/scripts/*.py` - standalone, standard-library-only helper CLIs shipped directly inside each skill

Today that bundle includes:

- 16 skills
- 13 bundled Python CLIs
- 2 slash commands

End users typically copy those directories into their own project under `.opencode/` or another harness-specific location.

## What Loom Is

Loom treats the filesystem as the interface.

- Markdown files hold durable project state
- tickets are the live execution ledger
- packets are bounded handoff contracts for fresh-context execution
- critique and docs stay separate from execution truth
- helper scripts only mechanize structural work that benefits from determinism

The point is to let another agent enter a repository cold, read the visible corpus, and continue safely without reconstructing hidden norms from chat history or a private runtime.

## What Loom Is Not

- not a monolithic `loom` CLI
- not a long-running orchestration service
- not a database-backed project manager
- not a normal app or library with a runtime and test suite

Verification here is primarily structural: lint the shipped CLIs, validate record structure, validate links, and keep the Markdown corpus truthful.

## Repository Structure

```text
.
├── rules/       # always-on doctrine and appendices
├── skills/      # skill bundles with SKILL.md, references/, scripts/
├── commands/    # slash-command prompt definitions
├── .loom/       # dogfooding records, packets, verification, memory
├── .opencode/   # local consumption surface used by this repo itself
├── AGENTS.md    # repository-specific contributor guidance
└── README.md
```

Important boundary:

- `rules/`, `skills/`, and `commands/` are the maintained product source
- `.loom/` and `.opencode/` are dogfooding and consumption artifacts, not the source of truth for the shipped product

## Core Surfaces

If you are new to the repo, start here:

- `rules/loom.md` - core Loom doctrine and operating order
- `rules/layers.md` - artifact boundaries and truth ownership
- `skills/loom-workspace/` - workspace discovery, diagnostics, scope resolution
- `skills/loom-tickets/` - canonical execution ledger workflow
- `skills/loom-ralph/` - bounded packetized fresh-context execution

Other included skills cover specs, plans, research, initiatives, critique, docs, constitution maintenance, and the memory subsystem.

The current slash-command surface is:

- `commands/loom-memory-reflect.md`
- `commands/loom-memory-housekeeping.md`

## Quickstart

### 1. Copy the Loom bundle into your project

Example:

```bash
mkdir -p .opencode
cp -R /path/to/agent-loom/rules /path/to/agent-loom/skills /path/to/agent-loom/commands .opencode/
```

That gives your project the always-on doctrine, skill bundle, slash commands, and each skill's standalone helper scripts.

### 2. Read the doctrine in order

For a cold start, the minimum useful reading path is:

1. `rules/loom.md`
2. `constitution:main` in your workspace
3. the skill that owns the next durable action

### 3. Establish workspace trust first

In a Loom-enabled workspace, the normal first move is to diagnose the workspace before trusting downstream records or packet work.

From this repo, for example:

```bash
skills/loom-workspace/scripts/workspace.py diagnose --json
```

## Typical Workflow

1. Diagnose workspace health and scope ownership.
2. Read or create the owning ticket.
3. Decide whether the work is local editing, validation, or bounded child execution.
4. If execution should happen in a fresh context, compile a Ralph packet.
5. Run the bounded step.
6. Reconcile the result back into the ticket ledger.
7. Run critique or docs follow-through when the change class calls for it.

Loom keeps those layers separate on purpose: plans stay strategic, tickets stay operational, critique stays adversarial, docs stay explanatory.

## Bundled Workflow Areas

- `loom-workspace` - workspace bootstrap, status, diagnosis, links, scope
- `loom-tickets` - ticket creation, linking, dependencies, verification
- `loom-ralph` - packet scaffolding and post-run verification
- `loom-critique` - review packets and durable critique records
- `loom-docs` - durable explanatory docs and docs packets
- `loom-specs`, `loom-plans`, `loom-research`, `loom-initiatives`, `loom-constitution` - canonical record maintenance
- `loom-memory-context`, `loom-memory-reflect`, `loom-memory-housekeeping` - optional memory subsystem operations
- `loom-explainer`, `loom-humanizer`, `loom-skill-authoring` - supporting authoring skills

## Verification And Development

There is no traditional test suite in this repo.

The normal verification path is structural:

```bash
uvx ruff check skills/*/scripts/*.py
uvx ruff format --check skills/*/scripts/*.py
skills/loom-workspace/scripts/workspace.py diagnose --json
skills/loom-tickets/scripts/tickets.py create ticket
```

Useful repo-local commands:

```bash
skills/loom-workspace/scripts/workspace.py status
skills/loom-workspace/scripts/workspace.py diagnose --fix
skills/loom-workspace/scripts/workspace.py scope README.md
skills/loom-ralph/scripts/ralph.py packet "ticket:0002" ralph --mode execution --style reference-first --allow-write-ref "ticket:0002"
```

## Contributing

If you are changing the product, treat these as the source surfaces:

- `rules/`
- `skills/`
- `commands/`

Important repo rules:

- edit skill-local CLI behavior directly in `skills/*/scripts/*.py`
- keep shipped skills self-contained
- do not treat `.loom/` or `.opencode/` as product source of truth
- prefer small, direct changes over scaffolding or hidden abstraction

Read `AGENTS.md` before making non-trivial changes. It contains the repository's authoritative guidance on structure, style, validation, and cross-surface consistency.

## Why This Repo Exists

The goal is to make Loom portable, inspectable, and usable across harnesses.

Instead of hiding the system inside one runtime, Agent Loom puts the operating model in visible Markdown doctrine, skill bundles, canonical records, and thin deterministic helpers. The durable asset is the protocol and work discipline, not a single implementation shell.
