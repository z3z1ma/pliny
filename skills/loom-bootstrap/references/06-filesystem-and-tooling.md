# Filesystem And Tooling

This is an ordered bootstrap reference for the `loom-bootstrap` skill.

Loom assumes the filesystem is already a rich interface.

A well-shaped Loom workspace should be queryable with ordinary tools.

## Default Tool Posture

Prefer plain tools first:

- `rg` for graph queries and heading/status scans
- `find` or `fd` for discovery
- `git` for ownership, diff, and history
- `cat`, `tee`, `cp`, `mv`, `mkdir`, and related shell primitives for direct file work
- `sort`, `uniq`, `comm`, `cut`, `paste`, `xargs` for rollups
- `sed`, `awk`, or `perl` for lightweight transformations
- `wc`, `stat`, `date`, `mktemp` for operational checks

The protocol does not prescribe one implementation path.

Do not narrow "plain tools" to only search primitives such as `rg` and `find`.
Ordinary shell composition is first-class Loom behavior.
Pipelines that combine `awk`, `sed`, `cat`, `xargs`, `sort`, `comm`, `jq`,
`yq`, `git`, and similar utilities are often the clearest and most powerful
way to inspect, validate, and reshape the graph.

Use `jq` or `yq` when they are present and clearly helpful.
Use inline Python when the shell would become harder to read than the logic justifies.
Harness-native helpers are still acceptable when they are genuinely the better
ergonomic fit, especially for reading one specific file or applying one precise
single-file edit, but they do not replace the general shell toolbox.

## The Filesystem Is The Graph

A Loom workspace is designed so that these operations are meaningful:

```bash
rg -n '^id:' .loom
rg -n 'ticket:<token>' .loom
find .loom/tickets -name '*.md'
git log --oneline .loom/wiki
```

The agent should not wait for a specialized query runtime before it can understand the graph.
Specialized helpers may exist, but the graph should still yield to ordinary
command composition.

For a larger catalog of ordinary-tool recipes for tickets, packets, claims,
evidence, critique, stale records, and placeholder scans, use
`skills/loom-records/references/query-and-linking.md`. Those recipes are
discovery aids, not mandatory runtime dependencies or validation proof by
themselves.

## Creating Files

When you need to create a record, prefer one of these:

### Copy a template

Copy from the installed Loom skill package path for the current harness. In a
source checkout or repo-root skill installation, that may look like:

```bash
cp skills/loom-tickets/templates/ticket.md ".loom/tickets/<YYYYMMDD>-<token>-<short-slug>.md"
```

### Emit a here-doc

Set the slug and question before running, then validate the temporary file before
moving it into `.loom/research/`. Research records do not use `draft` status;
keep `status: active` only when the copied record has a real research question.

```bash
slug="${LOOM_RESEARCH_SLUG:-}"
question="${LOOM_RESEARCH_QUESTION:-}"

case "$slug" in
  ""|*[!a-z0-9-]*)
    printf 'Set LOOM_RESEARCH_SLUG to a lowercase slug before writing.\n' >&2
    exit 1
    ;;
esac

if [ -z "$question" ]; then
  printf 'Set LOOM_RESEARCH_QUESTION before writing an active research record.\n' >&2
  exit 1
fi

now="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
path=".loom/research/${slug}.md"

if [ -e "$path" ]; then
  printf 'Research record already exists; choose a new slug or reconcile the existing record first.\n' >&2
  exit 1
fi

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

if ! cat > "$tmp" <<EOF
---
id: research:${slug}
kind: research
status: active
created_at: ${now}
updated_at: ${now}
scope:
  kind: repository
  repositories:
    - repo:root
links: {}
---

# Question

${question}
EOF
then
  printf 'Failed to write temporary research record.\n' >&2
  exit 1
fi

if rg -n '<[^>]+>|\bTBD\b|\bTODO\b' "$tmp"; then
  printf 'Record still contains placeholders; repair before relying on it.\n' >&2
  exit 1
fi

mv "$tmp" "$path" || exit 1
trap - EXIT
```

### Use an inline snippet

If you need to generate a token, normalize a slug, or create several similar files, a small inline shell or Python snippet is acceptable.

## Ticket Token Generation

A portable shell pattern for ticket tokens is:

```bash
token="$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 8)"
stamp="$(date -u +%Y%m%d)"
```

Use the token in the canonical ticket ID and in the filename.

## Frontmatter Queries

When you want structured data from one Loom record without introducing a custom
parser, prefer extracting the first YAML frontmatter block with a fence-aware
`awk` filter and piping it into `yq`.

```bash
awk 'BEGIN{found=0} /^---$/{found++; next} found==1' .loom/... | yq ...
```

That pattern is the encouraged native-tool baseline for single-record
frontmatter inspection because it stays transparent, composes with ordinary
Unix pipelines, and does not require Loom-specific helper code.

## Link Queries

The standard way to answer "what points at this?" is text search.

Examples:

```bash
rg -n 'spec:<slug>' .loom
rg -n 'wiki:<slug>' .loom
rg -n 'evidence:<slug>' .loom
```

Typed references are intentionally plain text so ordinary search is enough.

## Scope Resolution

Use native repository inspection before trusting nested paths:

```bash
git rev-parse --show-toplevel
git -C path/to/target rev-parse --show-toplevel
```

Fail closed if ownership is ambiguous.

## Harness Invocation

Loom does not require a specific transport for fresh-context work.

Any of these are acceptable if the packet contract is preserved:

- a harness-native subagent system
- a headless CLI invocation
- a manual handoff into a new context window
- another reproducible mechanism documented in `.loom/harness.md`

The protocol cares about the contract, not the transport.

## Command Surface Canonicality

Slash commands, prompt wrappers, and harness adapters are invocation
conveniences.

Deleting a command surface should not delete a Loom capability. Durable behavior
belongs in bootstrap doctrine, skills, references, templates, and canonical
records.

Commands may invoke acceptance, review, shipping, retrospective, or Ralph
workflows. They do not own those workflows' truth, and they never own ticket
closure, critique verdicts, evidence sufficiency, or accepted wiki explanation.

## When Shell Gets Awkward

Use inline Python for things like:

- extracting or aggregating frontmatter from many files
- bulk broken-reference audits
- non-trivial filename rewrites
- cross-file index regeneration

That is not a violation of Loom.
The violation would be making the protocol dependent on a shipped helper runtime instead of the agent's judgment.

## Anti-Patterns

Do not:

- build a hidden second system when simple file operations would do
- force one command style on every harness
- assume the presence of tools you have not checked
- collapse the toolbox to a few favored helpers when ordinary shell
  composition would be clearer or more composable
- let convenience wrappers replace understanding of the artifact graph

The best Loom operator is comfortable reading and writing the corpus directly.
