# Initiative Script Reference

Use package-local script paths from this skill bundle.

The examples below assume invocation through `scripts/initiatives.py` inside `loom-initiatives`.

## `scripts/initiatives.py create`

Purpose:

- create an initiative record scaffold under `.loom/initiatives/`
- with no slug, validate initiative records instead

Example:

```bash
scripts/initiatives.py create improve-operator-workflows
```

## `scripts/initiatives.py link`

Purpose:

- add or remove typed research, spec, plan, or ticket links on an initiative

Example:

```bash
scripts/initiatives.py link "initiative:improve-operator-workflows" --add "plan:bootstrap-cli-reference-docs"
```
