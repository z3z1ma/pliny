# Memory Cookbook

This cookbook documents the Memory subsystem CLI and shows many practical ways
to use it from shells and scripts. It is based on direct code tracing of the
memory module.

## Mental model

- Notes are Markdown files with YAML frontmatter.
- SQLite index is derived and rebuildable; the files are the source of truth.
- Each note has a stable id that must match the filename stem.
- Notes are stored in a vault (default `.loom/memory/`).

## Vault layout and discovery

Default vault layout (created by `memory init`):

```
 .loom/memory/
  notes/                     # shared, committed
  personal/notes/            # personal, gitignored
  personal/ephemeral/notes/  # ephemeral scratch, gitignored
  meta.json                  # committed config
  index.sqlite3              # derived cache, gitignored
```

Vault selection:

- `--vault <path>` or `MEMORY_VAULT` env var
- If the path is relative and you are in a git repo, it resolves relative to
  the repo root. Otherwise, relative to the current working directory.

## Frontmatter schema

Required keys:

- `id` (matches filename stem, link-safe)
- `title`
- `created_at` (RFC3339 UTC)
- `updated_at` (RFC3339 UTC)

Optional keys:

- `tags` (list)
- `aliases` (list)
- `scopes` (list)
- `links` (list)
- `visibility` (shared|personal|ephemeral)
- `status` (active|deprecated)

Notes:

- Tags are normalized to lowercase and must be `A-Za-z0-9_-`.
- Visibility is implied by path. If frontmatter and path disagree, you will
  see warnings during indexing.

## Global flags and output formats

Global flags (accepted before or after subcommands):

- `--vault` select vault directory
- `--format` one of: `json` (default), `jsonl`, `text`, `md`, `prompt`
- `--deterministic` disable recency boost, omit context `generated_at`
- `--quiet` reduce stderr warnings (output still returns structured data)

Convenience aliases and shorthands:

- `--vault-dir`, `--vault_root` -> `--vault`
- `--stdout-format` -> `--format`
- `--json` -> `--format json`
- `--jsonl` -> `--format jsonl`
- `--md`, `--markdown` -> `--format md`
- `--prompt` -> `--format prompt`

## Environment variables

- `MEMORY_VAULT` default vault root
- `MEMORY_EDITOR` editor for `--interactive` (falls back to `VISUAL` or `EDITOR`)
- `MEMORY_DEFAULT_VISIBILITY` default visibilities for `recall`/`list` (comma-separated; default: `shared,personal`)

## Scopes

Scopes are structured context labels used to filter recall results.

Kinds:

- `file:src/app.py`
- `folder:src/`
- `filetype:py`
- `command:pytest -q`
- `tag:infra`

Notes:

- `file` and `folder` are repo-relative when in a git repo.
- `file` and `folder` support glob wildcards (`*`, `?`, `[]`) in the path value.
- Unknown scope kinds are ignored during parsing and matching.
- `--allow-missing-scopes` bypasses file existence checks.
- `--command` is shorthand for `--scope command:...` (supported by `add`, `edit`, and `recall`).

## Links

Links are detected from note bodies and indexed into a link graph.

Supported formats:

- Wikilinks: `[[note-id]]`, `[[note-id|alias]]`, `[[note-id#anchor]]`
- Markdown links: `[text](note-id)` or `[text](path/to/note.md)`

Resolution rules:

- Prefer exact id match.
- Otherwise, match title or aliases (case-folded).
- Ambiguous or missing targets are tracked and reported by `link validate`.

## Commands

### prime

Print this built-in operating manual.

```
loom memory prime
loom memory prime --format json
```

### init

Initialize vault layout, meta.json, gitignore safety, and the sqlite index.

```
loom memory init
loom memory init --vault .loom/memory
```

### add

Create a new note. Title can be inferred from the first non-empty body line
if `--title` is omitted.

Common flags:

- `--title`
- `--id` (advanced; must be link-safe)
- `--tag` (repeatable; comma-separated ok)
- `--alias` (repeatable)
- `--link` (repeatable; adds frontmatter `links`)
- `--related` (repeatable; appends `Related: [[...]]` line)
- `--scope` (repeatable)
- `--command` (shorthand for adding `--scope command:...`)
- `--visibility` shared|personal|ephemeral
- `--status` active|deprecated
- `--folder` subfolder under visibility root
- `--body` (string; use `--body -` to read stdin)
- `--interactive` open editor for body
- `--allow-missing-scopes`

Examples:

```
loom memory add --title "Retry behavior" --body "..." --tag infra --scope file:src/worker.py
echo "Body" | loom memory add --title "Note from stdin" --tag notes
cat spec.md | loom memory add --title "Spec" --tag spec --scope folder:docs/
loom memory add "Title from positional" --body "Body"
loom memory add --title "Scratch" --visibility ephemeral --body "..."
loom memory add --title "Personal" --visibility personal --body "..."
loom memory add --title "Organize" --folder infra/retries --body "..."
```

### edit

Edit an existing note by id. Supports body replacement or append, plus tag,
alias, scope, visibility, and status updates.

Body flags:

- `--body` replace body text
- `--from-stdin` replace body from stdin (strict)
- `--append` append text
- `--append-from-stdin` append from stdin (strict)
- `--interactive` open editor (human path)

Metadata flags:

- `--title`
- `--tag` / `--remove-tag` / `--clear-tags`
- `--alias` / `--remove-alias` / `--clear-aliases`
- `--link` / `--remove-link` / `--clear-links`
- `--related` (append a `Related: [[...]]` line)
- `--scope` / `--remove-scope` / `--clear-scopes`
- `--command` (shorthand for adding `--scope command:...`)
- `--visibility` shared|personal|ephemeral (moves file)
- `--status` active|deprecated
- `--allow-missing-scopes`

Examples:

```
loom memory edit retry-behavior --append "New findings"
cat new_body.md | loom memory edit retry-behavior --from-stdin
echo "Append" | loom memory edit retry-behavior --append-from-stdin
loom memory edit retry-behavior --tag infra --remove-tag legacy
loom memory edit retry-behavior --scope file:src/worker.py
loom memory edit retry-behavior --visibility personal
```

### recall

Recall notes with FTS + filters. Default output is JSON.

Aliases:

- `loom memory get` -> `loom memory recall`
- `loom memory remember` -> `loom memory recall`

Key flags:

- `--limit` (default 8)
- `--tag` / `--not-tag`
- `--scope` / `--not-scope`
- `--command` (shorthand for `--scope command:...`)
- `--visibility` (repeatable; default shared)
- `--include-deprecated`
- `--since` (RFC3339 or YYYY-MM-DD)
- `--until` (RFC3339 or YYYY-MM-DD)
- `--and` (AND semantics for multiple tag/scope filters)
- `--or` (OR semantics between query tokens; default AND)
- `--fts-raw` (treat the query as a raw SQLite FTS expression)
- `--scoped-only` (drop unscoped notes when scope filters exist)
- `--full` (include body with size cap)
- `--max-body-chars` (default 800; 4000 when `--context`)
- `--context` (render a context pack)
- `--max-chars` (context pack size cap)
- `--expand` (k-hop link expansion)

Examples:

```
loom memory recall "retries" --scope file:src/worker.py
loom memory recall "timeout" --tag infra --tag retries --and
loom memory recall "api" --not-tag deprecated
loom memory recall "foo" --since 2025-01-01
loom memory recall --tag onboarding --visibility shared --visibility personal
loom memory get "retri"  # prefix matching by default
```

### list

List recent notes (temporal browse; no query required).

Aliases:

- `loom memory ls` -> `loom memory list`
- `loom memory recent` -> `loom memory list`

Examples:

```
loom memory list
loom memory list --tag infra --limit 50
loom memory list --since 2026-02-01 --until 2026-02-09
```

### show

Show a note's markdown (or just its YAML frontmatter).

```
loom memory show retry-behavior
loom memory show retry-behavior --meta
```

### open

Open a note in your editor.

```
loom memory open retry-behavior
```

### forget

Forget notes. Default is soft-forget by setting `status=deprecated` (hidden from default recall/list).

Alias:

- `loom memory archive` -> `loom memory forget`

Safety:

- Requires a query or at least one filter.
- Default is dry-run; use `--apply` to make changes.

Examples:

```
loom memory forget --tag legacy
loom memory forget --tag legacy --apply
loom memory forget "outdated auth" --apply
loom memory forget --since 2025-01-01 --apply
loom memory forget --tag secrets --hard --apply
```

### around

Show notes created/updated near another note (temporal edges).

```
loom memory around retry-behavior
loom memory around retry-behavior --by created --k 20 --window-days 7
```

### timeline

Browse recent notes grouped by day.

```
loom memory timeline
loom memory timeline --days 14
loom memory timeline --by created
```

Context packs (text output):

```
loom memory recall "retries" --context --format text
loom memory recall "retries" --context --format md --expand 1
loom memory recall --tag infra --context --format prompt
loom memory recall --scope file:src/app.py --context --format prompt --max-chars 8000
```

Notes:

- `--context` requires a query or tag/scope/command.
- `--context` cannot use JSON output; use `text`, `md`, or `prompt`.

### link

Link graph utilities.

Backlinks:

```
loom memory link backlinks retry-behavior
loom memory link backlinks retry-behavior --limit 10
```

Neighbors:

```
loom memory link neighbors retry-behavior
loom memory link neighbors retry-behavior --k 2
```

Validate broken or ambiguous links:

```
loom memory link validate
loom memory link validate --id retry-behavior
loom memory link validate --format md
```

Graph edge list:

```
loom memory link graph
loom memory link graph --include-unresolved
```

Suggest likely related notes (non-mutating):

```
loom memory link suggest retry-behavior
loom memory link suggest retry-behavior --limit 20
```

### grep

Regex search notes (literal regex; no ranking).

```
loom memory grep "timeout\\s+error" --ignore-case
loom memory grep "\bbackoff\b" --tag infra
```

### reindex

Rebuild the derived sqlite index (safe and deterministic).

```
loom memory reindex
```

### janitor

Find or fix stale file scopes after files move/delete.

```
loom memory janitor report
loom memory janitor report --visibility shared --limit 50
loom memory janitor fix --apply
```

## Unix-style recipes

### Capture command output

```
pytest -q 2>&1 | loom memory add --title "pytest failure" --tag test --command "pytest -q"
git status -sb | loom memory add --title "status snapshot" --tag git --command "git status"
```

### Use stdin for body replacement

```
cat notes/retries.md | loom memory edit retry-behavior --from-stdin
```

### Append structured updates

```
cat <<'EOF' | loom memory edit retry-behavior --append-from-stdin
- 2026-02-02: observed exponential backoff jitter mismatch
EOF
```

### Find and summarize with jq

```
loom memory recall "retries" --format json \
  | jq -r '.[] | "\(.id)\t\(.title)"'
```

### Use fzf to open a note

```
nid=$(loom memory recall "" --tag infra --format json | jq -r '.[].id' | fzf)
loom memory edit "$nid" --interactive
```

### Merge knowledge into a context pack

```
loom memory recall "auth" --scope folder:src/auth/ --context --format prompt --expand 1
```

### Detect broken links nightly

```
loom memory link validate --format text | sed -n '1,50p'
```

## Integration patterns

### Ticket -> memory

```
loom ticket show ab-1234 --raw | loom memory add --title "Ticket ab-1234" --tag ticket
```

### GitHub issue -> memory

```
gh issue view 123 --json title,body -q '.title + "\n\n" + .body' \
  | loom memory add --title "GH-123" --tag github --scope command:"gh issue view 123"
```

### Capture a design decision

```
cat decision.md | loom memory add --title "Decision: retry policy" --tag decision --scope file:src/worker.py
```

### Use multiple vaults

```
loom memory --vault .loom/memory init
loom memory --vault ../shared/.loom/memory recall "protocol"
```

## Troubleshooting

Missing vault:

```
loom memory init
```

Ambiguous or missing id:

```
loom memory recall "<query>"
loom memory link validate
```

Editor not found:

```
export MEMORY_EDITOR=nvim
```

Stale file scopes after refactor:

```
loom memory janitor report
loom memory janitor fix --apply
```

## Design notes

- The index is safe to delete and rebuild (`reindex`).
- Recall scoring combines FTS + scope match + recency (unless deterministic).
- Notes are only rewritten when you ask (edit/add), keeping diffs merge-friendly.
