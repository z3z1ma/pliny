# Ralph Script Reference

Use package-local script paths from this skill bundle.

The examples below assume invocation through `scripts/ralph.py` inside `loom-ralph`.

## `scripts/ralph.py packet`

Purpose:

- scaffold a bounded Ralph execution packet record under `.loom/runs/ralph/`

Arguments:

- `target_ref`: canonical target ref, usually a ticket ref
- `subsystem`: use `ralph` in this skill
- `--mode`: packet mode
- `--style`: packet style
- `--allow-write-ref`: repeatable allowed-write ref for execution packets
- `--output`: optional output path override

Output:

- prints the compiled packet path relative to the workspace

Example:

```bash
scripts/ralph.py packet "ticket:0002" ralph --mode execution --style reference-first --allow-write-ref "ticket:0002"
```

## `scripts/ralph.py verify`

Purpose:

- create verification evidence after a Ralph run or supporting check

Arguments:

- `slug`: verification slug
- `--link`: verification frontmatter links
- `--path`, `--repository`, `--workspace-scope`: scope inputs

Example:

```bash
scripts/ralph.py verify ralph-ticket-0002-run --link "ticket:0002"
```
