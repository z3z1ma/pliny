# Docs Script Reference

Use package-local script paths from this skill bundle.

The examples below assume invocation through `scripts/docs.py` inside `loom-docs`.

## `scripts/docs.py create`

Purpose:

- create a documentation record scaffold under `.loom/docs/`

Example:

```bash
scripts/docs.py create admin-query-contract-reference --status draft --link ticket=ticket:0002
```

## `scripts/docs.py packet`

Purpose:

- scaffold a docs packet record under `.loom/runs/docs/`

Example:

```bash
scripts/docs.py packet "ticket:0002" docs --mode execution --style reference-first --allow-write-ref "ticket:0002"
```

## `scripts/docs.py link`

Purpose:

- add or remove truth-source and verification links on a docs record

Example:

```bash
scripts/docs.py link "doc:admin-query-contract-reference" --add "verification:admin-query-contract-doc-evidence"
```

## `scripts/docs.py verify`

Purpose:

- create verification evidence for docs-supporting checks or docs runs

Example:

```bash
scripts/docs.py verify admin-query-contract-doc-evidence --link "doc:admin-query-contract-reference"
