# Loom Doctrine

## Purpose

Loom is a Markdown-first way of organizing long-horizon work so that another agent can enter the workspace, understand the current state, and continue without guessing hidden context.

The important pieces are:

- the core rules in this directory
- task-specific skills in the Loom skill bundle, typically exposed to operators under `.opencode/skills/`
- canonical records in designated `.loom/` subtrees
- durable packets, run artifacts, and verification artifacts that support bounded execution

The practical goal is simple:

- another agent should be able to enter a Loom workspace cold
- read the core rules, then `constitution:main`, then one relevant skill
- understand what work is being done
- know which artifact to read or update
- know when to compile a packet and launch a fresh child run
- know how to reconcile the result without inventing policy

If the core rules leave you needing more concrete shape, read the appendix material under `appendices/`.

- Read `appendices/worked-example-flow.md` when you want one end-to-end parent workflow example.
- Read `appendices/common-schema-conventions.md` and `appendices/layer-schemas.md` when editing structured records and you need field or section expectations.
- Read `appendices/naming-conventions.md` when naming new files, records, or helper scripts.
- Read `appendices/memory-module.md` when the optional `.loom/memories/` module is present and you need its non-canonical memory rules.

## Always-On Rules

1. Canonical project truth lives in canonical `.loom/` subtrees.
2. Tickets are the sole live execution ledger.
3. Packets are bounded execution contracts, not transcript dumps.
4. Packet-consuming flows SHOULD run in fresh harness contexts.
5. Child write authority MUST be explicitly bounded by the packet allowed write set.
6. Scope MUST fail closed.
7. Helper scripts MUST mechanize visible Markdown rules and MUST NOT invent hidden ontology.
8. Skills MAY refine local behavior, but MUST NOT override these rules.
9. Before starting any non-trivial Loom work, agents MUST read `constitution:main` so local execution stays aligned with durable project policy.

## Agent and Helper Boundary

The agent is the primary operator. Helper scripts are narrow mechanical utilities that serve the agent where determinism matters more than judgment.

Scripts earn their place when they provide structural guarantees the agent cannot reliably provide on its own: record validation, frontmatter parsing and scaffolding, link integrity, scope resolution, workspace diagnostics, and frontmatter-aware querying. These are mechanical tasks where reproducible, deterministic results matter.

Everything else is agent work. The agent reads records, populates content, searches the workspace, edits artifacts, makes decisions, orchestrates workflow steps, and reconciles outcomes. Workflow steps like Ralph execution, critique, and docs follow-through are agent actions -- the agent launches a fresh context with a compiled packet, uses its standard capabilities to do the work, and returns the result. These steps do not need custom orchestration scripts.

The boundary is simple: if the task requires deterministic structural integrity, a script may own it. If the task requires understanding, judgment, or composition, the agent owns it. Do not wrap agent work in scripts. Do not add a script for something the agent already handles well with its own capabilities and standard tools.

## Workspace Entry Rule

When entering a repository for Loom work, resolve the workspace root before reading or mutating Loom artifacts.

Use this order:

1. search upward for the nearest directory containing both `.git/` and `.loom/`
2. if no established workspace exists, allow the current working directory as the workspace root unless it is a non-root subdirectory of a git repository
3. if `.loom/` does not exist or is incomplete, the workspace must be initialized before proceeding — the loom-workspace skill owns workspace bootstrapping and repair
4. if `.loom/` exists but workspace health is uncertain, diagnose before trusting records for downstream work

If the current working directory is a non-root subdirectory of a git repository and no established workspace exists above it, fail closed and surface the ambiguity rather than guessing.

## Loom Operating Order

When operating inside a Loom workspace, use the corpus in this order:

1. start from the core rules
2. read `constitution:main` before choosing a local path through the work
3. choose the skill that owns the current artifact or workflow
4. read that skill's references and examples before editing or launching work
5. read the relevant canonical records in `.loom/`
6. use deterministic scripts only to mechanize already-published rules

This order matters because the rules set the stable operating posture, the constitution establishes durable project policy, the skill tells you how to handle the current kind of work, and the records tell you the current state.

## Instruction-Writing Doctrine

Rules and skills SHOULD lead with positive operating instructions.

That means they should answer:

- what situation has been detected
- what artifact now owns the work
- what the agent should read next
- what action the agent should take next
- what output or mutation is expected
- how to tell whether the action succeeded

Prohibitions still matter, but they are secondary. Use them to close a known failure mode after the positive path has already been stated.

Good pattern:

- first say what to do
- then say what evidence to produce
- then say when to escalate
- only then add narrow guardrails for known bad behavior

Weak pattern:

- a list of things to avoid without a primary procedure

## Record-Writing Doctrine

When writing or updating Loom records, prefer detail-first, self-contained records over terse reminders.

The writing bar is:

- a future agent should be able to read the record alone plus its explicit links and act without guessing hidden context
- the record should define terms of art in plain language or avoid them
- the record should explain why the work matters, not just what file changed
- the record should preserve enough context for truthful resumption after the current session ends

For important records, especially plans and tickets, assume the next reader is a novice to the workspace who has only the working tree and the visible Loom corpus.

That means records should be:

- self-contained
- explicit about purpose and scope
- concrete about expected outcomes and verification
- durable enough to survive handoff

Avoid records that are technically present but operationally thin.

Non-canonical memory under `.loom/memories/` may be useful supporting context, but it does not replace canonical records and does not relax the truth hierarchy.

Examples of operationally thin records:

- a ticket that says "make progress" without enough context to execute safely
- a plan that lists tasks but does not explain the intended sequencing, rationale, or proof strategy
- a doc that restates conclusions without showing what evidence supports them

## Working Defaults

- frontmatter is stored as JSON-compatible structured frontmatter between `---` fences so the helper layer can stay stdlib-only
- canonical records remain Markdown-first and human-readable
- validation is strict on structure and soft on prose
- packet files persist by default under `.loom/runs/`
- verification that must participate in the durable evidence graph should be recorded as Markdown verification records under `.loom/verification/`

For the detailed field and status vocabulary behind these defaults, read `appendices/common-schema-conventions.md`.

## Positive Operating Posture

When the next action is unclear, the parent agent should work through this sequence:

1. identify whether the task has durable consequences
2. resolve the workspace root explicitly
3. if the resolved git root does not yet contain `.loom/` or is missing canonical subtrees, load the loom-workspace skill to bootstrap and repair the workspace before further Loom work
4. if `.loom/` exists but health is uncertain, diagnose workspace health before trusting it
5. read `constitution:main` and any clearly relevant constitutional decision or roadmap records
6. choose the owning skill and load it
7. resolve the repository and worktree scope explicitly
8. read the current canonical record state
9. decide whether the work is local editing, local validation, or packet-consuming child execution
10. if packet-consuming work is needed, compile a packet and launch a fresh child context
11. validate and reconcile the resulting state back into canonical records
