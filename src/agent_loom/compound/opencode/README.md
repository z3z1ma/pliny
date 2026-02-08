# OpenCode Compound System

This repo includes a production-ready **OpenCode plugin + workflow commands** to make an agentic coding setup *self-compounding* via durable “procedural memory” (**Skills**).

It supports:

- ✅ **Plan → Work → Review → Compound → Repeat** workflow commands (`/workflow-*`)
- ✅ Integration with:
  - `loom ticket`
  - `loom memory`
  - `loom workspace`
- ✅ **Automatic observation logging** (tool calls + session events)
- ✅ **Automatic post-turn learning** on `session.idle`
  - extracts/updates **instincts**
  - creates/updates **skills**
  - refreshes derived docs (`LOOM.md`, `.loom/compound/ROADMAP.md`, `.loom/compound/INSTINCTS.md`)

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
  Human-owned overview and stable project guardrails.
- `LOOM.md`
  Derived always-on context (compound-managed) including workflow pointers, core context, and a small instincts summary.
- `.loom/compound/ROADMAP.md`
  Loom direction as an empirical compass (AI-managed sections).
  Also contains an embedded AI-first changelog block (bounded; no "no changes" entries).

### Memory

- `.opencode/skills/<skill-name>/SKILL.md`
  OpenCode skills (primary source of procedural memory)
- `.loom/compound/instincts.json`
  Source of truth for instincts
- `.loom/compound/INSTINCTS.md`
  Index view (AI-managed)
- `.opencode/memory/observations.jsonl`
  Append-only observation log (**gitignored by default**)

### Evidence (Episodes)

- `.loom/compound/episodes/YYYY/MM/<episode_id>.json`
  Committed evidence capsules built from (observations + git diff). These are the durable, lossless-ish bridge between runtime telemetry and compiled instincts/skills.

### Plugin + commands

- `.opencode/plugins/compound_engineering.ts`
  The OpenCode plugin
- `.opencode/commands/workflow-*.md`
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
- `.loom/compound/instincts.json` and `.loom/compound/INSTINCTS.md` (instinct store + index)

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

- The plugin packages a small context snapshot (recent observations + git diffstat).
- The model generates structured proposals (instinct/skill candidates).
- Loom applies them deterministically via `loom compound learn` and records an Episode under `.loom/compound/episodes/...`.

---

## Workflow commands

- `/workflow-plan`
  Recall memory (`loom memory recall`), inspect ticket backlog, create tickets, write plan
- `/workflow-work`
  Create a worktree (`loom workspace ...`), implement tasks, update tickets
- `/workflow-review`
  Review work, adjust tickets, prepare merge
- `/workflow-compound`
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
- `COMPOUND_AUTO_PROMPT_MAX_CHARS=18000`

### Session-start maintenance (optional)

- `COMPOUND_REFRESH_ON_START=1|0` (default `0`)
  If enabled, runs `loom compound update` when a session starts.
- `COMPOUND_PRIME_ON_START=1|0` (default `0`)
  Alias toggle for the same behavior (kept for clarity).

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

- `loom compound init`
- Preview changes: `loom compound init --dry-run`

### Upgrade

Default upgrades are non-destructive:

- Re-running init will **not** overwrite skills or memory.
- To refresh scaffold files (plugin/commands/agents/prompts), use:
  - `loom compound init --force`

### Run

1. Run `loom compound init` once (installs scaffolding).
2. Start OpenCode normally.
   - Optional: set `COMPOUND_REFRESH_ON_START=1` to keep derived context up to date automatically.
3. Use `/workflow-plan` and proceed through the workflow.
4. Let the plugin autolearn on idle turns (it runs a background prompt that uses `bash` + `loom compound ...`).

---

## Safety model

This plugin is intentionally limited:

- ✅ Writes: observations.jsonl (append-only; gitignored by default)
- ✅ Triggers: background autolearn prompts
- ✅ Calls Loom: for compounding maintenance (`loom compound update`)
- ❌ Does **not** write product code

If you want it to mutate application code automatically, you can do that, but you should probably also install a fire alarm and start journaling.
