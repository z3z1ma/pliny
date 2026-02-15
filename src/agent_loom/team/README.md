# Team Cookbook

This cookbook documents the Team subsystem CLI and the operating model behind
it. It is based on direct code tracing of the team module, including run state,
tmux orchestration, inbox durability, merge queue behavior, and sidecar health.

## Mental model

- Team is tmux-native orchestration for long-horizon, multi-agent work.
- It does not replace git, workspace, or ticket; it composes them.
- Every run is explicit state under `.loom/team/runs/<team>/run.json`.
- Workers operate in isolated worktrees (managed by workspace).
- Tickets are the durable work ledger (managed by loom ticket).
- Messages are durable (disk inbox) with best-effort tmux nudges.
- There is no daemon; everything is CLI-driven.

## Module architecture

### Responsibility boundaries

**CLI layer** (`team/cli.py`):
- Parser construction and argument validation only
- Dispatches to command handler modules
- Must NOT contain business logic or state manipulation
- Uses shared output helpers from `core/cli_output.py`

**Command handlers** (`team/commands/*.py`):
- Grouped by domain: lifecycle, workers, objective, inbox, merge, utils
- Each module owns command implementation for its domain
- Delegates to `team/core.py` for run state and tmux orchestration
- Uses `team/output.py` for JSON/text emission via shared primitives

**Core orchestration** (`team/core.py`):
- Run state management (start/pause/resume/disband)
- Worker lifecycle and worktree coordination
- Inbox and messaging
- Merge queue
- Sprint and objective state
- tmux session/window/pane management
- **Critical:** This file is a known hotspot (~6500 LOC) undergoing decomposition

**Domain modules**:
- `team/permissions.py`: role guards and environment checks
- `team/utilities.py`: shared helpers (parsing, git, pathing)
- `team/inbox.py`: inbox storage backend
- `team/merge_queue.py`: merge queue storage
- `team/models.py`: run state and message dataclasses
- `team/tmux.py`: tmux subprocess wrappers

**Output contract** (`team/output.py`):
- Wraps `core/cli_output.py` shared primitives
- Adds team-specific JSON envelope metadata if needed
- All CLI commands MUST use these helpers, not local duplicates

### Guardrails

1. **No duplicate output helpers**: All CLI serialization/emission uses `core/cli_output.py` primitives via `team/output.py`. Local helper duplication is a regression.
2. **Command handlers stay thin**: Business logic belongs in `team/core.py` or domain modules, not in `team/commands/*.py`.
3. **Hotspot size control**: `team/core.py` is monitored for growth. New functionality should extract to domain modules when feasible.
4. **Import direction**: Domain modules may NOT import from `team/commands/*`. Command handlers import from domain modules and core.

## Storage layout

```
.loom/team/
  runs/
    <team>/
      run.json                  # authoritative run state
      CHARTER.md                # objective + sprint context (source of truth)
      inbox/                    # durable messages (unacked)
      inbox/read/               # acked messages
      worktrees/                # per-run ws worktrees (workers + integrator)
      merge/                    # merge-queue state
      captures/                 # tmux capture output (txt + json)
      snapshots/status.json     # status snapshot for UI/inspection
      events/                   # event timeline (json files)
      sidecars/                 # sidecar logs + pidfiles
      artifacts/                # future/optional
```

## Run discovery and repo roots

- `--repo` selects a path inside the canonical repo; Team resolves the git root.
- Without `--repo`, Team searches upward for `.loom/team/runs/<team>/run.json`.
- The canonical tickets dir is always `<repo>/.loom/ticket` and is injected into
  tmux panes as `TICKET_DIR`.

## Global flags and JSON output

- `--repo` path inside repo (defaults to CWD)
- `--json` emit machine-readable output

JSON success uses `{"ok": true, ...}`. JSON errors use
`{"ok": false, "code": ..., "error": ..., "hint": ..., "suggestions": ...}`.

## Environment variables

Team injects these into tmux panes:

- `TEAM_NAME`
- `TEAM_RUN_ID`
- `TEAM_RUN_DIR`
- `TEAM_ROLE` (manager|worker|investigator|integrator)
- `TEAM_WORKER_ID`
- `TEAM_TICKET_ID`
- `TEAM_SPRINT_NAME`
- `TEAM_SPRINT_TAG`
- `TICKET_DIR`

## Duration syntax

Most time-based flags accept a compact duration string:

- `30s`, `5m`, `2h`, `7d`

## Targets (send/capture/bounce)

Targets resolve in this order:

- `manager` / `mgr`
- worker id (e.g. `w1`)
- worktree key (e.g. `merge-queue`)
- tmux window name
- ticket id (if uniquely assigned)

If ambiguous, Team will error. `merge-queue` aliases to the integrator.

## Command cookbook

### init

Install/sync Team agent definitions in the repo root:

```
loom team init
loom team init --repo /path/to/repo
loom team init --force
```

`start` will fail if agent files are missing. Commit them once.

### start

Start (or resume) a run and create the tmux session + manager window:

```
loom team start my-team --objective "Ship the sprint" --repo /path/to/repo
```

Useful flags:

- `--session` override tmux session name
- `--harness opencode|claude|omp|codex`
- `--bin <path>` override harness binary
- `--model`, `--manager-model`, `--worker-model`, `--investigator-model`, `--integrator-model`
- `--mount SRC[:DEST]` symlink repo-root paths into worktrees (repeatable)
- `--clear-mounts` clear persisted mounts
- `--max-headcount N` limit active worker+investigator count (0 = unlimited)
- `--target-branch main` (ship target)
- `--remote origin`
- `--push` / `--no-push`
- `--manager-window <name>`
- `--force` recreate manager window

omp examples:
```
loom team start my-team --harness omp --model opus
loom team start my-team --harness omp --manager-model opus --worker-model gpt-4o
```

codex examples:

```
loom team start my-team --harness codex --model gpt-5.3-codex
loom team start my-team --harness codex --manager-model gpt-5.3-codex --worker-model gpt-5-codex
```

For `--harness omp`, Team still reads `manager_agent` / `worker_agent` / `investigator_agent` / `integrator_agent` from run state. The matching agent markdown file is parsed and appended to omp's system prompt via `--append-system-prompt`.

For `--harness codex`, Team extracts the same agent prompt body and writes a per-pane instructions file under `.loom/team/runs/<team>/agents/codex/<recipient>.md`, then launches codex with `--config model_instructions_file=...`.

codex sidecar sandboxing is role-aware:
- manager / investigator / integrator run with `--sandbox read-only --ask-for-approval on-request`
- workers run with `--sandbox workspace-write --ask-for-approval on-request`

codex sidecar state is isolated per pane via `CODEX_HOME=.loom/team/runs/<team>/sessions/codex/<recipient>`.

### attach

Attach to the manager window:

```
loom team attach my-team
```

### status

Show run status and roster:

```
loom team status my-team
loom team status my-team --show-dead
loom team --json status my-team
```

Also persists a status snapshot at `.loom/team/runs/<team>/snapshots/status.json`.

### doctor

Diagnose tmux/run-state drift and suggest fixes:

```
loom team doctor my-team
```

### capture

Capture recent tmux output and persist a copy under `captures/`:

```
loom team capture my-team manager
loom team capture my-team w1 --lines 400
loom team capture my-team merge-queue --no-join
```

### send

Durable message + best-effort tmux nudge:

```
loom team send my-team w1 "Status?"
loom team send my-team manager --message "Ready for review"
loom team send my-team w1 --force --message "Please check inbox"
```

### inbox

Disk-backed durable inbox:

```
loom team inbox my-team list
loom team inbox my-team list --to manager --unacked
loom team inbox my-team show <MSG_ID>
loom team inbox my-team ack <MSG_ID>
loom team inbox my-team send --to w1 --message "Ping" --kind note
```

### objective

Show or update the run objective (writes `CHARTER.md` and nudges manager):

```
loom team objective my-team show
loom team objective my-team set --message "New objective"
loom team objective my-team append --file objective.md
cat update.txt | loom team objective my-team append --stdin
```

Flags: `--no-nudge`, `--force` (allow nudge even if pane is unsafe).

### sprint / prep-sprint

Sprint metadata (name + tag) and prep ticket:

```
loom team prep-sprint my-team --name "Bridge cleanup"
loom team prep-sprint my-team --name "Bridge cleanup" --no-spawn
loom team sprint my-team show
loom team sprint my-team set --name "Bridge cleanup" --tag sprint:bridge
loom team sprint my-team clear
```

`prep-sprint` creates a prep ticket and optionally spawns an investigator.

### spawn (worker or investigator)

Spawn a worker for a ticket (each worker owns one ticket):

```
loom team spawn my-team ab-1234
loom team spawn my-team ab-1234 --role investigator
loom team spawn my-team ab-1234 --worker-id w7 --window "w7-ab-1234"
loom team spawn my-team ab-1234 --worktree-key auth-spike
loom team spawn my-team ab-1234 --branch team/ab-1234 --base-ref origin/main
```

Resume a retired worker in its existing worktree:

```
loom team spawn my-team ab-1234 --worker-id w3 --resume
loom team resume-worker my-team w3
```

### retire / mark-retirable

Retire a worker (worktree preserved), then mark its worktree eligible for janitor:

```
loom team retire my-team w3
loom team mark-retirable my-team w3
```

### pause / resume (clock-out / clock-in)

Pause and resume a run without losing state:

```
loom team pause my-team
loom team resume my-team

loom team clock-out my-team
loom team clock-in my-team
```

### wait / snooze

Block for a duration; wake early on inbox activity:

```
loom team wait my-team 5m
loom team snooze my-team 10m
```

Inside a team tmux session, you can omit the team name:

```
loom team wait 5m
```

Use `--quiet` to reduce stdout noise.

### spawn-integrator

Spawn (or recover) the merge integrator:

```
loom team spawn-integrator my-team
loom team spawn-integrator my-team --force
loom team spawn-integrator my-team --require-clean
```

Optional: override merge target config:

```
loom team spawn-integrator my-team --target-branch main --remote origin --no-push
```

### merge queue

Queue and process integration work:

```
loom team merge my-team enqueue --ticket ab-1234 --branch team/ab-1234 --from-worker w1
loom team merge my-team list
loom team merge my-team list --all
loom team merge my-team next --claim-by integrator
loom team merge my-team done <ITEM_ID> --result merged --note "ok"
```

`--result` must be `merged`, `blocked`, or `dropped`.

### ship

Merge merge-queue into the target branch (manager-only):

```
loom team ship my-team
loom team ship my-team --force-clean
loom team ship my-team --no-push
```

Ship automatically syncs tickets and compound learning changes before merging.

### done

Check if a run is 100% done and optionally notify the manager:

```
loom team done my-team
loom team done my-team --notify --resend-after-s 21600
```

Definition used is conservative: no active workers, no pending merge items,
no unshipped merges, and all worker tickets closed.

### janitor

Cleanup long-retired workers and retirable worktrees:

```
loom team janitor my-team
loom team janitor my-team --dry-run
loom team janitor my-team --older-than 30d --prune-orphans
```

Janitor only deletes worktrees marked retirable.

### disband

Kill the tmux session and optionally remove worktrees/state:

```
loom team disband my-team
loom team disband my-team --remove-worktrees
loom team disband my-team --keep-state
```

### bounce

Force-restart a worker agent process via its sidecar:

```
loom team bounce my-team w1 --reason "stuck"
loom team bounce my-team ab-1234
```

### tui (internal)

Sidecar harness for tmux panes (normally used by Team automatically):

```
loom team tui /path/to/worktree --harness opencode --agent loom-team-worker --model gpt-4.1
loom team tui /path/to/worktree --harness omp --agent loom-team-worker --model opus
loom team tui /path/to/worktree --harness codex --agent loom-team-worker --model gpt-5-codex
```

### prime

Print this built-in operating manual:

```
loom team prime
loom team prime --json
```

## Unix philosophy recipes

### List active worker ids

```
loom team --json status my-team \
  | jq -r '.workers | to_entries[] | select(.value.retired!=true) | select(.value.alive==true) | .key'
```

### Capture every active worker

```
loom team --json status my-team \
  | jq -r '.workers | to_entries[] | select(.value.retired!=true) | .key' \
  | xargs -n 1 -I {} loom team capture my-team {}
```

### Mass-check-in all workers

```
loom team --json status my-team \
  | jq -r '.workers | to_entries[] | select(.value.retired!=true) | .key' \
  | xargs -n 1 -I {} loom team send my-team {} "Please post a ticket update"
```

### Find unacked manager inbox

```
loom team inbox my-team list --to manager --unacked
```

### Claim a merge item with fzf

```
item=$(loom team --json merge my-team list | jq -r '.items[] | "\(.id)\t\(.branch)"' | fzf | cut -f1)
loom team merge my-team done "$item" --result merged --note "ok"
```

### Pipe a status snapshot into a note

```
loom team --json status my-team | jq . | loom memory add --title "Team status" --tag team
```

## Troubleshooting

Agents not initialized

```
loom team init --repo /path/to/repo
```

tmux session missing

```
loom team start my-team --repo /path/to/repo
loom team resume my-team
```

Worker pane missing

```
loom team doctor my-team
loom team resume-worker my-team w1
```

Integrator wedged or dirty

```
loom team spawn-integrator my-team --force
loom team spawn-integrator my-team --require-clean
```

Headcount limit reached

```
loom team status my-team --show-dead
loom team retire my-team <WORKER_ID>
loom team start my-team --max-headcount 0
```

Ship push failed

```
git push origin main
loom team ship my-team --no-push
```
