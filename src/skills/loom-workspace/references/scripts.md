# Workspace Script Reference

Use package-local script paths from this skill bundle.

The examples below assume invocation through `scripts/...` inside `loom-workspace`.

## `scripts/show_status.py`

Purpose:

- summarize current record counts by kind and status

Arguments:

- `--json`: emit a machine-readable JSON summary instead of grouped text

Output:

- grouped text counts by record kind and status
- JSON summary when `--json` is provided

Example:

```bash
python3 "scripts/show_status.py" --json
```

## `scripts/diagnose_workspace.py`

Purpose:

- check workspace health before trusting packet, review, or durable-edit flows
- with `--fix`, create missing `.loom/` root and canonical subtree directories before reporting

Arguments:

- `--json`: emit a machine-readable doctor report
- `--fix`: create missing `.loom/` directories, then re-check and report the final state

Output:

- text summary with workspace path, health, skill count, record issue count, and link issue count
- lists fixed directories when `--fix` created them
- lists remaining missing directories or subtrees that could not be auto-fixed
- JSON doctor report when `--json` is provided
- non-zero exit status when the workspace is unhealthy

Example:

```bash
python3 "scripts/diagnose_workspace.py" --json
python3 "scripts/diagnose_workspace.py" --fix
python3 "scripts/diagnose_workspace.py" --fix --json
```

## `scripts/list_records.py`

Purpose:

- list canonical records before linking, routing, or packet compilation

Arguments:

- `--kind`: optional kind filter such as `ticket` or `plan`
- `--status`: optional status filter
- `--include-runs`: include run artifacts in the listing
- `--json`: emit JSON instead of tab-separated text

Output:

- JSON array when `--json` is provided
- otherwise one tab-separated line per record: `id kind status path`

Example:

```bash
python3 "scripts/list_records.py" --kind ticket --status ready --json
```

## `scripts/validate_record.py`

Purpose:

- validate one record or the visible record set before trusting it

Arguments:

- `path`: optional record path; omit it to validate all discovered records
- `--json`: emit structured JSON issues

Example:

```bash
python3 "scripts/validate_record.py" ".loom/tickets/agel2-0002-inventory-shared-loom-script-clis.md"
```

## `scripts/check_links.py`

Purpose:

- confirm that typed record links resolve across the workspace

Arguments:

- `--json`: emit structured JSON issues

Example:

```bash
python3 "scripts/check_links.py"
```

## `scripts/resolve_scope.py`

Purpose:

- discover repository ownership for the workspace or for one target path

Arguments:

- `--path`: optional target path to resolve to one owning repository/worktree
- `--json`: emit structured JSON output

Output:

- repository inventory when `--path` is omitted
- owner payload for one target path when `--path` is provided

Example:

```bash
python3 "scripts/resolve_scope.py" --json --path ".loom/constitution/constitution.md"
```
