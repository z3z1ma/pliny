# AGENTS.md

> **SYSTEM INSTRUCTION**: You are a Loom-native entity. Loom is your operating system for intent (`ticket`), code state (`workspace`), coordination (`team`), and learning (`memory`).
> **CRITICAL**: The examples below are **primitives**, not recipes. Do not collapse into rigid workflows. Compose these tools dynamically to solve complex, novel problems. Use `loom --json` for machine-readable output.

Never assume you know the full interface. When in doubt, use `--help` to explore available commands and flags.

1. Start with:
```
loom
loom --help
loom <noun> --help
```
2. Prefer **introspection over recall**.
3. Flags are intentionally expressive; combine them instead of searching for “the one right command”.

## 1. Intent & State (Loom Ticket)

**Source of Truth:** Git-backed files in `.tickets/`. Use this to track *what* you are doing and *why*.

* **Model:** Graph-based (deps, links). Statuses: `open` -> `in_progress` -> `closed`.
* **Primitives:**
* `loom ticket create "$TITLE" --type [task|bug|epic] --priority [0-4]` -> Returns `$TID`.
* `loom ticket show $TID` -> Returns metadata + body + relationships (blockers).
* `loom ticket update $TID --status in_progress --assignee $AGENT_ID`
* `loom ticket dep-add $TID $BLOCKER_TID` / `loom ticket link $TID $RELATED_TID`
* `loom ticket list --status open --assignee $AGENT_ID`



## 2. Isolation & Safety (Loom Workspace)

**Mechanism:** Git worktrees + polyrepo control. Never work in the root dirty. Use snapshots for resilience.

* **Repo Mode:** One repo, multiple parallel worktrees.
* **Poly Mode:** Multiple repos, orchestrated sets.
* **Primitives:**
* `loom workspace status` -> Shows current branch/sha/dirty.
* `loom workspace worktree ensure $BRANCH --base-ref main` -> Idempotent worktree creation.
* `loom workspace snapshot capture $NAME` -> Save state before risky ops.
* `loom workspace snapshot restore $NAME --yes` -> Revert to safety.
* `loom workspace poly exec --repos "foo,bar" -- git fetch` -> Bulk ops (poly only).



## 3. Coordination & Scale (Loom Team)

NOTE: Do NOT use this unless you are explicitly asked to.

**Mechanism:** `tmux`-based agent orchestration. You are a node in a swarm.

* **Roles:** Manager (you?), Worker (execution), Investigator (research), Integrator (merge-queue).
* **Communication:** Durable inbox + signals.
* **Primitives:**
* `loom team spawn $TEAM_NAME $TID` -> Spawns worker in isolated worktree for $TID.
* `loom team inbox list --to manager --unacked` -> Check signals.
* `loom team send $TARGET "$MSG"` -> Coordination signal.
* `loom team merge enqueue --ticket $TID --branch $BRANCH` -> Handover for shipping.



## 4. Learning & Context (Loom Memory)

**Mechanism:** Persistent, semantic graph. Autolearning enabled.

* **Loop:** Plan -> Work -> Review -> **Compound**.
* **Primitives:**
* `loom memory recall "$QUERY"` -> Fetch relevant context/skills.
* `loom memory add --title "$TOPIC" --body "$CONTENT"` -> Persist new knowledge.
* `loom compound` -> Trigger learning extraction from current session.



## Composability Patterns (Do not limit yourself to these)

* **The Safe Refactor:** `ticket create` -> `workspace worktree ensure` -> `workspace snapshot capture "pre-refactor"` -> *Attempt Code* -> `test` -> *Fail?* -> `workspace snapshot restore`.
* **The Fan-Out:** `ticket create "Epic"` -> `investigator` (breakdown) -> `ticket create` (subtasks) -> `team spawn` (parallel workers).
* **The Context Load:** `memory recall` -> *Inject into* `ticket update` (design doc).

## Guiding Principles

1. **Atomic Updates:** Use `loom ticket update` sparingly; prefer `add-note` for logs.
2. **Isolation First:** Always create a worktree for a ticket. Never pollute `main`.
3. **Fail Noisily:** If `workspace status` is dirty, stop. If `ticket` is blocked, stop.
4. **Compound:** If you solve a novel error, `memory add` the solution immediately.

> **OPTIMIZATION**: Prefer `loom <cmd> --json` for parsing. Use `jq` to filter. Example:
> `loom ticket list --json | jq -r '.tickets[] | select(.priority < 2) | .id'`
