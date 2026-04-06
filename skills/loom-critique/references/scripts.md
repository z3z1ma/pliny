# Critique Script Reference

Use package-local script paths from this skill bundle.

The examples below assume invocation through `scripts/critique.py` inside `loom-critique`.

## `scripts/critique.py create`

Purpose:

- create a critique record scaffold under `.loom/critique/`

Example:

```bash
scripts/critique.py create review-ticket-0002 --link ticket=ticket:0002
```

## `scripts/critique.py packet`

Purpose:

- scaffold a critique packet record under `.loom/runs/critique/`

Example:

```bash
scripts/critique.py packet "ticket:0002" critique --mode review-only --style reference-first
```

## `scripts/critique.py link`

Purpose:

- add or remove reviewed-artifact, follow-up, or verification links on a critique record

Example:

```bash
scripts/critique.py link "critique:review-ticket-0002" --add "doc:admin-query-contract-reference"
```

## `scripts/critique.py verify`

Purpose:

- create verification evidence for critique-supporting checks or review runs

Example:

```bash
scripts/critique.py verify critique-ticket-0002-evidence --link "critique:review-ticket-0002"
