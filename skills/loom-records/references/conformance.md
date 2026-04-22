# Protocol Conformance

This is a human and agent checklist, not a required validator.

A Loom workspace is conformant enough when these are true:

- owner paths exist when they contain records, and bootstrap can create the
  standard tree when needed
- `constitution:main` exists
- common record frontmatter fields are present
- ticket states are legal
- non-ticket statuses follow the shared lifecycle grammar
- ticket templates start as `proposed`, not `ready`
- claim references are qualified across records as `<record-id>#ACC-001`
- packets declare source fingerprint, context budget, execution context, and
  child write boundary
- parent reconciliation updates tickets, evidence, critique, and wiki owners
- packets do not remain `compiled` after reconciliation
- tickets do not close with unresolved required critique
- wiki pages cite accepted sources and do not own behavior or policy
- commands do not own unique protocol behavior
- utility skills are not required for the protocol kernel

## Conformance Tiers

Use the lightest tier that keeps the work honest.

### Loom Lite

For small repositories and early adoption:

- `constitution:main`
- tickets for live execution
- evidence when claims need proof
- critique when risk warrants it
- wiki optional

### Loom Standard

The default shape for serious repository work:

- constitution / initiative / plan / ticket chain when strategy matters
- Ralph packets for bounded fresh-context work
- evidence for proof
- critique for meaningful behavior, code, workflow, or authority changes
- wiki and retrospective follow-through when understanding should persist

### Loom Strict

Use when auditability, parallel work, or cross-harness handoff matters:

- namespaced claim references
- source fingerprints
- execution context
- claim matrix on tickets nearing closure
- required critique profiles and finding dispositions
- workspace scope aliases when more than one repo or worktree is plausible
- examples or conformance checks for protocol changes

## Tree Materialization

The canonical `.loom/` tree is lazily materialized.

Git may not preserve empty directories, so absence of an empty owner directory
is not itself nonconformance. A bootstrap pass should be able to create the
standard tree, and any directory that contains records should use the canonical
path for that owner.

## Useful Spot Checks

```bash
rg --files-without-match '^id:' .loom --glob '{constitution,initiatives,research,specs,plans,tickets,critique,wiki,evidence,packets}/**/*.md'
rg --files-without-match '^status:' .loom --glob '{constitution,initiatives,research,specs,plans,tickets,critique,wiki,evidence,packets}/**/*.md'
rg -n '^status:' .loom --glob '{constitution,initiatives,research,specs,plans,tickets,critique,wiki,evidence,packets}/**/*.md'
rg -n '[a-z]+:[a-z0-9-]+#(REQ|ACC|CLAIM)-[0-9]{3}' .loom --glob '*.md'
find commands -maxdepth 1 -type f -name '*.md' | sort
find skills -maxdepth 2 -name SKILL.md | sort
```

## Drift Response

If a check fails, route to the owner:

- structure or grammar -> `loom-records`
- ticket state -> `loom-tickets`
- behavior contract -> `loom-specs`
- sequencing -> `loom-plans`
- review findings -> `loom-critique`
- accepted explanation -> `loom-wiki`
- durable policy -> `loom-constitution`
