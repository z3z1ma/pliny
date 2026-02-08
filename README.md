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
| Ticket | `loom ticket` | `.tickets/<status>/` | Intent and execution state as Markdown + frontmatter, with deps/links/claims |
| Workspace | `loom workspace` | `workspace.json`, `.loom/`, `.loom-repo/` | Worktree lifecycle, snapshots, multi-repo coordination, service deps |
| Team | `loom team` | `.team/` | tmux-native orchestration: manager/workers/inbox/merge queue |
| Memory | `loom memory` | `.memory/` | Obsidian-like Markdown notes; derived SQLite cache for recall |
| Compound | `loom compound` | `.opencode/` | Compounding: skills as procedural memory (SKILL.md), plus tooling scaffolding |
| Dashboard | `loom dashboard` | - | HTTP API for dashboards (see `docs/openapi.yaml`) |

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

## Quickstart (repo mode)

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
loom team spawn core <ticket-id>
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
loom compound update
# optional: commit compound-managed artifacts
loom compound sync
```

The point: memory captures context, skills capture procedure.

## Workspace modes

- Repo mode: one repo, many worktrees.
- Poly mode: multi-repo control plane (repo sets, tags, worktree groups, and service dependency metadata).

Example poly flow:

```bash
loom workspace poly init
loom workspace add api git@github.com:org/api.git --clone
loom workspace add web git@github.com:org/web.git --clone
loom workspace worktree add sprint-42 --all
loom workspace services refresh-index --print
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
