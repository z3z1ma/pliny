# Workspace Cookbook

This cookbook documents the Workspace subsystem CLI and shows many ways to use
it from shells, scripts, and other tools. It is based on direct code tracing of
the workspace module.

## Mental model

- Two modes, intentionally orthogonal:
  - `loom workspace poly` manages a polyrepo workspace at a control-plane root.
  - `loom workspace` (repo mode) manages worktrees inside a single git repo.
- The modes never dispatch into each other automatically.
- JSON is always available via `--json` (anywhere on the command line).

## Storage layout

Poly workspace (workspace root):

```
workspace.json
.loom/
repos/
worktrees/
states/
services/
  index.json
```

Repo mode (inside a git repo):

```
.loom-repo/
  worktrees/
.git/info/exclude  # ignore .loom-repo/
```

## Guardrails and dispatch rules

- `workspace poly` requires BOTH `workspace.json` and `.loom/` at the root.
- `workspace poly` refuses to run from within managed repos or worktrees.
- `workspace` (repo mode) must run inside a git repository.
- No implicit dispatch: running `loom workspace status` in a poly root is not
  allowed and will error. Use `loom workspace poly status` instead.

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

## Selection primitives (poly mode)

Many poly commands require explicit intent when touching multiple repos.
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

Create or ensure worktrees inside `.loom-repo/worktrees/<branch>`.

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

Create sandbox worktrees under `.loom-repo/worktrees/sandbox/<name>`.

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

## Poly workspace commands

### poly init

Initialize a poly workspace control plane.

```
loom workspace poly init
```

### poly add / rm / list

Manage repo inventory in `workspace.json`.

```
loom workspace poly add billing git@github.com:org/billing.git --clone
loom workspace poly add api https://github.com/org/api.git --default-branch main
loom workspace poly add core git@github.com:org/core.git --shallow --depth 10
loom workspace poly add core git@github.com:org/core.git --force

loom workspace poly rm api
loom workspace poly rm api --delete-clone --yes-delete
loom workspace poly rm api --delete-service-md --yes-delete

loom workspace poly list
```

### poly repo edit

Update repo metadata in `workspace.json`.

```
loom workspace poly repo edit api --default-branch main --add-tag platform
loom workspace poly repo edit api --rm-tag legacy --description "API service"
loom workspace poly repo edit api --shallow --depth 50
loom workspace poly repo edit api --no-shallow
```

### poly set upsert / rm / show / ls

Manage repo sets for selection.

```
loom workspace poly set upsert core api billing
loom workspace poly set upsert backend @core tag:infra
loom workspace poly set show backend
loom workspace poly set ls
loom workspace poly set rm backend
```

### poly sync / status / context / branch

```
loom workspace poly sync --all --clone
loom workspace poly sync --repos api billing
loom workspace poly status --tag infra
loom workspace poly context --all

loom workspace poly branch feature/foo --all
loom workspace poly branch feature/foo --base-ref main --clone --allow-dirty --all
loom workspace poly branch feature/foo --reset --yes --all
```

### poly exec

Run commands across repos (or across a worktree group).

```
loom workspace poly exec --all -- echo ok
loom workspace poly exec --repos api billing -- ls -la
loom workspace poly exec --tag infra --jobs 4 -- git status -sb
loom workspace poly exec --group sprint-42 --all -- git status -sb
loom workspace poly exec --group sprint-42 --require-clean --all -- git status -sb
```

### poly worktree add / rm / ls / prune

Create or remove a worktree group under `worktrees/<group>/<repo>`.

```
loom workspace poly worktree add sprint-42 --all --clone
loom workspace poly worktree add sprint-42 --repos api billing --base-ref main
loom workspace poly worktree rm sprint-42 --repos api --yes
loom workspace poly worktree rm sprint-42 --all --yes --force
loom workspace poly worktree ls
loom workspace poly worktree prune --all
```

### poly worktree status / check-clean / check-divergence / diff

```
loom workspace poly worktree status sprint-42 --all
loom workspace poly worktree check-clean sprint-42 --all
loom workspace poly worktree check-clean sprint-42 --allow-untracked --all
loom workspace poly worktree check-divergence sprint-42 --base origin/main --all
loom workspace poly worktree diff sprint-42 --all --mode dirty
loom workspace poly worktree diff sprint-42 --all --mode cumulative --base origin/main
```

### poly worktree annotate / rebase / push / gc

```
loom workspace poly worktree annotate sprint-42 --purpose "Feature sprint" --ttl 7d
loom workspace poly worktree rebase sprint-42 --base-ref main --all
loom workspace poly worktree push sprint-42 --all --set-upstream
loom workspace poly worktree push sprint-42 --all --force --yes
loom workspace poly worktree gc --older-than 14 --yes
loom workspace poly worktree gc --older-than 30 --unclaimed-only --yes
```

### poly snapshot capture / diff / restore

Snapshots can target repos or a worktree group.

```
loom workspace poly snapshot capture sprint-42 --all
loom workspace poly snapshot capture sprint-42 --group sprint-42 --all
loom workspace poly snapshot diff sprint-42
loom workspace poly snapshot restore sprint-42 --yes
loom workspace poly snapshot restore sprint-42 --yes --force-clean
```

### poly lease acquire / release / ls

Leases are agent-safe locks stored under `.loom/leases`.

```
loom workspace poly lease acquire group:sprint-42
loom workspace poly lease acquire group:sprint-42 --force
loom workspace poly lease release group:sprint-42
loom workspace poly lease ls
```

### poly sandbox create / promote / gc

Sandbox worktrees are group-scoped with TTLs.

```
loom workspace poly sandbox create --group spike --base-ref main --all --ttl 2h
loom workspace poly sandbox promote --group spike
loom workspace poly sandbox gc --yes
```

### poly services refresh-index / deps

Services metadata lives in `services/<repo>.md`. The index is derived.

```
loom workspace poly services refresh-index
loom workspace poly services refresh-index --print

loom workspace poly deps show api
loom workspace poly deps who-uses api
loom workspace poly deps closure api
loom workspace poly deps impacted api
```

### poly deepen

Deepen history for shallow clones.

```
loom workspace poly deepen api --depth 200
```

## Unix-style recipes

### Pipe diffs into review tools

```
loom workspace worktree diff --mode cumulative --base origin/main \
  | less
```

### Run tests across a repo set

```
loom workspace poly exec --set backend --jobs 4 -- uv run pytest -q
```

### Discover impacted services from a change

```
loom workspace poly deps impacted api | jq -r '.impacted[]'
```

### Record a snapshot before a risky rebase

```
loom workspace poly snapshot capture pre-rebase --group sprint-42 --all
loom workspace poly worktree rebase sprint-42 --base-ref main --all
loom workspace poly snapshot diff pre-rebase
```

### Enforce clean worktrees before pushing

```
loom workspace poly worktree check-clean sprint-42 --all
loom workspace poly worktree push sprint-42 --all
```

### Guard a shared group with leases

```
loom workspace poly lease acquire group:sprint-42
loom workspace poly worktree gc --unclaimed-only --yes
```

## Troubleshooting

Not in poly control plane:

```
loom workspace poly init
```

Refused to operate on many repos:

```
loom workspace poly status --all
loom workspace poly status --repos api billing
```

Worktree remove refused:

```
loom workspace worktree rm feature/foo --yes
loom workspace poly worktree rm sprint-42 --all --yes
```

Snapshot restore refused:

```
loom workspace snapshot restore baseline --yes
loom workspace poly snapshot restore baseline --yes
```

## Design notes

- Poly mode is a control plane over multiple repos and group worktrees.
- Repo mode is minimal, safe, and git-native for a single repo.
- Services metadata is human-editable; index is derived.
- Snapshots are JSON snapshots of branch/commit/dirty state, not full backups.
