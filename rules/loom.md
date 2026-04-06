# Loom Doctrine

## Purpose

Loom is a Markdown-first protocol for organizing long-horizon work so that another agent can enter the workspace, understand the current state, and continue without guessing hidden context.

Everything in Loom is a plain file in a directory tree. That is the design, not a limitation. Because the corpus is ordinary Markdown on disk, every tool that operates on files operates on Loom:

- `grep -R "ticket:0004" .loom` is a graph query
- `find .loom/tickets -name "*.md"` is record discovery
- `git log --oneline .loom/specs/` is a change history
- reading a file is reading the record
- editing a file is editing the record
- deleting a file is retiring the record (after reconciling references)

The filesystem is the interface. The directory tree is the schema. Standard tools are first-class operators. Loom does not need a runtime, a database, or a custom query layer. The entire protocol is legible to `grep`.

## How It Works

The important pieces are:

- the core rules in this directory
- task-specific skills in the Loom skill bundle
- canonical records in designated `.loom/` subtrees
- durable packets, run artifacts, and verification artifacts that support bounded child execution

The practical goal:

- another agent enters a Loom workspace cold
- reads the core rules, then `constitution:main`, then one relevant skill
- understands what work is being done
- knows which artifact to read or update
- knows when to compile a packet and launch a fresh child run
- knows how to reconcile the result without inventing policy

If the core rules leave you needing more concrete shape, read the appendix material under `appendices/`.

- `appendices/worked-example-flow.md` — one end-to-end parent workflow
- `appendices/common-schema-conventions.md` and `appendices/layer-schemas.md` — field and section expectations for structured records
- `appendices/naming-conventions.md` — file and record naming
- `appendices/memory-module.md` — the optional `.loom/memories/` module

## The Filesystem Is The API

Loom artifacts are normal files. That means the agent operates on them with normal tools.

### Reading and searching

Read records directly from the filesystem. Search the corpus with `grep`, `find`, `rg`, or the harness search tools. There is no separate query interface.

```bash
# Find all active tickets
grep -rl '"status": "active"' .loom/tickets/

# Find everything that references a spec
grep -R "spec:packet-governance" .loom

# List all critique records
find .loom/critique -name "*.md"

# Check which tickets link to a plan
grep -l "plan:execution-rollout" .loom/tickets/*.md
```

These are not workarounds. They are the intended way to navigate the corpus. The protocol is designed so that standard text-search tools produce meaningful answers.

### Editing

Edit record prose directly with the harness edit tools or any text editor. Records are Markdown. The agent writes content into them the same way it writes code or documentation.

### Deleting and renaming

When removing or renaming a record, search for references first, update them, then perform the file operation:

```bash
grep -R "ticket:0003" .loom    # find all references
# ... edit those files to remove or update the references ...
rm .loom/tickets/agel-0003-old-ticket.md
```

The sequence matters: search, reconcile, then remove.

### Observing the corpus

Because the corpus is plain text and version-controlled, ordinary tools give you powerful visibility:

```bash
git diff .loom/                          # what changed since last commit
git log --oneline .loom/tickets/         # ticket change history
wc -l .loom/memories/user/observations.md  # memory file size check
find .loom -name "*.md" | wc -l          # total record count
```

## Helper Scripts

Helper CLIs exist for a narrow purpose: to provide structural determinism where the agent cannot reliably provide it.

Scripts earn their place when they guarantee:

- correct frontmatter scaffolding and parsing
- required-section enforcement
- link integrity checks
- workspace diagnostics and scope resolution
- record validation against known schemas

Scripts do not earn their place for:

- reading records (the agent reads files)
- writing record content (the agent edits files)
- searching the corpus (the agent uses `grep` and `find`)
- deleting records (the agent uses file operations)

The boundary: if the task requires structural determinism, a script may own it. If the task requires understanding, judgment, or composition, the agent owns it with standard tools.

Helper-created records are structural scaffolds. They are valid starting points with correct frontmatter and section headings, expected to be filled in with normal editing tools afterward.

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

## Workspace Entry

When entering a repository for Loom work, resolve the workspace root before reading or mutating Loom artifacts.

1. search upward for the nearest directory containing both `.git/` and `.loom/`
2. if no established workspace exists, allow the current working directory as the workspace root unless it is a non-root subdirectory of a git repository
3. if `.loom/` does not exist or is incomplete, the workspace must be initialized before proceeding
4. if `.loom/` exists but workspace health is uncertain, inspect it directly with native file tools before trusting records for downstream work

If the current working directory is a non-root subdirectory of a git repository and no established workspace exists above it, fail closed.

## Operating Order

When operating inside a Loom workspace:

1. start from the core rules
2. read `constitution:main` before choosing a local path through the work
3. choose the skill that owns the current artifact or workflow
4. read that skill's references and examples before editing or launching work
5. read the relevant canonical records directly
6. use deterministic scripts only to mechanize already-published rules

This order matters because the rules set the stable operating posture, the constitution establishes durable project policy, the skill tells you how to handle the current kind of work, and the records tell you the current state.

## Record-Writing Doctrine

When writing or updating Loom records, prefer detail-first, self-contained records over terse reminders.

The writing bar:

- a future agent should be able to read the record alone plus its explicit links and act without guessing hidden context
- the record should explain why the work matters, not just what file changed
- the record should preserve enough context for truthful resumption after the current session ends

For important records, especially plans and tickets, assume the next reader is a novice who has only the working tree and the visible Loom corpus.

Avoid records that are technically present but operationally thin:

- a ticket that says "make progress" without enough context to execute safely
- a plan that lists tasks but does not explain the intended sequencing or proof strategy
- a doc that restates conclusions without showing what evidence supports them

## Instruction-Writing Doctrine

Rules and skills SHOULD lead with positive operating instructions: what to do, what evidence to produce, when to escalate. Prohibitions close known failure modes after the positive path is stated.

## Working Defaults

- frontmatter is JSON-compatible structured data between `---` fences
- canonical records remain Markdown-first and human-readable
- ordinary corpus work happens through standard file tools
- helper-created records are structural scaffolds, expected to be edited further
- validation is strict on structure and soft on prose
- packet files persist under `.loom/runs/`
- verification records live under `.loom/verification/`

For the detailed field and status vocabulary, read `appendices/common-schema-conventions.md`.

## When The Next Action Is Unclear

Work through this sequence:

1. identify whether the task has durable consequences
2. resolve the workspace root explicitly
3. if `.loom/` is missing or incomplete, bootstrap it before further Loom work
4. if `.loom/` exists but health is uncertain, inspect it directly with native file tools and targeted checks
5. read `constitution:main` and any clearly relevant constitutional records
6. choose the owning skill and load it
7. resolve repository and worktree scope explicitly
8. read the current canonical record state directly
9. decide whether the work is local editing, local validation, or packet-consuming child execution
10. if packet-consuming work is needed, compile a packet and launch a fresh child context
11. validate and reconcile the resulting state back into canonical records
