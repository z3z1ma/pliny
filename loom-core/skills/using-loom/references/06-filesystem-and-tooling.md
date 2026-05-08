# Filesystem And Tooling

This is an ordered reference for the `using-loom` skill.

Loom assumes the filesystem is the graph. A Loom workspace should be legible
through files and tools, not dependent on a hidden runtime.

## Tool Posture

Prefer ordinary tools first: `rg` for graph queries, `find` or `fd` for discovery,
`git` for ownership and history, shell primitives for file work, rollup tools
such as `sort`/`uniq`/`xargs`, `sed`/`awk`/`perl` for small transformations, and
`wc`/`stat`/`date`/`mktemp` for operational checks.

The protocol does not prescribe one command style. Pipelines using `awk`, `sed`,
`cat`, `xargs`, `sort`, `jq`, `yq`, `git`, and similar utilities are first-class
Loom behavior when clearest. Use inline Python when shell composition would be
harder to read. Harness helpers are fine for focused reads or precise edits, but
do not replace the general toolbox.

## Query The Graph Directly

These should be meaningful operations:

```bash
rg -n '^id:' .loom
rg -n 'ticket:<token>' .loom
find .loom/tickets -name '*.md'
git log --oneline .loom/wiki
```

Specialized helpers may exist, but agents must not wait for them. Richer recipes
may live in `skills/loom-records/references/query-and-linking.md`; they are
discovery aids, not mandatory dependencies or proof by themselves.

## Create Records From Owning Templates

When creating a record, start from the relevant skill's `templates/` directory and
use the safest available method: harness file tools, shell, editor actions, or a
small one-off script if proportional. In a split checkout templates may live under
`loom-core/skills/.../templates/`; in an installed root, under
`skills/.../templates/`.

Before treating the file as truth, clear placeholders, set real frontmatter,
follow naming and ID rules, link the right owner layer, and run the smallest
honest structural check.

Ticket tokens should be portable and appear in both the ID and filename:

```bash
token="$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 8)"
stamp="$(date -u +%Y%m%d)"
```

## Inspect Frontmatter, Links, And Scope

For one record's YAML frontmatter, use transparent extraction rather than a Loom
parser when possible:

```bash
awk 'BEGIN{found=0} /^---$/{found++; next} found==1' .loom/... | yq ...
```

Typed references are plain text, so backlink checks are text search:

```bash
rg -n 'spec:<slug>' .loom
rg -n 'wiki:<slug>' .loom
rg -n 'evidence:<slug>' .loom
```

Before trusting nested paths, resolve repository ownership with native Git checks:

```bash
git rev-parse --show-toplevel
git -C path/to/target rev-parse --show-toplevel
```

Fail closed when scope or ownership is ambiguous.

## Handoffs And Command Surfaces

Loom requires no specific fresh-context transport. A harness subagent, headless
CLI, manual handoff, or mechanism documented in `.loom/harness.md` is acceptable
when the packet contract is preserved.

Slash commands, prompt wrappers, and adapters are conveniences. Deleting one must
not delete a Loom capability; durable behavior belongs in using-Loom doctrine,
skills, references, templates, and canonical records. Commands may invoke
acceptance, review, shipping, retrospective, or Ralph, but never own ticket
closure, critique verdicts, evidence sufficiency, or accepted wiki explanation.

## Anti-Patterns

Do not build a hidden second system, force one command style on every harness,
assume unchecked tools exist, collapse the toolbox to a few favored helpers, or
let convenience wrappers replace understanding of the artifact graph.
