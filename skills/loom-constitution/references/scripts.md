# Constitutional Script Reference

Use package-local script paths from this skill bundle.

The examples below assume invocation through `scripts/constitution.py` inside `loom-constitution`.

## `scripts/constitution.py create constitution`

Purpose:

- create or intentionally replace a constitution record scaffold
- with no slug, validate constitution records instead

Example:

```bash
scripts/constitution.py create constitution main
```

## `scripts/constitution.py create decision`

Purpose:

- create one numbered decision record under `.loom/constitution/decisions/`

Example:

```bash
scripts/constitution.py create decision packet-trust-boundary
```

## `scripts/constitution.py create roadmap`

Purpose:

- create one roadmap record for strategic direction and milestone framing

Example:

```bash
scripts/constitution.py create roadmap bootstrap-the-markdown-first-protocol-corpus
```

## `scripts/constitution.py link`

Purpose:

- add or remove typed links on decision and roadmap records after the prose is in place

Example:

```bash
scripts/constitution.py link "roadmap:bootstrap-the-markdown-first-protocol-corpus" --add "decision:0002"
```

## `scripts/constitution.py diagnose`

Purpose:

- validate structural integrity before leaving the constitutional layer

Example:

```bash
scripts/constitution.py diagnose --json
```
