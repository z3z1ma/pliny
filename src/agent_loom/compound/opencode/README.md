# OpenCode Compound System

This repo includes a production-ready **OpenCode plugin + workflow commands** to make an agentic coding setup *self-compounding* via durable “procedural memory” (**Skills**).

It supports:

- ✅ **Plan → Work → Review → Compound → Repeat** commands (`/workflows:*`)
- ✅ Integration with:
  - `loom ticket`
  - `loom memory`
  - `loom workspace`
- ✅ **Automatic observation logging** (tool calls + session events)
- ✅ **Automatic post-turn learning** on `session.idle`
  - extracts/updates **instincts**
  - creates/updates **skills**
  - refreshes `AGENTS.md` and `LOOM_ROADMAP.md`

---

## Why this exists

Humans are great at “learning the hard way,” then forgetting the lesson two days later and learning it again.
This system makes that failure mode expensive by turning repeat patterns into:

1. **Observations** (automatic logs)
2. **Instincts** (small heuristics)
3. **Skills** (durable procedural memory, auto-discovered by the agent)

Skills compound. That’s the entire trick.

---

## Files and folders

### Core context files

- `AGENTS.md`
  Rules, workflow pointers, and a small always-on core context (second-order compression).
- `LOOM_ROADMAP.md`
  Loom direction as an empirical compass (AI-managed sections).
  Also contains an embedded AI-first changelog block (bounded; no "no changes" entries).

### Memory

- `.opencode/skills/<skill-name>/SKILL.md`
  OpenCode skills (primary source of procedural memory)
- `.opencode/memory/instincts.json`
  Source of truth for instincts
- `.opencode/memory/INSTINCTS.md`
  Index view (AI-managed)
- `.opencode/memory/observations.jsonl`
  Append-only observation log (**gitignored by default**)

### Plugin + commands

- `.opencode/plugins/compound_engineering.ts`
  The OpenCode plugin
- `.opencode/commands/workflows:*.md`
  Plan/Work/Review/Compound command set

### What is managed (and why)

Treat these as three classes:

1) Scaffold (safe to refresh):

- `.opencode/plugins/**` (tooling + autolearn loop)
- `.opencode/commands/**` (workflow UX)
- `.opencode/agents/**` (subagent presets)
- `.opencode/compound/prompts/**` (prompt templates)

2) Persistent cognitive state (do not overwrite during upgrades):

- `.opencode/skills/**` (procedural memory)
- `.opencode/memory/instincts.json` and `.opencode/memory/INSTINCTS.md` (instinct store + index)

3) Runtime-only artifacts (should be gitignored):

- `.opencode/memory/observations.jsonl` (append-only tool/event log)
- `.opencode/memory/autolearn_failures/**` (autolearn failure breadcrumbs)
- `.opencode/compound/state.json` (local plugin state)

---

## How the “automatic compounding” works

### 1) Observation capture (always-on)

The plugin logs:

- `tool.execute.before/after` (args are redacted when huge)
- selected session events (eg `command.executed`, `session.idle`)

These go into `.opencode/memory/observations.jsonl`.

### 2) Autolearn on `session.idle`

When the session goes idle (agent has finished a turn):

- The plugin packages:
  - recent observations
  - git diffstat + changed files
  - current skills list
  - current top instincts
- It prompts the model using `.opencode/compound/prompts/autolearn.md`
- The model returns a **CompoundSpec v2 JSON**
- The plugin applies it (skills/instincts/memos/docs/changelog only)
- It refreshes indexes (`compound_sync` behavior)

---

## Workflow commands

- `/workflows:plan`
  Recall memory (`loom memory recall`), inspect ticket backlog, create tickets, write plan
- `/workflows:work`
  Create a worktree (`loom workspace ...`), implement tasks, update tickets
- `/workflows:review`
  Review work, adjust tickets, prepare merge
- `/workflows:compound`
  Extract learnings into skills + memos + docs

---

## Configuration (env vars)

### Auto-learning

- `COMPOUND_AUTO=1|0`
  Enable/disable autolearn (default `1`)
- `COMPOUND_AUTO_COOLDOWN_SECONDS=120`
  Minimum time between autolearn runs
- `COMPOUND_AUTO_MIN_NEW_OBSERVATIONS=12`
  Minimum new observation records before an autolearn run
- `COMPOUND_AUTO_MAX_OBSERVATIONS_IN_PROMPT=80`
- `COMPOUND_AUTO_MAX_SKILLS_PER_RUN=3`
- `COMPOUND_AUTO_MAX_INSTINCT_UPDATES_PER_RUN=8`
- `COMPOUND_AUTO_PROMPT_MAX_CHARS=18000`

### Observation logging

- `COMPOUND_LOG_OBSERVATIONS=1|0` (default `1`)
- `COMPOUND_OBSERVATIONS_MAX_BYTES=33554432` (default 32MB)

### Tool wiring

- `COMPOUND_LOOM_BIN=loom`

### Claude mirroring

- `COMPOUND_MIRROR_CLAUDE=1|0` (default `1`)

---

## Quick start

### Install

Preferred install path (safe, idempotent):

- `loom compound init --dest .`
- Preview changes: `loom compound init --dest . --dry-run`

### Upgrade

Default upgrades are non-destructive:

- Re-running init will **not** overwrite skills or memory.
- To refresh scaffold files (plugin/commands/agents/prompts), use:
  - `loom compound init --dest . --force`

### Run

1. Start OpenCode normally. The plugin bootstraps missing files and syncs indexes.
2. Use `/workflows:plan` and proceed through the workflow.
3. Let the plugin autolearn on idle turns, or run it manually:
   - `compound_autolearn_now`

---

## Safety model

This plugin is intentionally limited:

 - ✅ Writes: skills, instincts, memos, AGENTS.md, LOOM_ROADMAP.md
- ❌ Does **not** write product code

If you want it to mutate application code automatically, you can do that, but you should probably also install a fire alarm and start journaling.
