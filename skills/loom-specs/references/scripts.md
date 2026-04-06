# Spec Script Reference

Use package-local script paths from this skill bundle.

The examples below assume invocation through `scripts/specs.py` inside `loom-specs`.

## `scripts/specs.py create`

Purpose:

- create a spec scaffold under `.loom/specs/`
- with no slug, validate specs instead

Example:

```bash
scripts/specs.py create helper-cli-reference --link constitution=constitution:main
```

## `scripts/specs.py link`

Purpose:

- add or remove typed upstream and downstream links on a spec

Example:

```bash
scripts/specs.py link "spec:helper-cli-reference" --add "plan:bootstrap-cli-reference-docs"
```
