# Workspace Cookbook

This cookbook documents the Workspace subsystem CLI and shows many ways to use
it from shells, scripts, and other tools. It is based on direct code tracing of
the workspace module.

## Mental model

- Two modes, intentionally orthogonal:
  - `loom workspace harness` manages a multi-repo workspace at a control-plane root.
  - `loom workspace` (repo mode) manages worktrees inside a single git repo.
- The modes never dispatch into each other automatically.
- JSON is always available via `--json` (anywhere on the command line).

## Why use workspace harness (beyond git)

- Annotations + TTL: purpose/ticket/owner/ttl on worktrees and groups.
- Safe cleanup/GC: TTL-based suggest/apply flows that avoid surprise deletions.
- Deterministic multi-repo intent: explicit selection (`--repos`, `--set`, `--tag`, `--all`).
- Cross-repo exec + context: run commands across repos/groups with stable summaries.
- Snapshots: capture/diff/restore branch/sha/dirty state for recovery and audit.
- Components/deps context: human-editable component metadata with a derived index.

## User stories

- Sprint work: create a group worktree for a sprint branch across a repo set.
- Incident response: create a short-lived sandbox group with an expiry TTL.
- Agent fanout: run tests/lints across a tag/set with bounded parallelism.
- Cleanup day: suggest/apply removal of expired groups/worktrees, respecting leases.

## Storage layout

Harness workspace (workspace root):

```
.loom/
  workspaces/
    workspace.json
    repos/
    worktrees/
    states/
    meta/
      groups/
    leases/
    components/
      index.json
```

Repo mode (inside a git repo):

```
.loom/workspace/
  worktrees/
  meta/
    worktrees/
.git/info/exclude  # ignore .loom/workspace/
```

## Guardrails and dispatch rules

- `workspace harness` requires `.loom/workspaces/workspace.json` at the harness root.
- `workspace harness` refuses to run from within managed repos or worktrees.
- `workspace` (repo mode) must run inside a git repository.
- No implicit dispatch: running `loom workspace status` in a harness root is not
  allowed and will error. Use `loom workspace harness status` instead.

## Global JSON contract

`--json` can appear anywhere. JSON output is an envelope:

```
{
  "ok": true,
  "cmd": "worktree ls",
  "root": "/abs/path",
  "data": { ... },
  "meta": { "generated_at": "..." }
}
```

For non-JSON output, many commands emit human-readable summaries. Diff commands
emit raw patches for pipe-friendly usage.

## Selection primitives (harness mode)

Many harness commands require explicit intent when touching multiple repos.
Use one of:

- `--repos repoA repoB` (comma-separated ok)
- `--set <set>` (repo_sets from `workspace.json`)
- `--tag <tag>` (repo entry tags)
- `--all` (explicitly allow many)

Repo sets support recursion and tags:

- `@setname` expands another set
- `tag:infra` expands all repos tagged `infra`

## Branch/worktree naming

- Worktree paths encode branch/group names so slashes are safe.
- Example: `feature/foo` becomes a single directory segment.

## Durations and TTL

TTL strings accept `<N>[s|m|h|d|w]` or raw seconds (e.g., `30m`, `2h`, `7d`).

## Repo mode commands

### init

Initialize repo-local workspace directories and git excludes.

```
loom workspace init
```

### status

Show repo branch, commit, and dirty flag.

```
loom workspace status
loom workspace --json status
```

### worktree add / ensure / ensure-detached

Create or ensure worktrees inside `.loom/workspace/worktrees/<branch>`.

```
loom workspace worktree add feature/foo
loom workspace worktree add feature/foo --base-ref origin/main
loom workspace worktree add feature/foo --path ../scratch/foo

loom workspace worktree ensure feature/foo
loom workspace worktree ensure feature/foo --allow-dirty
loom workspace worktree ensure feature/foo --path ../scratch/foo

loom workspace worktree ensure-detached --path ../scratch/pin --ref 1a2b3c4
```

### worktree status / check-clean / check-divergence

```
loom workspace worktree status --worktree feature/foo
loom workspace worktree check-clean --worktree feature/foo
loom workspace worktree check-clean --allow-untracked
loom workspace worktree check-divergence --worktree feature/foo --base origin/main
```

### worktree diff

```
loom workspace worktree diff --worktree feature/foo --mode dirty
loom workspace worktree diff --worktree feature/foo --mode cumulative --base origin/main
loom workspace worktree diff --max-bytes 500000
```

### worktree annotate

Attach metadata (purpose, ticket, ttl). Used by cleanup and GC.

```
loom workspace worktree annotate feature/foo --purpose "Investigate retry" --ticket ab-1234
loom workspace worktree annotate feature/foo --ttl 2d --owner alex
```

### worktree rm / rm-path / prune / ls

```
loom workspace worktree ls
loom workspace worktree rm feature/foo --yes
loom workspace worktree rm feature/foo --yes --force
loom workspace worktree rm-path ../scratch/foo --yes
loom workspace worktree prune
```

### merge attempt

Attempt a local merge in a worktree. Can hard reset with `--force-clean`.

```
loom workspace merge attempt --worktree ../scratch/foo --base main --topic feature/foo
loom workspace merge attempt --worktree ../scratch/foo --base main --topic feature/foo --force-clean
```

### cleanup suggest / apply

Suggest and apply worktree cleanup based on metadata TTL.

```
loom workspace cleanup suggest
loom workspace cleanup apply --id feature/foo --yes
```

### sandbox create / promote / gc

Create sandbox worktrees under `.loom/workspace/worktrees/sandbox/<name>`.

```
loom workspace sandbox create --base main --name spike --ttl 2h --purpose "spike"
loom workspace sandbox promote --from sandbox/spike --to feature/spike
loom workspace sandbox gc --yes
```

### snapshot capture / diff / restore

Repo-local snapshots track branch/commit/dirty state.

```
loom workspace snapshot capture baseline
loom workspace snapshot diff baseline
loom workspace snapshot restore baseline --yes
loom workspace snapshot restore baseline --yes --force-clean
```

## Harness workspace commands

All commands in this section use `loom workspace harness ...`.

## Leases (harness coordination)

Leases are a harness-only coordination primitive stored under `.loom/workspaces/leases/`.

- They are NOT related to ticket claims and are not automatically tied to tickets.
- They do NOT prevent parallel work on multiple branches/worktrees.
- They are an *optional* exclusive coordination lock for higher-level harness operations.
- Leases are time-bound by default (TTL); renew them if a long-running process needs the hold.

Primary use cases:
- Protect a group from automated cleanup/GC while it is actively in use.
- Avoid two orchestrators/agents mutating the same group concurrently.

Examples:

```
# Mark a group in-use so cleanup/GC can skip it (default TTL: 8h).
loom workspace harness lease acquire group:sprint-42

# Explicit TTL (or disable expiry).
loom workspace harness lease acquire group:sprint-42 --ttl 2h
loom workspace harness lease acquire group:sprint-42 --ttl none

# Renew (bumps updated_at; optionally change TTL).
loom workspace harness lease renew group:sprint-42
loom workspace harness lease renew group:sprint-42 --ttl 4h

# Inspect.
loom workspace harness lease show group:sprint-42

# Release when done.
loom workspace harness lease release group:sprint-42

# List current leases.
loom workspace harness lease ls
```

### harness init

Initialize a harness workspace control plane.

```
loom workspace harness init
loom workspace harness init --root /path/to/my-harness
loom workspace harness init --symlinks
```

### harness add / rm / list

Manage repo inventory in `workspace.json`.

```
loom workspace harness add billing git@github.com:org/billing.git --clone
loom workspace harness add api https://github.com/org/api.git --default-branch main
loom workspace harness add core git@github.com:org/core.git --shallow --depth 10
loom workspace harness add core git@github.com:org/core.git --force

loom workspace harness rm api
loom workspace harness rm api --delete-clone --yes-delete
loom workspace harness rm api --delete-component-md --yes-delete

loom workspace harness list
```

### harness repo edit

Update repo metadata in `workspace.json`.

```
loom workspace harness repo edit api --default-branch main --add-tag platform
loom workspace harness repo edit api --rm-tag legacy --description "API service"
loom workspace harness repo edit api --shallow --depth 50
loom workspace harness repo edit api --no-shallow
```

### harness set upsert / rm / show / ls

Manage repo sets for selection.

```
loom workspace harness set upsert core api billing
loom workspace harness set upsert backend @core tag:infra
loom workspace harness set show backend
loom workspace harness set ls
loom workspace harness set rm backend
```

### harness sync / status / context / branch

```
loom workspace harness sync --all --clone
loom workspace harness sync --repos api billing
loom workspace harness status --tag infra
loom workspace harness context --all

loom workspace harness branch feature/foo --all
loom workspace harness branch feature/foo --base-ref main --clone --allow-dirty --all
loom workspace harness branch feature/foo --reset --yes --all
```

### harness exec

Run commands across repos (or across a worktree group).

```
loom workspace harness exec --all -- echo ok
loom workspace harness exec --repos api billing -- ls -la
loom workspace harness exec --tag infra --jobs 4 -- git status -sb
loom workspace harness exec --group sprint-42 --all -- git status -sb
loom workspace harness exec --group sprint-42 --require-clean --all -- git status -sb
```

### harness worktree add / rm / ls / prune

Create or remove a worktree group under `worktrees/<group>/<repo>`.

```
loom workspace harness worktree add sprint-42 --all --clone
loom workspace harness worktree add sprint-42 --repos api billing --base-ref main

# Override where the group's worktrees are created (path/<repo>).
# This is useful for integration with Loom Team and other orchestrators.
loom workspace harness worktree add sprint-42 --all --path ../team-runs/sprint-42

loom workspace harness lease acquire group:sprint-42
loom workspace harness worktree rm sprint-42 --all --yes --require-lease group:sprint-42

loom workspace harness worktree rm sprint-42 --repos api --yes
loom workspace harness worktree rm sprint-42 --all --yes --force
loom workspace harness worktree ls
loom workspace harness worktree prune --all
```

### harness worktree status / check-clean / check-divergence / diff

```
loom workspace harness worktree status sprint-42 --all
loom workspace harness worktree check-clean sprint-42 --all
loom workspace harness worktree check-clean sprint-42 --allow-untracked --all
loom workspace harness worktree check-divergence sprint-42 --base origin/main --all
loom workspace harness worktree diff sprint-42 --all --mode dirty
loom workspace harness worktree diff sprint-42 --all --mode cumulative --base origin/main
```

### harness worktree annotate / rebase / push / gc

```
loom workspace harness worktree annotate sprint-42 --purpose "Feature sprint" --ttl 7d
loom workspace harness worktree rebase sprint-42 --base-ref main --all
loom workspace harness worktree push sprint-42 --all --set-upstream
loom workspace harness worktree push sprint-42 --all --force --yes
loom workspace harness worktree gc --older-than 14 --yes
loom workspace harness worktree gc --older-than 30 --skip-leased --yes
```

### harness snapshot capture / diff / restore

Snapshots can target repos or a worktree group.

```
loom workspace harness snapshot capture sprint-42 --all
loom workspace harness snapshot capture sprint-42 --group sprint-42 --all
loom workspace harness snapshot diff sprint-42
loom workspace harness snapshot restore sprint-42 --yes
loom workspace harness snapshot restore sprint-42 --yes --force-clean
```

### harness lease acquire / release / ls

Leases are optional coordination locks stored under `.loom/workspaces/leases`.
They are primarily used to mark a group in-use so cleanup/GC can skip it.

```
loom workspace harness lease acquire group:sprint-42
loom workspace harness lease acquire group:sprint-42 --force
loom workspace harness lease release group:sprint-42
loom workspace harness lease ls
```

### harness sandbox create / promote / gc

Sandbox worktrees are group-scoped with TTLs.

```
loom workspace harness sandbox create --group spike --base-ref main --all --ttl 2h
loom workspace harness sandbox promote --group spike
loom workspace harness sandbox gc --yes
```

### harness components refresh-index / deps

Component metadata lives in `components/<repo>.md`. The index is derived.

```
loom workspace harness components refresh-index
loom workspace harness components refresh-index --print

# Alias for components (microservice naming)
loom workspace harness services refresh-index

loom workspace harness deps show api
loom workspace harness deps who-uses api
loom workspace harness deps closure api
loom workspace harness deps impacted api
```

### impact

Impact analysis answers: "Given these changed repos, what components are impacted?".
It uses `components/index.json` (forward deps + reverse deps) and emits a deterministic report.

```
loom workspace harness impact repos api
loom workspace harness impact repos api billing

loom workspace harness snapshot capture pre-rebase --group sprint-42 --all
loom workspace harness impact snapshot pre-rebase
```

### harness deepen

Deepen history for shallow clones.

```
loom workspace harness deepen api --depth 200
```

## Unix-style recipes

### Pipe diffs into review tools

```
loom workspace worktree diff --mode cumulative --base origin/main \
  | less
```

### Run tests across a repo set

```
loom workspace harness exec --set backend --jobs 4 -- uv run pytest -q
```

### Discover impacted components from a change

```
loom workspace harness impact repos api | jq -r '.impacted[]'
```

### Record a snapshot before a risky rebase

```
loom workspace harness snapshot capture pre-rebase --group sprint-42 --all
loom workspace harness worktree rebase sprint-42 --base-ref main --all
loom workspace harness snapshot diff pre-rebase
```

### Enforce clean worktrees before pushing

```
loom workspace harness worktree check-clean sprint-42 --all
loom workspace harness worktree push sprint-42 --all
```

### Guard a shared group with leases

```
loom workspace harness lease acquire group:sprint-42
loom workspace harness worktree gc --skip-leased --yes
```

## Troubleshooting

Not in harness control plane:

```
loom workspace harness init
```

Refused to operate on many repos:

```
loom workspace harness status --all
loom workspace harness status --repos api billing
```

Worktree remove refused:

```
loom workspace worktree rm feature/foo --yes
loom workspace harness worktree rm sprint-42 --all --yes
```

Snapshot restore refused:

```
loom workspace snapshot restore baseline --yes
loom workspace harness snapshot restore baseline --yes
```

## Design notes

- Harness mode is a control plane over multiple repos and group worktrees.
- Repo mode is minimal, safe, and git-native for a single repo.
- Components metadata is human-editable; index is derived.
- Snapshots are JSON snapshots of branch/commit/dirty state, not full backups.
