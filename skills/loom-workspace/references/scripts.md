# Workspace Script Reference

Use package-local script paths from this skill bundle.

The examples below assume invocation through `scripts/workspace.py` inside `loom-workspace`.

## `scripts/workspace.py diagnose`

Purpose:

- check workspace health before trusting durable edits
- with `--fix`, create missing `.loom/` root and canonical subtree directories before reporting

Arguments:

- `--json`: emit a machine-readable doctor report
- `--fix`: create missing `.loom/` directories, then re-check and report the final state

Output:

- text or JSON workspace health report
- non-zero exit status when the workspace is unhealthy

Example:

```bash
scripts/workspace.py diagnose --fix --json
```

## `scripts/workspace.py create`

Purpose:

- create a new record scaffold or validate an existing record family

Arguments:

- `kind`: record kind such as `ticket`, `spec`, or `doc`
- `slug`: optional slug; omit it to validate that record family
- `--status`, `--link`: frontmatter inputs
- `--path`, `--repository`, `--workspace-scope`: scope inputs
- `--json`: emit validation issues as JSON

Examples:

```bash
scripts/workspace.py create ticket
scripts/workspace.py create spec helper-cli-reference
```

## `scripts/workspace.py check-links`

Purpose:

- confirm that typed record links resolve across the workspace

Arguments:

- `--json`: emit structured JSON issues

Example:

```bash
scripts/workspace.py check-links
```

## `scripts/workspace.py link`

Purpose:

- add or remove typed record links

Arguments:

- `target`: record ref to mutate
- `--add=KEY=REF` or `--add=kind:ref`: repeatable link addition
- `--remove=KEY=REF` or `--remove=kind:ref`: repeatable link removal

Example:

```bash
scripts/workspace.py link "ticket:0002" --add "verification:ticket-0002-check"
```

## `scripts/workspace.py verify`

Purpose:

- create a verification record under `.loom/verification/`

Arguments:

- `slug`: verification slug
- `--link`: verification frontmatter links
- `--path`, `--repository`, `--workspace-scope`: scope inputs

Example:

```bash
scripts/workspace.py verify ticket-0002-check --link "ticket:0002"
```

## `scripts/workspace.py scope`

Purpose:

- resolve repository ownership for one target path when scope is ambiguous

Arguments:

- `--path`: target path to resolve to one owning repository/worktree
- `--json`: emit structured JSON output

Example:

```bash
scripts/workspace.py scope --json --path ".loom/constitution/constitution.md"
```
