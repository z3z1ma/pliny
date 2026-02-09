# Loom

Loom is an agent-native development substrate for terminal AI. It turns a Git repo into a durable environment where agents can plan, execute, coordinate, remember, and learn without relying on scrollback or fragile prompt chains.

Loom stays close to Unix primitives: files, worktrees, and tmux. The CLI is intentionally forgiving (agentic UX): it normalizes common "close enough" inputs and fails with actionable errors.

If you can `git clone` it, Loom can live in it.

## Highlights

- File-backed by default: artifacts you can open, diff, and review.
- Work isolation via git worktrees and snapshots.
- Multi-agent orchestration with tmux plus a disk-backed inbox.
- Two kinds of long-term memory: open-ended notes and reusable procedures.
- Deterministic CLI surfaces (output treated as a contract and locked by focused tests).

## How Loom works

Loom is not a framework. It is a set of state primitives and CLIs that agree on where things live on disk and how agents should interact with them.

- Intent is a document (tickets).
- Execution happens in isolated worktrees (workspace).
- Coordination is operational (tmux + inbox + merge queue).
- Memory is inspectable (Markdown notes).
- Learning is durable (skills as Markdown).

## Subsystems

Each subsystem has a CLI surface and an on-disk footprint.

| Subsystem | CLI | On disk | What it's for |
| --- | --- | --- | --- |
| Ticket | `loom ticket` | `.loom/ticket/` | Intent and execution state as Markdown + frontmatter, with deps/links/claims |
| Workspace | `loom workspace` | `.loom/workspaces/workspace.json`, `.loom/workspace/` | Worktree lifecycle, snapshots, multi-repo coordination, component deps |
| Team | `loom team` | `.loom/team/` | tmux-native orchestration: manager/workers/inbox/merge queue |
| Memory | `loom memory` | `.loom/memory/` | Obsidian-like Markdown notes; derived SQLite cache for recall |
| Compound | `loom compound` | `.opencode/` | Compounding: skills as procedural memory (SKILL.md), plus tooling scaffolding |
| Dashboard | `loom dashboard` | - | HTTP API for dashboards (see `docs/openapi.yaml`) |

## Starter snippets (agent copy/paste)

These are intentionally directive. They explain what each subsystem is for, why it matters, and when to reach for it; the mechanics are progressive disclosure via `-h` and `prime`.

Canonical loop (what Loom is optimizing for):

- Ticket: externalize intent + state (the work ledger)
- Workspace: isolate execution (safe, parallel worktrees)
- Memory: persist what you learned and general domain knowledge (scoped, recallable context)
- Compound: persist how to do it next time (procedures as Skills)

Treat the CLI as the source of truth. Prefer `loom ...` commands over hand-editing `.loom/**` files so locks/audits/indexes stay consistent.

### Ticket

We use Loom Ticket for Git-backed issue tracking and as the durable work ledger for agents.

A ticket is a single Markdown document with YAML frontmatter (status/priority/type/tags) plus a readable body (description/design/notes). Tickets also have first-class relationships: deps (blocking), links (related), and parent/children (hierarchy), so "ready vs blocked" is computable rather than debatable. Writes are guarded (locks), auditable (jsonl audit log), and automatable (`--json` outputs), which is what makes it safe for humans and agents to collaborate. References are flexible: ids, `#id`, filenames, and paths normalize to a ticket id; partial ids resolve unless ambiguous.

This matters because agents lose state without file-backed intent: tickets act as the write-ahead log that prevents rework and makes progress reviewable. The deps/ready/blocked surfaces turn planning into a graph problem instead of a vibe check. Claims (leases) provide an explicit concurrency primitive: multiple agents can look, but only one should mutate at a time.

Operationally, any non-trivial work starts with a ticket; treat it as the source of truth for scope, current status, and next actions. Use Ticket for tasks/bugs/features and coordination; put reusable lessons into Memory and durable procedure into Compound. Use deps when something is truly blocked, use notes for short timestamped progress, and use `--json` when driving from scripts. If you are about to hand-edit a ticket file, stop: prefer `loom ticket update` so locks/audit/normalization rules are respected.

On disk: `.loom/ticket/`

Start here:

```bash
loom ticket -h
loom ticket prime

loom ticket create "<title>" --type task --priority 2 --tags docs
loom ticket ready
loom ticket show <ticket-id>
loom ticket add-note <ticket-id> "<progress update>"
```

If you're coordinating multiple agents:

```bash
loom ticket claim <ticket-id> --ttl 45m
loom ticket dep-add <ticket-id> <blocking-ticket-id>
loom ticket view <ticket-id>
```

Use these when you need planning leverage (not more prose):

```bash
loom ticket ready
loom ticket blocked
loom ticket dep <ticket-id>
loom ticket query --format json
```

Common failure mode this prevents: "we kept working, but nobody can explain the current state." Tickets make state a file.

### Memory

We use Loom Memory for durable knowledge and context packs: Obsidian-like Markdown notes with scopes + links, indexed for fast recall.

The files are the source of truth (Markdown + YAML frontmatter); the sqlite index is derived and rebuildable. Notes can be scoped to the real world: `file:...`, `folder:...`, `glob:...`, `command:...`, `filetype:...`, `tag:...`. Memory is also a link graph: wikilinks like `[[concept]]` turn isolated notes into navigable context. Visibilities exist for a reason: shared (committed), personal (gitignored), ephemeral (scratch). Use the right bucket.

This matters because agents need small, relevant context: scoped recall produces a tight context pack instead of dumping the vault into the prompt. Memory captures the "why" behind decisions and the "gotchas" behind fixes, which tickets should not carry forever. Because the index is derived, you can trust the on-disk notes and rebuild safely (`reindex`) when needed.

Write Memory after you discover a sharp edge, a convention, a design rationale, a flaky test root cause, or a debugging playbook. Before starting similar work, recall memory scoped to the code or command you are about to touch. When files move, run janitor to keep file scopes honest; when a note is obsolete, deprecate it (soft forget) instead of deleting history. Capture command output into Memory when it is evidence (test failures, logs, repro steps) and scope it with `command:`.

On disk: `.loom/memory/`

Start here:

```bash
loom memory -h
loom memory prime

loom memory recall "<query>" --context --format prompt
loom memory add --title "<title>" --body "<what you learned>" --command "<the command you ran>"
```

Rules of thumb:

- Prefer Memory for durable notes; prefer Tickets for work items.
- Scope notes to the thing that triggered them (`--command` or `--scope file:...`) so recall stays relevant.
- Add wikilinks like `[[concept-id]]` in note bodies when you reference concepts.

High leverage commands (context hygiene):

```bash
loom memory recall "<query>" --scope file:<path> --context --format prompt
loom memory grep "<regex>"
loom memory link validate
loom memory janitor report
```

Common failure mode this prevents: "we fixed it once, then forgot the real reason." Memory makes the why retrievable.

### Workspace

We use Loom Workspace for safe, repeatable execution: isolate changes in worktrees, snapshot before risk, and coordinate across repos explicitly when needed.

This is a single-repo worktree manager; the harness subcommand space is a multi-repo control plane, and they do not auto-dispatch into each other. Workspace provides guardrails: deterministic selection (`--repos`/`--set`/`--tag`/`--all`), safe cleanup (TTL + suggest/apply), and recovery tools (snapshots/diffs). It is the "where" of work: every agent or ticket should have a dedicated worktree; risky operations should be preceded by a snapshot. Sandbox worktrees exist for spikes with expiry; annotate/TTL features exist so cleanup can be safe and unsurprising.

This matters because git worktrees are cheap isolation and Loom makes them systematic (naming, metadata, cleanup) so parallel agent work stays sane. Snapshots and diffs are the difference between a controlled experiment and a mystery; they make failures reproducible and reversible. Harness mode prevents accidental cross-repo blast radius by forcing explicit intent when touching many repos.

Before you change code, ensure a worktree for the branch/ticket. If you are about to rebase/merge/force-clean, snapshot first. Use sandbox worktrees for spikes with TTL and cleanup suggest/apply to remove expired work safely. Use harness mode when you need to run commands, create branches, or manage worktrees across many repos; if you are about to run a command across many repos, use harness selection flags explicitly so the blast radius is intentional.

On disk: repo mode `.loom/workspace/`; harness mode `.loom/workspaces/workspace.json`

Start here:

```bash
loom workspace -h
loom workspace prime

loom workspace worktree ensure <branch> --base-ref main
loom workspace snapshot capture pre-change
loom workspace worktree diff --mode dirty
```

If you're about to do something risky:

```bash
loom workspace snapshot capture pre-rebase
loom workspace merge attempt --worktree <path> --base main --topic <branch>
```

If you're operating across many repos (harness mode):

```bash
loom workspace harness -h
loom workspace harness init
loom workspace harness status --all
loom workspace harness exec --tag <tag> --jobs 4 -- uv run pytest -q
```

Common failure mode this prevents: "the repo is dirty and I don't know where the change came from." Worktrees + snapshots isolate causality.

### Compound

We use Loom Compound for deterministic learning: convert repeated wins (and failures) into Skills so future agents follow procedure, not vibes.

Skills are procedural memory stored as Markdown (`.opencode/skills/<name>/SKILL.md`) with crisp, repeatable steps. Compound records evidence (Episodes) and governance (Decisions) so "this is how we do it" is traceable and reviewable. It can regenerate derived artifacts (`refresh`) and stage/commit learning outputs (`sync`) so the repo stays coherent. Compound is how you turn a good run into institutional memory that survives model swaps, new teammates, and time.

This matters because the highest leverage output of agent work is durable procedure: skills prevent rediscovering workflows every week. Determinism + evidence reduce prompt drift; skills become a stable contract that agents can follow and reviewers can trust. Compounding turns "tribal knowledge" into files you can diff, enforce, and ship.

Use Compound after review/ship, after incidents, or whenever you notice a repeated pattern that should become a procedure. Use it when you want consistent tool usage across agents/repos (preferred commands, safety steps, regression test patterns). If you hear yourself say "next time, remember to...", that is a Skill candidate.

On disk: `.opencode/skills/`, `.loom/compound/`

Start here:

```bash
loom compound -h
loom compound prime

loom compound init
loom compound refresh
loom compound sync
```

## Install

Requirements:

- Python >= 3.11
- `git` (ticket/workspace/team)
- `tmux` (team)

Install from source (recommended while Loom is greenfield):

```bash
uv tool install --force --reinstall .[dev]
```

Confirm the CLI:

```bash
loom --help
```

## Quickstart (single repo)

Initialize everything:

```bash
loom init --yes --workspace-mode repo
```

Create a ticket (intent as a Markdown doc):

```bash
loom ticket create "Ship agent dashboard" --type task --priority 1
```

Create/ensure an isolated worktree:

```bash
loom workspace worktree ensure agent-dashboard --base-ref main
```

Start a team run and spawn a worker on the ticket:

```bash
loom team start core --objective "Build the Loom dashboard"
loom team spawn core <ticket-id> # the manager handles this for you, but this is how you would do it manually if you wanted to script it or drive it from an agent
```

Pause/resume a run (clock out/in):

```bash
loom team clock-out core
loom team clock-in core
```

Tip: the manuals are built into the CLIs:

```bash
loom ticket prime
loom memory prime
loom workspace prime
```

## Agentic UX (grounded in the CLI)

Loom normalizes common, plausible variants before parsing.

- Team:
  - `loom team clock in core` -> `clock-in`
  - `loom team inbox core --unread` -> `inbox <TEAM> list --unacked`
  - `--repo-root` -> `--repo`
- Memory:
  - `--vault-dir` -> `--vault`
  - `--json` / `--jsonl` -> `--format json|jsonl`
- Ticket:
  - `--ticket-dir` -> `--tickets-dir`
  - `--noaudit` -> `--no-audit`
  - glued flags like `-p1` are accepted

Most surfaces have machine-readable output options (`--json`, `--format json`, etc.). When in doubt: `loom <cmd> -h`.

One practical example from `loom team send`: delivery is best-effort to tmux, but always durable to the inbox when tmux delivery is not possible.

## Learning: memory + skills

Loom has two complementary persistence mechanisms:

- Memory (`loom memory`): open-ended notes as Markdown with YAML frontmatter; the SQLite index is derived and rebuildable.
- Skills (`loom compound learn`): procedural memory as `.opencode/skills/*/SKILL.md`.

The intended workflow is:

Plan -> Work -> Review -> Compound

Practical loop:

```bash
loom memory recall "worktree safety" --context
loom memory add --title "Worktree safety" --body "Snapshot before force-clean"
loom compound init
loom compound refresh
# optional: commit compound-managed artifacts
loom compound sync
```

The point: memory captures context, skills capture procedure.

## Workspace modes

- Repo mode: one repo, many worktrees.
- Harness mode: multi-repo control plane (repo sets, tags, worktree groups, and component dependency metadata).

Example harness flow:

```bash
loom workspace harness init
loom workspace add api git@github.com:org/api.git --clone
loom workspace add web git@github.com:org/web.git --clone
loom workspace worktree add sprint-42 --all
loom workspace harness components refresh-index --print
loom workspace deps show api
```

## Philosophy and tradeoffs (Beads, Gastown)

Loom is in the same problem space as projects like:

- Beads: https://github.com/steveyegge/beads
- Gastown: https://github.com/steveyegge/gastown

Loom's choices are intentionally conservative and legible:

- Documents over records: tickets are Markdown documents with frontmatter, meant to be read directly.
- Visible operations: teams are tmux sessions with disk state you can inspect; Loom automates tmux instead of abstracting it away.
- File-backed learning: memory and skills are plain files; derived indexes are rebuildable.

The goal is patchability: humans and agents can understand the system by reading the repo.

This is also why Loom is opinionated about UX: it would rather accept plausible inputs and steer you toward safe operations than require perfect syntax and fail late.

## Server API

```bash
loom dashboard --host 127.0.0.1 --port 8764
```

Spec: `docs/openapi.yaml`.

## Development

```bash
uv run basedpyright
uv run ruff check .
uv run pytest
```

## Docs

- `AGENTS.md` (agent primitives)
- `LOOM.md` (system context)
- `.loom/compound/ROADMAP.md` (direction + changelog)
