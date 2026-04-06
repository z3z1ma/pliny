# Memory Context Scripts

## `scripts/memory.py memory scan`

Purpose:

- list compact L0 summaries of memory files before deciding what to read

Arguments:

- `--domain all|system|user`: restrict output to one memory domain
- `--json`: emit structured JSON rows

Examples:

```bash
scripts/memory.py memory scan
scripts/memory.py memory scan --domain user
scripts/memory.py memory scan --json
```

## `scripts/memory.py memory validate`

Purpose:

- validate the manifest, required files, and L0 coverage for the memory module

Arguments:

- `--json`: emit structured JSON summary

Examples:

```bash
scripts/memory.py memory validate
scripts/memory.py memory validate --json
```
