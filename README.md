# Loom - Markdown-Native Control Plane

Loom is a harness-agnostic protocol for long-horizon AI knowledge work.

It treats the filesystem as the interface, Markdown as the durable medium, and
fresh-context packets as the default way to delegate bounded implementation.
Critique and wiki work may reuse packet discipline, but their domain workflows
own review and synthesis.

This package is intentionally **not** a runtime, service, daemon, MCP, or product CLI.

It ships:

- a mandatory `loom-bootstrap` skill with ordered doctrine references that teach
  the model how Loom thinks and how Loom must be used
- on-demand `skills/` that teach the model how to operate each subsystem in detail
- Markdown templates and query recipes instead of bundled Python helpers
- a cohesive explanation layer: **Loom Wiki**

Read `PROTOCOL.md` for the stable protocol summary.

Loom is best understood as a source-of-truth type system plus a transaction
protocol for fallible AI workers. The workers are disposable. The graph is
durable. The parent is the transaction coordinator. Tickets are the execution
ledger. Evidence stores observed artifacts. Critique pressure-tests claims.
Wiki is the accepted explanation layer.

## The Core Shape

Loom has three operating axes:

- **layers**: typed owners for different kinds of truth
- **loops**: outer-loop shaping and inner-loop execution
- **packets**: bounded contracts for fresh-context work

A Loom transaction uses the kernel roles defined in `PROTOCOL.md`: owners,
claims, packets, evidence, critique, acceptance disposition, and promotion.

The layer model is the type system. Canonical owner layers own project truth;
support surfaces help recovery and handoff without becoming truth owners.

| Layer | Owns |
| --- | --- |
| constitution | durable identity, principles, hard constraints, precedent |
| initiative | strategic outcome |
| research | evidence synthesis, investigations, options, rejected paths, null results |
| spec | intended behavior and acceptance contract |
| plan | sequencing and rollout strategy |
| ticket | live execution state |
| evidence | observed artifacts |
| critique | adversarial findings and verdicts |
| wiki | accepted explanation |
| packet | bounded child-worker contract, not project truth |
| memory | optional support context only |

The rule that keeps the graph coherent is simple: truth ownership is by layer,
not by recency.

For software work, the codebase owns current implementation reality. Specs own
reusable intended behavior and acceptance contracts. Tickets own scoped execution,
ticket-local criteria when no spec exists, and acceptance disposition. Evidence
bridges implementation to claims, and critique judges whether the bridge is
strong enough.

## The Two Loops

### Outer loop

The outer loop scopes and re-scopes the work.

Its backbone progression is:

`constitution -> initiative -> plan -> ticket`

Use conditional gates before plan or ticket:

- route to research when evidence synthesis, tradeoffs, or conclusions are missing
- route to spec when intended behavior or acceptance criteria are fuzzy

### Inner loop

The inner loop is **Ralph**.

Ralph is one bounded packet, one fresh worker, one iteration, one reconciliation
pass.

A parent agent compiles a packet, launches or delegates one fresh-context execution step, receives a bounded outcome, merges truth back into the ticket, and either continues, stops, escalates, or routes into critique/wiki.

Critique and Wiki may reuse packet discipline, but their domain workflows own
review and synthesis. They are sibling routes, not Ralph-governed execution.

The deeper invariant is ownership-preserving mutation: every durable claim,
behavior, evidence artifact, risk, and explanation lands in the artifact that owns that
kind of truth.

### Transaction spine

Every non-trivial Loom transaction follows the same spine:

`route -> shape -> ready -> execute -> reconcile -> verify -> accept -> promote -> close`

If a step cannot be completed honestly, route backward to the owner that can fix
the gap instead of advancing on vibes.

## Repository Layout

```text
.
├── README.md
├── PROTOCOL.md
├── ARCHITECTURE.md
├── AGENTS.md
├── examples/         # golden protocol fixtures and traces, not truth owners
├── optional-utilities/
└── skills/
```

Expose the frontmatter `name` and `description` from each `skills/*/SKILL.md`.
Agents must use `skills/loom-bootstrap` first unless its ordered bootstrap
references are already loaded in the current context by a harness adapter. Then
hydrate the task-specific skill when relevant.

Inside a Loom-enabled project, the canonical runtime tree is expected to look roughly like this:

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

## Installation Model

The intended installation pattern is simple:

1. install or expose `skills/` as the Loom package
2. keep skill names/descriptions from `skills/*/SKILL.md` visible
3. use `skills/loom-bootstrap` first unless the same ordered doctrine is already
   loaded by the adapter
4. hydrate the full `skills/<name>/SKILL.md` only when that skill is relevant
5. let the model read templates and references from that skill as needed

Read `Installing Loom` section for the recommended adoption path, native install or
registration commands, and harness-specific caveats.

## Protocol Core And Workflows

The core protocol is the visible graph of canonical owner layers plus durable
support surfaces.

Canonical owner layers:

- constitution
- initiative
- research
- spec
- plan
- ticket
- evidence
- critique
- wiki

Durable support surfaces:

- packet
- memory
- workspace support records

Workflows such as brainstorm, debug, spike, sketch, map, Git-backed isolation,
review, accept, ship, retrospective, repair, and wiki write/audit are
compositions through those layers. They should not create new truth owners
unless a genuinely new kind of truth exists.

Harness adapters expose the skill package through each harness's native skill or
plugin system. They may preload `loom-bootstrap` references where the harness
supports it cleanly, but they do not own semantics. Optional utilities stay under
`optional-utilities/` and are not part of the default protocol install.

## Installing Loom

Loom installs as a skills package.

The product surface is `skills/`. Native harness adapters may add metadata,
manifests, or preload hooks around that directory, but they do not add a second
Loom ontology and they do not replace the skills.

### Required Loading Model

Expose the frontmatter `name` and `description` from each `skills/*/SKILL.md`.

The `loom-bootstrap` skill is mandatory. Agents should use it before starting any
work unless the same ordered bootstrap doctrine is already loaded in the current
context by a native adapter.

`loom-bootstrap` reads these references in order:

1. `skills/loom-bootstrap/references/01-core-identity.md`
2. `skills/loom-bootstrap/references/02-truth-and-authority.md`
3. `skills/loom-bootstrap/references/03-outer-loop.md`
4. `skills/loom-bootstrap/references/04-ralph-inner-loop.md`
5. `skills/loom-bootstrap/references/05-critique-and-wiki.md`
6. `skills/loom-bootstrap/references/06-filesystem-and-tooling.md`
7. `skills/loom-bootstrap/references/07-validation-and-honesty.md`

Harnesses may preload those references as always-on context. That is an adapter
optimization over the same skill package, not a separate doctrine source.

### Native Harness Installs

Use the native package system for each harness.

| Harness | Native path | Loom surface |
| --- | --- | --- |
| Claude Code | Claude plugin manifest and marketplace metadata | `skills/`, plus optional `SessionStart` preload from `loom-bootstrap` references |
| Codex | Codex plugin manifest and marketplace metadata | `skills/` with `loom-bootstrap` as the required entry skill |
| OpenCode | `open-loom` plugin | `skills/`, plus OpenCode `instructions` preload from `loom-bootstrap` references |
| Cursor | Cursor plugin/skill package | `skills/` with `loom-bootstrap` as the required entry skill |
| Gemini CLI | Gemini extension/skill package | `skills/` with `loom-bootstrap` as the required entry skill |

There is no supported Makefile, shell installer, or cross-harness fallback copy
script. Older generated installs should be treated as legacy local state and
cleaned up manually if they are still present.

### Quick Install Commands

Use the harness-native command for your environment:

| Harness | Command |
| --- | --- |
| Claude Code | `claude plugin marketplace add z3z1ma/agent-loom && claude plugin install loom@agent-loom --scope user` |
| OpenCode | `opencode plugin open-loom --global` |
| Codex | `codex plugin marketplace add z3z1ma/agent-loom` |
| Cursor | `mkdir -p ~/.cursor/plugins/local && git clone https://github.com/z3z1ma/agent-loom.git ~/.cursor/plugins/local/agent-loom` |
| Gemini CLI | `gemini extensions install https://github.com/z3z1ma/agent-loom` |

Codex currently requires opening `/plugins` after marketplace registration to
install or enable `loom`. Cursor's command above uses Cursor's native local plugin
directory until `agent-loom` is listed in Cursor Marketplace; after listing, the
Cursor Agent chat command should be `/add-plugin agent-loom`.

### Minimal Harness Instruction

When a harness has an `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, user rules, or a
similar instruction surface, point it at the skill rather than copying doctrine:

```md
Loom is active in this workspace. Before any work, use the `loom-bootstrap` skill
unless Loom's ordered bootstrap doctrine is already loaded in the current context.
After bootstrap, route work through the Loom skill that owns the next truth
change.
```

That instruction is a pointer, not a new source of truth.

### Claude Code

This repository includes a Claude Code plugin manifest at
`.claude-plugin/plugin.json` and a local marketplace catalog at
`.claude-plugin/marketplace.json`.

The plugin exposes canonical `skills/` directly from the repository root and
declares `claude-hooks/hooks.json` as its Claude hook config. Loom uses that hook
surface to emit the ordered `loom-bootstrap` references as same-session
`SessionStart` hook stdout.

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

The hook preload is a bonus. The canonical surface remains `skills/`, especially
`skills/loom-bootstrap`.

### Codex

This repository includes a Codex plugin manifest at `.codex-plugin/plugin.json`
and a marketplace catalog at `.agents/plugins/marketplace.json`. The plugin
exposes canonical `skills/` directly from the repository root and is shaped for a
Git-backed remote marketplace entry.

The target native remote path is Codex marketplace registration with the
repository URL:

```bash
codex plugin marketplace add z3z1ma/agent-loom
```

Once installed plugin skill discovery is validated, users should be able to open
Codex's `/plugins` browser and install or enable `loom` from the `agent-loom`
marketplace.

Current evidence still needs installed plugin skill-discovery validation for
`loom-bootstrap`, so this is not yet a broadly accepted Codex release path. The
repository `.codex/` hook fixture proves optional trusted project preload of
bootstrap references; it is not the product install path.

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

Users working from a cloned repository should point OpenCode at the local plugin
file instead:

```json
{
  "plugin": ["file:///absolute/path/to/agent-loom/open-loom.mjs"]
}
```

`open-loom` registers the bundled skill root with `config.skills.paths` and adds
ordered `loom-bootstrap` references to `config.instructions`.

For a local structural check that does not require a model request, run:

```bash
node open-loom.mjs --smoke
```

### Cursor

This repository includes a Cursor plugin manifest at `.cursor-plugin/plugin.json`.
The manifest follows Cursor's native plugin format and exposes canonical `skills/`
with `"skills": "./skills/"`.

Until `agent-loom` is listed in Cursor Marketplace, install from the Git repository
as a local native Cursor plugin:

```bash
mkdir -p ~/.cursor/plugins/local && git clone https://github.com/z3z1ma/agent-loom.git ~/.cursor/plugins/local/agent-loom
```

Restart Cursor or run Developer: Reload Window after cloning. Once the Marketplace
listing exists, install from Cursor Agent chat with:

```text
/add-plugin agent-loom
```

### Gemini CLI

This repository includes a Gemini CLI extension manifest at
`gemini-extension.json`. The extension exposes canonical `skills/` and uses
`contextFileName` to load `gemini-bootstrap.md`, which imports the ordered
`skills/loom-bootstrap/references/*.md` files with Gemini's native context import
syntax.

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

The context preload is a bonus. The canonical surface remains `skills/`,
especially `skills/loom-bootstrap`.

### Workspace Bootstrap

Loom does not create a runtime database. In a project that uses Loom, the agent
creates and edits `.loom/` records directly using the relevant skills and
templates.

The common workspace tree is:

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
└── memory/
```

Use `skills/loom-workspace`, `skills/loom-constitution`, and
`skills/loom-tickets` for the first records.
