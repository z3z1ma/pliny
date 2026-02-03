# Ticket Cookbook

This cookbook documents every CLI surface in the Ticket subsystem and shows
many ways to drive it from shells, scripts, and other tools. Examples assume
the main entrypoint is `loom ticket`, but the parser is named
`agent-loom-ticket` and can be invoked directly if the standalone binary is
installed.

## Mental model

- Tickets live as Markdown files with YAML frontmatter in `.tickets/`.
- Each ticket is one file: `.tickets/<id>.md`.
- The CLI is designed for both humans (readable text) and machines (`--json`).
- Dependency graph primitives are first class: deps, links, parent/children.
- Optional claims/leases enable safe multi-agent concurrency.

## Storage layout

```
.tickets/
  config.yaml                 # optional, generated on first create
  <id>.md                      # ticket file
  .locks/
    <id>.lock                  # per-ticket lock while writing
    leases/<id>.json           # claim leases
    audit.lock                 # audit log lock
  .audit/
    audit-YYYY-MM-DD.jsonl     # command audit log
  .cache/                      # derived caches
```

## Tickets directory discovery

The CLI finds `.tickets/` in this order:

1. `--tickets-dir` flag (or `--ticket-dir` alias)
2. `TICKET_DIR` env var (absolute or repo-root-relative)
3. Git repo root `.tickets/` (preferred)
4. Walk up parent directories to find `.tickets/`

If none exists, `init` and `create` will create it at the git root (or cwd
if not in a repo). Other commands error with a helpful hint.

## Ticket id and reference forms

Ticket references normalize to a bare id. All of these are accepted:

- `ab-1234`
- `#ab-1234`
- `ab-1234.md`
- `.tickets/ab-1234.md`
- `/abs/path/to/.tickets/ab-1234.md`

Partial ids are resolved by prefix/contains matching. Ambiguous matches will
error with a list of candidates.

## Frontmatter schema

The YAML frontmatter uses kebab-case keys, not snake_case. The CLI will
reject underscore keys.

Required

- `id`: ticket id (filename stem)

Common fields

- `status`: open|ready|in_progress|blocked|review|closed
- `priority`: 0..4 (0 highest)
- `type`: task|bug|feature|epic|chore
- `deps`: list of ids (this ticket depends on these)
- `links`: list of ids (symmetric loose relationships)
- `parent`: id (parent/child hierarchy)
- `tags`: list of strings
- `assignee`: string
- `external-ref`: string (GitHub/Jira ref or URL)

Claim fields (usually managed by the CLI)

- `claimed-by`
- `claimed-at`
- `claim-expires`
- `claim-ttl`
- `heartbeat`

External sync cache

- `external`: dict
- `last-sync`

## Global flags

Every subcommand accepts these:

- `--json` emit machine-readable JSON with `ok`/`error` keys
- `--tickets-dir` override tickets directory (absolute or repo-root-relative)
- `--no-audit` disable audit logging
- `--audit-writes-only` only audit write commands

Convenience aliases recognized before parsing:

- `--ticket-dir` -> `--tickets-dir`
- `--noaudit` -> `--no-audit`
- `--dryrun` -> `--dry-run`

Short flag glue (auto-expanded): `-p1`, `-mmsg`, `-aalex`, `-Tinfra`.

## Environment variables

Core

- `TICKET_DIR`: override tickets directory
- `TICKET_AGENT`: agent identifier for claims (default `user@host:pid`)
- `TEAM_SPRINT_TAG`: auto-added tag on `create` (use `--no-sprint-tag` to skip)

Audit and policy

- `TK_AUDIT_MODE`: all|writes|off (default all)
- `TK_AUDIT=0`: hard-disable audit logging
- `TK_REQUIRE_CLAIM=1`: require active claim for write commands

GitHub sync

- `GITHUB_TOKEN`: GitHub API token (optional but recommended)
- `TK_GITHUB_REPO`: default `owner/repo` for `gh-123` shorthand

Jira sync

- `TK_JIRA_BASE_URL` or `JIRA_BASE_URL`
- `TK_JIRA_TOKEN` or `JIRA_TOKEN` (bearer)
- `TK_JIRA_EMAIL` + `TK_JIRA_API_TOKEN` (basic)
- `JIRA_EMAIL` + `JIRA_API_TOKEN`

## Status, priority, and type normalization

Status aliases accepted by `--status` and `status` command:

- `open`: open, todo, new, backlog
- `ready`: ready, next, queued
- `in_progress`: inprogress, wip, doing, started, progress
- `blocked`: blocked, stuck, waiting, hold
- `review`: review, pr, ready_for_review
- `closed`: closed, done, complete, completed

Priority aliases accepted by `--priority`:

- 0..4
- P0..P4
- critical|blocker|urgent|highest -> 0
- high -> 1
- medium|med|normal -> 2
- low -> 3
- lowest|trivial -> 4

Type aliases accepted by `--type`:

- feat -> feature
- bugfix -> bug

## Output shapes (JSON mode)

All JSON outputs are wrapped with `ok: true` for success, or `ok: false`
with `error`/`code` for failures.

- `list/ready/blocked/closed` -> `{count, tickets:[...]}`
- `show` -> `{ticket, relationships, body, frontmatter, lease}`
- `dep` -> `{root, nodes, edges, health}`
- `view` -> `{ticket, graph:{nodes,edges}, health}`
- `query` -> JSONL/JSON/YAML (see `query` section)

## Command cookbook

### version

Print tool name + version.

```
loom ticket version
loom ticket --json version
```

### init

Initialize `.tickets/` in the discovered tickets directory.

```
loom ticket init
loom ticket --tickets-dir ./_tickets init
```

### create

Create a new ticket with an auto-generated id. Title can be positional or
`--title` (do not pass both unless identical).

Flags

- `--title`
- `-d/--description`
- `--design`
- `--acceptance`
- `-t/--type` (default task)
- `-p/--priority` (default 2)
- `-a/--assignee`
- `--external-ref`
- `--parent`
- `--tags` (comma-separated)
- `--no-sprint-tag`

Examples

```
loom ticket create "Implement orchestration layer" -t epic -p 1 --tags ai,infra
loom ticket create --title "Fix flaky tests" -t bug -p 1 -d "Investigate race" --tags ci,infra
loom ticket create "Spec UI" --design "Figma: https://..." --acceptance "- buttons match" --tags ux
loom ticket create "Follow up" --parent ab-1234 --tags followup
loom ticket create "Default assignee from git config"
loom ticket create "Skip sprint tag" --no-sprint-tag
```

### status

Set status explicitly (respects status aliases).

```
loom ticket status ab-1234 ready
loom ticket status ab-1234 in_progress
loom ticket status ab-1234 blocked
loom ticket status ab-1234 review
loom ticket status ab-1234 closed
```

Use `--force` to override claim enforcement or active claim by another agent.

### start / close / reopen

Shortcuts for common status transitions.

```
loom ticket start ab-1234
loom ticket close ab-1234
loom ticket reopen ab-1234
```

### list (and ls alias)

List tickets with filters. Default excludes closed.

Flags

- `--status`
- `--type`
- `--priority` (exact)
- `--prio-min` / `--prio-max`
- `-a/--assignee`
- `-T/--tag`
- `--all` include closed
- `--limit` (0 = unlimited)

Examples

```
loom ticket list
loom ticket ls --status open
loom ticket list --type bug --prio-max 1
loom ticket list --priority P0
loom ticket list --prio-min 1 --prio-max 2 --tag infra
loom ticket list --assignee "Alex" --all --limit 50
```

### ready

List tickets that are not blocked and have no unresolved dependencies. Any
non-terminal status (open|ready|in_progress|review) can be considered ready
if deps are clear. Use filters to narrow.

```
loom ticket ready
loom ticket ready --type task --prio-max 2
loom ticket ready --assignee "Alex" -T sprint
```

### blocked

List tickets explicitly blocked or with open deps.

```
loom ticket blocked
loom ticket blocked -a "Alex" -T infra
```

### closed

List recently modified closed tickets (mtime descending).

```
loom ticket closed
loom ticket closed --limit 10 -a "Alex"
```

### show

Show a ticket with relationships + body.

```
loom ticket show ab-1234
loom ticket show .tickets/ab-1234.md
loom ticket show /abs/path/.tickets/ab-1234.md
```

Raw file output (frontmatter + body):

```
loom ticket show ab-1234 --raw
```

### update

Atomic field updates. Reads body from stdin if `--body` is not provided.

Flags

- `--title`
- `--status`
- `--priority`
- `--type`
- `--assignee`
- `--tags` (comma-separated, `--tags ""` clears)
- `--external-ref`
- `--body`
- `--add-note` (alias for `add-note`, cannot be combined)
- `--force`

Examples

```
loom ticket update ab-1234 --status in_progress
loom ticket update ab-1234 --title "New title"
loom ticket update ab-1234 --priority 0 --type bug
loom ticket update ab-1234 --assignee "Alex" --tags infra,ci
loom ticket update ab-1234 --external-ref gh:org/repo#123
```

Replace body from a file or pipe:

```
cat new_body.md | loom ticket update ab-1234
curl -sL https://example.com/spec.md | loom ticket update ab-1234
```

Use update as note alias:

```
loom ticket update ab-1234 --add-note "Progress update"
echo "Status update" | loom ticket update ab-1234 --add-note
```

### add-note (and note alias)

Append a timestamped note under `## Notes` (created if missing). Supports
positional note, `--note`/`--body`, or stdin.

```
loom ticket add-note ab-1234 "Started investigation"
loom ticket note ab-1234 --note "Found repro"
echo "Quick update" | loom ticket add-note ab-1234
```

### dep

Show dependency tree for a ticket (deps only).

```
loom ticket dep ab-1234
loom ticket --json dep ab-1234
```

### dep-add / dep-rm

Add or remove dependencies. Cycle detection runs on add.

```
loom ticket dep-add ab-1234 ab-2222
loom ticket dep-rm ab-1234 ab-2222
```

### dep-cycle

Find dependency cycles (ignores closed tickets).

```
loom ticket dep-cycle
```

### link / unlink

Link tickets symmetrically or remove the link.

```
loom ticket link ab-1234 ab-2222
loom ticket link ab-1234 ab-2222 ab-3333
loom ticket unlink ab-1234 ab-2222
```

### view

Orchestration view for a ticket: deps + children graph.

```
loom ticket view ab-1234
loom ticket --json view ab-1234
```

### claim / heartbeat / release

Claims are leases stored in `.tickets/.locks/leases/<id>.json`.

- `claim` sets `claimed_by`, `claim_expires`, and `heartbeat`
- `heartbeat` refreshes heartbeat; `--no-extend` keeps expiry fixed
- `release` deletes the lease

TTL format is `<number><unit>` with units `s|m|h|d` (example: `30m`).

```
loom ticket claim ab-1234 --ttl 45m
loom ticket heartbeat ab-1234
loom ticket heartbeat ab-1234 --no-extend
loom ticket release ab-1234
```

### swarm

Show agent claim activity within a time window (default 2h).

```
loom ticket swarm
loom ticket swarm --active-within 30m
```

### sync

Stage and commit `.tickets/` changes. Uses git status under the repo root.

```
loom ticket sync
loom ticket sync -m "chore: tickets"
```

### sync-external

Sync external refs for one ticket or all tickets with `external_ref` set.
Supports GitHub and Jira.

```
loom ticket sync-external
loom ticket sync-external ab-1234
loom ticket sync-external --dry-run
loom ticket sync-external --force
```

External ref formats

- GitHub: `gh:owner/repo#123` or `gh-123` (requires `TK_GITHUB_REPO`)
- Jira: `jira:PROJ-123` or a Jira browse URL

### query

Dump tickets and optionally apply a JMESPath expression. Default format is
JSONL (one JSON per line). Use `--format json|yaml` for other modes.

```
loom ticket query
loom ticket query "[?status=='open']"
loom ticket query "[].{id:id,title:title,prio:priority,status:status}"
loom ticket query --format json
loom ticket query --format yaml
```

Note: `--json` output cannot be YAML.

### prime

Print canonical usage and schema in one place.

```
loom ticket prime
loom ticket prime --json
```

## Unix philosophy recipes

### Pipe notes from other tools

```
git log -1 --pretty=%B | loom ticket add-note ab-1234
curl -sL https://example.com/incident.txt | loom ticket add-note ab-1234
```

### Replace body from stdin

```
cat spec.md | loom ticket update ab-1234
```

### Bulk status changes with jq + xargs

```
loom ticket --json list | jq -r '.tickets[] | select(.status=="open") | .id' \
  | xargs -n 1 loom ticket start
```

### Pick a ticket with fzf

```
tid=$(loom ticket --json list | jq -r '.tickets[] | "\(.id)\t\(.title)"' | fzf | cut -f1)
loom ticket show "$tid"
```

### Watch for active claims

```
watch -n 5 'loom ticket swarm'
```

### Generate a sprint list

```
loom ticket list --tag sprint --all --limit 200
```

### Create tickets from a text list

```
while IFS= read -r line; do
  loom ticket create "$line" --tags backlog
done < ideas.txt
```

### Link all tickets in a batch

```
loom ticket link ab-1234 ab-2345 ab-3456 ab-4567
```

## Integration patterns

### GitHub issue -> ticket

```
num=$(gh issue create --title "Bug: crash" --body "Steps..." --json number -q .number)
loom ticket create "Bug: crash" -t bug --external-ref "gh:owner/repo#$num" --tags bug,gh
loom ticket sync-external ab-1234
```

### Jira issue -> ticket

```
loom ticket create "Investigate PROJ-123" --external-ref "jira:PROJ-123" -t bug
loom ticket sync-external ab-1234
```

### Pull remote text into local body

```
curl -sL https://example.com/rfc.md | loom ticket update ab-1234
```

### Keep tickets in a separate directory

```
loom ticket --tickets-dir ../shared/.tickets init
loom ticket --tickets-dir ../shared/.tickets list
```

## Claims, locks, and safety

- `--force` bypasses claim enforcement and other-agent claims.
- With `TK_REQUIRE_CLAIM=1`, all write commands require an active claim.
- If you see lock errors, wait and retry or remove a stale lock file.

Write commands include:

- init, create, status, start, close, reopen
- dep-add, dep-rm, link, unlink
- add-note, note, update
- claim, release, heartbeat
- sync, sync-external

## Troubleshooting

Missing .tickets

```
loom ticket init
```

Ambiguous id

```
loom ticket list
loom ticket show <full-id>
```

Claim enforcement error

```
loom ticket claim <id>
loom ticket update <id> --force
```

Audit disabled

```
TK_AUDIT_MODE=off loom ticket list
TK_AUDIT=0 loom ticket list
```

## Example end-to-end workflow

```
loom ticket init
loom ticket create "Implement orchestration layer" -t epic -p 1 --tags ai,infra
loom ticket ready
loom ticket claim ab-1234 --ttl 45m
loom ticket start ab-1234
loom ticket add-note ab-1234 "Started work. Next: outline API."
loom ticket dep-add ab-1234 ab-5678
loom ticket view ab-1234
loom ticket close ab-1234
loom ticket release ab-1234
loom ticket sync -m "chore: tickets"
```
