# Research Script Reference

Use package-local script paths from this skill bundle.

The examples below assume invocation through `scripts/research.py` inside `loom-research`.

## `scripts/research.py create`

Purpose:

- create a research note scaffold under `.loom/research/`
- with no slug, validate research notes instead

Example:

```bash
scripts/research.py create shared-script-cli-inventory
```

## `scripts/research.py link`

Purpose:

- add or remove typed links on an existing research note

Example:

```bash
scripts/research.py link "research:shared-script-cli-inventory" --add "ticket:0002"
```
