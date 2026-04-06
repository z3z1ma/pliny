# Workspace Query Reference

Use native file and git commands directly. `loom-workspace` does not ship a helper CLI.

## Direct Workspace Query Ideas

The queries below are examples, not a canonical command surface. Use them as portable patterns when you need to inspect the workspace corpus directly.

State rollup across the main Loom layers:

```bash
rg --no-filename -o '"kind":\s*"[^"]+"|"status":\s*"[^"]+"' .loom/{constitution,research,initiatives,specs,plans,tickets,critique,docs,verification} | sort | uniq -c
```

Records with workspace-wide or multi-repository scope that deserve extra care before editing:

```bash
rg --multiline -l '"repository_scope":\s*\{\s*"kind":\s*"(workspace|multi_repository)"' .loom/{constitution,research,initiatives,specs,plans,tickets,critique,docs,verification}
```

Execution-facing queue across tickets, plans, critique, and docs:

```bash
rg -n '"status":\s*"(active|blocked|review_required|complete_pending_acceptance|draft|accepted|stale)"' .loom/{tickets,plans,critique,docs}
```

Current Loom directory layout at a glance:

```bash
find .loom -maxdepth 2 -type d | sort
```

Everything that references one target record across the corpus:

```bash
rg -n 'ticket:0002|plan:bootstrap-cli-reference-docs|spec:minimum-proven-core-workflow-surface' .loom
```

## Direct bootstrap

Create the standard Loom directory tree directly when you need to bootstrap or repair missing structure:

```bash
mkdir -p .loom/{constitution,research,initiatives,specs,plans,tickets,critique,docs,runs,verification}
```

## Repository Ownership

Resolve the repository root for one target directory by asking git directly from that directory:

```bash
git -C "<target-dir>" rev-parse --show-toplevel
```

If you only have a file path, run the same command from its nearest existing parent directory.

## When Native Queries Are Not Enough

When you need record-aware scaffolding, validation, or mutation, switch to the owning skill rather than reaching for a workspace-level helper.

- use ticket commands for ticket creation, link mutation, and verification creation
- use specs, plans, research, docs, critique, or constitution commands inside those artifact-owning skills
- keep `loom-workspace` focused on inspection, routing, and fail-closed decisions
