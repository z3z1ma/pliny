# Plan Script Reference

Use package-local script paths from this skill bundle.

The examples below assume invocation through `scripts/plans.py` inside `loom-plans`.

## `scripts/plans.py create`

Purpose:

- create a plan scaffold under `.loom/plans/`
- with no slug, validate plans instead

Example:

```bash
scripts/plans.py create bootstrap-cli-reference-docs --status active
```

## `scripts/plans.py link`

Purpose:

- add or remove typed links between a plan and its governing or downstream records

Example:

```bash
scripts/plans.py link "plan:bootstrap-cli-reference-docs" --add "ticket:0002"
```
