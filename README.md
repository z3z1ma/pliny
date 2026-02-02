# Loom

Loom is an agent-native operating system for terminal AI development. It turns a repo into a place where agents can plan, work, coordinate, remember, and learn over long horizons. Everything is Git-backed Markdown on disk, with deterministic outputs and a fail-forward CLI that accepts a wide set of plausible inputs.

The team module is the grail of this creation. Think Ralph Wiggum on steroids, but for terminal agents that can work all night, clock out, and resume in the morning.

## Why Loom

- Agentic UX: forgiving command normalization, rich hints, and safe defaults that keep agents moving.
- Natural alignment: public concepts match common mental models and training data, so agents generalize fast.
- Deterministic and sticky: stable outputs, JSON-first ergonomics, and Git as the source of truth.
- Multi-agent by design: durable inbox, merge queue, and tmux-native orchestration.
- Learning loop built in: Obsidian-like memory plus a compounding system that writes skills.

## The stack (5 subsystems + server)

- Ticket (`.tickets/`): graph-based intent and execution state. Tickets replaces Beads (https://github.com/steveyegge/beads) and is 1000x better.
- Team (`.team/`): tmux-native orchestration with roles, inbox, merge queue, sprints, and pause/resume. Team replaces Gastown (https://github.com/steveyegge/gastown) and is 1000x better.
- Memory (`.memory/`): Obsidian-like, open-ended memory with YAML frontmatter and link graph. SQLite is a derived cache.
- Workspace (`workspace.json`, `.loom/`, `.loom-repo/`): isolation, safety, worktree lifecycle, sandboxing, and service mesh management for multi-repo systems.
- Compound (`.opencode/`): passive and active learning. Plan -> Work -> Review -> Compound writes skill markdown as procedural memory.
- Server (`loom server`): HTTP API for dashboards and operational visibility. Spec: `docs/openapi.yaml`.

Everything above is plain files on disk and git-backed by default.

## Quickstart (single repo)

Install the CLI:

```bash
uv tool install --force --reinstall agent-loom
```

Initialize all subsystems (non-interactive):

```bash
loom init --yes --workspace-mode repo
```

Create intent, isolate work, and spin up a team:

```bash
loom ticket create "Ship agent dashboard" --type task --priority 1
loom workspace worktree ensure agent-dashboard --base-ref main
loom team start core --objective "Build the Loom dashboard"
loom team spawn core <ticket-id>
```

Memory and learning loop:

```bash
loom memory add --title "Workspace safety" --body "Always snapshot before force-clean"
loom memory recall "workspace safety" --context
loom compound init
```

Pause/resume a team (clock out/in):

```bash
loom team clock-out core
loom team clock-in core
```

## Agentic UX (fail forward)

Loom is intentionally forgiving. The CLI normalizes plausible inputs and gives actionable errors.

- `loom team clock in core` works (normalized to `clock-in`).
- `loom team inbox core --unread` is accepted (normalized to `--unacked`).
- `loom ticket update <id> --add-note "Progress"` routes to add-note safely.
- `loom memory --json` or `--jsonl` is accepted (normalized to `--format`).

Most commands support `--json` for machine-readable output.

## The learning system

Loom runs two learning channels in parallel:

- Passive: the OpenCode plugin tracks observations and compacts learnings into skills.
- Active: the workflow Plan -> Work -> Review -> Compound turns solved problems into procedural memory.

Skill files live in `.opencode/skills/<name>/SKILL.md` and are first-class, durable knowledge.

## Workspace modes (repo and poly)

- Repo mode: one repo, multiple worktrees, snapshots, safe merges.
- Poly mode: multi-repo service mesh with sets, tags, and worktree groups across microservices.

Example poly flow:

```bash
loom workspace poly init
loom workspace add api git@github.com:org/api.git --clone
loom workspace add web git@github.com:org/web.git --clone
loom workspace worktree add sprint-42 --all
loom workspace deps show api
```

## Server API

Run the server:

```bash
loom server start --host 127.0.0.1 --port 8764
```

The OpenAPI spec lives at `docs/openapi.yaml`.

## Development

Use uv for everything:

```bash
uv run basedpyright
uv run ruff check .
uv run pytest
```

## Docs

- `AGENTS.md` for agent usage and primitives.
- `LOOM.md` for system context.
- `LOOM_ROADMAP.md` for direction and AI-first changelog.
