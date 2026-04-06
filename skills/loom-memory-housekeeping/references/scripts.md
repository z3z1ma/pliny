# Memory Housekeeping Scripts

## `scripts/memory.py memory validate`

Use this command to validate the module before and after structural edits.

```bash
scripts/memory.py memory validate
scripts/memory.py memory validate --json
```

## `scripts/memory.py memory scan`

Use this command when you want a quick summary of regular memory files.

```bash
scripts/memory.py memory scan
```

## `scripts/memory.py memory rebuild-glacier`

Use this command after archive edits so the glacier catalog stays truthful.

```bash
scripts/memory.py memory rebuild-glacier
```

## `scripts/memory.py memory rebuild-links`

Use this command after link-heavy edits so the backlink map stays truthful.

```bash
scripts/memory.py memory rebuild-links
```
